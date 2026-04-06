"""
Tkinter UI for the security alarm monitor: COM selection, live sensors, status, tray.
"""

from __future__ import annotations

import queue
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from serial_handler import SerialHandler

try:
    from plyer import notification
except ImportError:
    notification = None  # type: ignore

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None  # type: ignore
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore


def _tray_image_ok():
    if Image is None or ImageDraw is None:
        return None
    img = Image.new("RGB", (64, 64), (40, 120, 60))
    d = ImageDraw.Draw(img)
    d.ellipse((12, 12, 52, 52), fill=(80, 200, 100))
    return img


def _tray_image_alarm():
    if Image is None or ImageDraw is None:
        return None
    img = Image.new("RGB", (64, 64), (80, 30, 30))
    d = ImageDraw.Draw(img)
    d.ellipse((12, 12, 52, 52), fill=(220, 60, 60))
    return img


class AlarmMonitorApp:
    def __init__(self, handler: "SerialHandler", event_queue: queue.Queue) -> None:
        self.handler = handler
        self.event_queue = event_queue
        self.root = tk.Tk()
        self.root.title("Security Alarm Monitor")
        self.root.minsize(420, 320)
        self.root.geometry("480x380")

        self._tray_icon: Optional[object] = None
        self._withdrawn_to_tray = False

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._poll_queue()

    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        row0 = ttk.Frame(main)
        row0.pack(fill=tk.X, **pad)
        ttk.Label(row0, text="COM port:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(row0, textvariable=self.port_var, width=28, state="readonly")
        self.port_combo.pack(side=tk.LEFT, padx=(8, 4))
        ttk.Button(row0, text="Refresh", command=self._refresh_ports).pack(side=tk.LEFT)

        row1 = ttk.Frame(main)
        row1.pack(fill=tk.X, **pad)
        self.btn_connect = ttk.Button(row1, text="Connect", command=self._connect)
        self.btn_connect.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_disconnect = ttk.Button(row1, text="Disconnect", command=self._disconnect, state=tk.DISABLED)
        self.btn_disconnect.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_start = ttk.Button(row1, text="Start monitoring", command=self._start_monitor, state=tk.DISABLED)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_stop = ttk.Button(row1, text="Stop monitoring", command=self._stop_monitor, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT)

        self.auto_reconnect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            main,
            text="Auto-reconnect if USB drops",
            variable=self.auto_reconnect_var,
            command=self._toggle_autoreconnect,
        ).pack(anchor=tk.W, **pad)

        sep = ttk.Separator(main, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=8)

        grid = ttk.Frame(main)
        grid.pack(fill=tk.BOTH, expand=True)
        for i in range(2):
            grid.columnconfigure(i, weight=1)

        ttk.Label(grid, text="Light (A0)", font=("", 10, "bold")).grid(row=0, column=0, sticky=tk.W, **pad)
        self.lbl_light = ttk.Label(grid, text="—", font=("Consolas", 11))
        self.lbl_light.grid(row=0, column=1, sticky=tk.W, **pad)

        ttk.Label(grid, text="Sound (A1)", font=("", 10, "bold")).grid(row=1, column=0, sticky=tk.W, **pad)
        self.lbl_sound = ttk.Label(grid, text="—", font=("Consolas", 11))
        self.lbl_sound.grid(row=1, column=1, sticky=tk.W, **pad)

        ttk.Label(grid, text="Proximity (D7)", font=("", 10, "bold")).grid(row=2, column=0, sticky=tk.W, **pad)
        self.lbl_prox = ttk.Label(grid, text="—", font=("Consolas", 11))
        self.lbl_prox.grid(row=2, column=1, sticky=tk.W, **pad)

        ttk.Label(grid, text="System status", font=("", 10, "bold")).grid(row=3, column=0, sticky=tk.W, **pad)
        self.lbl_status = ttk.Label(grid, text="ALL OK", font=("Segoe UI", 12, "bold"), foreground="#1a7f37")
        self.lbl_status.grid(row=3, column=1, sticky=tk.W, **pad)

        row_tray = ttk.Frame(main)
        row_tray.pack(fill=tk.X, **pad)
        if pystray is not None and Image is not None:
            ttk.Button(row_tray, text="Minimize to tray", command=self._minimize_to_tray).pack(side=tk.LEFT)
        else:
            ttk.Label(row_tray, text="Install pystray + Pillow for system tray.", foreground="gray").pack(side=tk.LEFT)

        self.status_bar = ttk.Label(main, text="Disconnected", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(8, 0))

        self._refresh_ports()

    def _toggle_autoreconnect(self) -> None:
        self.handler.set_auto_reconnect(self.auto_reconnect_var.get())

    def _refresh_ports(self) -> None:
        from serial_handler import list_com_ports

        ports = list_com_ports()
        values = [p[1] for p in ports]
        self._port_map = {p[1]: p[0] for p in ports}
        self.port_combo["values"] = values
        if values:
            if self.port_var.get() not in self._port_map:
                self.port_var.set(values[0])
        else:
            self.port_var.set("")

    def _selected_device(self) -> Optional[str]:
        label = self.port_var.get()
        return self._port_map.get(label)

    def _connect(self) -> None:
        dev = self._selected_device()
        if not dev:
            messagebox.showwarning("COM port", "Select a COM port or click Refresh.")
            return
        if self.handler.connect(dev):
            self.btn_connect.config(state=tk.DISABLED)
            self.btn_disconnect.config(state=tk.NORMAL)
            self.btn_start.config(state=tk.NORMAL)
            self.status_bar.config(text=f"Connected to {dev}")
        else:
            self.status_bar.config(text="Connection failed")

    def _disconnect(self) -> None:
        self.handler.stop_monitoring()
        self.handler.disconnect()
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.DISABLED)
        self.status_bar.config(text="Disconnected")

    def _start_monitor(self) -> None:
        self.handler.start_monitoring()
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

    def _stop_monitor(self) -> None:
        self.handler.stop_monitoring()
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def _set_status_ok(self) -> None:
        self.lbl_status.config(text="ALL OK", foreground="#1a7f37")
        self._update_tray_icon(False)

    def _set_status_alarm(self) -> None:
        self.lbl_status.config(text="ALARM TRIGGERED", foreground="#c41e3a")
        self._update_tray_icon(True)

    def _show_windows_notification(self) -> None:
        if notification is None:
            return
        try:
            notification.notify(
                title="Security Alert",
                message="Alarm has been triggered!",
                app_name="Security Alarm Monitor",
                timeout=8,
            )
        except Exception:
            pass

    def _ensure_tray(self) -> None:
        if pystray is None or Image is None:
            return
        if self._tray_icon is not None:
            return

        def on_show(icon, item):
            self.root.after(0, self._show_from_tray)

        def on_quit(icon, item):
            self.root.after(0, self._quit_from_tray)

        menu = pystray.Menu(
            pystray.MenuItem("Show window", on_show, default=True),
            pystray.MenuItem("Quit", on_quit),
        )
        img = _tray_image_ok()
        assert img is not None
        self._tray_icon = pystray.Icon("security_alarm", img, "Security Alarm Monitor", menu)

        def run_tray():
            assert self._tray_icon is not None
            self._tray_icon.run()

        threading.Thread(target=run_tray, daemon=True).start()

    def _update_tray_icon(self, alarm: bool) -> None:
        if self._tray_icon is None:
            return
        try:
            icon_img = _tray_image_alarm() if alarm else _tray_image_ok()
            if icon_img is not None:
                self._tray_icon.icon = icon_img
        except Exception:
            pass

    def _minimize_to_tray(self) -> None:
        self._ensure_tray()
        if self._tray_icon is None:
            self.root.iconify()
            return
        self._withdrawn_to_tray = True
        self.root.withdraw()

    def _show_from_tray(self) -> None:
        self._withdrawn_to_tray = False
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _quit_from_tray(self) -> None:
        self.handler.stop_monitoring()
        self.handler.disconnect()
        if self._tray_icon:
            try:
                self._tray_icon.stop()
            except Exception:
                pass
        self.root.quit()
        sys.exit(0)

    def _on_close(self) -> None:
        self.handler.stop_monitoring()
        self.handler.disconnect()
        if self._tray_icon:
            try:
                self._tray_icon.stop()
            except Exception:
                pass
        self.root.destroy()
        sys.exit(0)

    def _poll_queue(self) -> None:
        try:
            while True:
                ev = self.event_queue.get_nowait()
                self._handle_event(ev)
        except queue.Empty:
            pass
        self.root.after(50, self._poll_queue)

    def _handle_event(self, ev: dict) -> None:
        t = ev.get("type")
        if t == "telemetry":
            self.lbl_light.config(text=str(ev["light"]))
            self.lbl_sound.config(text=str(ev["sound"]))
            self.lbl_prox.config(text=ev["proximity_label"])
        elif t == "alarm_triggered":
            self._set_status_alarm()
            self._show_windows_notification()
        elif t == "alarm_cleared":
            self._set_status_ok()
        elif t == "serial_connected":
            self.status_bar.config(text=f"Connected to {ev.get('port', '')}")
        elif t == "serial_reconnected":
            self.status_bar.config(text=f"Reconnected to {ev.get('port', '')}")
        elif t == "serial_disconnected":
            self.status_bar.config(text="Disconnected")
        elif t == "serial_error":
            self.status_bar.config(text=f"Serial error: {ev.get('message', '')}")
        elif t == "monitor_started":
            self.status_bar.config(text="Monitoring…")
        elif t == "monitor_stopped":
            self.status_bar.config(text="Monitoring stopped")

    def run(self) -> None:
        self.root.mainloop()


def run_app(handler: "SerialHandler", event_queue: queue.Queue) -> None:
    app = AlarmMonitorApp(handler, event_queue)
    app.run()
