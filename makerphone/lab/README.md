# MakerPhone Lab 0.1.0

Standalone host-side browser simulator and PC / Raspberry Pi USB bench. This is **not** working handset firmware.

## Start

Requires Python 3 and Chromium or Microsoft Edge for Web Serial (the simulator itself can run without USB).

```bash
python3 run_makerphone_lab.py
```

Then open `http://127.0.0.1:8765/makerphone_lab.html`.

Controls: arrows = left 5-way; I/J/K/L = right 5-way; Enter = select; C = call; Escape = end/back; 0–9, * and # = keypad.

Local contacts, call *simulations*, drafts and logs are saved in browser local storage. Export any data you need before clearing the browser. The host protocol is 115200 baud newline-delimited JSON; see [interface baseline](../docs/INTERFACES.md).

**Not connected:** modem, actual calls/SMS, live SIM, speaker/mic hardware tests, haptics, battery telemetry and microSD. A USB connection alone does not make those operational.

Original input: `makerphone_lab_pi_pc.zip`, with `makerphone_lab.html`, `run_makerphone_lab.py` and `README.txt`.
