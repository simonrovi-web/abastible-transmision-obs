#!/usr/bin/env python3
"""Stingers en HTML para OBS (Abastible).
Genera:
  out/ABAS_Stinger.html            → fuente única con los 6 diseños; la dispara CONTROL_EN_VIVO y corta la escena en el momento justo
  out/ABAS_Stinger_<Diseño>.html   → un archivo por diseño; se reproduce solo al hacerse visible en OBS (o con ?loop=1 para verlo)
  stinger_render.html              → para renderizar las versiones en video (.webm con transparencia)"""
import base64, io
from PIL import Image

def png(p, w):
    im = Image.open(p); im.thumbnail((w, w)); b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
LOGO = png('logo_mono.png', 1100)
BLOB = open('blob_path.txt').read().strip()
DESIGNS = [('ola', 'Ola'), ('burbuja', 'Burbuja'), ('capsulas', 'Capsulas'), ('llama', 'Llama'), ('anillos', 'Anillos'), ('mosaico', 'Mosaico')]

ENGINE = r'''
var LOGO="__LOGO__",BLOB="__BLOB__";
var OR='#FE5000',OR2='#FF7A33',ORD='#E84800',AZ='#001489',AZ2='#003594',BL='#ffffff';
function cl(x){return Math.max(0,Math.min(1,x))}
function eio(x){x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
function eo(x){x=cl(x);return 1-Math.pow(1-x,3)}
function ei(x){x=cl(x);return x*x*x}
function back(x){x=cl(x);var c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}
// fases: entrada (EIN), pantalla tapada, salida (EOUT). El corte de escena va a la mitad (TOTAL/2).
function phases(TOTAL){var e=Math.min(.62,TOTAL*.32);return{EIN:e,EOUT:e,o:TOTAL-e}}
function logo(T,TOTAL,w){var P=phases(TOTAL),li=back((T-P.EIN*.7)/.35),lo=ei((T-(P.o-.12))/.25),op=cl((T-P.EIN*.7)/.15)*(1-lo);
 return '<img src="'+LOGO+'" style="position:absolute;left:50%;top:50%;width:'+(w||820)+'px;opacity:'+op+';transform:translate(-50%,-50%) scale('+(li*(1-lo*.5))+')">'}
function wavePanel(x,col,amp,ph,dir){var p,y;if(dir>0){p='M-300 -60 L'+x+' -60 ';for(y=-60;y<=1140;y+=30)p+='L'+(x+Math.sin(y/140+ph)*amp).toFixed(1)+' '+y+' ';p+='L-300 1140 Z'}
 else{p='M2220 -60 L'+x+' -60 ';for(y=-60;y<=1140;y+=30)p+='L'+(x-Math.sin(y/140+ph)*amp).toFixed(1)+' '+y+' ';p+='L2220 1140 Z'}return '<path d="'+p+'" fill="'+col+'"/>'}
var D={
 ola:function(T,TOTAL){var P=phases(TOTAL),cols=[AZ,ORD,OR],s='';
  for(var i=0;i<3;i++){var d=i*.07,a=eio((T-d)/(P.EIN-.12)),b=eio((T-P.o-d*.6)/(P.EOUT-.1));
   s+=b<=0?wavePanel(-320+a*2440,cols[i],40+i*10,T*3+i,1):wavePanel(-200+b*2440,cols[i],40+i*10,T*3+i,-1)}
  return svg(s)+logo(T,TOTAL)},
 burbuja:function(T,TOTAL){var P=phases(TOTAL),o=P.o-.1,cols=[AZ,OR],s='';
  for(var j=0;j<2;j++){var a=eio((T-j*.09)/(P.EIN-.09)),b=ei((T-o-(1-j)*.09)/(P.EOUT-.09)),k=Math.max(0,a*(1-b)),S=44*Math.pow(k,2.2),rot=-28+28*a+(b>0?20*b:0);
   s+='<g transform="translate(960 540) rotate('+rot+') scale('+S+') translate(-50 -39.1)"><path d="'+BLOB+'" fill="'+cols[j]+'"/></g>'}
  return svg(s)+logo(T,TOTAL)},
 capsulas:function(T,TOTAL){var P=phases(TOTAL),N=7,h=1080/N,s='';
  for(var r=0;r<N;r++){var dist=Math.abs(r-(N-1)/2),d=dist*.045,a=eio((T-d)/(P.EIN-.15)),b=eio((T-P.o-d)/(P.EOUT-.15)),col=r%2?ORD:OR,y=r*h-2;
   var x=b<=0?(-2700+a*2600):(-100+b*2300);
   s+='<rect x="'+(x-80)+'" y="'+(y+h*.18)+'" width="2600" height="'+(h*.64)+'" rx="'+(h*.32)+'" fill="'+AZ+'"/>';
   s+='<rect x="'+x+'" y="'+y+'" width="2600" height="'+(h+4)+'" rx="'+(h/2)+'" fill="'+col+'"/>'}
  return svg(s)+logo(T,TOTAL)},
 llama:function(T,TOTAL){var P=phases(TOTAL),M=12,w=1920/M,s='';
  for(var c=0;c<M;c++){var d=(Math.sin(c*1.7)*.5+.5)*.12,a=eio((T-d)/(P.EIN-.14)),b=eio((T-P.o-d)/(P.EOUT-.14)),col=c%3===1?OR2:(c%3===2?ORD:OR);
   var H=1400,y=b<=0?(1100-a*(H-40)):(1100-(H-40)-b*(H+200)),x=c*w-3;
   s+='<rect x="'+x+'" y="'+(y-60)+'" width="'+(w+6)+'" height="'+H+'" rx="'+(w/2)+'" fill="'+AZ+'"/>';
   s+='<rect x="'+x+'" y="'+y+'" width="'+(w+6)+'" height="'+H+'" rx="'+(w/2)+'" fill="'+col+'"/>'}
  return svg(s)+logo(T,TOTAL)},
 anillos:function(T,TOTAL){var P=phases(TOTAL),R=1180,cols=[AZ,BL,OR],s='';
  for(var i=0;i<3;i++){var a=eio((T-i*.08)/(P.EIN-.16)),b=eio((T-P.o-(2-i)*.06)/(P.EOUT-.12)),ro=R*a,ri=R*b*1.02;
   if(ro<=ri)continue;s+='<path fill-rule="evenodd" fill="'+cols[i]+'" d="M'+(960-ro)+' 540a'+ro+' '+ro+' 0 1 0 '+(2*ro)+' 0a'+ro+' '+ro+' 0 1 0 '+(-2*ro)+' 0'+(ri>0?'M'+(960-ri)+' 540a'+ri+' '+ri+' 0 1 0 '+(2*ri)+' 0a'+ri+' '+ri+' 0 1 0 '+(-2*ri)+' 0':'')+'Z"/>'}
  return svg(s)+logo(T,TOTAL)},
 mosaico:function(T,TOTAL){var P=phases(TOTAL),C=12,Rw=7,w=160,h=1080/Rw,s='';
  for(var r=0;r<Rw;r++)for(var c=0;c<C;c++){var dx=(c-(C-1)/2)/((C-1)/2),dy=(r-(Rw-1)/2)/((Rw-1)/2),dist=Math.sqrt(dx*dx+dy*dy)/1.42,
   a=back((T-dist*.22)/(P.EIN-.22)),b=ei((T-P.o-dist*.2)/(P.EOUT-.2)),k=Math.max(0,a*(1-b))*1.12,col=((r*5+c*3)%7===0)?AZ:((r+c)%2?OR:ORD);
   if(k<=0)continue;var cx=c*w+w/2,cy=r*h+h/2;s+='<rect x="'+(cx-w*k/2)+'" y="'+(cy-h*k/2)+'" width="'+(w*k)+'" height="'+(h*k)+'" rx="'+(30*k)+'" fill="'+col+'"/>'}
  return svg(s)+logo(T,TOTAL)}};
function svg(s){return '<svg viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute;inset:0">'+s+'</svg>'}
function drawAt(root,design,T,TOTAL){root.innerHTML=(T<0||T>TOTAL)?'':(D[design]||D.ola)(T,TOTAL)}
// sonido: "whoosh" de entrada y salida + campanita al tapar (Web Audio, sin archivos)
var AC=null;function sfx(TOTAL){try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();var t0=AC.currentTime+.02,P=phases(TOTAL);
 function whoosh(at,dur,f0,f1,g){var n=AC.sampleRate*dur,buf=AC.createBuffer(1,n,AC.sampleRate),d=buf.getChannelData(0);for(var i=0;i<n;i++)d[i]=Math.random()*2-1;
  var src=AC.createBufferSource();src.buffer=buf;var bp=AC.createBiquadFilter();bp.type='bandpass';bp.Q.value=1.2;bp.frequency.setValueAtTime(f0,at);bp.frequency.exponentialRampToValueAtTime(f1,at+dur*.6);
  var gn=AC.createGain();gn.gain.setValueAtTime(0,at);gn.gain.linearRampToValueAtTime(g,at+dur*.55);gn.gain.linearRampToValueAtTime(0,at+dur);src.connect(bp);bp.connect(gn);gn.connect(AC.destination);src.start(at);src.stop(at+dur)}
 function ding(at,f,g){var o=AC.createOscillator(),gn=AC.createGain();o.type='sine';o.frequency.value=f;gn.gain.setValueAtTime(g,at);gn.gain.exponentialRampToValueAtTime(.0001,at+1.1);o.connect(gn);gn.connect(AC.destination);o.start(at);o.stop(at+1.2)}
 whoosh(t0,P.EIN+.15,500,5000,.5);ding(t0+P.EIN*.75,880,.12);ding(t0+P.EIN*.82,1318.5,.07);whoosh(t0+P.o-.05,P.EOUT+.1,4500,600,.4)}catch(e){}}
// reproductor (el logo se decodifica al cargar para que el primer cuadro no se atrase)
try{var _li=new Image();_li.src=LOGO;if(_li.decode)_li.decode()}catch(e){}
var PLAY=null;function play(design,TOTAL,sound){PLAY={d:design,T0:performance.now(),TOT:TOTAL};if(sound)sfx(TOTAL);
 var root=document.getElementById('st');(function f(){if(!PLAY)return;var T=(performance.now()-PLAY.T0)/1000;drawAt(root,PLAY.d,T,PLAY.TOT);if(T<=PLAY.TOT)requestAnimationFrame(f);else{PLAY=null;root.innerHTML='';if(window.onDone)window.onDone()}})()}
'''

HEAD = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>%s</title><style>*{margin:0;padding:0}html,body{width:1920px;height:1080px;overflow:hidden;background:transparent}#st{position:absolute;inset:0}</style></head><body><div id="st"></div><script>'
ENG = ENGINE.replace('__LOGO__', LOGO).replace('__BLOB__', BLOB)

# 1) fuente única controlada desde CONTROL_EN_VIVO
CTL = HEAD % 'Abastible · Stinger HTML' + ENG + r'''
var Q=new URLSearchParams(location.search),LASTID=null;
// solo órdenes recientes: si OBS recarga la fuente no repite la última animación
function onLive(d){var s=d&&d.stinger;if(!s||!s.id||s.id===LASTID)return;LASTID=s.id;if(Math.abs(Date.now()-s.id)>8000)return;play(s.d,+s.dur||2,s.sound!==false)}
window.addEventListener('abas',function(e){onLive(e.detail)});
try{new BroadcastChannel('abas').onmessage=function(e){onLive(e.data)}}catch(e){}
if(Q.get('demo')){var dd=Q.get('demo'),tt=+(Q.get('dur')||2);(function lp(){play(dd,tt,false);setTimeout(lp,(tt+1)*1000)})()}
</script></body></html>'''
open('out/ABAS_Stinger.html', 'w').write(CTL)

# 2) un archivo por diseño: se reproduce cuando la fuente se hace visible en OBS
for key, name in DESIGNS:
    one = HEAD % ('Abastible · Stinger ' + name) + ENG + r'''
var Q=new URLSearchParams(location.search),DES="__KEY__",DUR=+(Q.get('dur')||2),SND=Q.get('sound')!=='0';
function go(){play(DES,DUR,SND)}
window.addEventListener('obsSourceVisibleChanged',function(e){if(e.detail&&e.detail.visible)go()});
window.addEventListener('obsSourceActiveChanged',function(e){if(e.detail&&e.detail.active&&Q.get('onactive')==='1')go()});
document.addEventListener('keydown',function(e){if(e.key===' ')go()});
if(Q.get('loop')==='1'){(function lp(){go();setTimeout(lp,(DUR+1)*1000)})()}else if(!window.obsstudio)setTimeout(go,300);
</script></body></html>'''.replace('__KEY__', key)
    open('out/ABAS_Stinger_%s.html' % name, 'w').write(one)

# 3) página para renderizar a video
REN = HEAD % 'render' + ENG + r'''
var Q=new URLSearchParams(location.search);window.render2=function(T){drawAt(document.getElementById('st'),Q.get('m'),T,+(Q.get('total')||2))};
</script></body></html>'''
open('stinger_render.html', 'w').write(REN)
print('ok', [d[1] for d in DESIGNS])
