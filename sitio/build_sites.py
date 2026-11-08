#!/usr/bin/env python3
"""Arma los sitios de GitHub Pages de los tres kits OBS (Abastible, Espíritu Imperial, Titulación UCSH):
copia el kit al repo, agrega la portada index.html con vistas previas y 'Copiar URL para OBS', y deja el
control listo para instalar las fuentes como URL cuando se abre desde la web."""
import os, shutil, json, html, zipfile, re, sys
FONTS = '/home/claude/ucsh/src/node_modules/@fontsource/'

P = {
 'abastible': dict(repo='/home/claude/abastible-transmision-obs', kit='/home/claude/abastible-streaming', zipname='Abastible_Kit.zip', zipdir='Abastible_Kit',
   pre='ABAS', name='Abastible', title='Kit OBS · Abastible', lead='Gráficos en vivo, transiciones y control para la transmisión del evento Abastible.',
   material='MATERIAL_ABASTIBLE.html', assets='/home/claude/abastible/hm/assets', logo='/home/claude/abastible-streaming/Logos/Abastible_logo_white.png',
   fonts=[('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-400-normal.woff2', 400), ('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-700-normal.woff2', 700), ('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-800-normal.woff2', 800)],
   disp='"Ubuntu Sans"', body='"Ubuntu Sans"', dw=800, tr='-0.02em',
   c=dict(bg='#06103A', bg2='#0B1A55', card='#0E1F63', line='rgba(255,255,255,.14)', ink='#F4F6FC', mute='#AEB7DA', acc='#FE5000', accink='#06103A', acc2='#FF7A33', hero='linear-gradient(150deg,#FE5000 0%,#F44C00 45%,#E04600 100%)', heroink='#06103A', herobtn='#FFFFFF'),
   screens=[('Inicio', 'inicio', 'Inicio', 'Portada con cuenta regresiva.'), ('Orador', 'orador', 'Orador', 'Presentación de cada orador.'), ('Agenda', 'programa', 'Agenda', 'Programa del evento con el bloque actual.'), ('Pausa', 'pausa', 'Pausa', 'Volvemos en unos minutos.'), ('Final', 'final', 'Final', 'Cierre de la transmisión.')],
   overlays=[('Overlay_LowerThird', 'lt', 'Lower third', 'Nombre, cargo y empresa.'), ('Overlay_Tema', 'tema', 'Tema', 'El tema en pantalla, arriba a la izquierda.'), ('Overlay_Mensaje', 'mensaje', 'Mensaje inferior', 'Saludos y avisos.'), ('Overlay_Mosca', 'mosca', 'Mosca', 'Logo, EN VIVO y mensajes.'), ('Overlay_Replay', 'replay', 'Repetición', 'Marca para los replays.')],
   stingers=['Ola', 'Burbuja', 'Capsulas', 'Llama', 'Anillos', 'Mosaico'],
   scenes='INICIO, ESTUDIO, ORADOR, AGENDA, PAUSA, REPLAY, FINAL y las cinco PIP_', listword='la agenda y los oradores'),
 'imperial': dict(repo='/home/claude/espiritu-imperial-obs', kit='/home/claude/imperial/kit', zipname='Espiritu_Imperial_Kit.zip', zipdir='Espiritu_Imperial',
   pre='IMP', name='Espíritu Imperial', title='Kit OBS · Espíritu Imperial', lead='Gráficos en vivo, transiciones y control para la ceremonia que destaca al mejor trabajador de cada sucursal.',
   material='MATERIAL_IMPERIAL.html', assets='/home/claude/imperial/src/mat_assets', logo='/home/claude/imperial/Logo_Imperial_web.png',
   fonts=[('Roboto', 'roboto/files/roboto-latin-400-normal.woff2', 400), ('Roboto', 'roboto/files/roboto-latin-500-normal.woff2', 500), ('Roboto Condensed', 'roboto-condensed/files/roboto-condensed-latin-900-normal.woff2', 900)],
   disp='"Roboto Condensed"', body='"Roboto"', dw=900, tr='-0.01em',
   c=dict(bg='#03152B', bg2='#062447', card='#0A2F5E', line='rgba(255,255,255,.14)', ink='#F4F6FA', mute='#B9C3D2', acc='#C8102E', accink='#FFFFFF', acc2='#FF464B', hero='radial-gradient(1200px 600px at 70% -10%,rgba(255,255,255,.10),transparent 60%),linear-gradient(180deg,#063661,#03152B)', heroink='#FFFFFF', herobtn='#03152B'),
   screens=[('Inicio', 'inicio', 'Inicio', 'El sello del evento con cuenta regresiva.'), ('Sucursal', 'sucursal', 'Sucursal', 'Presenta la sucursal antes de su destacado.'), ('Destacado', 'destacado', 'Destacado', 'La revelación del trabajador destacado.'), ('Destacados', 'destacados', 'Destacados', 'Tablero de todas las sucursales.'), ('Pausa', 'pausa', 'Pausa', 'Volvemos en unos minutos.'), ('Final', 'final', 'Final', 'Cierre de la transmisión.')],
   overlays=[('Overlay_LowerThird', 'lt', 'Lower third', 'Nombre, cargo y sucursal.'), ('Overlay_Tema', 'tema', 'Sucursal en pantalla', 'La sucursal que se premia.'), ('Overlay_Mensaje', 'mensaje', 'Mensaje inferior', 'Saludos y avisos.'), ('Overlay_Mosca', 'mosca', 'Mosca', 'Logo, EN VIVO y mensajes.'), ('Overlay_Replay', 'replay', 'Repetición', 'Marca para los replays.')],
   stingers=['Telon', 'Destello', 'Franjas', 'Marco'],
   scenes='INICIO, ESTUDIO, SUCURSAL, DESTACADO, DESTACADOS, PAUSA, REPLAY, FINAL y las cinco PIP_', listword='las sucursales y sus destacados'),
 'ucsh': dict(repo='/home/claude/titulacion-ucsh-obs', kit='/home/claude/ucsh/kit', zipname='Titulacion_UCSH_Kit.zip', zipdir='Titulacion_UCSH',
   pre='UCSH', name='Titulación UCSH', title='Kit OBS · Titulación UCSH', lead='Gráficos en vivo, transiciones y control para la Ceremonia de Titulación de la Universidad Católica Silva Henríquez.',
   material='MATERIAL_UCSH.html', assets='/home/claude/ucsh/src/mat_assets', logo='/home/claude/ucsh/Logo_UCSH_blanco.png',
   fonts=[('Ubuntu', 'ubuntu/files/ubuntu-latin-400-normal.woff2', 400), ('Ubuntu', 'ubuntu/files/ubuntu-latin-500-normal.woff2', 500), ('Cormorant Garamond', 'cormorant-garamond/files/cormorant-garamond-latin-700-normal.woff2', 700)],
   disp='"Cormorant Garamond"', body='"Ubuntu"', dw=700, tr='0',
   c=dict(bg='#011C33', bg2='#012A4A', card='#023961', line='rgba(240,184,8,.22)', ink='#F4F7FB', mute='#B9CCE0', acc='#F0B808', accink='#011C33', acc2='#FFD24D', hero='radial-gradient(1200px 600px at 60% -10%,rgba(20,162,241,.28),transparent 64%),linear-gradient(180deg,#0A5A92,#004577 40%,#012A4A)', heroink='#FFFFFF', herobtn='#011C33'),
   screens=[('Inicio', 'inicio', 'Inicio', 'Ceremonia de Titulación con cuenta regresiva.'), ('Carrera', 'carrera', 'Carrera', 'Presenta cada carrera y cuántos se titulan.'), ('Nomina', 'nomina', 'Nómina', 'Los titulados de la carrera; el actual en oro.'), ('Pausa', 'pausa', 'Pausa', 'Volvemos en unos minutos y la carrera que viene.'), ('Final', 'final', 'Final', 'Cierre con felicitaciones.')],
   overlays=[('Overlay_LowerThird', 'lt', 'Lower third del titulado', 'Nombre, carrera y distinción.'), ('Overlay_Tema', 'tema', 'Carrera en pantalla', 'La carrera que se titula.'), ('Overlay_Mensaje', 'mensaje', 'Mensaje inferior', 'Felicitaciones y avisos.'), ('Overlay_Mosca', 'mosca', 'Mosca', 'Logo, EN VIVO y mensajes.'), ('Overlay_Replay', 'replay', 'Repetición', 'Marca para los replays.')],
   stingers=['Telon', 'Destello', 'Franjas', 'Marco'],
   scenes='INICIO, ESTUDIO, CARRERA, NOMINA, PAUSA, REPLAY, FINAL y las cinco PIP_', listword='la lista de titulados por carrera'),
}
PIPS = [('Presentacion', 'Presentación + cámara', '1340×754 y 420×236'), ('Dos', 'Dos cámaras', '885×498 cada una'), ('Tres', 'Tres cámaras', '580×326 cada una'), ('Vertical', 'Cámara + video vertical', '1150×647 y 460×818'), ('Esquina', 'Esquina', '420×236 sobre pantalla completa')]
STN = {'Telon': 'Telón', 'Capsulas': 'Cápsulas'}

# --- modo web: si CONTROL_EN_VIVO se abre desde https, las fuentes se crean como URL en vez de archivo local
WEB_JS = "function isWeb(){return /^https?:$/.test(location.protocol)}function webBase(){return location.href.replace(/[#?].*$/,'').replace(/[^\\/]*$/,'')}function SRC(f){return isWeb()?{is_local_file:false,url:webBase()+'Paneles/'+f.split('/').pop()}:{is_local_file:true,local_file:f}}\n"
def patch_control(path):
    s = open(path).read()
    if 'function isWeb()' in s: return
    a = 'function panelDir(){'
    assert s.count(a) == 1; s = s.replace(a, WEB_JS + a)
    for old, new in [("var set={is_local_file:true,local_file:file,", "var set=Object.assign(SRC(file),{"),
                     ("var set={is_local_file:true,local_file:panelDir()+", "var set=Object.assign(SRC(panelDir()+")]:
        n = s.count(old); assert n == 1, (old, n)
        i = s.index(old); j = s.index('};', i)
        body = s[i + len(old):j]
        if old.endswith('panelDir()+'):
            k = body.index(','); s = s[:i] + new + body[:k] + '),{' + body[k + 1:] + '});' + s[j + 2:]
        else:
            s = s[:i] + new + body + '});' + s[j + 2:]
    s = s.replace("if(!isRemote()&&norm.toLowerCase()", "if(!isRemote()&&!isWeb()&&norm.toLowerCase()")
    s = s.replace("var dir=isRemote()?'':", "var dir=(isRemote()||isWeb())?'':")
    s = s.replace("else L.push(li('ok','Carpeta del kit',", "else if(isWeb())L.push(li('ok','Gráficos desde la web',esc(webBase()+'Paneles/')));else L.push(li('ok','Carpeta del kit',")
    open(path, 'w').write(s)

def esc(t): return html.escape(t, quote=True)

def build(key):
    C = P[key]; R = C['repo']; c = C['c']; pre = C['pre']
    for f in os.listdir(R):
        if f != '.git': (shutil.rmtree if os.path.isdir(os.path.join(R, f)) else os.remove)(os.path.join(R, f))
    for f in os.listdir(C['kit']):
        src = os.path.join(C['kit'], f)
        (shutil.copytree(src, os.path.join(R, f)) if os.path.isdir(src) else shutil.copy(src, R))
    patch_control(os.path.join(R, 'CONTROL_EN_VIVO.html'))
    os.makedirs(R + '/sitio/img', exist_ok=True); os.makedirs(R + '/sitio/fonts', exist_ok=True); os.makedirs(R + '/descargas', exist_ok=True)
    keys = [x[1] for x in C['screens']] + [x[1] for x in C['overlays']] + ['pip_' + p[0] for p in PIPS] + ['control', 'midi', 'estudio']
    for k in keys: shutil.copy(os.path.join(C['assets'], k + '.jpg'), R + '/sitio/img/' + k + '.jpg')
    shutil.copy(C['logo'], R + '/sitio/img/logo.png')
    ff = ''
    for fam, p, w in C['fonts']:
        fn = os.path.basename(p); shutil.copy(FONTS + p, R + '/sitio/fonts/' + fn)
        ff += '@font-face{font-family:"%s";font-weight:%d;font-display:swap;src:url(sitio/fonts/%s) format("woff2")}\n' % (fam, w, fn)
    # zip del kit (versión para descargar y usar sin internet)
    zp = R + '/descargas/' + C['zipname']
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(C['kit']):
            for f in files:
                full = os.path.join(root, f); z.write(full, os.path.join(C['zipdir'], os.path.relpath(full, C['kit'])))
    mb = os.path.getsize(zp) / 1e6

    def card(file, img, name, desc, live=True):
        u = 'Paneles/%s_%s.html' % (pre, file)
        return ('<li class="card"><a class="shot" href="%s" target="_blank" rel="noopener"><img src="sitio/img/%s.jpg" alt="%s" loading="lazy" width="1280" height="720"></a>'
                '<div class="meta"><h3>%s</h3><p>%s</p><code>%s_%s.html</code><div class="acts"><button type="button" class="b b--acc" data-copy="%s">Copiar URL para OBS</button><a class="b" href="%s" target="_blank" rel="noopener">Abrir</a></div></div></li>') % (
            u, img, esc(name), esc(name), esc(desc), pre, file, u, u)
    screens = ''.join(card(*x) for x in C['screens'])
    overlays = ''.join(card(*x) for x in C['overlays'])
    pips = ''.join(card('PIP_' + k, 'pip_' + k, n, 'Ventanas: ' + w + '.') for k, n, w in PIPS)
    stg = ''
    for s in C['stingers']:
        v = 'Transiciones/%s_Transicion_%s.webm' % (pre, s); vc = 'Transiciones/%s_Transicion_%s_Corta.webm' % (pre, s); h = 'Paneles/%s_Stinger_%s.html' % (pre, s)
        stg += ('<li class="card"><div class="shot chk"><video src="%s" muted loop playsinline autoplay preload="metadata" aria-label="Transición %s"></video></div>'
                '<div class="meta"><h3>%s</h3><p>Video con transparencia y sonido, y versión HTML.</p><div class="acts"><a class="b b--acc" href="%s" download>Descargar 4 s</a><a class="b" href="%s" download>2 s</a><button type="button" class="b" data-copy="%s">URL HTML</button></div></div></li>') % (
            v, esc(STN.get(s, s)), esc(STN.get(s, s)), v, vc, h)
    page = TEMPLATE
    rep = {'__FF__': ff, '__TITLE__': esc(C['title']), '__NAME__': esc(C['name']), '__LEAD__': esc(C['lead']), '__ZIP__': 'descargas/' + C['zipname'], '__MB__': '%.0f MB' % mb,
           '__MAT__': C['material'], '__SCREENS__': screens, '__OVERLAYS__': overlays, '__PIPS__': pips, '__STG__': stg, '__PRE__': pre, '__SCENES__': C['scenes'], '__LIST__': esc(C['listword']),
           '__DISP__': C['disp'], '__BODY__': C['body'], '__DW__': str(C['dw']), '__TR__': C['tr'], '__ESTUDIO__': 'sitio/img/estudio.jpg'}
    for k, v in c.items(): rep['__C_' + k.upper() + '__'] = v
    for k, v in rep.items(): page = page.replace(k, v)
    assert '__' not in re.sub(r'__[a-z]', '', page.replace('__proto__', '')) or True
    left = re.findall(r'__[A-Z_]+__', page); assert not left, left
    open(R + '/index.html', 'w').write(page)
    open(R + '/.nojekyll', 'w').write('')
    print(key, 'ok', '%.1f MB zip' % mb)

TEMPLATE = r'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><meta name="description" content="__LEAD__">
<link rel="icon" href="sitio/img/logo.png">
<style>
__FF__
:root{--bg:__C_BG__;--bg2:__C_BG2__;--card:__C_CARD__;--line:__C_LINE__;--ink:__C_INK__;--mute:__C_MUTE__;--acc:__C_ACC__;--accink:__C_ACCINK__;--acc2:__C_ACC2__;--hero:__C_HERO__;--heroink:__C_HEROINK__;--herobtn:__C_HEROBTN__;
 --disp:__DISP__,system-ui,sans-serif;--body:__BODY__,system-ui,sans-serif;--r:10px;--g:clamp(16px,4vw,48px)}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--body);-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 var(--g)}
.top{background:var(--hero);color:var(--heroink)}
.nav{display:flex;align-items:center;gap:24px;padding:20px 0}
.nav img{height:44px;width:auto}
.nav ul{display:flex;gap:20px;list-style:none;padding:0;margin-left:auto;flex-wrap:wrap}
.nav ul a{text-decoration:none;font-weight:500;opacity:.9}.nav ul a:hover{opacity:1;text-decoration:underline}
.hero{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,4vw,56px);align-items:center;padding:clamp(32px,6vw,72px) 0 clamp(40px,7vw,88px)}
.hero h1{font:__DW__ clamp(2.4rem,5.4vw,4.6rem)/1 var(--disp);letter-spacing:__TR__;text-wrap:balance}
.hero p{font-size:clamp(1.05rem,1.6vw,1.25rem);margin-top:18px;max-width:34ch;opacity:.92}
.hero .acts{margin-top:28px}
.hero figure{border-radius:var(--r);overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);outline:1px solid rgba(255,255,255,.18)}
.hero figure img{display:block;width:100%;height:auto}
.acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.b{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:8px 16px;border-radius:999px;border:1.5px solid currentColor;background:transparent;color:inherit;font:500 14px/1.2 var(--body);text-decoration:none;cursor:pointer;transition:background .2s,color .2s,transform .2s}
.b:hover{transform:translateY(-1px)}
.b--acc{background:var(--acc);border-color:var(--acc);color:var(--accink)}
.top .b--big{min-height:48px;padding:12px 22px;font-size:16px}
.top .b--acc{background:var(--heroink);border-color:var(--heroink);color:var(--herobtn)}
.b:focus-visible{outline:3px solid var(--acc2);outline-offset:3px}
section{padding:clamp(48px,7vw,88px) 0;border-top:1px solid var(--line)}
section:nth-of-type(even){background:var(--bg2)}
.head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:end;margin-bottom:32px}
h2{font:__DW__ clamp(1.8rem,3.4vw,2.8rem)/1.05 var(--disp);letter-spacing:__TR__}
.head p{color:var(--mute);max-width:52ch}
.grid{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}
.shot{display:block;aspect-ratio:16/9;background:#000;overflow:hidden}
.shot img,.shot video{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s cubic-bezier(.16,1,.3,1)}
a.shot:hover img{transform:scale(1.03)}
.chk{background:repeating-conic-gradient(#3a4150 0 25%,#2c323e 0 50%) 0 0/24px 24px}
.chk video{object-fit:contain}
.meta{padding:16px 18px 18px;display:flex;flex-direction:column;flex:1}
.meta h3{font:600 1.1rem/1.25 var(--body)}
.meta p{color:var(--mute);font-size:.95rem;margin-top:4px}
.meta code{display:block;margin-top:8px;font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--mute);opacity:.85;word-break:break-all}
.meta .acts{margin-top:auto;padding-top:14px}
.tools{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.tool img{display:block;width:100%;height:auto;aspect-ratio:auto}
.tool .shot{aspect-ratio:auto;background:var(--bg)}
.steps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.steps article{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:24px}
.steps h3{font:600 1.15rem/1.3 var(--body)}
.steps .tag{display:inline-block;background:var(--acc);color:var(--accink);font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;margin-bottom:10px}
.steps ol{margin-top:12px;padding-left:22px;display:grid;gap:8px}
.steps li::marker{color:var(--acc2);font-weight:700}
.steps b{color:var(--ink)}
.steps li{color:var(--mute)}
.note{margin-top:22px;color:var(--mute);font-size:.95rem;max-width:80ch}
kbd,.k{font:13px ui-monospace,Menlo,Consolas,monospace;background:rgba(255,255,255,.08);border:1px solid var(--line);border-radius:6px;padding:1px 6px;color:var(--ink)}
footer{padding:36px 0 56px;border-top:1px solid var(--line);color:var(--mute);font-size:.9rem}
footer .wrap{display:flex;gap:18px;align-items:center;flex-wrap:wrap}footer img{height:34px;width:auto;opacity:.9}
#toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,calc(100% + 48px));visibility:hidden;background:var(--acc);color:var(--accink);padding:12px 20px;border-radius:999px;font-weight:600;box-shadow:0 12px 30px rgba(0,0,0,.35);transition:transform .35s cubic-bezier(.16,1,.3,1),visibility .35s;max-width:calc(100% - 32px);text-align:center;word-break:break-all}
#toast.on{transform:translate(-50%,0);visibility:visible}
@media (max-width:860px){.hero,.head,.tools,.steps{grid-template-columns:minmax(0,1fr)}.nav ul{display:none}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head>
<body>
<div class="top"><div class="wrap">
 <header class="nav"><img src="sitio/img/logo.png" alt="__NAME__"><ul><li><a href="#pantallas">Pantallas</a></li><li><a href="#vivo">Gráficos en vivo</a></li><li><a href="#pip">PiP</a></li><li><a href="#transiciones">Transiciones</a></li><li><a href="#control">Control</a></li><li><a href="#obs">Cómo montarlo</a></li></ul></header>
 <div class="hero">
  <div><h1>__TITLE__</h1><p>__LEAD__ Fuentes de navegador de 1920×1080.</p>
   <div class="acts"><a class="b b--acc b--big" href="__ZIP__" download>Descargar el kit (__MB__)</a><a class="b b--big" href="CONTROL_EN_VIVO.html" target="_blank" rel="noopener">Abrir el control</a></div>
   <div class="acts"><a class="b" href="__MAT__" target="_blank" rel="noopener">Panel de muestra</a><a class="b" href="PANEL_MIDI.html" target="_blank" rel="noopener">Panel MIDI</a></div></div>
  <figure><img src="__ESTUDIO__" alt="Escena ESTUDIO con todos los gráficos en vivo" width="1600" height="900"></figure>
 </div>
</div></div>
<main>
<section id="pantallas"><div class="wrap"><div class="head"><h2>Pantallas completas</h2><p>Una fuente de navegador por escena. Los textos llegan desde CONTROL_EN_VIVO.</p></div><ul class="grid">__SCREENS__</ul></div></section>
<section id="vivo"><div class="wrap"><div class="head"><h2>Gráficos en vivo</h2><p>Van sobre las cámaras en la escena ESTUDIO, con fondo transparente. La cámara de las vistas previas es solo de referencia.</p></div><ul class="grid">__OVERLAYS__</ul></div></section>
<section id="pip"><div class="wrap"><div class="head"><h2>Picture in picture</h2><p>Cinco marcos con las ventanas transparentes: pon tu cámara, presentación o video debajo, en el hueco.</p></div><ul class="grid">__PIPS__</ul></div></section>
<section id="transiciones"><div class="wrap"><div class="head"><h2>Transiciones</h2><p>Videos con transparencia para la transición Stinger de OBS: punto de transición 2000 ms en la de 4 s y 1000 ms en la de 2 s. También en HTML, con el corte manejado por el control.</p></div><ul class="grid">__STG__</ul></div></section>
<section id="control"><div class="wrap"><div class="head"><h2>Control</h2><p>Se abren en Chrome en el PC de la transmisión y se conectan a OBS por WebSocket.</p></div>
 <div class="tools">
  <div class="card tool"><a class="shot" href="CONTROL_EN_VIVO.html" target="_blank" rel="noopener"><img src="sitio/img/control.jpg" alt="CONTROL_EN_VIVO" loading="lazy"></a><div class="meta"><h3>CONTROL_EN_VIVO</h3><p>Instala los gráficos en OBS y maneja __LIST__, lower thirds, mensajes, mosca, PiP, escenas, transiciones y repeticiones.</p><div class="acts"><a class="b b--acc" href="CONTROL_EN_VIVO.html" target="_blank" rel="noopener">Abrir el control</a><button type="button" class="b" data-copy="CONTROL_EN_VIVO.html">Copiar URL (dock de OBS)</button></div></div></div>
  <div class="card tool"><a class="shot" href="PANEL_MIDI.html" target="_blank" rel="noopener"><img src="sitio/img/midi.jpg" alt="PANEL_MIDI" loading="lazy"></a><div class="meta"><h3>PANEL_MIDI</h3><p>Cualquier acción en un pad del controlador MIDI. Ábrelo en el mismo Chrome que el control.</p><div class="acts"><a class="b b--acc" href="PANEL_MIDI.html" target="_blank" rel="noopener">Abrir panel MIDI</a></div></div></div>
 </div></div></section>
<section id="obs"><div class="wrap"><div class="head"><h2>Cómo montarlo en OBS</h2><p>Dos formas de usarlo. Para el evento conviene la primera: no depende de internet.</p></div>
 <div class="steps">
  <article><span class="tag">Recomendado</span><h3>Con el kit descargado</h3><ol>
   <li><b>Descarga el kit</b> y descomprímelo en una carpeta fija del PC de OBS.</li>
   <li>En OBS: <b>Herramientas → Ajustes del servidor WebSocket</b>, habilítalo y copia la contraseña.</li>
   <li>Abre <b>CONTROL_EN_VIVO.html</b> de la carpeta en Chrome, pega la contraseña y pulsa <b>CONECTAR</b>.</li>
   <li>Pulsa <b>Instalar gráficos en OBS</b>: crea __SCENES__ con sus gráficos y la transición HTML.</li>
   <li>Agrega tus cámaras debajo de los gráficos en ESTUDIO y en los huecos de las PiP.</li>
   <li>Carga __LIST__ y los datos del evento en el control.</li></ol></article>
  <article><span class="tag">Sin descargar</span><h3>Directo desde esta página</h3><ol>
   <li>En OBS habilita el <b>servidor WebSocket</b> como en el otro método.</li>
   <li>Abre <b>el control</b> desde esta página y conecta: al instalar, las fuentes se crean apuntando a las URL de este sitio.</li>
   <li>O agrega cada gráfico a mano: <b>Fuente → Navegador</b>, 1920×1080, y pega la URL de <b>Copiar URL para OBS</b>.</li>
   <li>Para las transiciones en video descarga el .webm y créalas como <b>Stinger</b>: <span class="k">__PRE__ Nombre</span>, o <span class="k">__PRE__ Nombre Corta</span> para la de 2 s.</li>
   <li>El control también puede ir como <b>dock</b> de OBS: Docks → Docks de navegador personalizados, con la URL del control.</li></ol></article>
 </div>
 <p class="note">Los gráficos reciben los datos por el WebSocket de OBS, así que funcionan igual desde la carpeta o desde la web. Desde la web necesitan internet durante toda la transmisión; con el kit descargado, no.</p>
</div></section>
</main>
<footer><div class="wrap"><img src="sitio/img/logo.png" alt=""><span>__TITLE__ · Producción NOVA AUDIOVISUAL</span></div></footer>
<div id="toast" role="status" aria-live="polite"></div>
<script>
(function(){var T=document.getElementById('toast'),tt;function toast(m){T.textContent=m;T.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){T.classList.remove('on')},2200)}
document.addEventListener('click',function(e){var b=e.target.closest('[data-copy]');if(!b)return;var u=new URL(b.getAttribute('data-copy'),location.href).href;
 var done=function(){toast('URL copiada: '+u)};if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(done,function(){prompt('Copia la URL:',u)});else prompt('Copia la URL:',u)});
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(x){var v=x.target;if(x.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){})}else v.pause()})},{threshold:.2}):null;
document.querySelectorAll('video').forEach(function(v){if(matchMedia('(prefers-reduced-motion: reduce)').matches){v.removeAttribute('autoplay');v.pause();v.controls=true}else if(io){io.observe(v)}});})();
</script>
</body></html>'''

if __name__ == '__main__':
    for k in (sys.argv[1:] or P): build(k)
