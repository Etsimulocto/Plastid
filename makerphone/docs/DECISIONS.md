# Architecture and hardware decision log

| ID | Question | Status | Next evidence needed |
| --- | --- | --- | --- |
| D-001 | ESP32-S3 vs Pi Zero 2 W Linux vs split | OPEN / unverified | software architecture, memory, idle/peak power, I/O map |
| D-002 | LTE modem model and AT&T support | OPEN / unverified | exact module, firmware, bands, carrier/SIM tests; VoLTE later |
| D-003 | TFT display model, controller, SPI pinout | OPEN / unverified | exact board/marking, power levels and dimensions |
| D-004 | 3×4 keypad version and footprint | OPEN / unverified | electrical/mechanical measurements |
| D-005 | Two Qwiic 5-way boards/address map | OPEN / unverified | scan both boards, verify unique I²C addresses |
| D-006 | Call/End physical inputs | OPEN / unverified | part and electrical interface |
| D-007 | Bob audio module role and interface | OPEN / unverified | audio topology and connector definition |
| D-008 | Battery, charger, regulator, haptics | OPEN / unverified | cell and peak-current measurements, safety review |
| D-009 | Four magnetic dock contacts and sync format | OPEN / unverified | pin/power/data architecture; interruption testing |
| D-010 | Final enclosure/hinge geometry | OPEN / unverified | measured part envelopes and antenna keep-out |
