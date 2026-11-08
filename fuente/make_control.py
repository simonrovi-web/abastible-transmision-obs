#!/usr/bin/env python3
"""Arma control_template.html (CONTROL_EN_VIVO de Abastible) reutilizando los motores probados del kit FCC2
(conexión OBS, instalación, transiciones y repeticiones sin negros) y las partes nuevas del evento."""
FCC = open('/home/claude/fcc/control_live_template.html').read()

def cut(a, b):
    i = FCC.index(a); j = FCC.index(b, i)
    return FCC[i:j]

def R(s, a, b, n=1):
    c = s.count(a)
    assert c == n, (a[:70], c)
    return s.replace(a, b)

SHA = cut('// SHA-256', '// ---------- estado ----------')

WS = cut('// ---------- OBS WebSocket v5 ----------', '// ---------- reloj ----------')
WS = R(WS, "ls('fcc2-ws',conf)", "ls('abas-ws',conf)")
WS = R(WS, "var c=ls('fcc2-ws')", "var c=ls('abas-ws')")
WS = R(WS, "if(window.rbStatus)rbStatus()}", "if(window.rbStatus)rbStatus();if(window.rbHide)rbHide()}")

INST = cut('// ---------- instalación, diagnóstico y vista de OBS ----------', '// ---------- colores y nombres de esquina ----------')
INST = R(INST, INST[INST.index('var PLAN=['):INST.index('function li(')], """var PLAN=[
 {scene:'INICIO',src:[['ABAS Inicio','ABAS_Inicio']]},
 {scene:'ESTUDIO',src:[['ABAS Tema','ABAS_Overlay_Tema'],['ABAS Lower Third','ABAS_Overlay_LowerThird'],['ABAS Mensaje','ABAS_Overlay_Mensaje'],['ABAS Mosca','ABAS_Overlay_Mosca']]},
 {scene:'ORADOR',src:[['ABAS Orador','ABAS_Orador']]},
 {scene:'AGENDA',src:[['ABAS Agenda','ABAS_Agenda']]},
 {scene:'PAUSA',src:[['ABAS Pausa','ABAS_Pausa']]},
 {scene:'REPLAY',src:[['ABAS Repeticion','ABAS_Overlay_Replay'],['ABAS Mosca','ABAS_Overlay_Mosca']]},
 {scene:'FINAL',src:[['ABAS Final','ABAS_Final']]},
 {scene:'PIP_PRESENTACION',src:[['ABAS PiP Presentacion','ABAS_PIP_Presentacion']]},
 {scene:'PIP_DOS',src:[['ABAS PiP Dos','ABAS_PIP_Dos']]},
 {scene:'PIP_TRES',src:[['ABAS PiP Tres','ABAS_PIP_Tres']]},
 {scene:'PIP_VERTICAL',src:[['ABAS PiP Vertical','ABAS_PIP_Vertical']]},
 {scene:'PIP_ESQUINA',src:[['ABAS PiP Esquina','ABAS_PIP_Esquina']]}];
""")
INST = INST.replace('FCC2_[A-Za-z_]+', 'ABAS_[A-Za-z_]+')
INST = R(INST, "event_name:'fcc2'", "event_name:'abas'")
INST = R(INST, "Descomprime FCC2_Kit.zip en una carpeta", "Descomprime el kit de Abastible en una carpeta")
INST = R(INST, " MARK=(found['FCC2_Overlay_Marcador']||['FCC2 Marcador'])[0];FCCIN=", " FCCIN=")
INST = R(INST, "var need=['FCC2_Overlay_Marcador','FCC2_VS','FCC2_Ganador','FCC2_Overlay_LowerThird','FCC2_Overlay_Replay','FCC2_Overlay_Mosca'];",
              "var need=['ABAS_Inicio','ABAS_Orador','ABAS_Agenda','ABAS_Pausa','ABAS_Final','ABAS_Overlay_LowerThird','ABAS_Overlay_Mosca','ABAS_Overlay_Tema','ABAS_Overlay_Mensaje','ABAS_Overlay_Replay'];")
INST = R(INST, "x.replace('FCC2_','').replace('Overlay_','')", "x.replace('ABAS_','').replace('Overlay_','')")
INST = R(INST, "'No hay gráficos FCC2 en esta colección de escenas'", "'No hay gráficos de Abastible en esta colección de escenas'")
INST = R(INST, "/^FCC2 /.test(inputs[i].inputName)", "/^ABAS /.test(inputs[i].inputName)")
INST = INST.replace("' 1 '", "' 1 '")
# prueba del marcador (no existe en este kit)
i = INST.index("$('btest').onclick"); j = INST.index("var PVHOLD=0;", i)
INST = INST[:i] + INST[j:]
INST = R(INST, "var PVHOLD=0;var MARK='FCC2 Marcador',FCCIN=[];", "var PVHOLD=0,FCCIN=[];")
i = INST.index("$('tot').value=S.clock.total"); INST = INST[:i]
# transiciones Abastible: Ola y Burbuja, largas (4 s, corte 2000 ms) y cortas (2 s, corte 1000 ms)
INST = R(INST, INST[INST.index('function trFile('):INST.index('async function trFix(')],
 "function trFile(name,path){var t=(name+' '+(path||'')).toLowerCase(),c=/cort[ao]/.test(t)?'_Corta':'';var M=[[/ola/,'Ola'],[/burbuja|circ/,'Burbuja'],[/c[aá]psula/,'Capsulas'],[/llama/,'Llama'],[/anillo/,'Anillos'],[/mosaico/,'Mosaico']];for(var i=0;i<M.length;i++)if(M[i][0].test(t))return M[i][1]+c;return null}\n")
INST = R(INST, "'En OBS: panel <b>Transiciones de escena</b> → <b>+</b> → <b>Stinger</b> → nómbrala <b>FCC2 Golpe</b> (repite para <b>FCC2 Rapida</b>, <b>FCC2 Replay</b>, <b>FCC2 Golpe Corta</b> y <b>FCC2 Rapida Corta</b>) y acepta aunque esté vacía. Luego pulsa AJUSTAR otra vez.'",
 "'En OBS: panel <b>Transiciones de escena</b> → <b>+</b> → <b>Stinger</b> → nómbrala <b>ABAS Ola</b> (repite para <b>ABAS Burbuja</b>, <b>ABAS Ola Corta</b> y <b>ABAS Burbuja Corta</b>) y acepta aunque esté vacía. Luego pulsa AJUSTAR otra vez.'")
INST = R(INST, "'«'+esc(nm)+'»: no es de FCC2, no se tocó','Si quieres que use un video FCC2, ponle Golpe, Rapida o Replay en el nombre.'",
 "'«'+esc(nm)+'»: no es de Abastible, no se tocó','Si quieres que use un video del kit, ponle Ola, Burbuja, Cápsulas, Llama, Anillos o Mosaico en el nombre.'")
INST = R(INST, "ns.path=dir+'FCC2_Transicion_'+f+'.webm'", "ns.path=dir+'ABAS_Transicion_'+f+'.webm'")
INST = R(INST, "'«'+esc(nm)+'» → FCC2_Transicion_'+f+'.webm'", "'«'+esc(nm)+'» → ABAS_Transicion_'+f+'.webm'")
INST = R(INST, "'Corte a 2000 ms · el video tapa la pantalla de 0,3 s a 3,7 s, así que el cambio de escena nunca se ve.'", "'Corte a 2000 ms · el video tapa toda la pantalla en ese momento, así que el cambio de escena no se ve.'")
INST = R(INST, "'Versión corta (2 s) · corte a 1000 ms · tapa la pantalla de 0,3 s a 1,7 s.'", "'Versión corta (2 s) · corte a 1000 ms.'")
INST = R(INST, "  await ensureReplay(true);\n", "  await ensureReplay(true);await ensurePip();await ensureStinger();\n")
INST = R(INST, "b.textContent='⚙ INSTALAR GRÁFICOS EN OBS'", "b.textContent='⚙ Instalar gráficos en OBS'")

RB = cut('// ---------- repeticiones (búfer de repetición de OBS) ----------', '// v2: Felipe Castro')
RB = R(RB, "var RBIN='FCC2 Repeticion Video'", "var RBIN='ABAS Repeticion Video'")
RB = R(RB, "S.hl=S.hl||[];S.rb=S.rb||{speed:50,len:10,back:true};", "S.hl=S.hl||[];S.rb=S.rb||{speed:100,len:15,after:'estudio'};")
RB = R(RB, "function hlLabel(){var f=S.f,c=S.clock;return {c:S.cur,num:f.numero||S.cur+1,round:c.round,t:fmt(c.len-remain()),r:U(f.r_nombre),b:U(f.b_nombre)}}",
 "function hlLabel(){var it=curItem(),d=new Date();return {c:S.cur,num:S.cur+1,t:String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0'),ti:it.t||'',o:it.o||''}}")
RB = R(RB, "var k=h.c;if(!G[k]){G[k]={c:k,num:h.num,r:h.r,b:h.b,items:[]};ord.push(k)}", "var k=h.c;if(!G[k]){G[k]={c:k,num:h.num,ti:h.ti,o:h.o,items:[]};ord.push(k)}")
RB = R(RB, "if(G[S.cur]==null&&S.fights[S.cur]){var f=S.fights[S.cur];G[S.cur]={c:S.cur,num:S.cur+1,r:U(S.f.r_nombre||f.r),b:U(S.f.b_nombre||f.b),items:[]};ord.push(S.cur)}",
 "if(G[S.cur]==null&&S.ag[S.cur]){var f=S.ag[S.cur];G[S.cur]={c:S.cur,num:S.cur+1,ti:f.t,o:f.o,items:[]};ord.push(S.cur)}")
RB = R(RB, "' combates)':''", "' bloques)':''")
RB = R(RB, "<b>COMBATE '+g.num+(cur?' · AL AIRE':'')+'</b><span>'+esc((g.r||'?')+' vs '+(g.b||'?'))+'</span>", "<b>BLOQUE '+g.num+(cur?' · AL AIRE':'')+'</b><span>'+esc([g.ti,g.o].filter(Boolean).join(' · ')||'—')+'</span>")
RB = R(RB, "title=\"Resumen de este combate\">▶ RESUMEN</button><button data-hx=\"'+k+'\" title=\"Borrar los clips de este combate\">", "title=\"Resumen de este bloque\">▶ Resumen</button><button data-hx=\"'+k+'\" title=\"Quitar los clips de este bloque\">")
RB = R(RB, "' · R'+h.round+' · '+h.t+'</span>", "' · '+h.t+'</span>")
RB = R(RB, "Sin clips todavía: usa ⏪ REPETIR o ★ GUARDAR MOMENTO.", "Sin clips todavía: usa ⏪ Repetir o ★ Guardar momento.")
RB = R(RB, "// nombre de archivo por combate: OBS guarda los clips como \"C07 NOMBRE vs NOMBRE <fecha>.mkv\"\nfunction rbPrefix(){var f=S.f,n=('0'+(S.cur+1)).slice(-2),ap=function(x){x=U(x).split(/\\s+/);return x.length>1?x[x.length-1]:x[0]||''};\n return ('FCC2 C'+n+' '+ap(f.r_nombre)+' vs '+ap(f.b_nombre))",
 "// nombre de archivo por bloque: OBS guarda los clips como \"ABAS B03 Titulo <fecha>.mkv\"\nfunction rbPrefix(){var it=curItem(),n=('0'+(S.cur+1)).slice(-2);\n return ('ABAS B'+n+' '+(it.t||'').slice(0,40))")
RB = R(RB, "toast('Clips del combate '+(c+1)+' quitados de la lista')", "toast('Clips del bloque '+(c+1)+' quitados de la lista')")
RB = R(RB, "b.textContent='¿SEGURO? TOCA OTRA VEZ';setTimeout(function(){b.dataset.ok='';b.textContent='🗑 BORRAR COMBATES ANTERIORES'},2500);return}\n b.dataset.ok='';b.textContent='🗑 BORRAR COMBATES ANTERIORES';",
 "b.textContent='¿Seguro? Toca otra vez';setTimeout(function(){b.dataset.ok='';b.textContent='🗑 Borrar otros bloques'},2500);return}\n b.dataset.ok='';b.textContent='🗑 Borrar otros bloques';")
RB = R(RB, "' clips de otros combates quitados de la lista'", "' clips de otros bloques quitados de la lista'")
RB = R(RB, "return toast('No hay momentos de este combate')", "return toast('No hay momentos de este bloque')")
RB = R(RB, "S.rp=label||'REPETICIÓN';", "S.rp=label||'REPETICIÓN';")
RB = R(RB, "$('rb_speed').value=String(S.rb.speed);$('rb_len').value=String(S.rb.len);if(S.rbV!==2){S.rb.after='estudio';S.rbV=2;save()}$('rb_after').value=S.rb.after||'estudio';",
 "$('rb_speed').value=String(S.rb.speed);$('rb_len').value=String(S.rb.len);$('rb_after').value=S.rb.after||'estudio';")
RB = R(RB, "S.rbPref=S.rbPref!==false;", "S.rbPref=!!S.rbPref;")

HST = open('hst.js').read()
PIPJS = open('/home/claude/pip_ctl.js').read().replace('__LAYOUTS__', '{"Presentacion": {"win": {"a": [60, 170, 1340, 754, "Presentación"], "b": [1440, 170, 420, 236, "Cámara"]}, "bg": true}, "Dos": {"win": {"a": [60, 250, 885, 498, "Cámara 1"], "b": [975, 250, 885, 498, "Cámara 2"]}, "bg": true}, "Tres": {"win": {"a": [60, 320, 580, 326, "Cámara 1"], "b": [670, 320, 580, 326, "Cámara 2"], "c": [1280, 320, 580, 326, "Cámara 3"]}, "bg": true}, "Vertical": {"win": {"a": [60, 200, 1150, 647, "Cámara"], "b": [1310, 170, 460, 818, "Video vertical"]}, "bg": true}, "Esquina": {"win": {"a": [1440, 744, 420, 236, "Cámara"]}, "bg": false}}').replace('__P__', 'ABAS')
MIDI = r"""
// ---------- atajos de la franja superior ----------
$('m_rb').onclick=function(){$('rb_play').click()};$('m_hl').onclick=function(){$('rb_save').click()};

// ---------- puente con PANEL_MIDI (misma PC, mismo Chrome) ----------
var CMD=null;try{CMD=new BroadcastChannel('abas-cmd')}catch(e){}
function midiState(){return{type:'state',ts:Date.now(),conn:WS.ok,trs:TRS.list,trcur:TRS.cur,scenes:SC.list,cur:SC.cur,prev:SC.prev,toprev:$('toprev').checked,
 rb:RB.active,playing:RB.playing,saving:!!RB.saving,rbpause:!!RB.userPause&&!RB.rew,rbrew:!!RB.rew,rbspd:RB.spdNow||100,
 show:{lt:!!S.show.lt,mosca:!!S.show.mosca,tema:!!S.show.tema,msg:!!S.show.msg},hst:S.hst.d,hstuse:!!S.hst.use,block:S.cur+1,nb:S.ag.length,pausa:!!S.pau.end}}
function doCmd(c,a){if(/^hst_/.test(c)){if(c==='hst_go')htmlTrans();else htmlTrans(c.slice(4))}else switch(c){
 case 'trsel':case 'trgo':if(!WS.ok)return toast('Conecta OBS primero');reqP('SetCurrentSceneTransition',{transitionName:a}).then(function(r){if(!(r.requestStatus&&r.requestStatus.result))return toast('No existe la transición «'+a+'» en OBS');TRS.cur=a;loadTrans();toast('Transición: '+a);if(c==='trgo')setTimeout(function(){$('btrans').click()},80)});break;
 case 'scene':goScene(a);break; case 'sceneP':goScene(a,false);break; case 'sceneV':toPreview(a);break;
 case 'trans':$('btrans').click();break; case 'toprev':$('toprev').checked=!$('toprev').checked;break;
 case 'next':loadBlock(S.cur+1);break; case 'prev':loadBlock(S.cur-1);break;
 case 'lt_cur':$('blt_cur').click();break; case 'tgl_lt':(S.show.lt?$('blth'):$('blt_cur')).click();break;
 case 'tgl_tema':(S.show.tema?$('tm_hide'):$('tm_show')).click();break;
 case 'tgl_msg':(S.show.msg?$('ms_hide'):$('ms_show')).click();break;
 case 'tgl_mosca':(S.show.mosca?$('mo_hide'):$('mo_show')).click();break;
 case 'pausa_go':$('pa_go').click();break;
 case 'replay':$('rb_play').click();break; case 'replay5':case 'replay10':case 'replay15':RB.len1=+c.slice(6);$('rb_play').click();break; case 'replayslow':RB.spd1=50;$('rb_play').click();break; case 'moment':$('rb_save').click();break;
 case 'rb_pause':tpPause();break; case 'rb_backplay':tpBackPlay();break; case 'rb_rew':tpRewind();break; case 'rb_back2':tpSeek(-2000);break; case 'rb_back5':tpSeek(-5000);break; case 'rb_fwd2':tpSeek(2000);break; case 'rb_restart':$('tp_restart').click();break; case 'rb_slow':tpSlow();break; case 'rb_speed':tpCycle();break; case 'rb_scrub':tpScrub(+a||0);break;
 case 'reel':$('rb_reel').click();break; case 'reelall':$('rb_reelall').click();break; case 'stop':$('rb_stop').click();break}
 if(CMD)setTimeout(function(){CMD.postMessage(midiState())},120)}
if(CMD){CMD.onmessage=function(e){var m=e.data;if(m&&m.type==='cmd')doCmd(m.cmd,m.arg);else if(m&&m.type==='hello')CMD.postMessage(midiState())};
 setInterval(function(){CMD.postMessage(midiState())},300)}
renderMo();renderAg();renderPpl();renderAir();push();runDiag();
</script></body></html>
"""

A = open('control_a.js').read()
A = A.replace('__SHA__', SHA).replace('__WS__', WS)
out = open('control_head.html').read() + A + '\n' + INST + '\n' + RB + HST + PIPJS + MIDI
assert 'S.fights' not in out and 'S.clock' not in out and 'fcc2' not in out.lower().replace('fcc2_kit', ''), [w for w in ['S.fights', 'S.clock', 'fcc2'] if w in out]
open('control_template.html', 'w').write(out)
print('ok', len(out))
