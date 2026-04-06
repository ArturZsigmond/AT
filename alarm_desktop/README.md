# Security Alarm Monitor (Python desktop)

Desktop app that connects to your **Base_code** Arduino sketch over USB serial (9600 baud), shows live sensor values, highlights **ALL OK** vs **ALARM TRIGGERED**, sends a Windows toast when the alarm fires, and can **minimize to the system tray** while still reading serial in the background.

## Prerequisites

- Windows 10/11 (notifications and tray tested on Windows)
- Python 3.10+ recommended
- Arduino programmed with `Base_code/Base_code.ino` and connected via USB

## Install

Open a terminal in the `alarm_desktop` folder:

```bash
cd path\to\Arduino\alarm_desktop
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

With venv active as above, or:

```bash
path\to\Arduino\alarm_desktop\.venv\Scripts\python.exe path\to\Arduino\alarm_desktop\main.py
```

## Usage

1. Click **Refresh** if your board is not listed; choose the COM port (e.g. `COM3`).
2. **Connect** — opens serial at **9600** baud.
3. **Start monitoring** — a background thread reads lines without freezing the UI.
4. **Minimize to tray** (optional) — hides the window; use the tray icon **Show window** or **Quit**.

**Auto-reconnect** (on by default): if the USB cable is unplugged, the reader retries opening the same port periodically while monitoring is on.

## Serial protocol (matches your sketch)

- Telemetry (repeated):  
  `Light: <int> | Sound: <int> | Proximity: <0|1>`
- Alarm:  
  `ALARM TRIGGERED → SCREAMING`
- Return to idle:  
  `DONE → BACK TO IDLE`

**Proximity label:** the sketch treats **LOW** as object detected, so **Proximity: 0** is shown as **Detected**, **1** as **Not Detected**.

## Troubleshooting

- **No COM ports:** install the board’s USB driver (e.g. CH340/CP210x); plug the board in; click **Refresh**.
- **Garbage or no data:** ensure baud rate on the PC is **9600** and only **one** program has the port open (close Serial Monitor in Arduino IDE).
- **No toast:** Windows may block notifications for Python; check **Settings → System → Notifications** and allow the app / Python.
- **Tray button missing:** install `pystray` and `Pillow`; otherwise use **Minimize** on the window — serial keeps running as long as the app is open and monitoring is started.

## Project layout

| File | Role |
|------|------|
| `main.py` | Entry point |
| `serial_handler.py` | COM listing, threaded read loop, parsing, reconnect |
| `ui.py` | Tkinter GUI, queue polling, notifications, tray |
