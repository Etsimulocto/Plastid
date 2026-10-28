# Plastid

Product name: **Plastid**. Pi bench: `pi_bench.py` (standalone Python/pyserial app with an embedded browser interface). No ZIP download needed.

On Raspberry Pi OS:

```bash
sudo apt install python3-serial git
cd ~
git clone --branch setup/makerphone-lab --single-branch https://github.com/Etsimulocto/Plastid.git Plastid
cd ~/Plastid
python3 plastid/pi_bench.py --port /dev/ttyACM0
```

Open `http://127.0.0.1:8765`. Close other serial viewers and any existing application using port 8765. The existing firmware sends a legacy project identity, accepted here for compatibility only; it does not need to be reflashed. The Pi bench offers firmware identity/status/diagnostics and a **simulated** keypad/dialer/menu. Its contact/message/file menu screens are placeholders, not yet the full prior offline app.

Never expose the service to external network interfaces without adding authentication. The local default `127.0.0.1` is intentional.
