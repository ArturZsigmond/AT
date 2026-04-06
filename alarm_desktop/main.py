#!/usr/bin/env python3
"""
Security Alarm Monitor — desktop companion for the Arduino sketch in Base_code/Base_code.ino

Run from this folder:
  python main.py
"""

from __future__ import annotations

import queue

from serial_handler import SerialHandler
from ui import run_app


def main() -> None:
    event_queue: queue.Queue = queue.Queue()
    handler = SerialHandler(event_queue)
    run_app(handler, event_queue)


if __name__ == "__main__":
    main()
