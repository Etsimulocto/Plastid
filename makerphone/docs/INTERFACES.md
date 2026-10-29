# Interface and protocol baseline

## Host / handset serial (SIMULATED PROTOCOL CONTRACT)

MakerPhone Lab 0.1.0 proposes **115200 baud, newline-delimited JSON**. The current application can request a Web Serial connection in Chromium/Edge; firmware implementation is not yet demonstrated. These messages are *examples from the simulator*, not a verified on-device protocol.

Host → device:

```json
{"op":"hello","app":"MakerPhone Lab","version":"0.1.0"}
{"op":"diag.run","id":"..."}
{"op":"input","control":"keypad","key":"2"}
{"op":"input","control":"stickL","key":"up"}
{"op":"display.test"}
{"op":"modem.status"}
```

Device → host:

```json
{"type":"hello","board":"esp32s3","fw":"0.1.0"}
{"type":"status","component":"modem","state":"ready"}
{"type":"diag","component":"display","state":"pass","detail":"..."}
{"type":"log","level":"INFO","message":"..."}
{"type":"button","control":"keypad","key":"2"}
```

**Pending**: formal schema/version negotiation, request/response IDs, maximum frame size, errors/timeouts, reconnect, transport safety and firmware-side test fixtures.

## Physical interfaces (UNVERIFIED)

| Interface | Target / candidate | Status |
| --- | --- | --- |
| Display | SPI 2.4-inch TFT | controller, voltage and pins TBD |
| Keypad | 3×4 matrix | connector and GPIO assignment TBD |
| Left/right control | two I²C 5-way navigation boards | addresses TBD; don't assume both can share defaults |
| Cellular | separate LTE modem via suitable link | model, AT interface, voltage, SIM and antenna TBD |
| Bob | separate audio module requirement | wiring/interface and placement TBD |
| USB-C | service/firmware and host diagnostic access | topology TBD |
| Dock | four magnetic contacts | **no pin assignment yet**; electrical safety before use |
| microSD | base archive | capacity, file format and recovery protocol TBD |

**Safety**: no suggested wiring or dock pinout should be interpreted as tested. Do not connect a LiPo, modem supply or magnetic power contacts from this document alone.
