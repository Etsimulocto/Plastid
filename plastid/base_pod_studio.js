/* Plastid Base + Pod Studio — simulation only, saved locally. */
(()=>{"use strict";
const KEY='plastid-device-studio-v1';
let s={phoneDock:false,podDock:false,phoneCharge:63,podCharge:72,baseCharge:'mains',audio:'phone',call:'idle',caller:'Anna',message:'See you this afternoon!',podScreen:'home',screen:'dashboard',size:22,contrast:true,brightness:65,alerts:true,log:[]};
try{s={...s,...JSON.parse(localStorage.getItem(KEY)||'{}')}}catch(_){}
const q=(x)=>document.querySelector(x);
const css=document.createElement('style');css.textContent=`
#plastid-devices{margin:18px 0;padding:20px;border:1px solid #3e5465;border-radius:18px;background:#101d29;color:#eef6fc;font:18px system-ui}
#plastid-devices h2{font-size:24px;margin:0 0 8px}#plastid-devices h3{font-size:20px;margin:12px 0}#plastid-devices p{line-height:1.5}
.pd-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:15px 0}.pd-tabs button,.pd-actions button{background:#234c5e;color:#fff;border:2px solid #81a7b7;border-radius:10px;min-height:48px;padding:10px 14px;font:inherit;cursor:pointer}
.pd-tabs button[aria-selected=true]{background:#087b84}.pd-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.pd-card{padding:15px;border:1px solid #456172;border-radius:14px;background:#182c3d}.pd-actions{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.pd-display{background:#02080c;border:7px solid #536c7d;border-radius:12px;color:#fff;min-height:150px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px;text-align:center;padding:14px;max-width:350px;margin:auto}
.pd-display b{font-size:var(--pd-font,22px);line-height:1.2}.pd-display small{font-size:14px;color:#b1d7df}
#plastid-devices label{display:flex;flex-direction:column;gap:6px;margin:8px 0}#plastid-devices input,#plastid-devices select{background:#071722;color:#fff;border:2px solid #688b9c;min-height:42px;border-radius:8px;font-size:17px;padding:6px}
#plastid-devices .pd-on{color:#96f1ba}.pd-muted{color:#bad0d9}.pd-log{max-height:140px;overflow:auto;font:13px monospace;background:#050e16;padding:10px;border-radius:8px}
@media(max-width:600px){#plastid-devices{padding:12px}.pd-grid{grid-template-columns:1fr}}
`;document.head.appendChild(css);
const host=document.createElement('section');host.id='plastid-devices';host.setAttribute('aria-label','Plastid Base and Pod simulator');
function save(){localStorage.setItem(KEY,JSON.stringify(s))}
function event(t){s.log.unshift(new Date().toLocaleTimeString()+' · '+t);s.log=s.log.slice(0,40);save()}
function button(action,label){return `<button type="button" data-a="${action}">${label}</button>`}
function row(name,value){return `<p><strong>${name}</strong> — ${value}</p>`}
function nav(){return `<div class="pd-tabs" role="tablist" aria-label="Device sections">${['dashboard','base','pod','simulator'].map(k=>`<button role="tab" aria-selected="${s.screen===k}" data-tab="${k}">${k[0].toUpperCase()+k.slice(1)}</button>`).join('')}</div>`}
function base(){return `<div class="pd-grid"><div class="pd-card"><h3>Charging bays</h3>
${row('Phone bay',s.phoneDock?'Docked · charging simulation':'Empty')}
${row('Pod bay',s.podDock?'Docked · charging simulation':'Empty')}
<div class="pd-actions">${button('dockPhone',s.phoneDock?'Undock Phone':'Dock Phone')}${button('dockPod',s.podDock?'Undock Pod':'Dock Pod')}</div>
<p class="pd-muted">Physical charging is unimplemented. Six-contact data/power link is a design candidate; no pin assignments yet.</p></div>
<div class="pd-card"><h3>Base touchscreen</h3>${row('Archive','Not installed · simulated')}${row('Backups','Not yet implemented')}${row('Update service','Design pending')}
<div class="pd-actions">${button('backup','Simulate backup')}${button('diagnostic','Run simulated check')}</div>
<p class="pd-muted">Actual data transfer, storage integrity, charging and firmware updates are not active.</p></div>
<div class="pd-card"><h3>Speakerphone routing</h3>${row('Audio output',s.audio.toUpperCase())}
${row('Call',s.call==='active'?'Simulated call active':s.call==='incoming'?'Simulated incoming call':'Idle')}
<div class="pd-actions">${button('baseAudio','Route to Base')}${button('phoneAudio','Route to Phone')}</div>
<p class="pd-muted">Audio routing is modeled only; no microphone or loudspeaker connected.</p></div></div>`}
function pod(){let text=s.podScreen==='message'?s.message:s.podScreen==='call'?s.caller:s.podScreen==='battery'?'Battery '+s.podCharge+'%':'READY';
let sub=s.podScreen==='message'?'Message preview':s.podScreen==='call'?'Incoming caller':s.podScreen==='battery'?'Charge simulated':s.call==='incoming'?'Incoming call':'Phone connected (simulated)';
return `<div class="pd-grid"><div class="pd-card"><h3>Pod 128×64 screen concept</h3><div class="pd-display" style="--pd-font:${s.size}px"><small>PLASTID POD · 128×64 CONCEPT</small><b>${text.replace(/[<>&"]/g,'')}</b><small>${sub}</small></div>
<div class="pd-actions">${button('up','▲')}${button('left','◀')}${button('select','● Select')}${button('right','▶')}${button('down','▼')}</div>
<p class="pd-muted">Joystick/button actions are simulated. No hardware Pod is paired.</p></div>
<div class="pd-card"><h3>Accessibility</h3><label>Large text size <strong>${s.size}px (concept preview)</strong><input type="range" data-k="size" min="18" max="38" value="${s.size}"></label>
<label><span>Alerts</span><select data-k="alerts"><option value="true" ${s.alerts?'selected':''}>On</option><option value="false" ${!s.alerts?'selected':''}>Off</option></select></label>
<p class="pd-muted">Font size saved separately for the Pod. This is not a pixel-accurate OLED firmware renderer yet.</p></div>
<div class="pd-card"><h3>Pod status</h3>${row('Connection','Simulated BLE data')}${row('Speaker / mic','Unverified')}${row('Battery',s.podCharge+'% simulated')}${row('Voice transport','Unselected · requires audio test')}
<div class="pd-actions">${button('podAudio','Route call to Pod')}${button('home','Pod home')}</div></div></div>`}
function simulator(){return `<div class="pd-grid"><div class="pd-card"><h3>Simulated call</h3><div class="pd-actions">${button('incoming','Incoming call')}${button('answer','Answer')}${button('hangup','End call')}</div>${row('State',s.call)}${row('Current audio',s.audio)}</div>
<div class="pd-card"><h3>Simulated notification</h3><div class="pd-actions">${button('message','New text alert')}${button('missed','Missed call')}${button('lowBattery','Low Pod battery')}</div><p class="pd-muted">Nothing is sent to a cellular network, Bluetooth device, or speaker.</p></div></div>`}
function render(){host.innerHTML=`<h2>Plastid · Base & Pod</h2><p class="pd-muted">Integrated system design simulator. Phone remains the cellular gateway. No Base or Pod hardware is connected.</p>${nav()}${s.screen==='base'?base():s.screen==='pod'?pod():s.screen==='simulator'?simulator():`<div class="pd-grid"><div class="pd-card"><h3>Base</h3>${row('Phone',s.phoneDock?'Docked':'Away')}${row('Pod',s.podDock?'Docked':'Away')}${row('Speakerphone',s.audio==='base'?'Selected (simulated)':'Standby')}${button('tabBase','Open Base')}</div><div class="pd-card"><h3>Phone</h3>${row('Cellular','No modem yet')}${row('Prototype','ESP32-S3 USB bridge working')}${row('Call',s.call)}<p class="pd-muted">Phone workspace remains in the original full app.</p></div><div class="pd-card"><h3>Pod</h3>${row('Display','128×64 OLED target')}${row('Audio','Bluetooth path unverified')}${row('Battery',s.podCharge+'% simulated')}${button('tabPod','Open Pod')}</div></div>`}
<h3>Simulation events</h3><div class="pd-log" aria-live="polite">${s.log.slice(0,12).map(t=>'<div>'+t.replace(/[<>&"]/g,'')+'</div>').join('')||'No simulated events yet.'}</div>`;
}
host.addEventListener('click',e=>{const tab=e.target.closest('[data-tab]');if(tab){s.screen=tab.dataset.tab;save();render();return}
const a=e.target.closest('[data-a]')?.dataset.a;if(!a)return;
switch(a){
case 'tabBase':s.screen='base';break;case 'tabPod':s.screen='pod';break;
case 'dockPhone':s.phoneDock=!s.phoneDock;event('Phone '+(s.phoneDock?'docked':'undocked'));break;
case 'dockPod':s.podDock=!s.podDock;event('Pod '+(s.podDock?'docked':'undocked'));break;
case 'baseAudio':s.audio='base';event('Base audio selected (simulated)');break;
case 'phoneAudio':s.audio='phone';event('Phone audio selected (simulated)');break;
case 'podAudio':s.audio='pod';event('Pod audio selected (simulated)');break;
case 'incoming':s.call='incoming';s.podScreen='call';event('Incoming call (simulated)');break;
case 'answer':if(s.call==='incoming'){s.call='active';event('Call answered (simulated)')}break;
case 'hangup':s.call='idle';event('Call ended (simulated)');break;
case 'message':s.podScreen='message';event('New message notification (simulated)');break;
case 'missed':s.podScreen='call';event('Missed call notification (simulated)');break;
case 'lowBattery':s.podCharge=15;s.podScreen='battery';event('Pod battery low (simulated)');break;
case 'diagnostic':event('Simulated Base diagnostic complete; hardware unverified');break;
case 'backup':event('Backup DEMO only — no data was copied');break;
case 'up':s.podScreen='message';break;case 'down':s.podScreen='battery';break;
case 'left':s.podScreen='home';break;case 'right':s.podScreen='call';break;
case 'select':if(s.call==='incoming'){s.call='active';event('Pod answered simulated call')}else event('Pod select');break;
case 'home':s.podScreen='home';break;
}save();render()});
host.addEventListener('change',e=>{const k=e.target.dataset.k;if(!k)return;s[k]=e.target.type==='range'?Number(e.target.value):e.target.value==='true';save();render()});
host.addEventListener('input',e=>{if(e.target.dataset.k==='size'){s.size=Number(e.target.value);save();render()}});
(document.querySelector('.shell')||document.body).appendChild(host);render();
})();