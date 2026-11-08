# Kit de transmisión · Evento Abastible

Gráficos en vivo para OBS con la identidad visual de Abastible: naranjo `#FE5000`, azul `#001489` / `#003594`, tipografías Ubuntu Sans y Titillium Web, y la silueta del isotipo como forma base. Los colores, las fuentes y el logo se tomaron del sitio abastible.cl porque no se contaba con el manual de marca. Si llega el manual, conviene revisar contra él tonos, áreas de respeto y usos del logo.

## Contenido

| Archivo / carpeta | Para qué sirve |
|---|---|
| `MATERIAL_ABASTIBLE.html` | Panel de muestra de todo el material: pantallas, gráficos en vivo, PiP, transiciones y control. Ábrelo en Chrome para revisar o mostrar el kit. |
| `CONTROL_EN_VIVO.html` | Página de control. Se conecta a OBS y maneja programa, oradores, lower thirds, tema, mensajes, mosca, pantallas, repeticiones y transiciones. |
| `PANEL_MIDI.html` | Controlar todo desde un controlador MIDI. Ábrelo en el mismo Chrome que el control. |
| `Paneles/` | Gráficos para OBS: Inicio, Orador, Agenda, Pausa, Final y overlays (Lower third, Tema, Mensaje, Mosca, Repetición), más los **stingers en HTML** (`ABAS_Stinger.html` y `ABAS_Stinger_<Diseño>.html`). |
| `Transiciones/` | Los mismos 6 diseños en video con transparencia y sonido, para la transición Stinger nativa de OBS: 4 s (corte 2000 ms) y **Corta** de 2 s (corte 1000 ms), en 1080p y `720p/`. `ABAS_transiciones_muestra.mp4` los muestra todos. |
| `Logos/` | Logo a color, logo blanco para fondos azules, versión monocroma e isotipo. |

## Puesta en marcha (una vez, en el PC de OBS)

1. Descomprime el kit en una carpeta fija, por ejemplo Documentos.
2. En OBS: **Herramientas → Ajustes del servidor WebSocket** → habilitar → copiar la contraseña.
3. Abre `CONTROL_EN_VIVO.html` en Chrome, pega la contraseña y pulsa **CONECTAR**.
4. En **Configurar OBS** pulsa **⚙ Instalar gráficos en OBS**. Se crean las escenas INICIO, ESTUDIO, ORADOR, AGENDA, PAUSA, REPLAY, FINAL y las cinco PIP_ con sus gráficos. No se borra nada de lo que ya tengas.
5. En la escena ESTUDIO, agrega tus cámaras **debajo** de los gráficos.
6. Transiciones: el control ya usa los stingers HTML (ver abajo). Si además quieres las versiones en video, crea en OBS transiciones Stinger con el nombre del diseño, por ejemplo **ABAS Ola**, **ABAS Mosaico** o **ABAS Llama Corta** (pueden quedar vacías), y pulsa **🎬 Ajustar transiciones**.
7. En **Datos del evento** completa nombre, fecha, hora, lugar y web. En **Programa del evento** pega o escribe los bloques con el formato `09:30 | Título | Orador | Cargo | Empresa`.

## Durante el evento

- **SIGUIENTE ▶** pasa al bloque siguiente. Se actualizan Orador, Agenda, el tema en pantalla y "A continuación" de la Pausa.
- **Orador del bloque actual** muestra su lower third. Desde la lista puedes mostrar a cualquier persona, y se oculta solo después del tiempo elegido.
- **Pantallas completas**: cuenta regresiva de Inicio (hasta la hora del evento o X minutos), cuenta de Pausa y foto opcional del orador.
- **Repeticiones**: ⏪ Repetir, ★ Momento y resumen por bloque, con pausa, rebobinar y cámara lenta sin negros.
- **Teclado**: `1`–`9` ponen la escena en vista previa, `Shift` + número la pasa directo al aire, `P` repite y `M` guarda un momento.

## Picture in picture (PiP)

Cinco marcos en `Paneles/ABAS_PIP_<Formato>.html`. El fondo de marca tapa todo menos las ventanas, que quedan transparentes para que se vea lo que pongas debajo en OBS:

| Escena | Formato | Ventanas |
|---|---|---|
| `PIP_PRESENTACION` | Presentación + cámara | 1340×754 y 420×236 |
| `PIP_DOS` | Dos cámaras | 885×498 cada una |
| `PIP_TRES` | Tres cámaras | 580×326 cada una |
| `PIP_VERTICAL` | Cámara + video vertical (celular) | 1150×647 y 460×818 |
| `PIP_ESQUINA` | Cámara chica sobre una pantalla completa | 420×236 |

*Instalar gráficos* crea las cinco escenas con el marco, una fuente de color del tamaño exacto en cada ventana (reemplázala por tu cámara, presentación o video y ajústala con *Transformar → Ajustar a la pantalla*) y el stinger HTML encima. En la tarjeta **Picture in picture** del control escribes el título y el nombre y cargo de cada ventana (por ejemplo el orador y quien modera); **Persona actual en la ventana A** pone ahí al orador del momento.

## Transiciones en HTML (stingers)

Seis diseños con la marca, naranjo dominante con acentos azules y el logo en blanco: **Ola**, **Burbuja**, **Cápsulas**, **Llama**, **Anillos** y **Mosaico**. Cada uno tapa la pantalla completa a la mitad de su duración y trae su propio sonido (se genera en el navegador, sin archivos).

**Forma recomendada, desde el control.** *Instalar gráficos* agrega la fuente **ABAS Stinger HTML** encima de todo en cada escena. En la tarjeta **Transiciones HTML** eliges diseño, duración (1,5 · 2 · 3 · 4 s) y sonido:

- **🎬 Vista previa al aire con esta**: lanza la animación y, cuando la pantalla está tapada, pasa la vista previa al aire con un corte. Después deja en OBS la transición que tenías.
- **▶ Probar**: solo reproduce la animación, sin cambiar de escena.
- **Usar esta animación en el botón TRANSICIÓN**: el botón TRANSICIÓN del control y del MIDI usan el stinger HTML.
- En el **PANEL_MIDI** está el grupo *Transiciones HTML*, con un botón por diseño.

**Archivos sueltos para usar en OBS a mano.** `Paneles/ABAS_Stinger_<Diseño>.html` se reproduce cada vez que la fuente se hace visible en OBS (ojo de la fuente, o al aparecer con un "Mostrar" de escena). Agrégalo como *Navegador → Archivo local*, 1920×1080, y marca *Controlar audio mediante OBS* si quieres el sonido en la transmisión. Opciones en la ruta (cámbiala a URL si las usas): `?dur=3` cambia la duración, `?sound=0` sin sonido, `?loop=1` repite en bucle para verlo, `?onactive=1` también al pasar la escena al aire. Abierto en Chrome, la barra espaciadora lo reproduce.

> OBS no acepta un HTML directamente como transición *Stinger* (esa solo usa video). Por eso el control hace el corte en el momento justo, y en `Transiciones/` están los mismos diseños en video para quien prefiera la transición nativa.
