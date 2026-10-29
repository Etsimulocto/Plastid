/* Plastid visual UI editor v0.1 - browser only, no board flashing. */
(()=>{'use strict';
const STORE='plastid-ui-editor-v1';
const defaults={font:'system-ui',size:18,screenFont:18,screenColor:'#e8f3f7',screenBg:'#071724',bg:'#09131c',panel:'#101f2b',text:'#ffffff',muted:'#b9c8d1',accent:'#48d6d0',keySize:54,phoneWidth:470,uiScale:100,highContrast:false};
let cfg={...defaults};try{cfg={...cfg,...JSON.parse(localStorage.getItem(STORE)||'{}')}}catch(_){}
const safe=(x)=>String(x).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const css=document.createElement('style');css.id='plastid-ui-editor-style';document.head.appendChild(css);
const editor=document.createElement('section');editor.id='plastid-editor';editor.className='panel';editor.setAttribute('aria-label','Plastid appearance editor');
editor.innerHTML=`<div class="panel-head"><h2>Visual UI editor</h2><span class="tag">LIVE PREVIEW · LOCAL</span></div>
<div class="plastid-editor-inner"><p class="muted">Designed for comfortable landscape reading. Changes apply immediately and stay in this browser. Physical TFT layout will need separate device firmware later.</p>
<div class="plastid-edit-grid">
<label>Font family<select data-p="font"><option value="system-ui">System / clear</option><option value="Arial, sans-serif">Arial</option><option value="Verdana, sans-serif">Verdana</option><option value="Tahoma, sans-serif">Tahoma</option><option value="Georgia, serif">Georgia</option><option value="monospace">Monospace</option></select></label>
<label>App text size <output data-o="size"></output><input data-p="size" type="range" min="14" max="32" step="1"></label>
<label>Phone preview text size <output data-o="screenFont"></output><input data-p="screenFont" type="range" min="12" max="30" step="1"></label>
<label>Preview width <output data-o="phoneWidth"></output><input data-p="phoneWidth" type="range" min="320" max="750" step="10"></label>
<label>Keypad button height <output data-o="keySize"></output><input data-p="keySize" type="range" min="44" max="95" step="1"></label>
<label>Screen text color<input data-p="screenColor" type="color"></label>
<label>Screen background<input data-p="screenBg" type="color"></label>
<label>App background<input data-p="bg" type="color"></label>
<label>Panel color<input data-p="panel" type="color"></label>
<label>Main text<input data-p="text" type="color"></label>
<label>Secondary text<input data-p="muted" type="color"></label>
<label>Accent color<input data-p="accent" type="color"></label>
<label class="plastid-switch"><input data-p="highContrast" type="checkbox"> High contrast</label>
</div><div class="row plastid-editor-actions">
<button class="btn primary" id="plastid-save-theme">Save theme</button>
<button class="btn" id="plastid-export-theme">Export JSON</button>
<label class="btn" for="plastid-import-theme" style="cursor:pointer">Import JSON</label><input id="plastid-import-theme" type="file" accept=".json,application/json" hidden>
<button class="btn danger" id="plastid-reset-theme">Reset to defaults</button></div>
<div class="muted small" id="plastid-save-note" role="status" aria-live="polite">Editing live; not saved until you click Save theme.</div>
</div>`;
const scaffold=document.createElement('style');
scaffold.textContent=`#plastid-editor{margin:16px 0} .plastid-editor-inner{padding:18px}.plastid-edit-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}.plastid-edit-grid label{display:flex;flex-direction:column;gap:8px;font-weight:650}.plastid-edit-grid input[type="range"]{width:100%;height:32px;accent-color:var(--cyan)}.plastid-edit-grid input[type="color"]{height:44px;width:100%;background:transparent;border:1px solid var(--line);border-radius:8px}.plastid-edit-grid select{min-height:44px;background:var(--panel);color:var(--text);border:1px solid var(--line);padding:10px}.plastid-switch{flex-direction:row!important;align-items:center}.plastid-switch input{width:25px;height:25px}.plastid-editor-actions{margin-top:20px}.plastid-editor-actions button{min-height:44px}@media(min-width:950px){body.plastid-wide .layout{grid-template-columns:minmax(440px, 1fr) minmax(420px,1.15fr)}body.plastid-wide .phone{max-width:var(--plastid-phone-width)!important}}@media(max-width:700px){.plastid-edit-grid{grid-template-columns:1fr}}`;
document.head.appendChild(scaffold);
function apply(){
 const c=cfg;document.body.classList.add('plastid-wide');
 css.textContent=`:root{--bg:${c.bg};--panel:${c.panel};--text:${c.text};--muted:${c.muted};--cyan:${c.accent};--plastid-phone-width:${c.phoneWidth}px}body{background:${c.bg}!important;color:${c.text}!important;font-family:${c.font}!important;font-size:${c.size}px!important}.shell{max-width:1900px}.panel{background:${c.panel}!important}.phone{max-width: min(100%, ${c.phoneWidth}px)!important}.btn,.tab,.input,.select{font-size:max(16px,1em)!important;min-height:44px}.key{min-height:${c.keySize}px!important}.key b{font-size:clamp(20px,${c.size+5}px,38px)!important}.key small{font-size:clamp(12px,${c.size-3}px,22px)!important}.panel-head h2,.card h3{font-size:1em!important}.muted,.small,.pill,.notice,.sim-help,.screen-meta,.tag,.status{font-size:.84em!important}.tabpage{line-height:1.6} .logbox{font-size: max(13px,.75em)}${c.highContrast?'body{background:#000!important}.panel,.card{background:#000!important;border-color:#fff!important}.muted{color:#fff!important}.btn,.key{border:2px solid white!important}':''}`;
 window.plastidScreenTheme={fontSize:c.screenFont,color:c.screenColor,bg:c.screenBg};
 if(typeof window.drawScreen==='function')window.drawScreen();
}
function refresh(){editor.querySelectorAll('[data-p]').forEach(el=>{let k=el.dataset.p;el.type==='checkbox'?el.checked=!!cfg[k]:el.value=cfg[k]});editor.querySelectorAll('[data-o]').forEach(el=>{const k=el.dataset.o;el.textContent=cfg[k]+(k==='phoneWidth'||k==='keySize'||k==='size'||k==='screenFont'?' px':'')});apply()}
editor.addEventListener('input',e=>{let el=e.target;if(!el.matches('[data-p]'))return;cfg[el.dataset.p]=el.type==='checkbox'?el.checked:el.type==='range'?Number(el.value):el.value;refresh();editor.querySelector('#plastid-save-note').textContent='Unsaved changes · live preview'});
editor.querySelector('#plastid-save-theme').onclick=()=>{localStorage.setItem(STORE,JSON.stringify(cfg));editor.querySelector('#plastid-save-note').textContent='Theme saved on this Raspberry Pi browser.'};
editor.querySelector('#plastid-export-theme').onclick=()=>{const blob=new Blob([JSON.stringify({app:'Plastid',version:1,theme:cfg},null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='plastid-theme.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};
editor.querySelector('#plastid-import-theme').onchange=async e=>{try{const text=await e.target.files[0].text();const obj=JSON.parse(text);if(obj.app!=='Plastid'||!obj.theme)throw Error('Not a Plastid theme');for(const [key,val] of Object.entries(obj.theme)){if(!(key in defaults))continue;if(typeof defaults[key]!==typeof val)continue;if(typeof val==='number'){const bounds={size:[14,32],screenFont:[12,30],phoneWidth:[320,750],keySize:[44,95]};if(bounds[key]&&(val<bounds[key][0]||val>bounds[key][1]))continue}if(key.endsWith('Color')||['bg','panel','text','muted','accent'].includes(key)){if(!/^#[0-9a-f]{6}$/i.test(val))continue}if(key==='font'&&!['system-ui','Arial, sans-serif','Verdana, sans-serif','Tahoma, sans-serif','Georgia, serif','monospace'].includes(val))continue;cfg[key]=val}refresh();editor.querySelector('#plastid-save-note').textContent='Theme imported; click Save to retain it'}catch(err){alert('Import failed: '+err.message)}};
editor.querySelector('#plastid-reset-theme').onclick=()=>{if(!confirm('Reset appearance settings only? Contacts and messages are unaffected.'))return;cfg={...defaults};localStorage.removeItem(STORE);refresh()};
const host=document.querySelector('.shell');if(host){host.append(editor);refresh()}
})();