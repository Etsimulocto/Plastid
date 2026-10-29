#!/usr/bin/env bash
# Plastid desktop launcher — opens the existing full Pi app without replacing it.
set -u
ROOT="$HOME/Plastid"
APP="$ROOT/plastid"
URL="http://127.0.0.1:8765"
PORT="${PLASTID_SERIAL_PORT:-/dev/ttyACM0}"
ready() { python3 - <<'PY'
import socket
s=socket.socket();s.settimeout(.4)
try:s.connect(('127.0.0.1',8765));exit(0)
except OSError:exit(1)
finally:s.close()
PY
}
if ! ready; then
 if [ ! -f "$APP/pi_bridge_server.py" ]; then
  (command -v zenity >/dev/null && zenity --error --title=Plastid --text="Plastid's full-app bridge is not installed at $APP/pi_bridge_server.py. Restore the full app first; your existing files were not changed.") || echo "Plastid bridge missing: $APP/pi_bridge_server.py" >&2
  exit 1
 fi
 mkdir -p "$HOME/.local/state/plastid"
 (cd "$ROOT" && nohup python3 "$APP/pi_bridge_server.py" --port "$PORT" >>"$HOME/.local/state/plastid/launcher.log" 2>&1 </dev/null &)
 for _ in $(seq 1 30); do ready && break; sleep .3; done
fi
if ready; then
 xdg-open "$URL" >/dev/null 2>&1 || true
else
 (command -v zenity >/dev/null && zenity --error --title=Plastid --text="Plastid could not start. See ~/.local/state/plastid/launcher.log") || echo "Plastid could not start; see launcher.log" >&2
 exit 1
fi
