# Plastid — Pi app, full simulator and device workspaces

**Current name: Plastid.** The product consists of Phone + Pod + Base. See [root README](../README.md) and [architecture/status](ARCHITECTURE.md).

## Existing Pi hardware verification

The connected ESP32-S3 development board has **16 MB flash, 8 MB PSRAM**; firmware v0.1.0 provides a tested USB JSON identity handshake on `/dev/ttyACM0` at 115200 baud. Its older project identity is tolerated for migration; it does not make the board a finished phone or prove any cellular/audio/docking features. Preserve the original flash backup on the Pi.

## Pull updates

```bash
cd ~/Plastid
git pull origin setup/makerphone-lab
```

The **full prior app** is preferred for Phone UI design; don't confuse it with the smaller `pi_bench.py`, which is only a bench/diagnostics interface.

### Full app with optional visual UI editor and Base/Pod studio

If the full app has already been restored locally and `plastid/plastid_lab.html` exists:

```bash
cd ~/Plastid
python3 plastid/install_ui_editor.py
python3 plastid/install_base_pod.py
python3 plastid/pi_bridge_server.py --port /dev/ttyACM0
```

Open **http://127.0.0.1:8765** locally. Refresh with Ctrl+Shift+R after integration. Stop other processes occupying the same port/serial device before starting the bridge.

If full-app HTML is missing, `restore_full_app.py` attempts to restore it from the **historical local source** on that Pi. This is conditional: it may fail if the earlier downloaded app is absent; the full app itself is **not currently committed as a standalone source artifact**. Run only if you have the original local source:

```bash
python3 plastid/restore_full_app.py
```

**Base & Pod studio** (`base_pod_studio.js` + `install_base_pod.py`) adds simulated docking states, a 128×64 Pod concept screen, button actions, simulated call state, routing selections and demo diagnostics/backups. **It does not charge devices, place calls, route real audio, transfer data or connect hardware.** The installer makes a backup of the HTML before changing it. Editor customization uses browser-local state, not physical display firmware.

### Minimal serial bench (alternative)

```bash
sudo apt install python3-serial git
cd ~/Plastid
python3 plastid/pi_bench.py --port /dev/ttyACM0
```

This separate bench supplies firmware identity, status and diagnostics plus *simulated* handset menus. It is **not** the full app and should never overwrite/replace the full app.

## Design principles

- Base controls docked Phone and Pod; undocked behavior follows user-configured alerts.
- Phone owns cellular calls and modem; Pod is a remote microphone/speaker and notification endpoint.
- Base is the preferred place for editing contacts/messages, diagnostics, large-screen maps and numbered written directions.
- Offline maps, Phone tethering, Bluetooth voice, battery/solar power, physical docks and robust backups are **proposed**, not verified.

**Security:** keep Pi app bound to localhost `127.0.0.1` until authentication and network security are engineered. Do not put API keys or personal contacts in this repository.

## Raspberry Pi desktop icon and one-click launcher

A spiral-themed Plastid launcher icon (SVG recreation of the approved design) and desktop/menu shortcut are provided in `plastid/`.

```bash
cd ~/Plastid
git pull origin setup/makerphone-lab
python3 plastid/install_desktop.py
```

This installs **Plastid.desktop** to `~/Desktop` and the app menu, installs `~/.local/share/icons/plastid.svg`, and creates `~/.local/bin/plastid-launch`. Double-click **Plastid**; on some Pi desktops select **Allow Launching** on first use. If the existing full app is running, the launcher opens it in the browser; otherwise it tries to start `plastid/pi_bridge_server.py --port /dev/ttyACM0` and then opens `http://127.0.0.1:8765`. It **does not replace the full HTML app or flash firmware**. The bridge must already be installed for the app to launch.

Troubleshooting: `~/.local/state/plastid/launcher.log`. The SVG is a vector adaptation intended for small Linux desktop icons, not pixel-identical to the generated artwork.
