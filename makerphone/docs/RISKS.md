# Initial risk register

| ID | Risk | Impact | Evidence | Mitigation |
| --- | --- | --- | --- | --- |
| R-001 | Carrier rejects the selected LTE module/SIM | High | unverified | Check current AT&T requirements and test exact hardware before commitment |
| R-002 | LTE transmit bursts exceed power supply budget | High | unverified | Measure current peaks; design regulation/decoupling only from validated data |
| R-003 | Incorrect TFT controller/raster/voltage | Medium | unverified | Identify exact module and verify raster and I/O |
| R-004 | Two 5-way boards collide on I²C | Medium | unverified | Set and measure distinct addresses |
| R-005 | Dock disconnect corrupts archive or firmware | High | unverified | use checksums, atomic writes, rollback/recovery tests |
| R-006 | Enclosure crowds antenna, hinge and battery | High | unverified | defer dimensional freeze until parts and keep-outs measured |
| R-007 | Simulator is mistaken for a working phone | High | confirmed boundary | label simulation explicitly in documentation and test reports |
