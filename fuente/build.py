#!/usr/bin/env python3
"""Genera las pantallas y overlays del kit de transmisión Abastible (carpeta out/)."""
import base64, os

B = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
F = 'node_modules/@fontsource/'
def face(fam, path, w):
    return '@font-face{font-family:"%s";font-weight:%d;src:url(data:font/woff2;base64,%s) format("woff2");}' % (fam, w, B(F + path))
FONTS = ''.join([
    face('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-400-normal.woff2', 400),
    face('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-500-normal.woff2', 500),
    face('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-700-normal.woff2', 700),
    face('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-800-normal.woff2', 800),
    face('Titillium Web', 'titillium-web/files/titillium-web-latin-400-normal.woff2', 400),
    face('Titillium Web', 'titillium-web/files/titillium-web-latin-600-normal.woff2', 600),
    face('Titillium Web', 'titillium-web/files/titillium-web-latin-700-normal.woff2', 700),
])

def small(png, w):
    from PIL import Image
    import io
    im = Image.open(png); im.thumbnail((w, w * 2)); b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
LOGO_W = small('logo_white.png', 1400)    # logo para fondos azules
LOGO_C = small('logo_color.png', 1400)    # logo a color para fondos blancos
ISO = small('isotipo.png', 700)           # isotipo (la "a" en el óvalo naranjo)
ISOM = small('isotipo_mono.png', 700)     # isotipo blanco (para fondos naranjos)
LOGO_M = small('logo_mono.png', 1400)     # logo blanco completo (para fondos naranjos)
BLOB = open('blob_path.txt').read().strip()  # silueta del isotipo, viewBox 0 0 100 78.2

# ---------------------------------------------------------------------------------------------
# Sistema visual tomado de abastible.cl: naranjo #FE5000, azul #001489 / #003594 (logo),
# blanco, grises #6A6A6A / #232323; Ubuntu Sans (títulos y texto) y Titillium Web (apoyo).
# Formas: la silueta redondeada del isotipo, esquinas muy redondeadas, nada de cortes en diagonal.
# ---------------------------------------------------------------------------------------------
BASE = r'''
:root{--or:#FE5000;--or2:#FF7A33;--or-rgb:254,80,0;--az:#001489;--az2:#003594;--azd:#000A45;--az-rgb:0,20,137;
 --ink:#fff;--gr:#6A6A6A;--gr2:#B9BED0;--cl:#F4F6FB;--dk:#232323}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;font-family:"Ubuntu Sans",sans-serif;color:var(--ink)}
.tw{font-family:"Titillium Web",sans-serif}
@keyframes floatA{0%,100%{transform:translate(0,0) rotate(-12deg)}50%{transform:translate(-30px,24px) rotate(-6deg)}}
@keyframes floatB{0%,100%{transform:translate(0,0) rotate(18deg)}50%{transform:translate(26px,-30px) rotate(24deg)}}
@keyframes ring{0%{transform:scale(.6);opacity:.55}100%{transform:scale(1.9);opacity:0}}
@keyframes up{from{opacity:0;transform:translateY(46px)}to{opacity:1;transform:none}}
@keyframes left{from{opacity:0;transform:translateX(-90px)}to{opacity:1;transform:none}}
@keyframes pop{0%{transform:scale(.2) rotate(-30deg);opacity:0}70%{transform:scale(1.08) rotate(3deg);opacity:1}100%{transform:none}}
@keyframes pulse{50%{opacity:.3}}
@keyframes breathe{50%{transform:scale(1.04)}}
@keyframes wave{to{transform:translateX(-50%)}}
'''
FULL = r'''
body{background:var(--or)}
.stage{position:relative;width:1920px;height:1080px;overflow:hidden;
 background:radial-gradient(1100px 760px at 72% 26%,rgba(255,96,24,.45),transparent 70%),radial-gradient(900px 600px at 8% 95%,rgba(200,54,0,.7),transparent 70%),linear-gradient(155deg,#FE5000 0%,#F44C00 45%,#E04600 100%)}
.blob{position:absolute;pointer-events:none}
.blob svg{width:100%;height:100%;overflow:visible}
.blob.o path{fill:var(--az)}
.blob.w path{fill:rgba(255,255,255,.14)}
.blob.l path{fill:none;stroke:rgba(255,255,255,.28);stroke-width:.35}
.blob.g path{fill:rgba(255,255,255,.08)}
.b1{width:1180px;height:923px;right:-330px;top:-260px;animation:floatA 16s ease-in-out infinite;opacity:.95}
.b2{width:900px;height:704px;left:-360px;bottom:-330px;animation:floatB 19s ease-in-out infinite}
.b4{width:620px;height:485px;right:-190px;top:-170px;animation:floatA 16s ease-in-out infinite}
.b3{width:1350px;height:1056px;right:-420px;top:-330px;animation:floatA 22s ease-in-out infinite reverse}
.waves{position:absolute;left:0;right:0;bottom:120px;height:180px;opacity:.22;overflow:hidden}
.waves svg{width:3840px;height:180px;animation:wave 18s linear infinite}
.waves path{fill:none;stroke:#fff;stroke-width:2}
.logo{position:absolute;top:64px;left:80px;width:330px}
.bar{position:absolute;left:0;right:0;bottom:0;height:120px;background:#fff;display:flex;align-items:center;padding:0 80px;gap:0;color:var(--az2);z-index:3}
.cell{display:flex;align-items:center;gap:18px;padding:0 44px;border-left:2px solid #E3E6EF;height:64px}
.cell:first-child{padding-left:0;border-left:0}
.cell svg{width:42px;height:42px;flex:none;stroke:var(--or);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.cell b{display:block;font-size:30px;font-weight:700;line-height:1.05;white-space:nowrap}
.cell span{display:block;font-family:"Titillium Web";font-size:23px;color:var(--gr);white-space:nowrap}
.cell.web{margin-left:auto;border-left:0;padding-right:0}
.cell.web b{color:var(--or)}
.pill{display:inline-flex;align-items:center;gap:12px;background:var(--az);color:#fff;font-weight:700;font-size:28px;letter-spacing:1.5px;padding:10px 30px 10px 24px;border-radius:999px;box-shadow:0 10px 30px rgba(0,10,69,.3)}
.pill i{width:12px;height:12px;border-radius:50%;background:#fff}
.pill.live i{animation:pulse 2s ease-in-out infinite}
.hide{display:none!important}
'''

def blob(cls, extra=''):
    return '<div class="blob %s" %s><svg viewBox="0 0 100 78.2"><path d="%s"/></svg></div>' % (cls, extra, BLOB)

WAVES = '<div class="waves"><svg viewBox="0 0 3840 180" preserveAspectRatio="none">' + ''.join(
    '<path d="M0 %d ' % (40 + i * 26) + ' '.join('Q %d %d %d %d' % (x + 120, 40 + i * 26 + (-34 if (x // 240) % 2 == 0 else 34), x + 240, 40 + i * 26) for x in range(0, 3840, 240)) + '"/>'
    for i in range(5)) + '</svg></div>'
BG = blob('w b1') + blob('l b3') + blob('g b2') + WAVES
BGC = blob('o b4') + blob('l b3') + blob('g b2') + WAVES   # fondo tranquilo: el naranjo queda en la esquina

I_CAL = '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'
I_PIN = '<svg viewBox="0 0 24 24"><path d="M12 22s7-7.2 7-12.5A7 7 0 0 0 5 9.5C5 14.8 12 22 12 22z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
I_CLK = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
I_WEB = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>'
BAR = ('<div class="bar"><div class="cell">' + I_CAL + '<div><b data-ev="fecha">FECHA DEL EVENTO</b><span data-ev="hora_txt">INICIO 09:00 HRS</span></div></div>'
       '<div class="cell">' + I_PIN + '<div><b data-ev="lugar">LUGAR</b><span data-ev="dir">DIRECCIÓN · CIUDAD</span></div></div>'
       '<div class="cell web">' + I_WEB + '<div><b data-ev="web">abastible.cl</b><span data-ev="hashtag">#Abastible</span></div></div></div>')

# --- recepción de datos desde CONTROL_EN_VIVO (OBS WebSocket → evento "abas", BroadcastChannel o localStorage) ---
LIVE = r'''
function fitEl(el){var mx=+el.dataset.max,mn=+el.dataset.min||20,f=mx;el.style.fontSize=f+'px';
 var over=el.dataset.fit==='h'?function(){return el.scrollHeight>el.clientHeight+4}:function(){return el.scrollWidth>el.clientWidth+1};
 while(over()&&f>mn){f-=2;el.style.fontSize=f+'px'}}
function fitAll(){document.querySelectorAll('[data-fit]').forEach(fitEl)}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function setT(sel,v){document.querySelectorAll(sel).forEach(function(el){if(v!=null&&el.textContent!==String(v))el.textContent=v})}
var LAST=0,D={};
function applyLive(d){if(!d||!d.ts||d.ts<LAST)return;LAST=d.ts;D=d;
 if(d.ev){for(var k in d.ev)setT('[data-ev="'+k+'"]',d.ev[k]);document.querySelectorAll('[data-evshow]').forEach(function(e){e.classList.toggle('hide',!(d.ev[e.dataset.evshow]||'').trim())})}
 if(window.onLive)window.onLive(d);fitAll()}
window.addEventListener('abas',function(e){applyLive(e.detail)});
try{new BroadcastChannel('abas').onmessage=function(e){applyLive(e.data)}}catch(e){}
window.addEventListener('storage',function(e){if(e.key==='abas-live')try{applyLive(JSON.parse(e.newValue))}catch(x){}});
try{var L0=JSON.parse(localStorage.getItem('abas-live')||'null');if(L0)applyLive(L0)}catch(e){}
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fitAll);setTimeout(fitAll,300);
var Q=new URLSearchParams(location.search);
'''

def page(title, css, body, js='', full=True):
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8"><title>' + title + '</title><style>' + FONTS + BASE +
            (FULL if full else 'html,body{background:transparent}') + css + '</style></head><body>' + body +
            '<script>' + LIVE + js + '</script></body></html>')

P = {}

# =========================================================== INICIO
P['ABAS_Inicio'] = page('Abastible · Inicio', r'''
.left{position:absolute;left:80px;top:330px;width:1060px}
.ev{font-size:118px;font-weight:800;line-height:.98;letter-spacing:-2px;max-height:360px;overflow:hidden;animation:left .9s .1s ease both}
.lema{font-family:"Titillium Web";font-size:40px;font-weight:600;color:var(--az);margin-top:22px;animation:left .9s .25s ease both}
.cd{position:absolute;right:120px;top:380px;width:560px;text-align:center;animation:up .9s .3s ease both}
.cd .card{background:#fff;color:var(--az2);border-radius:44px;padding:40px 30px 34px;box-shadow:0 30px 80px rgba(0,0,0,.35)}
.cd small{display:block;font-family:"Titillium Web";font-size:28px;font-weight:700;letter-spacing:3px;color:var(--or)}
.cd b{display:block;font-size:150px;font-weight:800;line-height:1;letter-spacing:-3px;font-variant-numeric:tabular-nums;margin-top:6px}
.cd span{display:block;font-size:24px;color:var(--gr);margin-top:6px;letter-spacing:1px}
.iso{position:absolute;right:300px;top:230px;width:150px;animation:pop .8s .1s cubic-bezier(.16,1,.3,1) both}
.rings{position:absolute;right:120px;top:380px;width:560px;height:560px;pointer-events:none}
.rings i{position:absolute;inset:0;border:3px solid rgba(255,255,255,.35);border-radius:50%;animation:ring 4.5s ease-out infinite}
.rings i:nth-child(2){animation-delay:1.5s}.rings i:nth-child(3){animation-delay:3s}
.soon{font-size:56px!important}
''', '<div class="stage">' + BG + '<img class="logo" src="' + LOGO_M + '">'
 + '<div class="left"><div class="pill live" style="animation:left .8s ease both"><i></i><span data-ev="kicker_ini">TRANSMISIÓN EN VIVO</span></div>'
 + '<div class="ev" data-ev="nombre" data-fit="h" data-max="118" data-min="64" style="margin-top:34px">NOMBRE DEL EVENTO</div>'
 + '<div class="lema" data-ev="lema" data-evshow="lema">Lema o bajada del evento</div></div>'
 + '<div class="rings"><i></i><i></i><i></i></div>'
 + '<div class="cd"><div class="card"><small id="cdl">COMENZAMOS EN</small><b id="cd">10:00</b><span id="cds">LA TRANSMISIÓN PARTE A LAS 09:00</span></div></div>'
 + BAR + '</div>', r'''
var TGT=null;
window.onLive=function(d){if(d.ini){TGT=d.ini.target||null;if(d.ini.label)document.getElementById('cdl').textContent=d.ini.label}tick()};
function tick(){var b=document.getElementById('cd'),s=document.getElementById('cds');var hora=(D.ev&&D.ev.hora)||'';
 if(!TGT){b.textContent=hora||'PRONTO';b.classList.toggle('soon',!hora);s.textContent=hora?'HORA DE INICIO':'';return}
 var r=Math.max(0,Math.round((TGT-Date.now())/1000));b.classList.remove('soon');
 b.textContent=r>=3600?Math.floor(r/3600)+':'+String(Math.floor(r%3600/60)).padStart(2,'0')+':'+String(r%60).padStart(2,'0'):String(Math.floor(r/60)).padStart(2,'0')+':'+String(r%60).padStart(2,'0');
 s.textContent=r>0?(hora?'LA TRANSMISIÓN PARTE A LAS '+hora:''):'¡YA COMENZAMOS!'}
setInterval(tick,250);tick();''')

# =========================================================== PAUSA
P['ABAS_Pausa'] = page('Abastible · Pausa', r'''
.c{position:absolute;left:0;right:0;top:210px;text-align:center}
.iso{width:230px;animation:breathe 3.2s ease-in-out infinite}
.t{font-size:120px;font-weight:800;letter-spacing:-2px;line-height:1;margin-top:26px;animation:up .8s ease both}
.s{font-family:"Titillium Web";font-size:38px;font-weight:600;color:rgba(255,255,255,.9);margin-top:14px;animation:up .8s .1s ease both}
.clk{display:inline-block;margin-top:30px;font-size:84px;font-weight:800;color:var(--az);font-variant-numeric:tabular-nums;letter-spacing:2px}
.next{display:inline-flex;align-items:center;gap:26px;margin-top:34px;background:#fff;color:var(--az2);border-radius:999px;padding:14px 40px 14px 16px;box-shadow:0 20px 60px rgba(0,0,0,.35);animation:up .8s .25s ease both;max-width:1500px}
.next small{background:var(--or);color:#fff;font-weight:700;font-size:24px;letter-spacing:1.5px;padding:12px 26px;border-radius:999px;white-space:nowrap}
.next b{font-size:36px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.next span{font-family:"Titillium Web";font-size:26px;color:var(--gr);white-space:nowrap}
''', '<div class="stage">' + BGC + '<img class="logo" src="' + LOGO_M + '">'
 + '<div class="c"><img class="iso" src="' + ISOM + '"><div class="t" id="pt">VOLVEMOS EN UNOS MINUTOS</div><div class="s" id="ps">Gracias por acompañarnos</div>'
 + '<div class="clk hide" id="pc">05:00</div><br><div class="next hide" id="pn"><small>A CONTINUACIÓN</small><b id="pnt"></b><span id="pnh"></span></div></div>'
 + BAR + '</div>', r'''
var END=null;
window.onLive=function(d){var p=d.pau||{};document.getElementById('pt').textContent=p.titulo||'VOLVEMOS EN UNOS MINUTOS';document.getElementById('ps').textContent=p.sub||'';
 END=p.end||null;var a=d.ag||{},it=(a.items||[])[a.next!=null?a.next:(a.cur||0)+1];
 var n=document.getElementById('pn');n.classList.toggle('hide',!it||!p.next);if(it){document.getElementById('pnt').textContent=it.t||'';document.getElementById('pnh').textContent=[it.h,it.o].filter(Boolean).join(' · ')}tick()};
function tick(){var c=document.getElementById('pc');if(!END){c.classList.add('hide');return}c.classList.remove('hide');var r=Math.max(0,Math.round((END-Date.now())/1000));c.textContent=String(Math.floor(r/60)).padStart(2,'0')+':'+String(r%60).padStart(2,'0')}
setInterval(tick,250);''')

# =========================================================== FINAL
P['ABAS_Final'] = page('Abastible · Final', r'''
.c{position:absolute;left:0;right:0;top:250px;text-align:center}
.lg{width:820px;animation:up .9s ease both}
.t{font-size:112px;font-weight:800;letter-spacing:-2px;line-height:1;margin-top:60px;animation:up .9s .15s ease both}
.t em{font-style:normal;color:inherit}
.s{font-family:"Titillium Web";font-size:40px;font-weight:600;color:rgba(255,255,255,.9);margin-top:18px;animation:up .9s .25s ease both}
''', '<div class="stage">' + BGC
 + '<div class="c"><img class="lg" src="' + LOGO_M + '"><div class="t" id="ft">GRACIAS POR ACOMPAÑARNOS</div><div class="s" id="fs" data-ev="nombre">NOMBRE DEL EVENTO</div></div>'
 + BAR + '</div>', r'''
window.onLive=function(d){var f=d.fin||{};var t=document.getElementById('ft');var tt=f.titulo||'GRACIAS POR ACOMPAÑARNOS';var w=tt.split(' ');
 t.textContent=tt;if(f.sub)document.getElementById('fs').textContent=f.sub};''')

# =========================================================== ORADOR ("A continuación")
P['ABAS_Orador'] = page('Abastible · Orador', r'''
.av{position:absolute;left:150px;top:300px;width:560px;height:438px;animation:pop .9s cubic-bezier(.16,1,.3,1) both}
.av svg{width:100%;height:100%;overflow:visible;filter:drop-shadow(0 30px 60px rgba(0,0,0,.4))}
.av path{fill:var(--az)}
.av .ini{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:190px;font-weight:800;letter-spacing:-6px;color:#fff;padding-bottom:20px}
.av img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;-webkit-mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 78.2'><path d='__BLOB__'/></svg>") center/100% 100% no-repeat}
.info{position:absolute;left:790px;top:290px;width:1000px}
.nm{font-size:110px;font-weight:800;line-height:1;letter-spacing:-2px;margin-top:30px;max-height:226px;overflow:hidden;animation:left .8s .1s ease both}
.cg{font-family:"Titillium Web";font-size:40px;font-weight:600;color:var(--az);margin-top:16px;animation:left .8s .2s ease both}
.tema{margin-top:46px;background:#fff;color:var(--az2);border-radius:36px;padding:30px 40px;box-shadow:0 24px 70px rgba(0,0,0,.35);animation:up .8s .35s ease both}
.tema small{display:block;font-family:"Titillium Web";font-size:24px;font-weight:700;letter-spacing:2px;color:var(--or)}
.tema b{display:block;font-size:48px;font-weight:700;line-height:1.12;margin-top:6px;max-height:120px;overflow:hidden}
.tema span{display:block;font-size:24px;color:var(--gr);margin-top:10px}
''', '<div class="stage">' + BGC + '<img class="logo" src="' + LOGO_M + '">'
 + '<div class="av"><svg viewBox="0 0 100 78.2"><path d="' + BLOB + '"/></svg><img id="oph" class="hide" alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><div class="ini" id="oi">NA</div></div>'
 + '<div class="info"><div class="pill"><i></i><span id="ok">A CONTINUACIÓN</span></div>'
 + '<div class="nm" id="on" data-fit="h" data-max="110" data-min="60">NOMBRE APELLIDO</div><div class="cg" id="oc">Cargo · Empresa</div>'
 + '<div class="tema" id="otb"><small>CHARLA</small><b id="ot" data-fit="h" data-max="48" data-min="30">Título de la charla</b><span id="oh"></span></div></div>'
 + BAR + '</div>', r'''
function ini(n){var w=(n||'').trim().split(/\s+/).filter(Boolean);return ((w[0]||'')[0]||'')+((w.length>1?w[w.length-1]:'')[0]||'')}
window.onLive=function(d){var o=d.ora||{};document.getElementById('ok').textContent=o.kicker||'A CONTINUACIÓN';
 document.getElementById('on').textContent=o.o||'NOMBRE APELLIDO';document.getElementById('oi').textContent=ini(o.o).toUpperCase()||'·';
 document.getElementById('oc').textContent=[o.c,o.e].filter(Boolean).join(' · ');
 document.getElementById('ot').textContent=o.t||'';document.getElementById('otb').classList.toggle('hide',!o.t);document.getElementById('oh').textContent=o.h?('HORA '+o.h):'';
 var ph=document.getElementById('oph');if(o.foto){ph.src=o.foto;ph.classList.remove('hide');document.getElementById('oi').classList.add('hide')}else{ph.classList.add('hide');document.getElementById('oi').classList.remove('hide')}};''').replace('__BLOB__', BLOB)

# =========================================================== AGENDA
P['ABAS_Agenda'] = page('Abastible · Agenda', r'''
.hd{position:absolute;left:80px;top:200px;display:flex;align-items:flex-end;gap:30px}
.hd b{font-size:96px;font-weight:800;letter-spacing:-2px;line-height:.9}
.hd span{font-family:"Titillium Web";font-size:34px;font-weight:600;color:var(--az);padding-bottom:8px}
.list{position:absolute;left:80px;right:80px;top:322px;display:flex;flex-direction:column;gap:12px}
.it{display:flex;align-items:center;gap:30px;height:72px;padding:0 34px 0 14px;border-radius:999px;background:rgba(255,255,255,.14);animation:left .6s ease both}
.it .h{flex:none;width:150px;height:52px;border-radius:999px;background:rgba(0,20,137,.35);display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:700;font-variant-numeric:tabular-nums}
.it .t{flex:1;font-size:34px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.it .o{font-family:"Titillium Web";font-size:26px;color:rgba(255,255,255,.9);white-space:nowrap;max-width:620px;overflow:hidden;text-overflow:ellipsis}
.it.past{opacity:.55}
.it.cur{background:#fff;color:var(--az2);box-shadow:0 18px 50px rgba(0,0,0,.35);height:86px}
.it.cur .h{background:var(--az);color:#fff}
.it.cur .o{color:var(--gr)}
.it.cur .t::after{content:"AHORA";margin-left:18px;font-size:22px;letter-spacing:1px;color:var(--or);vertical-align:3px}
''', '<div class="stage">' + BGC + '<img class="logo" src="' + LOGO_M + '">'
 + '<div class="hd"><b>PROGRAMA</b><span data-ev="nombre">NOMBRE DEL EVENTO</span></div><div class="list" id="al"></div>' + BAR + '</div>', r'''
var MAXR=7;
window.onLive=function(d){var a=d.ag||{},L=a.items||[],c=a.cur||0;var s=Math.max(0,Math.min(c-2,L.length-MAXR));
 var h=L.slice(s,s+MAXR).map(function(it,j){var i=s+j;return '<div class="it'+(i<c?' past':i===c?' cur':'')+'" style="animation-delay:'+(j*.06)+'s"><div class="h">'+esc(it.h||'')+'</div><div class="t">'+esc(it.t||'')+'</div><div class="o">'+esc([it.o,it.c].filter(Boolean).join(' · '))+'</div></div>'}).join('');
 var el=document.getElementById('al');if(el.dataset.k!==h){el.dataset.k=h;el.innerHTML=h}};''')

# =========================================================== LOWER THIRD (overlay)
P['ABAS_Overlay_LowerThird'] = page('Abastible · Lower third', r'''
#lt{position:absolute;left:96px;bottom:100px;display:flex;align-items:center;visibility:hidden;transition:bottom .4s}
#lt.up{bottom:200px}
#lt.in,#lt.out{visibility:visible}
.mk{position:relative;z-index:2;width:184px;height:144px;margin-right:-96px;filter:drop-shadow(0 12px 26px rgba(0,0,0,.35))}
.mk::before{content:"";position:absolute;inset:-12px -14px;background:#fff;border-radius:58% 50% 52% 46%/62% 58% 44% 40%;transform:rotate(-10deg);box-shadow:0 10px 24px rgba(0,0,0,.25)}
.mk img{position:relative;width:100%;height:100%;object-fit:contain}
.card{position:relative;background:linear-gradient(100deg,#FE5000,#F44C00 60%,#E04600);border-radius:999px;padding:22px 80px 22px 130px;min-width:640px;box-shadow:0 18px 50px rgba(0,0,0,.28);overflow:hidden}
.card::after{content:"";position:absolute;top:0;bottom:0;width:120px;left:-160px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.22),transparent);transform:skewX(-18deg)}
.nm{font-size:56px;font-weight:800;color:#fff;line-height:1.05;letter-spacing:-1px;white-space:nowrap}
.cg{font-family:"Titillium Web";font-size:30px;font-weight:600;color:rgba(255,255,255,.92);margin-top:2px;white-space:nowrap}
.cg b{color:var(--az);font-weight:700}
.ln{position:absolute;left:130px;bottom:14px;height:6px;width:120px;border-radius:6px;background:var(--az);transform-origin:left}
.isoW{display:none}
#lt.in .mk{animation:pop .7s cubic-bezier(.16,1,.3,1) both}
#lt.in .card{animation:wipe .7s .15s cubic-bezier(.7,0,.2,1) both}
#lt.in .card::after{animation:shine 4.5s 1.2s ease-in-out infinite}
#lt.in .nm{animation:left .6s .4s ease both}
#lt.in .cg{animation:left .6s .52s ease both}
#lt.in .ln{animation:grow .6s .65s ease both}
@keyframes wipe{from{clip-path:inset(0 100% 0 0 round 999px)}to{clip-path:inset(0 0 0 0 round 999px)}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes shine{0%{left:-160px}30%,100%{left:110%}}
#lt.out .nm,#lt.out .cg,#lt.out .ln{animation:fadeo .25s ease both}
#lt.out .card{animation:wipeo .45s .15s cubic-bezier(.7,0,.3,1) both}
#lt.out .mk{animation:popo .35s .45s ease both}
@keyframes fadeo{to{opacity:0;transform:translateY(-14px)}}
@keyframes wipeo{from{clip-path:inset(0 0 0 0 round 999px)}to{clip-path:inset(0 100% 0 0 round 999px)}}
@keyframes popo{to{transform:scale(0) rotate(-25deg);opacity:0}}
''', '<div id="lt"><div class="mk"><img src="' + ISO + '"></div>'
 + '<div class="card"><div class="nm" id="nm" data-max="56" data-min="34" data-fit="w">Nombre Apellido</div><div class="cg" id="cg">Cargo · <b>Empresa</b></div><div class="ln"></div></div></div>', r'''
var V=false,K='';
function render(l){document.getElementById('nm').textContent=l.nombre||'Nombre Apellido';
 var c=esc(l.cargo||''),e=esc(l.empresa||'');document.getElementById('cg').innerHTML=c&&e?c+' · <b>'+e+'</b>':(c||'<b>'+e+'</b>');
 var w=Math.max(document.getElementById('nm').scrollWidth,document.getElementById('cg').scrollWidth);document.querySelector('.card').style.width=Math.min(1500,Math.max(640,w+215))+'px';fitAll()}
function play(c){var el=document.getElementById('lt');el.classList.remove('in','out');void el.offsetWidth;if(c)el.classList.add(c)}
window.onLive=function(d){var show=!!(d.show&&d.show.lt),l=d.lt||{},k=JSON.stringify(l);
 document.getElementById('lt').classList.toggle('up',!!(d.show&&d.show.msg));
 if(show&&(!V||k!==K)){var go=function(){K=k;render(l);play('in')};if(V){play('out');setTimeout(go,850)}else go();V=true}
 else if(!show&&V){V=false;play('out')}};
if(Q.get('demo'))setTimeout(function(){window.onLive({show:{lt:true},lt:{nombre:'Nombre Apellido',cargo:'Gerente General',empresa:'Abastible'}})},300);''', full=False)

# =========================================================== MOSCA (overlay)
P['ABAS_Overlay_Mosca'] = page('Abastible · Mosca', r'''
.mo{position:absolute;right:60px;top:52px;display:flex;flex-direction:column;align-items:flex-end;gap:10px;transform-origin:right top;transition:opacity .4s,transform .35s,top .35s,bottom .35s}
.mo.bl,.mo.tl{right:auto;left:60px;align-items:flex-start;transform-origin:left top}
.mo.br,.mo.bl{top:auto;bottom:52px;flex-direction:column-reverse;transform-origin:right bottom}
.mo.bl{transform-origin:left bottom}
.mo img{width:300px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.55))}
.mo .row{display:flex;gap:10px;align-items:center}
.live{display:flex;align-items:center;gap:10px;background:var(--az);color:#fff;border-radius:999px;padding:6px 18px 6px 14px;font-weight:700;font-size:22px;letter-spacing:1.5px;box-shadow:0 6px 18px rgba(0,0,0,.3)}
.live i{width:11px;height:11px;border-radius:50%;background:#fff;animation:pulse 2s ease-in-out infinite}
.msg{background:#BF3E00;color:#fff;border-radius:999px;padding:6px 20px;font-family:"Titillium Web";font-weight:600;font-size:22px;max-width:560px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:opacity .5s;box-shadow:0 6px 18px rgba(0,0,0,.3)}
.msg.off{opacity:0}
''', '<div class="mo" id="mo"><img src="' + LOGO_W + '"><div class="row"><div class="msg" id="msg">abastible.cl</div><div class="live" id="live"><i></i><span id="est">EN VIVO</span></div></div></div>', r'''
var MS=[],mi=0,C={pos:'tr',scale:1,op:1,live:true,msgs:true},SH=true;
function apply(){var m=document.getElementById('mo');m.className='mo '+(C.pos||'tr');m.style.transform='scale('+(+C.scale||1)+')';m.style.opacity=SH?(C.op==null?1:C.op):0;
 if(/^b/.test(C.pos)&&C.avoid)m.style.bottom=C.avoid+'px';else m.style.bottom='';
 document.getElementById('live').classList.toggle('hide',!C.live);document.getElementById('msg').classList.toggle('hide',!C.msgs||!MS.length);document.getElementById('est').textContent=C.estado||'EN VIVO'}
window.onLive=function(d){if(d.mosca){C=d.mosca;MS=C.list||[]}SH=!(d.show&&d.show.mosca===false);if(mi>=MS.length)mi=0;document.getElementById('msg').textContent=MS[mi]||'';apply()};
setInterval(function(){if(MS.length<2)return;var el=document.getElementById('msg');el.classList.add('off');setTimeout(function(){mi=(mi+1)%MS.length;el.textContent=MS[mi];el.classList.remove('off')},550)},6000);apply();''', full=False)

# =========================================================== TEMA ACTUAL (overlay arriba a la izquierda)
P['ABAS_Overlay_Tema'] = page('Abastible · Tema', r'''
#tm{position:absolute;left:60px;top:56px;display:flex;align-items:stretch;max-width:1180px;visibility:hidden}
#tm.in,#tm.out{visibility:visible}
.k{background:var(--az);color:#fff;font-weight:700;font-size:22px;letter-spacing:1.5px;padding:0 22px 0 18px;border-radius:999px 0 0 999px;display:flex;align-items:center;gap:10px}
.k i{width:10px;height:10px;border-radius:50%;background:#fff}
.t{background:var(--or);color:#fff;font-size:30px;font-weight:700;padding:12px 30px 12px 22px;border-radius:0 999px 999px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.t span{font-family:"Titillium Web";font-weight:600;color:rgba(255,255,255,.88);font-size:24px;margin-left:12px}
#tm.in .k{animation:pop .5s cubic-bezier(.16,1,.3,1) both}
#tm.in .t{animation:wipe .6s .12s cubic-bezier(.7,0,.2,1) both}
#tm.out{animation:fo .4s ease both}
@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes fo{to{opacity:0;transform:translateY(-20px)}}
''', '<div id="tm"><div class="k"><i></i><span id="tk">AHORA</span></div><div class="t" id="tt">Título de la charla</div></div>', r'''
var V=false,K='';
window.onLive=function(d){var s=!!(d.show&&d.show.tema),t=d.tema||{},k=JSON.stringify(t),el=document.getElementById('tm');
 var go=function(){K=k;document.getElementById('tk').textContent=t.kicker||'AHORA';document.getElementById('tt').innerHTML=esc(t.titulo||'')+(t.sub?'<span>'+esc(t.sub)+'</span>':'');el.classList.remove('in','out');void el.offsetWidth;el.classList.add('in')};
 if(s&&(!V||k!==K)){if(V){el.classList.remove('in');el.classList.add('out');setTimeout(go,420)}else go();V=true}
 else if(!s&&V){V=false;el.classList.remove('in');el.classList.add('out')}};''', full=False)

# =========================================================== MENSAJE / ZÓCALO (overlay abajo)
P['ABAS_Overlay_Mensaje'] = page('Abastible · Mensaje', r'''
#zc{position:absolute;left:0;right:0;bottom:0;height:86px;display:flex;align-items:stretch;transform:translateY(110%);transition:transform .6s cubic-bezier(.7,0,.2,1)}
#zc.on{transform:none}
.lb{flex:none;background:var(--az);color:#fff;font-weight:800;font-size:28px;letter-spacing:1.5px;display:flex;align-items:center;gap:16px;padding:0 40px 0 50px;border-radius:0 999px 999px 0;z-index:2;box-shadow:8px 0 24px rgba(0,0,0,.25)}
.lb img{height:46px}
.tx{flex:1;background:linear-gradient(90deg,#E04600,#F44C00 40%,#FE5000);margin-left:-40px;padding-left:70px;display:flex;align-items:center;overflow:hidden;position:relative}
.tx span{font-family:"Titillium Web";font-weight:600;font-size:34px;white-space:nowrap;color:#fff}
.tx.mv span{animation:tick var(--d,20s) linear infinite;padding-left:100%}
@keyframes tick{from{transform:translateX(0)}to{transform:translateX(-100%)}}
.tx span.chg{animation:none;opacity:0}
''', '<div id="zc"><div class="lb"><img src="' + small('logo_mono.png', 300) + '"><span id="zl">INFORMACIÓN</span></div><div class="tx" id="ztx"><span id="zt">Mensaje</span></div></div>', r'''
var K='',IT=[],ii=0,TT=null;
function showItem(){var sp=document.getElementById('zt'),box=document.getElementById('ztx');sp.textContent=IT[ii]||'';box.classList.remove('mv');sp.style.paddingLeft='';
 requestAnimationFrame(function(){if(sp.scrollWidth>box.clientWidth-80){box.style.setProperty('--d',Math.max(10,sp.scrollWidth/140)+'s');box.classList.add('mv')}})}
window.onLive=function(d){var on=!!(d.show&&d.show.msg),m=d.msg||{};document.getElementById('zc').classList.toggle('on',on);
 var k=JSON.stringify(m);if(k===K)return;K=k;document.getElementById('zl').textContent=m.label||'INFORMACIÓN';IT=(m.items||[]).filter(Boolean);ii=0;showItem();
 clearInterval(TT);if(IT.length>1)TT=setInterval(function(){ii=(ii+1)%IT.length;showItem()},(+m.every||10)*1000)};''', full=False)

# =========================================================== REPETICIÓN (overlay)
P['ABAS_Overlay_Replay'] = page('Abastible · Repetición', r'''
.rp{position:absolute;left:60px;top:52px;display:flex;align-items:center;gap:16px;background:var(--or);border-radius:999px;padding:10px 32px 10px 12px;box-shadow:0 10px 30px rgba(0,0,0,.35);animation:pop .6s cubic-bezier(.16,1,.3,1) both}
.rp .ic{width:58px;height:58px;border-radius:50%;background:var(--az);display:flex;align-items:center;justify-content:center}
.rp .ic svg{width:34px;height:34px;fill:#fff}
.rp b{font-size:34px;font-weight:800;letter-spacing:2px}
.rec{position:absolute;left:0;right:0;top:0;bottom:0;border:10px solid rgba(var(--or-rgb),.55);border-radius:0;pointer-events:none}
''', '<div class="rec"></div><div class="rp"><div class="ic"><svg viewBox="0 0 24 24"><path d="M11 6v12L2 12zM21 6v12l-9-6z"/></svg></div><b id="rt">REPETICIÓN</b></div>', r'''
window.onLive=function(d){if(d.replay&&d.replay.texto)document.getElementById('rt').textContent=d.replay.texto};''', full=False)


# =========================================================== PICTURE IN PICTURE (marcos con ventanas transparentes)
import sys; sys.path.insert(0, '/home/claude')
import pipgen
PIPCSS = r"""
body{background:transparent!important}
.pbg{position:absolute;inset:0;overflow:hidden;background:radial-gradient(1100px 760px at 72% 26%,rgba(255,96,24,.45),transparent 70%),radial-gradient(900px 600px at 8% 95%,rgba(200,54,0,.7),transparent 70%),linear-gradient(155deg,#FE5000 0%,#F44C00 45%,#E04600 100%)}
.win{position:absolute;border-radius:28px;box-shadow:0 0 0 6px #fff,0 24px 60px rgba(0,0,0,.35)}
.plogo{position:absolute;top:56px;right:70px;width:300px}
.ptitle{position:absolute;left:60px;top:64px;max-width:1300px;font-size:64px;font-weight:800;letter-spacing:-1px;line-height:1.05;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lab{position:absolute;display:inline-flex;align-items:baseline;gap:14px;background:#fff;color:var(--az2);border-radius:999px;padding:10px 28px 12px;box-shadow:0 12px 30px rgba(0,0,0,.25);white-space:nowrap;overflow:hidden}
.lab b{font-size:30px;font-weight:800;overflow:hidden;text-overflow:ellipsis}
.lab span{font-family:"Titillium Web";font-size:23px;font-weight:600;color:var(--gr)}
.lab.in{background:var(--az);color:#fff}.lab.in span{color:#C9D2F2}
"""
for k, L in pipgen.LAYOUTS.items():
    P['ABAS_PIP_' + k] = page('Abastible · PiP ' + L['nombre'], PIPCSS, pipgen.body(k, BGC, LOGO_M), pipgen.js(k, 28))

os.makedirs('out', exist_ok=True)
for k, v in P.items():
    open('out/%s.html' % k, 'w').write(v)
print(list(P))
