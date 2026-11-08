#!/usr/bin/env python3
"""Arma el kit final en ../abastible-streaming: control, panel MIDI, paneles y transiciones."""
import base64, os, shutil, glob, io
from PIL import Image
OUT = '/home/claude/abastible-streaming'
B = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
F = 'node_modules/@fontsource/'
FONTS = ''.join('@font-face{font-family:"%s";font-weight:%d;src:url(data:font/woff2;base64,%s) format("woff2");}' % (f, w, B(F + p)) for f, p, w in [
    ('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-400-normal.woff2', 400),
    ('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-500-normal.woff2', 500),
    ('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-700-normal.woff2', 700),
    ('Ubuntu Sans', 'ubuntu-sans/files/ubuntu-sans-latin-800-normal.woff2', 800)])
im = Image.open('logo_white.png'); im.thumbnail((600, 600)); b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
LOGO = 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
os.makedirs(OUT + '/Paneles', exist_ok=True); os.makedirs(OUT + '/fuente', exist_ok=True); os.makedirs(OUT + '/Logos', exist_ok=True)
for src, dst in [('control_template.html', 'CONTROL_EN_VIVO.html'), ('midi_template.html', 'PANEL_MIDI.html')]:
    if os.path.exists(src):
        open(OUT + '/' + dst, 'w').write(open(src).read().replace('__FONTS__', FONTS).replace('__LOGO__', LOGO))
for f in glob.glob('out/ABAS_*.html'):
    shutil.copy(f, OUT + '/Paneles/')
for f in ['logo_color.png', 'logo_white.png', 'logo_mono.png', 'isotipo.png', 'isotipo_mono.png']:
    shutil.copy(f, OUT + '/Logos/' + f.replace('logo_', 'Abastible_logo_').replace('isotipo', 'Abastible_isotipo'))
for f in ['build.py', 'make_control.py', 'control_head.html', 'control_a.js', 'midi_template.html', 'make_midi.py', 'stinger.html', 'assemble.py', 'blob_path.txt', 'build_stingers.py', 'hst.js', 'stinger_render.html']:
    if os.path.exists(f): shutil.copy(f, OUT + '/fuente/')
print('ok')
