#!/usr/bin/env python3
"""Adapta el PANEL_MIDI probado del kit FCC2 al evento Abastible (canal propio, acciones y marca)."""
import re
s = open('/home/claude/fcc/midi_template.html').read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
R('<title>FCC 2 · Panel MIDI</title>', '<title>Abastible · Panel MIDI</title>')
R(':root{--red:#e3121b;--red2:#ff2a2a;--ink:#f1f1f1;--mute:#9a9a9a;--line:rgba(255,255,255,.12);--card:#121212;--bg:#080808;--ok:#2ecc71;--warn:#f5b301;--blue:#2f6bff}',
  ':root{--red:#FE5000;--red2:#FF7A33;--ink:#F3F5FB;--mute:#9AA3C7;--line:rgba(255,255,255,.12);--card:#0B1442;--bg:#050A2C;--ok:#22C55E;--warn:#F5B301;--blue:#2f6bff}')
# tipografía de la marca
s = s.replace('font-family:"Bebas";', 'font-family:"Ubuntu Sans";font-weight:700;').replace('font-family:"Oswald"', 'font-family:"Ubuntu Sans"')
s = s.replace('<img src="__LOGO__" alt="FCC">', '<img src="__LOGO__" alt="Abastible">')
R('<h1>PANEL MIDI <em>FCC 2</em></h1>', '<h1>PANEL MIDI <em>ABASTIBLE</em></h1>')
s = s.replace("fcc2-midi", "abas-midi").replace("'fcc2-cmd'", "'abas-cmd'")
# acciones del evento
i = s.index('var GROUPS=['); j = s.index('var KIND=', i)
s = s[:i] + """var GROUPS=[
 ['PROGRAMA',[['prev','◀ Bloque anterior'],['next','Bloque siguiente ▶'],['pausa_go','⏱ Iniciar cuenta de pausa']]],
 ['GRÁFICOS',[['lt_cur','👤 Lower third del orador actual'],['tgl_lt','Mostrar/ocultar lower third'],['tgl_tema','Mostrar/ocultar tema'],['tgl_msg','Mostrar/ocultar mensaje inferior'],['tgl_mosca','Mostrar/ocultar mosca']]],
 ['REPETICIONES',[['replay','⏪ Repetir ahora'],['replay5','⏪ Repetir 5 s'],['replay10','⏪ Repetir 10 s'],['replay15','⏪ Repetir 15 s'],['replayslow','🐢 Repetir lenta'],['moment','★ Guardar momento'],['reel','▶ Resumen del bloque'],['reelall','▶ Resumen de todo'],['stop','■ Detener repetición']]],
 ['CONTROL DE LA REPETICIÓN EN PANTALLA',[['rb_pause','❚❚ Pausar / seguir'],['rb_rew','◀◀ Rebobinar (toca otra vez para seguir)'],['rb_backplay','⏪▶ Atrás 3 s y reproducir'],['rb_back2','◀◀ Retroceder 2 s'],['rb_back5','⏪ Retroceder 5 s'],['rb_fwd2','▶▶ Adelantar 2 s'],['rb_restart','↺ Repetir clip de nuevo'],['rb_slow','🐢 Cámara lenta (activar/quitar)'],['rb_speed','⚡ Cambiar velocidad'],['rb_scrub','🎚 Perilla o fader: mover el video']]],
 ['CAMBIO DE ESCENA',[['trans','⇄ Transición (modo estudio)'],['toprev','Alternar "a vista previa"']]],
 ['TRANSICIONES HTML (vista previa al aire con la animación)',[['hst_go','🎬 Con la animación elegida'],['hst_ola','🌊 Ola'],['hst_burbuja','🫧 Burbuja'],['hst_capsulas','💊 Cápsulas'],['hst_llama','🔥 Llama'],['hst_anillos','◎ Anillos'],['hst_mosaico','▦ Mosaico']]]];
""" + s[j:]
i = s.index('var KIND='); j = s.index('\n', i)
s = s[:i] + "var KIND={trans:'CAMBIO',toprev:'CAMBIO',prev:'PROGRAMA',next:'PROGRAMA',pausa_go:'PAUSA',lt_cur:'LOWER THIRD',tgl_lt:'GRÁFICO',tgl_tema:'GRÁFICO',tgl_msg:'GRÁFICO',tgl_mosca:'GRÁFICO',replay:'REPETICIÓN',replay5:'REPETICIÓN',replay10:'REPETICIÓN',replay15:'REPETICIÓN',replayslow:'REPETICIÓN',moment:'REPETICIÓN',reel:'REPETICIÓN',reelall:'REPETICIÓN',stop:'REPETICIÓN',rb_pause:'CONTROL REPLAY',rb_rew:'CONTROL REPLAY',rb_backplay:'CONTROL REPLAY',rb_back2:'CONTROL REPLAY',rb_back5:'CONTROL REPLAY',rb_fwd2:'CONTROL REPLAY',rb_restart:'CONTROL REPLAY',rb_slow:'CONTROL REPLAY',rb_speed:'CONTROL REPLAY',rb_scrub:'PERILLA',hst_go:'TRANSICIÓN HTML',hst_ola:'TRANSICIÓN HTML',hst_burbuja:'TRANSICIÓN HTML',hst_capsulas:'TRANSICIÓN HTML',hst_llama:'TRANSICIÓN HTML',hst_anillos:'TRANSICIÓN HTML',hst_mosaico:'TRANSICIÓN HTML'};" + s[j:]
i = s.index('var SHORT='); j = s.index('\n', i)
s = s[:i] + "var SHORT={prev:'◀ BLOQUE',next:'BLOQUE ▶',pausa_go:'⏱ PAUSA',lt_cur:'👤 ORADOR',tgl_lt:'LOWER 3RD',tgl_tema:'TEMA',tgl_msg:'MENSAJE',tgl_mosca:'MOSCA',replay:'REPETIR',replay5:'REPETIR 5 S',replay10:'REPETIR 10 S',replay15:'REPETIR 15 S',replayslow:'REPETIR LENTA',moment:'★ MOMENTO',reel:'RESUMEN',reelall:'RESUMEN TODO',stop:'■ STOP',rb_rew:'◀◀ REBOBINAR',rb_backplay:'⏪▶ ATRÁS+PLAY',rb_pause:'❚❚ PAUSA',rb_back2:'◀◀ −2 S',rb_back5:'⏪ −5 S',rb_fwd2:'+2 S ▶▶',rb_restart:'↺ DE NUEVO',rb_slow:'🐢 LENTA',rb_speed:'⚡ VELOCIDAD',rb_scrub:'🎚 MOVER VIDEO',trans:'TRANSICIÓN',toprev:'A PREVIA',hst_go:'🎬 HTML',hst_ola:'🎬 OLA',hst_burbuja:'🎬 BURBUJA',hst_capsulas:'🎬 CÁPSULAS',hst_llama:'🎬 LLAMA',hst_anillos:'🎬 ANILLOS',hst_mosaico:'🎬 MOSAICO'};" + s[j:]
R("function trNm(n){return n.replace(/^FCC2\\s*/i,'')}", "function trNm(n){return n.replace(/^ABAS\\s*/i,'')}")
# colores de estado
i = s.index(" switch(a){case 'clock'"); j = s.index("  case 'trans':return['yellow',false];default:return['blue',false]}}", i)
s = s[:i] + """ switch(a){
  case 'replay':case 'replay5':case 'replay10':case 'replay15':case 'replayslow':return s.saving?['yellow',true]:s.playing?['red',true]:s.rb?['red',false]:['dim',false];
  case 'moment':return s.saving?['yellow',true]:s.rb?['blue',false]:['dim',false];
  case 'stop':return s.playing?['red',true]:['dim',false];
  case 'reel':case 'reelall':return s.playing?['red',false]:['blue',false];
  case 'tgl_lt':case 'lt_cur':return s.show&&s.show.lt?['green',false]:['yellow',false];
  case 'tgl_tema':return s.show&&s.show.tema?['green',false]:['dim',false];
  case 'tgl_msg':return s.show&&s.show.msg?['green',false]:['dim',false];
  case 'tgl_mosca':return s.show&&s.show.mosca?['green',false]:['dim',false];
  case 'pausa_go':return s.pausa?['green',true]:['blue',false];
  case 'prev':return s.block>1?['blue',false]:['dim',false];case 'next':return s.block<s.nb?['yellow',false]:['dim',false];
  case 'toprev':return s.toprev?['green',false]:['dim',false];
  case 'rb_pause':return !s.playing?['dim',false]:s.rbpause?['yellow',true]:['green',false];
  case 'rb_rew':return !s.playing?['dim',false]:s.rbrew?['yellow',true]:['blue',false];
  case 'rb_backplay':case 'rb_back2':case 'rb_back5':case 'rb_fwd2':case 'rb_restart':case 'rb_scrub':return s.playing?['blue',false]:['dim',false];
  case 'rb_slow':return !s.playing?['dim',false]:(s.rbspd<100?['red',false]:['blue',false]);
  case 'rb_speed':return s.playing?['blue',false]:['dim',false];
  case 'hst_go':return s.hstuse?['green',false]:['yellow',false];
  case 'hst_ola':case 'hst_burbuja':case 'hst_capsulas':case 'hst_llama':case 'hst_anillos':case 'hst_mosaico':return a.slice(4)===s.hst?['green',false]:['yellow',false];
""" + s[j:]
R("var TRD=['FCC2 Golpe','FCC2 Golpe Corta','FCC2 Rapida','FCC2 Rapida Corta','FCC2 Replay','Corte','Desvanecer']", "var TRD=['ABAS Ola','ABAS Ola Corta','ABAS Burbuja','ABAS Burbuja Corta','ABAS Capsulas','ABAS Llama','ABAS Anillos','ABAS Mosaico','Corte','Desvanecer']")
SC = "['INICIO','ESTUDIO','ORADOR','AGENDA','PAUSA','REPLAY','FINAL']"
s = s.replace("['INICIO','ESTUDIO','VS','GANADOR','REPLAY','PAUSA','AUSPICIADOR','FINAL']", SC)
i = s.index(" var rows=[sc.map(function(n){return 'scene:'+n}),"); j = s.index(" MAPS.forEach(function(x){if(x.m)sendLed(x.m,'off',false)});MAPS=[];", i)
s = s[:i] + """ var rows=[sc.map(function(n){return 'scenev:'+n}),
  ['trans','toprev','prev','next','lt_cur','tgl_tema','tgl_msg','tgl_mosca'],
  ['replay','moment','reel','stop','reelall','pausa_go','hst_go','hst_mosaico'],
  ['rb_pause','rb_rew','rb_backplay','rb_back5','rb_fwd2','rb_restart','rb_slow','rb_speed']];
""" + s[j:]
R(" return sc.concat(['trans','replay','replay5','moment','reel','stop','clock','reset','rminus','rplus','next','prev','tgl_marcador','tgl_lt','tgl_mosca','win_r','win_b'])}",
  " return sc.concat(['trans','next','prev','lt_cur','tgl_tema','tgl_msg','tgl_mosca','replay','moment','reel','stop','rb_pause','rb_rew','rb_slow'])}")
# textos de ayuda que nombran FCC
s = s.replace('FCC2_Kit', 'kit de Abastible').replace('FCC 2', 'Abastible')
left = [m for m in re.findall(r'.{30}(?:fcc|FCC|combate|COMBATE|peleador|marcador).{30}', s)]
print('referencias restantes:', len(left)); [print('  ', x) for x in left[:12]]

# --- pulido Impeccable: contraste sobre naranjo, estados sin brillo difuso, etiquetas pequeñas sin tracking amplio ---
import re as _re
s = s.replace('.chip.ok i{background:var(--ok);box-shadow:0 0 8px var(--ok)}', '.chip.ok i{background:var(--ok);box-shadow:0 0 0 3px rgba(46,204,113,.28)}')
s = _re.sub(r'box-shadow:0 0 1[46]px rgba\([^)]*\)', 'box-shadow:inset 0 0 0 2px rgba(255,255,255,.35)', s)
s = s.replace('.led.c-red{background:#ff2a2a;box-shadow:0 0 8px #ff2a2a}', '.led.c-red{background:#ff2a2a;box-shadow:0 0 0 2px rgba(255,42,42,.3)}')
s = s.replace('.led.c-green{background:#2ecc71;box-shadow:0 0 8px #2ecc71}', '.led.c-green{background:#2ecc71;box-shadow:0 0 0 2px rgba(46,204,113,.3)}')
s = s.replace('button.pri{background:var(--red);border-color:var(--red)}', 'button.pri{background:var(--red);border-color:var(--red);color:var(--bg)}')
s = s.replace('.ab.sel{background:var(--red);border-color:#fff}', '.ab.sel{background:var(--red);border-color:#fff;color:var(--bg)}')
for a in ['label{font-size:12px;letter-spacing:2px', 'th{font-size:12px;letter-spacing:2px', '.bt .tile small{font-size:11px;letter-spacing:2px', '.grp{margin:10px 0 4px;font-size:12px;letter-spacing:2px']:
    s = s.replace(a, a.replace('letter-spacing:2px', 'letter-spacing:.5px'))
s = s.replace('font-size:26px;letter-spacing:3px;display:flex;align-items:center;gap:10px}', 'font-size:26px;letter-spacing:1px;display:flex;align-items:center;gap:10px}').replace('font-size:24px;letter-spacing:3px;padding:12px 16px;', 'font-size:24px;letter-spacing:1px;padding:12px 16px;')
s = _re.sub(r'(\.toast\{[^}]*background:var\(--red\);)', r'\1color:var(--bg);', s, count=1)
s = _re.sub(r'(\.ps>i\{[^}]*background:var\(--red\);)', r'\1color:var(--bg);', s, count=1)
open('midi_template.html', 'w').write(s)
