"""
Background serial reader for the security alarm Arduino (9600 baud).
Parses telemetry lines and alarm state messages; uses a queue for thread-safe UI updates.
"""

from __future__ import annotations

import queue
import re
import threading
import time
from typing import Optional

import serial
from serial.tools import list_ports

# Matches: Light: 300 | Sound: 80 | Proximity: 1
_TELEMETRY_RE = re.compile(
    r"Light:\s*(\d+)\s*\|\s*Sound:\s*(\d+)\s*\|\s*Proximity:\s*([01])",
    re.IGNORECASE,
)


def list_com_ports() -> list[tuple[str, str]]:
    """Return [(device, description), ...] for available COM ports."""
    ports: list[tuple[str, str]] = []
    for p in list_ports.comports():
        desc = (p.description or "").strip() or "Serial device"
        ports.append((p.device, f"{p.device} — {desc}"))
    return ports


class SerialHandler:
    def __init__(self, event_queue: "queue.Queue") -> None:
        self._q = event_queue
        self._ser: Optional[serial.Serial] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._monitoring = False
        self._port: str = ""
        self._auto_reconnect = True
        self._reconnect_delay_s = 2.0
        self._lock = threading.Lock()

    @property
    def is_open(self) -> bool:
        with self._lock:
            return self._ser is not None and self._ser.is_open

    def set_auto_reconnect(self, enabled: bool) -> None:
        self._auto_reconnect = enabled

    def connect(self, port: str) -> bool:
        """Open serial port. Returns False on failure."""
        with self._lock:
            self._close_unlocked()
            self._port = port
            try:
                self._ser = serial.Serial(port, 9600, timeout=0.3)
                time.sleep(0.2)  # allow Arduino reset after USB open
            except (serial.SerialException, OSError) as e:
                self._ser = None
                self._q.put({"type": "serial_error", "message": str(e)})
                return False
        self._q.put({"type": "serial_connected", "port": port})
        return True

    def disconnect(self) -> None:
        with self._lock:
            self._monitoring = False
            self._close_unlocked()
        self._q.put({"type": "serial_disconnected"})

    def _close_unlocked(self) -> None:
        if self._ser is not None:
            try:
                if self._ser.is_open:
                    self._ser.close()
            except Exception:
                pass
            self._ser = None

    def start_monitoring(self) -> None:
        if not self.is_open:
            self._q.put({"type": "serial_error", "message": "Not connected."})
            return
        if self._thread and self._thread.is_alive():
            return
        self._monitoring = True
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()
        self._q.put({"type": "monitor_started"})

    def stop_monitoring(self) -> None:
        self._monitoring = False
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._thread = None
        self._q.put({"type": "monitor_stopped"})

    def _read_loop(self) -> None:
        while self._running and self._monitoring:
            ser = None
            with self._lock:
                ser = self._ser
            if ser is None or not ser.is_open:
                if self._auto_reconnect and self._port and self._monitoring:
                    time.sleep(self._reconnect_delay_s)
                    with self._lock:
                        if self._ser is None or not self._ser.is_open:
                            try:
                                self._ser = serial.Serial(self._port, 9600, timeout=0.3)
                                self._q.put({"type": "serial_reconnected", "port": self._port})
                            except (serial.SerialException, OSError) as e:
                                self._q.put({"type": "serial_error", "message": str(e)})
                else:
                    break
                continue
            try:
                raw = ser.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                self._handle_line(line)
            except (serial.SerialException, OSError) as e:
                self._q.put({"type": "serial_error", "message": str(e)})
                with self._lock:
                    self._close_unlocked()
                if not self._auto_reconnect or not self._monitoring:
                    break
                time.sleep(self._reconnect_delay_s)

    def _handle_line(self, line: str) -> None:
        if "ALARM TRIGGERED" in line:
            self._q.put({"type": "alarm_triggered", "raw": line})
            return
        if "DONE → BACK TO IDLE" in line or "DONE -> BACK TO IDLE" in line:
            self._q.put({"type": "alarm_cleared", "raw": line})
            return
        m = _TELEMETRY_RE.search(line)
        if m:
            light_v = int(m.group(1))
            sound_v = int(m.group(2))
            prox = int(m.group(3))
            # Arduino: objectDetected when proximity reads LOW (0)
            proximity_label = "Detected" if prox == 0 else "Not Detected"
            self._q.put(
                {
                    "type": "telemetry",
                    "light": light_v,
                    "sound": sound_v,
                    "proximity_raw": prox,
                    "proximity_label": proximity_label,
                }
            )
