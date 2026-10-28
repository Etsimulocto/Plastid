# Plastid

**Plastid** is the product and application name.

The Raspberry Pi app and ESP32-S3 bring-up are developed together, with simulated handset features clearly separated from physical hardware verification.

## Current app

The renamed Plastid Pi app package is `Plastid_App_v03.zip` (distributed as a conversation artifact pending repository source import). It uses `plastid_lab.html`, `run_plastid_lab.py`, and `pi_bridge_server.py`.

## Compatibility and migration

The flashed ESP32-S3 firmware v0.1.0 currently returns an older project label in its USB JSON identity. The Pi bridge accepts it as a **legacy identity only**. Do not reflash just to change that label. Browser local storage migrates from the old application key without deleting the original.

Existing earlier-named folders on this setup branch are historical staging artifacts, **not** the current product name. See [identity migration notes](PLASTID_IDENTITY.md).

No modem, physical screen, keypad, audio or dock is connected or verified.
