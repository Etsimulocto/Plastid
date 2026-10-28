# MakerPhone

Software-first, modular, repairable DIY flip-phone project.

**Current status:** Host-side simulator supplied as MakerPhone Lab 0.1.0; real cellular capabilities, ESP32-S3 handset firmware, dock sync and physical integrations are *not implemented or verified*.

## Run the existing bench app

```bash
cd makerphone/lab
python3 run_makerphone_lab.py
```

Open http://127.0.0.1:8765/makerphone_lab.html in Chromium or Edge. The browser app supports local simulations without hardware; Web Serial requires a compatible browser and physically connected device with matching firmware.

See [lab documentation](lab/README.md), [project charter](docs/PROJECT_CHARTER.md), [decision log](docs/DECISIONS.md), [interface baseline](docs/INTERFACES.md), [test log](docs/TEST_LOG.md) and [risks](docs/RISKS.md).

## Project folders

- `lab/`: host-side browser simulator / diagnostic bench
- `firmware/`: reserved for actual handset firmware, to be added after architecture decision
- `cradle/`: reserved for cradle/base sync/update service
- `docs/`: current engineering source of truth

The independent audio subsystem **Bob** and other named subsystems retain their identities until interfaces are deliberately agreed.
