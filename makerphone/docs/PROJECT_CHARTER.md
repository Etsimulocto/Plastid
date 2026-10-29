# MakerPhone project charter

**Owner:** Architect  
**Baseline:** 2026-10-28  
**Status:** software-first prototype; hardware selection remains open.

MakerPhone is a modular, repairable DIY cellular flip phone with a tactile 3×4 keypad, 2.4-inch TFT, dedicated Call and End buttons, two proposed 5-way navigation controls, a separate LTE modem, and a four-contact cradle/base for safe backup, updates, contacts, messages and image sync to microSD. A small audio component named **Bob** remains a distinct design requirement; its exact role and interface are unresolved.

## Design boundaries

- Preserve the choice between an ESP32-S3 handset, Raspberry Pi Zero 2 W Linux handset, or deliberate host/device split until phone functions, firmware support and power requirements are evaluated.
- Target AT&T service with a **test SIM**. Verify registration, data and messaging before introducing voice calling.
- The existing MakerPhone Lab is a **browser-based host simulator/bench application**, **not** ESP32 firmware and **not** evidence of modem connectivity, SMS delivery or calling.
- Record claims as **confirmed**, **measured**, **simulated**, or **unverified**. Test logs further distinguish bench-, carrier- and field-tested outcomes.
- Do not freeze pinouts, display driver, modem, power circuitry, bus addresses, connector assignments, or enclosure dimensions based on a concept or unverified part listing.
- Preserve module identity, serviceability, backups, interrupted-transfer recovery, and rollback rather than flattening separate subsystems into one software component.

## Planned sequence

1. Record the baseline requirements, open decisions, BOM, pin/bus map and risks.
2. Expand MakerPhone Lab diagnostics and tests; agree on a versioned host/handset protocol.
3. Bring up ESP32-S3 (if chosen) and verify display, keypad, two 5-way controls, Call/End inputs and USB identity.
4. Select and test exact LTE modem with the AT&T test SIM: AT control, registration, data, messaging, then hotspot if supported.
5. Develop offline-usable dialer, contacts, messages, images/files, settings and diagnostics.
6. Prototype safe four-contact docking and interruption-tolerant archive/update restore.
7. Measure audio, charging, battery, haptics, thermal and cellular peak-current behavior.
8. Implement and validate voice, then mechanically finish the modular flip enclosure.

## Proposed physical envelope (unverified)

- Screen target: 2.4-inch TFT, 320×240 landscape; 240×320 portrait in simulator.
- Earlier case sketch: approximately 68 × 118 × 23 mm, 170° opening, wood faces, ASA frame, brass hinge with M3 hardware. These are reference constraints, **not** finalized CAD.

## Source of truth

See [DECISIONS.md](DECISIONS.md), [BOM.csv](BOM.csv), [INTERFACES.md](INTERFACES.md), [TEST_LOG.md](TEST_LOG.md) and [RISKS.md](RISKS.md). The original project treatment was provided by the project owner and is retained separately as a baseline document.
