#!/usr/bin/env python3
"""Install Plastid Pi desktop launcher; don't modify the existing app."""
from pathlib import Path
import os,shutil,stat
root=Path(__file__).resolve().parent
home=Path.home()
icons=home/".local/share/icons"
apps=home/".local/share/applications"
desktop=home/"Desktop"
for d in (icons,apps,desktop):d.mkdir(parents=True,exist_ok=True)
icon=icons/"plastid.svg"
shutil.copy2(root/"plastid_icon.svg",icon)
script=home/".local/bin/plastid-launch"
script.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/"launch_plastid.sh",script)
script.chmod(script.stat().st_mode|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)
entry="[Desktop Entry]\nVersion=1.0\nType=Application\nName=Plastid\nComment=Plastid Phone, Pod and Base development studio\nExec="+str(script)+"\nIcon="+str(icon)+"\nTerminal=false\nCategories=Development;Utility;\nStartupNotify=true\n"
for p in (apps/"plastid.desktop",desktop/"Plastid.desktop"):
 p.write_text(entry,encoding="utf-8")
 p.chmod(0o755)
print("Installed Plastid launcher and icon.")
print("Desktop:",desktop/"Plastid.desktop")
print("Menu:",apps/"plastid.desktop")
print("Icon:",icon)
print("If Raspberry Pi OS asks to trust the desktop launcher, choose Allow Launching.")
