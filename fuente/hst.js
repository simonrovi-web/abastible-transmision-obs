
// ---------- transiciones HTML (stingers en HTML) ----------
// La fuente "ABAS Stinger HTML" está arriba de todo en cada escena. Al pedir una transición:
// 1) se dispara la animación, 2) a la mitad (pantalla 100 % tapada) se cambia la escena con un CORTE, 3) se repone la transición que había.
var HST_D=[['ola','Ola'],['burbuja','Burbuja'],['capsulas','Cápsulas'],['llama','Llama'],['anillos','Anillos'],['mosaico','Mosaico']];
var HSTIN='ABAS Stinger HTML';
S.hst=Object.assign({d:'ola',dur:2,snd:true,use:false},S.hst||{});var STG={last:{id:0,d:'ola',dur:2,sound:true},busy:false};
var _msgH=msg;msg=function(){var m=_msgH();m.stinger=STG.last;return m};
function hstName(d){for(var i=0;i<HST_D.length;i++)if(HST_D[i][0]===d)return HST_D[i][1];return d}
function hstFire(d,dur,snd){STG.last={id:Date.now(),d:d,dur:dur,sound:snd};push()}
async function hstCutName(){var r=await reqP('GetSceneTransitionList',{});var t=((r.responseData||{}).transitions||[]);
 for(var i=0;i<t.length;i++)if(/cut_transition/.test(t[i].transitionKind||''))return{name:t[i].transitionName,fade:false};
 for(i=0;i<t.length;i++)if(/fade_transition/.test(t[i].transitionKind||''))return{name:t[i].transitionName,fade:true};return null}
function wait(ms){return new Promise(function(r){setTimeout(r,ms)})}
async function htmlTrans(d,target){d=d||S.hst.d;var dur=+S.hst.dur||2,snd=!!S.hst.snd;
 if(!WS.ok){hstFire(d,dur,snd);return toast('Sin OBS: solo se reprodujo la animación')}
 if(STG.busy)return;STG.busy=true;
 try{var sl=(await reqP('GetSceneList',{})).responseData||{},prog=sl.currentProgramSceneName,prev=sl.currentPreviewSceneName,studio=!!prev;
  var to=target||(studio?prev:null);
  if(!to||to===prog){hstFire(d,dur,snd);toast(studio?'La vista previa es igual al aire: solo se reprodujo la animación':'Activa el Modo Estudio o elige una escena: solo se reprodujo la animación');return}
  var cut=await hstCutName(),old=(await reqP('GetCurrentSceneTransition',{})).responseData||{},oldName=old.transitionName,oldDur=old.transitionDuration;
  hstFire(d,dur,snd);await wait(dur*500);
  if(cut){await reqP('SetCurrentSceneTransition',{transitionName:cut.name});if(cut.fade)await reqP('SetCurrentSceneTransitionDuration',{transitionDuration:50})}
  if(studio&&!target)await reqP('TriggerStudioModeTransition',{});else await reqP('SetCurrentProgramScene',{sceneName:to});
  await wait(250);if(oldName&&cut&&oldName!==cut.name)await reqP('SetCurrentSceneTransition',{transitionName:oldName});if(cut&&cut.fade&&oldDur)await reqP('SetCurrentSceneTransitionDuration',{transitionDuration:oldDur});
  loadScenes();loadTrans()}
 finally{STG.busy=false}}
async function ensureStinger(){var il=await reqP('GetInputList',{});var ins=((il.responseData||{}).inputs||[]).map(function(x){return x.inputName});
 var set={is_local_file:true,local_file:panelDir()+'ABAS_Stinger.html',width:1920,height:1080,shutdown:false,restart_when_active:false,reroute_audio:true,fps_custom:true,fps:60};
 var sl=await reqP('GetSceneList',{});var scs=((sl.responseData||{}).scenes||[]).map(function(x){return x.sceneName});var n=0;
 for(var i=0;i<scs.length;i++){var sc=scs[i];
  if(ins.indexOf(HSTIN)<0){await reqP('CreateInput',{sceneName:sc,inputName:HSTIN,inputKind:'browser_source',inputSettings:set,sceneItemEnabled:true});ins.push(HSTIN);n++}
  else{var items=(((await reqP('GetSceneItemList',{sceneName:sc})).responseData||{}).sceneItems||[]).map(function(x){return x.sourceName});if(items.indexOf(HSTIN)<0){await reqP('CreateSceneItem',{sceneName:sc,sourceName:HSTIN});n++}}
  var all=(((await reqP('GetSceneItemList',{sceneName:sc})).responseData||{}).sceneItems||[]);var id=((await reqP('GetSceneItemId',{sceneName:sc,sourceName:HSTIN})).responseData||{}).sceneItemId;if(id!=null){await reqP('SetSceneItemIndex',{sceneName:sc,sceneItemId:id,sceneItemIndex:Math.max(0,all.length-1)});await reqP('SetSceneItemEnabled',{sceneName:sc,sceneItemId:id,sceneItemEnabled:true})}}
 await reqP('SetInputSettings',{inputName:HSTIN,inputSettings:set,overlay:true});
 // el audio del stinger sale por el mezclador (monitor y transmisión)
 await reqP('SetInputAudioMonitorType',{inputName:HSTIN,monitorType:'OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT'});return n}
function renderHst(){$('hst_g').innerHTML=HST_D.map(function(x){return '<button data-hd="'+x[0]+'" class="'+(x[0]===S.hst.d?'cur':'')+'">'+x[1]+'</button>'}).join('');
 $('hst_dur').value=String(S.hst.dur);$('hst_snd').checked=!!S.hst.snd;$('hst_use').checked=!!S.hst.use;
 var src='Paneles/ABAS_Stinger_'+hstName(S.hst.d).replace('á','a')+'.html?loop=1&sound=0&dur='+S.hst.dur;if($('hst_pv').getAttribute('src')!==src)$('hst_pv').setAttribute('src',src);
 $('air-hst').textContent=S.hst.use?'EN TRANSICIÓN':'SOLO MANUAL';$('air-hst').className='onair'+(S.hst.use?' v':'')}
$('hst_g').addEventListener('click',function(e){var b=e.target.closest('[data-hd]');if(!b)return;S.hst.d=b.dataset.hd;save();renderHst()});
$('hst_dur').onchange=function(){S.hst.dur=+this.value;save();renderHst()};
$('hst_snd').onchange=function(){S.hst.snd=this.checked;save()};
$('hst_use').onchange=function(){S.hst.use=this.checked;save();renderHst()};
$('hst_test').onclick=function(){hstFire(S.hst.d,+S.hst.dur,!!S.hst.snd)};
$('hst_go').onclick=function(){htmlTrans(S.hst.d)};
$('hst_inst').onclick=async function(){if(!WS.ok)return toast('Conecta OBS primero');if(isRemote())return toast('Se usa en el PC donde está OBS');var n=await ensureStinger();toast('Stinger HTML listo en todas las escenas'+(n?' ('+n+' agregados)':''))};
(function(){var o=$('btrans').onclick;$('btrans').onclick=function(){if(S.hst.use)htmlTrans(S.hst.d);else o.call(this)}})();
renderHst();
