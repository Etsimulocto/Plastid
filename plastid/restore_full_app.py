#!/usr/bin/env python3
"""Restore the full Plastid phone interface from the existing Pi app checkout.
Run once on the Pi. Never overwrites source or browser storage without backups.
"""
from pathlib import Path
import re
import shutil

dest=Path(__file__).resolve().parent
candidates=[
 Path.home()/"Downloads"/"MakerPhone_App_v02"/"makerphone_lab.html",
 Path.home()/"Downloads"/"MakerPhone_App_v02"/"MakerPhone_App_v02"/"makerphone_lab.html",
 Path.home()/"Downloads"/"Plastid_App_v03"/"plastid_lab.html",
 Path.home()/"Downloads"/"Plastid_App_v03"/"Plastid_App_v03"/"plastid_lab.html",
]
source=next((p for p in candidates if p.is_file()),None)
if source is None:
 raise SystemExit("Could not find your earlier full simulator. Keep ~/Downloads/MakerPhone_App_v02 in place and rerun; no files were changed.")
html=source.read_text(encoding="utf-8")
# Use the original full interface, preserving all pages and controls.
html=html.replace("MakerPhone", "Plastid").replace("makerphone", "plastid")
html=html.replace("localStorage.getItem('plastid-lab')||'{}'", "(localStorage.getItem('plastid-lab')||localStorage.getItem('makerphone-lab'))||'{}'")
# Preserve older localStorage and migrate only when Plastid storage is empty.
if "localStorage.getItem('plastid-lab')" in html and "localStorage.getItem('makerphone-lab')" not in html:
 html=html.replace("localStorage.getItem('plastid-lab')", "(localStorage.getItem('plastid-lab')||localStorage.getItem('makerphone-lab'))",1)
html=html.replace("Web Serial connects from Chromium-based browsers on Pi/PC.","The Raspberry Pi bridge connects to the ESP32 over USB at 115200 baud.")
html=html.replace("Web Serial requires a supported Chromium browser on localhost or secure origin","Pi USB bridge available from localhost")
html=html.replace("if(!('serial'in navigator))log('WARN','USB','Web Serial requires a supported Chromium browser on localhost or secure origin')","")
html=html.replace("if(!('serial' in navigator))log('WARN','USB','Web Serial requires a supported Chromium browser on localhost or secure origin')","")
html=html.replace("Connect USB</button>","Connect Pi USB</button>")
# Replace transport only; the dialer/contacts/messages/graphics/diagnostics are kept unchanged.
transport=r"""let plastidPoll=null, plastidSeq=0;
async function plastidApi(path,payload){
 const resp=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload||{})});
 const data=await resp.json();if(!resp.ok)throw Error(data.error||'USB bridge request failed');return data;
}
function sendObj(o,display=true){
 if(display)log('INFO','USB→',JSON.stringify(o));
 if(!state.usb){if(display)log('WARN','USB','not connected');return false}
 plastidApi('send',o).catch(e=>log('ERROR','USB','send failed: '+e.message));return true;
}
function sendCommand(op){if(op==='hello')sendObj({op:'hello',app:'Plastid Lab',version:'0.3.1'});else sendObj({op:op,id:'pl-'+Date.now()})}
async function connectUsb(){
 try{
  await plastidApi('connect',{});
  state.usb=true;
  $('#usbStatus').textContent='PI USB BRIDGE CONNECTED';
  $('#usbDot').className='dot ok';$('#metricUsb').textContent='ONLINE';
  $('#metricUsbDot').className='dot ok';$('#metricUsbText').textContent='serial bridge open';
  $('#connectBtn').disabled=true;$('#disconnectBtn').disabled=false;
  log('OK','USB','Pi serial bridge connected');
  if(plastidPoll)clearInterval(plastidPoll);
  plastidPoll=setInterval(plastidReceive,450);
  await new Promise(r=>setTimeout(r,2200));
  sendCommand('hello');
 }catch(e){log('ERROR','USB','connect failed: '+e.message);toast('Connection failed: '+e.message)}
}
async function plastidReceive(){
 if(!state.usb)return;
 try{
  const r=await fetch('/api/status?since='+plastidSeq);
  const d=await r.json();
  if(!d.connected){await disconnectUsb(false);return}
  for(const item of d.events||[]){plastidSeq=Math.max(plastidSeq,item.seq);handleLine(item.line)}
 }catch(e){log('WARN','USB','polling: '+e.message)}
}
async function disconnectUsb(doLog=true){
 if(plastidPoll){clearInterval(plastidPoll);plastidPoll=null}
 try{await plastidApi('disconnect',{})}catch(e){}
 state.usb=false;$('#usbStatus').textContent='SIMULATION MODE';$('#usbDot').className='dot';
 $('#metricUsb').textContent='OFFLINE';$('#metricUsbDot').className='dot warn';
 $('#metricUsbText').textContent='waiting for board';
 $('#connectBtn').disabled=false;$('#disconnectBtn').disabled=true;
 if(doLog)log('WARN','USB','serial disconnected')
}
"""
begin=html.find("function sendObj(")
finish=html.find("function handleLine(",begin)
if begin<0 or finish<0:raise SystemExit("Full app structure did not match; nothing changed.")
html=html[:begin]+transport+html[finish:]
begin=html.find("async function disconnectUsb(")
finish=html.find("function consoleSend(",begin)
if begin>=0 and finish>begin:
 html=html[:begin]+html[finish:]
target=dest/"plastid_lab.html"
if target.exists():
 shutil.copy2(target,target.with_suffix(".html.previous"))
target.write_text(html,encoding="utf-8")
# Put the known v0.2 localhost serial server next to the restored UI.
server_source=source.parent/"pi_bridge_server.py"
server_target=dest/"pi_bridge_server.py"
if not server_source.exists():raise SystemExit("App restored, but missing v0.2 pi_bridge_server.py")
if server_target.exists():shutil.copy2(server_target,server_target.with_suffix(".py.previous"))
server=server_source.read_text(encoding="utf-8")
server=server.replace("MakerPhone","Plastid").replace("makerphone","plastid")
server_target.write_text(server,encoding="utf-8")
print("Restored full Plastid app with Pi USB bridge")
print("Source:",source)
print("Run: python3 plastid/pi_bridge_server.py --port /dev/ttyACM0")
print("Open: http://127.0.0.1:8765")
