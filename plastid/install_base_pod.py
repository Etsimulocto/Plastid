#!/usr/bin/env python3
"""Install Base and Pod workspaces into full Plastid UI. No firmware changes."""
from pathlib import Path
import shutil
p=Path(__file__).resolve().parent
target=p/"plastid_lab.html"
script=p/"base_pod_studio.js"
if not target.exists():
 raise SystemExit("Full app missing. Run: python3 plastid/restore_full_app.py")
html=target.read_text(encoding="utf-8")
js=script.read_text(encoding="utf-8").replace("</script>","<\\/script>")
a="<!-- PLASTID BASE POD START -->"
b="<!-- PLASTID BASE POD END -->"
block=a+"\n<script>\n"+js+"\n</script>\n"+b
if a in html and b in html:
 start=html.index(a);stop=html.index(b)+len(b)
 updated=html[:start]+block+html[stop:]
else:
 if "</body>" not in html.lower():raise SystemExit("Unexpected HTML; no files changed.")
 updated=html.replace("</body>",block+"\n</body>")
if updated!=html:
 backup=target.with_suffix(".html.pre-base-pod")
 if not backup.exists():shutil.copy2(target,backup)
 target.write_text(updated,encoding="utf-8")
print("Base and Pod simulator installed in the full Plastid app.")
print("No ESP32 firmware or physical charging/audio modified.")
print("Refresh browser with Ctrl+Shift+R.")
