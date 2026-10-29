#!/usr/bin/env python3
"""Plastid Pi USB bench: serial bridge + local web interface. No flashing."""
import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import serial

HTML = r'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Plastid | Pi Bench</title><style>
:root{font:16px system-ui;color:#eaf2ff;background:#0b1220}body{max-width:1040px;margin:auto;padding:28px}
header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #34425c}small{color:#a4b3ce}
main{display:grid;grid-template-columns:minmax(260px,360px) 1fr;gap:25px;margin-top:20px}
section{border:1px solid #34425c;border-radius:18px;padding:22px;background:#152036}
.screen{background:#05142a;border:7px solid #243951;border-radius:12px;aspect-ratio:4/3;padding:15px;color:#b6f1e5;overflow:auto}
.keys{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:20px}button{border:1px solid #526887;background:#253f60;color:white;padding:13px;border-radius:10px;cursor:pointer;font-size:18px}
button:hover{background:#355d8b}button:focus-visible{outline:3px solid white}pre{overflow:auto;white-space:pre-wrap;word-break:break-word;max-height:300px;font-size:12px}
.menu{display:flex;flex-wrap:wrap;gap:8px}.menu button{font-size:14px}.ok{color:#6ee7b7}.warn{color:#f9c66a}
@media(max-width:720px){main{grid-template-columns:1fr}}
</style><header><div><h1>Plastid</h1><small>Raspberry Pi · ESP32-S3 development bench</small></div><strong id="state">Connecting…</strong></header>
<main><section><div class="screen"><small>PLASTID / SIMULATOR</small><h2 id="page">Home</h2><p id="entry">Dial a number or open a menu.</p><small>Keypad and menu are simulated. No SMS or calls are sent.</small></div>
<div class="keys" id="keys"></div><div class="menu" style="margin-top:12px"><button onclick="dial()">Call (simulation)</button><button onclick="clearDial()">End / Clear</button></div></section>
<section><h2>Device connection</h2><p>Physical USB serial: <strong id="port">—</strong></p><p>Firmware: <strong id="identity">Awaiting response</strong></p>
<div class="menu"><button onclick="cmd('hello')">Identify</button><button onclick="cmd('status')">Status</button><button onclick="cmd('diag.run')">Diagnostics</button><button onclick="cmd('modem.status')">Modem status</button></div>
<h2>Simulated phone screens</h2><div class="menu"><button onclick="menu('Contacts')">Contacts</button><button onclick="menu('Messages')">Messages</button><button onclick="menu('Files')">Files</button><button onclick="menu('Settings')">Settings</button></div>
<h2>Serial events</h2><pre id="log">Loading…</pre><small>Read-only by default; command buttons send only JSON to the existing bridge firmware. This is not a firmware uploader.</small></section></main>
<script>
let number='',cursor=0,all=[],live=false;
const $=s=>document.querySelector(s);
for(const key of ['1','2','3','4','5','6','7','8','9','*','0','#']){const b=document.createElement('button');b.textContent=key;b.onclick=()=>{number+=key;$('#page').textContent='Dialer';$('#entry').textContent=number};$('#keys').appendChild(b)}
function menu(p){$('#page').textContent=p;$('#entry').textContent=p==='Contacts'?'No contacts added in this bench yet.':p==='Messages'?'No modem installed; messages are simulated.':p==='Files'?'File storage module pending.':'USB identity and diagnostics available.'}
function dial(){$('#page').textContent='Call simulation';$('#entry').textContent=number||'No number entered'}
function clearDial(){number='';$('#page').textContent='Home';$('#entry').textContent='Dial a number or open a menu.'}
async function cmd(op){try{const r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({op})});const v=await r.json();if(!r.ok)throw Error(v.error);show('TX '+JSON.stringify({op}))}catch(e){show('ERROR '+e.message)}}
function show(s){all.push(s);all=all.slice(-100);$('#log').textContent=all.join('\n')}
async function poll(){try{const r=await fetch('/api/events?after='+cursor);const v=await r.json();$('#state').textContent=v.connected?'USB link open':'USB offline';$('#state').className=v.connected?'ok':'warn';$('#port').textContent=v.port;for(const e of v.events){cursor=e.id;show(e.time+' '+e.kind+' '+e.text);if(e.kind==='RX'){try{const x=JSON.parse(e.text);if(x.type==='hello')$('#identity').textContent=(x.project||'Unknown')+' / '+x.fw+' / '+x.board}catch(_){}}}}catch(e){$('#state').textContent='Server unavailable'}}setInterval(poll,1000);poll();
</script></html>'''

class Bridge:
    def __init__(self, port):
        self.port=port; self.events=[]; self.seq=0; self.lock=threading.Lock(); self.ser=None
        threading.Thread(target=self.listen,daemon=True).start()
    def emit(self,kind,msg):
        with self.lock:
            self.seq+=1; self.events.append(dict(id=self.seq,time=time.strftime('%H:%M:%S'),kind=kind,text=str(msg)[:1000]));self.events=self.events[-250:]
    def listen(self):
        while True:
            try:
                with serial.Serial(self.port,115200,timeout=.25,write_timeout=1,rtscts=False,dsrdtr=False,exclusive=True) as s:
                    s.dtr=False;s.rts=False
                    with self.lock:self.ser=s
                    self.emit('LINK','Serial connected; waiting for board startup')
                    time.sleep(2)
                    self.send({'op':'hello','app':'Plastid Pi Bench','version':'0.3'})
                    while True:
                        line=s.readline()
                        if line:self.emit('RX',line.decode('utf-8','replace').strip())
            except Exception as e:self.emit('LINK',f'Disconnected: {e}')
            finally:
                with self.lock:self.ser=None
            time.sleep(2)
    def send(self,obj):
        with self.lock:
            if self.ser is None or not self.ser.is_open:raise RuntimeError('ESP32 serial connection is offline')
            self.ser.write((json.dumps(obj,separators=(',',':'))+'\n').encode());self.ser.flush()
        self.emit('TX',json.dumps(obj))

class Handler(BaseHTTPRequestHandler):
    def send_json(self,status,value):
        payload=json.dumps(value).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def do_GET(self):
        if self.path.startswith('/api/events'):
            from urllib.parse import urlsplit,parse_qs
            try:after=int(parse_qs(urlsplit(self.path).query).get('after',['0'])[0])
            except ValueError:after=0
            with self.server.bridge.lock:
                b=self.server.bridge
                result=dict(connected=b.ser is not None,port=b.port,events=[x for x in b.events if x['id']>after][-100:])
            return self.send_json(200,result)
        if self.path in ('/','/index.html'):
            data=HTML.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
        self.send_json(404,{'error':'Not found'})
    def do_POST(self):
        if self.path!='/api/command':return self.send_json(404,{'error':'Not found'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<2 or n>256:raise ValueError('Invalid request length')
            body=json.loads(self.rfile.read(n));op=body.get('op')
            if op not in ('hello','status','diag.run','modem.status'):raise ValueError('Unsupported command')
            self.server.bridge.send({'op':op})
            self.send_json(200,{'sent':op})
        except (RuntimeError,ValueError,json.JSONDecodeError) as e:self.send_json(400,{'error':str(e)})
    def log_message(self,*_):pass

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',default='/dev/ttyACM0');p.add_argument('--listen',default='127.0.0.1');p.add_argument('--http-port',type=int,default=8765);args=p.parse_args()
    h=ThreadingHTTPServer((args.listen,args.http_port),Handler);h.bridge=Bridge(args.port)
    print(f'Plastid Pi Bench at http://{args.listen}:{args.http_port}  ESP32: {args.port}',flush=True)
    try:h.serve_forever()
    except KeyboardInterrupt:pass
