#!/usr/bin/env python3
"""Enable Plastid's live appearance editor on the existing full Pi app."""
from pathlib import Path
import shutil
p=Path(__file__).resolve().parent
html=p/'plastid_lab.html'
if not html.exists():
 raise SystemExit("Full Plastid app not found. Run python3 plastid/restore_full_app.py first.")
s=html.read_text(encoding='utf-8')
if '<script src="/ui_editor.js"></script>' not in s:
 s=s.replace('</body>','<script src="/ui_editor.js"></script></body>')
if "ctx.fillStyle='#071724';ctx.fillRect(0,0,w,h)" in s:
 s=s.replace("ctx.fillStyle='#071724';ctx.fillRect(0,0,w,h)", "ctx.fillStyle=(window.plastidScreenTheme?.bg||'#071724');ctx.fillRect(0,0,w,h)")
if "ctx.fillStyle='#e6f6ff';ctx.font='bold 11px monospace'" in s:
 s=s.replace("ctx.fillStyle='#e6f6ff';ctx.font='bold 11px monospace'", "ctx.fillStyle=(window.plastidScreenTheme?.color||'#e6f6ff');ctx.font='bold '+Math.max(10,Math.round((window.plastidScreenTheme?.fontSize||18)*.62))+'px monospace'")
if "ctx.font='bold 17px sans-serif'" in s:
 s=s.replace("ctx.font='bold 17px sans-serif'", "ctx.font='bold '+(window.plastidScreenTheme?.fontSize||18)+'px sans-serif'")
if '<script src="/ui_editor.js"></script>' not in s:
 raise SystemExit("App HTML has unexpected structure. No changes made.")
if s!=html.read_text(encoding='utf-8'):
 shutil.copy2(html, p/'plastid_lab.html.pre-editor')
 html.write_text(s,encoding='utf-8')
print("Plastid full UI appearance editor installed.")
print("Start: python3 plastid/pi_bridge_server.py --port /dev/ttyACM0")
print("Open: http://127.0.0.1:8765 (Ctrl+Shift+R to refresh)")
