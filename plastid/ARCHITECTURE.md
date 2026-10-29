# Plastid architecture and verification tracker

Updated 2026-10-28. **Planned** means proposed, **Simulated** means software demonstration only, **Verified** means a real tested observation. No BOM/pinout is frozen.

## Product structure

| Device | Owns | Interfaces | State |
| --- | --- | --- | --- |
| Phone | Cellular modem/SIM, calls/SMS, local contacts and independent handset UI | Pod wireless audio + control; Base dock data/power; potential cellular internet tether | ESP32-S3 USB bring-up verified; all cellular functions unverified |
| Pod | Rechargeable small 128×64 monochrome OLED, physical buttons, microphone, speaker, alert controls | Bluetooth data notifications and duplex audio from Phone; separate Base charging dock | UI simulator only; board/audio selection open |
| Base | Primary docked UI, 5–7 inch touchscreen candidate, loudspeaker/amplifier/mic, contacts/messages editing, archive/backups, maps, diagnostics, updates, two charging bays | Phone six-contact magnetic dock candidate; Pod dock; Wi-Fi, local storage and optional GNSS/solar | UI simulator only; physical design open |

**Authority:** Base is boss when docked, including UI and notification behavior. When separated, Phone and Pod follow individually configurable alerts. Phone remains the cellular call owner and independent fallback. Define takeover arbitration, emergency calling behavior, audio route failover and reconnection explicitly before implementation.

## Communication links to prototype

1. **Phone↔Pod data:** BLE messages for calls, SMS preview, battery/connection state and button commands. Test on two ESP32-S3 Minis is proposed, not performed.
2. **Phone↔Pod voice:** duplex microphone/speaker stream, call-answer/end and low-latency audio. S3 BLE notification success does not mean HFP voice works. Compare Bluetooth Classic capable original ESP32/S31, H4 LE Audio compatibility and a dedicated audio module; validate real two-way calling.
3. **Phone↔Base dock:** six flat magnetic contacts candidate. Engineering must choose VBUS/GND, data, orientation/detection, reverse polarity and overcurrent protection, hot plug safety and safe charge negotiation. No agreed pinout.
4. **Pod↔Base dock:** independent charge and optional data; protect exposed contacts and batteries. No agreed pinout.
5. **Phone→Base internet:** optional phone LTE tethering through Wi-Fi AP or docked network transport. Verify LTE modem data interface, IP forwarding/NAT, DNS, carrier plan requirements, concurrency with calls and idle power; AP support by itself is insufficient.
6. **Base speakerphone:** docked Phone owns cellular call; Base supplies local microphone, echo cancellation and amplifier. End-to-end audio path unverified.

## Base hardware shortlist

- Raspberry Pi 4 2–4 GB for prototype if available affordably; Pi Zero 2 W is less comfortable for full web maps; Pi 5 and CM5 are upgrade/custom carrier choices.
- Medium/large touchscreen, likely 5–7 inches for readable text and easier editing.
- microSD/SSD for backups and **licensed** offline map packages; storage medium does not increase CPU/RAM.
- Separate speakerphone audio interface/codec, amplifier, larger speaker, decent microphone; test acoustic echo cancellation.
- Mains power first; battery with BMS and optional properly regulated solar input later. Flat-bottomed portable chassis and carry handle/stand are concepts.
- Materials guesses (not quotes): Phone ~$120, Pod ~$80, Base ~$200, system ~$400. Battery/solar could exceed Base allowance.

## Mapping approach

- **Online Google Maps Platform** can power a custom simplified Base UI via approved Maps, Places and Routes services with billing, attribution, internet and terms compliance.
- **Offline regional maps** must use a separately licensed provider / compatible OpenStreetMap-derived extracts, suitable tiles/vector package, renderer and offline routing where needed. Do not bulk-download Google tiles or mix providers without verifying terms. Do not bulk-scrape the public OSM tile server.
- **Senior-first UX:** numbered, large-type written directions as the default; map pan/zoom as another view; saved places, destination search, optional spoken steps. Phone receives simplified directions or a small offline map only after performance/storage testing.
- Base location indicator requires actual GNSS/GPS hardware (or other verified location source), not merely saved maps. Route preview and dynamic turn-by-turn navigation are separate milestones.
- A Base travelling with the Phone could use Phone tethering for online Google Maps; independently powered Base is not yet built.

## Verified facts and incomplete work

**Verified:** USB ESP32-S3 at `/dev/ttyACM0`; 16 MB flash / 8 MB PSRAM; firmware v0.1.0 hello JSON response at 115200; original flash backup saved on Pi.

**Simulated:** Pi/PC Phone menus, Base docking and state controls, Pod OLED concepts/notifications, audio route selection buttons, contact/menu concepts and diagnostic/backup demos.

**Unverified:** all cellular hardware and services; GNSS, real OLED/TFT, actual keypad; Bluetooth hands-free voice or data between two Minis; dual charging; magnetic dock; Base speakerphone; maps rendering or route computation on final hardware; battery runtime/solar; data sync/backup/restore integrity.

## Next engineering test gates

1. Preserve full existing app and make sure local Base/Pod simulator installation is working.
2. Prove Pi↔ESP32 serial messaging remains stable while GUI is active.
3. Test two ESP32-S3 boards over BLE for alerts/commands/reconnect (only after second board is available).
4. Test real Bluetooth voice between proposed Phone and Pod architectures; do not finalize controller until successful.
5. Prototype one Base charging bay with protected power and detection before two-bay integration.
6. Prototype phone-to-Base connectivity: Wi-Fi AP join first; actual LTE routing after modem purchase.
7. Benchmark web maps and offline map rendering on candidate Pi before final board purchase.
8. Validate audio, battery safety and interruption-safe backup/restore on hardware before calling those features operational.
