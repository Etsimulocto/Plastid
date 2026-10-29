# Plastid

**Plastid** is a modular, repairable, accessibility-first communications system with three independent, cooperating devices: **Phone**, **Pod**, and **Base**. These are design and prototype plans, not claims of production readiness.

> Updated 2026-10-28. Engineering rule: distinguish **verified**, **simulated**, **proposed**, and **not yet tested**.

## The three devices

| Device | Role | Current planning allowance (not fixed BOM) |
| --- | --- | ---: |
| **Phone** | Standalone cellular flip phone: calls, SMS, contacts, easy-to-read 320×240-class landscape display and tactile keypad. Provides the cellular connection to other devices if tethering is implemented. | ~$120 |
| **Pod** | Small rechargeable Bluetooth companion with **128×64 OLED**, physical buttons, notifications, speaker and microphone. No text-entry keypad or cellular modem. Phone makes/receives the cellular calls; Pod is a remote hands-free endpoint. | ~$80 |
| **Base** | **Boss when devices are docked**: desktop/portable dual charging station, larger touchscreen, higher-quality speakerphone, contacts and message editor, device settings, diagnostics, backups, maps and readable written directions. Optional carry handle, battery and solar input. | ~$200 |

The allowances are conversation-level guesses for materials, **not** verified parts costs, requirements or retail prices.

### Base-first behavior

- Both **Phone and Pod sit in the Base to charge**. Their charging, dock identification and communications paths must be engineered and protected independently.
- **Base is boss** while devices are docked: it is the preferred control surface and manages notification/ringing behavior. Exact call-control, audio routing and failover rules remain to be specified.
- **Undocked devices** ring/alert according to their user-configured behavior, rather than a forced global rule.
- The **Phone remains usable alone** with its own cellular service. Base and Pod are optional add-ons.
- A **six-contact magnetic flat dock** is proposed for the Phone; power/data/audio allocation, current limit, short-circuit safety, docking orientation and hot-plug behavior are *not* finalized. Consider carrying digital audio via a data connection rather than assuming raw analog audio contacts.

## Maps and directions

The **Base** is the comfortable map/trip-planning device: medium/large touchscreen (5–7 inches under consideration), pan/zoom map, address entry, saved places, **large numbered written directions by default**, and optional position display with added GNSS/GPS hardware. The Phone can display simplified saved directions and, subject to its actual storage/rendering limits, a lightweight map. Pod may eventually announce instructions.

A **Google Maps Platform-powered custom online interface** is a candidate for the Base (Maps/Places/Routes, following their current terms, billing and attribution requirements). **Do not promise permanent downloads of Google's map tiles or unrestricted offline storage.** For offline region packages, investigate separately licensed OpenStreetMap-derived data, an offline renderer and a routing engine. Keep provider licensing and data provenance separate. Google Maps online access requires internet; GPS is a separate receiver and does not come from a large SD card.

**Connectivity proposal:** Base prefers household Wi-Fi if available; while away, Phone might share its cellular service over a Wi-Fi hotspot. ESP32-S3 SoftAP capability alone does **not** prove LTE-to-Wi-Fi NAT/routing, modem support, carrier tethering permission, performance or call concurrency. Also investigate a docked data link. None of these end-to-end paths are verified.

## Hardware directions (not yet purchased or locked)

- **Phone:** ESP32-S3 currently used only as an ESP32 development mule; cellular modem, SIM, display, keypad, charging and final controller selection pending. Phone-to-Pod Bluetooth hands-free audio path remains an engineering risk.
- **Pod:** Investigating compact ESP32 boards, including experiments using **two ESP32-S3 Minis** for BLE notifications, button actions and reconnection. ESP32-S3 does *not* have Bluetooth Classic HFP; a two-S3 BLE test alone does not prove duplex voice. Compare original ESP32, ESP32-S31, ESP32-H4 and dedicated audio designs against actual firmware/audio support and availability before purchasing. Round custom enclosure, possibly flat-bottomed, with accessible buttons.
- **Base:** Raspberry Pi **4** (especially used 2–4 GB) is a reasonable candidate; Pi Zero 2 W is constrained for modern browser maps, and Pi 5/Compute Module 5 is optional, not mandatory. Touchscreen, audio interface/amp/mic, dual protected chargers, power management and microSD/SSD are separate subsystems. Battery and solar are planned options, not wired or validated.

## Actually verified

On the Pi development host: USB ESP32-S3 enumerated at `/dev/ttyACM0`, identified as **16 MB flash / 8 MB PSRAM**, and first firmware **v0.1.0** was built, flashed and answered a serial JSON `hello` handshake at 115200 baud. A preserved original flash image exists on the development Pi. The first firmware's project field carries a **legacy label** and is accepted only for compatibility; next deliberate firmware release should use `Plastid`. Do not reflash merely to rename it.

**Not verified:** cellular modem registration, actual voice/SMS/data, physical UI display/keypad, Bluetooth call audio, maps on final hardware, charging, Base speakerphone, backup integrity, Phone hotspot routing, and dock operation.

## Software and docs

- [Pi/PC app instructions](plastid/README.md) — full-app restoration and optional Base/Pod simulator.
- [Identity and migration](PLASTID_IDENTITY.md) — Plastid is the only current product name.
- [Architecture and engineering checklist](plastid/ARCHITECTURE.md) — subsystem interfaces, open decisions and test gates.
- `makerphone/` — retained **historical** staging material, not a second product or current documentation authority.

Development is on `setup/makerphone-lab` (historic branch label; product remains **Plastid**). No ZIP download is needed to pull documentation or integration scripts.
