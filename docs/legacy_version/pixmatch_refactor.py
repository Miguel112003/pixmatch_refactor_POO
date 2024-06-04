""" Version documentada """
import base64
import json
import os
import random
import time as tm

import streamlit as st
from PIL import Image
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

vDrive = os.path.splitdrive(os.getcwd())[0]
# if vDrive == "C:": vpth = "C:/Users/Shawn/dev/utils/pixmatch/"   # local developer's disc
# else:

# Ruta relativa a la carpeta donde se tiene el código fuente y se ejecutará el programa.
ruta_en_disco = "./"

# Plantillas HTML para diferentes componentes de la interfaz de usuario en el juego

# Devuelve una cadena HTML formateada con un emoji grande para la interfaz principal del juego.
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

# Devuelve una cadena HTML formateada para un emoji presionado, utilizado en la interfaz del juego.
pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

# Devuelve una barra horizontal HTML para usar en la separación de secciones en la interfaz del juego.
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"  # thin divider line

# Define los estilos CSS para los botones utilizados en la interfaz del juego."""
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

# Inicializa o reinicia las variables del estado del juego almacenadas en el estado de sesión de Streamlit.
mystate = st.session_state
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
# Configuración inicial del juego
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7,
                                                        '']  # difficulty level, sec interval for autogen, total_cells_per_row_or_col, player name


# common functions
def ReduceGapFromPageTop(wch_section='main page'):
    """
    Ajusta el margen superior en las secciones específicas de la interfaz de usuario de Streamlit.

    Esta función modifica el estilo CSS para reducir el espacio en la parte superior de la página principal,
    la barra lateral o ambas, según el parámetro proporcionado. Se utiliza para mejorar la estética
    de la página y ajustar la visibilidad de los componentes UI según las necesidades del diseño.

    Args:
    wch_section (str): Define la sección de la interfaz donde se aplicará el ajuste. Las opciones válidas son:
                       - 'main page': Aplica el estilo solo a la página principal.
                       - 'sidebar': Aplica el estilo solo a la barra lateral.
                       - 'all': Aplica el estilo tanto a la página principal como a la barra lateral.

    Ejemplo de uso:
    ReduceGapFromPageTop('main page')  # Ajusta el espacio superior solo en la página principal.
    ReduceGapFromPageTop('sidebar')    # Ajusta el espacio superior solo en la barra lateral.
    ReduceGapFromPageTop('all')        # Ajusta el espacio superior en ambas secciones.
    """
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ",
                    True)  # Ajusta el espacio en la página principal
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ",
                    True)  # Ajusta el espacio en la barra lateral
    elif wch_section == 'all':
        # Ajusta el espacio tanto en la página principal como en la barra lateral
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)


def Leaderboard(what_to_do):
    """
     Administra las operaciones del tablero de líderes, incluyendo crear, escribir y leer el archivo de puntuaciones altas.

     Args:
     what_to_do (str): Especifica la acción a realizar sobre el leaderboard. Las opciones válidas son:
                       - 'create': Crea un archivo nuevo para el leaderboard si no existe uno.
                       - 'write': Registra la puntuación actual del jugador en el leaderboard, solo si el jugador ha proporcionado su nombre.
                       - 'read': Lee el archivo del leaderboard y muestra las puntuaciones si el archivo existe y el jugador ha proporcionado su nombre.

     Ejemplo de uso:
     Leaderboard('create')  # Crea un archivo de leaderboard si no existe.
     Leaderboard('write')   # Escribe en el leaderboard si el jugador ha proporcionado su nombre.
     Leaderboard('read')    # Lee y muestra el leaderboard si existe y el nombre del jugador está proporcionado.
     """
    if what_to_do == 'create':
        # Crea el archivo donde guardar la tabla de jugadores con mejores puntajes
        if mystate.GameDetails[3] != '':
            if os.path.isfile(ruta_en_disco + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(ruta_en_disco + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'write':
        # Escribe en el leaderboard si el jugador ha proporcionado su nombre y el archivo existe
        if mystate.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(ruta_en_disco + 'leaderboard.json'):
                leaderboard = json.load(open(ruta_en_disco + 'leaderboard.json'))  # read file
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3],
                                                                'HighestScore': mystate.myscore}
                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                if len(leaderboard) > 3:
                    for i in range(len(leaderboard) - 3): leaderboard.popitem()  # rmv last kdict ey

                json.dump(leaderboard, open(ruta_en_disco + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'read':
        # Lee y muestra el leaderboard si el archivo existe y el jugador ha proporcionado su nombre
        if mystate.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(ruta_en_disco + 'leaderboard.json'):
                leaderboard = json.load(open(ruta_en_disco + 'leaderboard.json'))  # read file

                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                sc0, sc1, sc2, sc3 = st.columns((2, 3, 3, 3))
                rknt = 0
                for key in leaderboard:
                    rknt += 1
                    if rknt == 1:
                        sc0.write('🏆 Ganadores anteriores:')
                        sc1.write(f"🥇 | {leaderboard[key]['NameCountry']}: {leaderboard[key]['HighestScore']}")
                    elif rknt == 2:
                        sc2.write(f"🥈 | {leaderboard[key]['NameCountry']}: {leaderboard[key]['HighestScore']}")
                    elif rknt == 3:
                        sc3.write(f"🥉 | {leaderboard[key]['NameCountry']}: {leaderboard[key]['HighestScore']}")


def InitialPage():
    """Configura y muestra la página inicial del juego, incluyendo la barra lateral y las reglas del juego."""
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        # Cargar y mostrar el logo del juego en la barra lateral
        sidebar_logo = Image.open(ruta_en_disco + 'sidebarlogo.jpg').resize((300, 390))
        st.image(sidebar_logo, use_column_width='auto')

    # Detalles y ayuda del juego
    # ViewHelp
    hlp_dtl = f"""<span style="font-size: 26px;">
       <ol>
       <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
       <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
       <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
       <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
       <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
       <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
       <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
       </ol></span>"""

    # Configuración de columnas para mostrar las reglas del juego y una imagen de ayuda
    sc1, sc2 = st.columns(2)
    random.seed()
    game_help_image_path = ruta_en_disco + random.choice(
        ["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    game_help_image = Image.open(game_help_image_path).resize((550, 550))
    sc2.image(game_help_image, use_column_width='auto')

    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_bar, True)
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)
    st.markdown(horizontal_bar, True)

    # Detalles del autor
    author_details = "<strong>Happy  play: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_details, unsafe_allow_html=True)


def ReadPictureFile(wch_fl):
    """Lee un archivo de imagen y devuelve su contenido codificado en base64."""
    try:
        file_path = f"{ruta_en_disco}{wch_fl}"
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.error(f"Error al leer el archivo de imagen: {str(e)}")
        return ""


def PressedCheck(vcell):
    """Verifica si un botón de la cuadrícula ha sido presionado y actualiza el estado del juego."""
    if not mystate.plyrbtns[vcell]['isPressed']:
        mystate.plyrbtns[vcell]['isPressed'] = True
        mystate.expired_cells.append(vcell)

        if mystate.plyrbtns[vcell]['eMoji'] == mystate.sidebar_emoji:
            mystate.plyrbtns[vcell]['isTrueFalse'] = True
            mystate.myscore += 5  # Aumenta la puntuación según la dificultad
            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1
        else:
            mystate.plyrbtns[vcell]['isTrueFalse'] = False
            mystate.myscore -= 1  # Penalización por error


def ResetBoard():
    """
    Reinicia el tablero del juego, configurando emojis aleatorios en cada celda de la cuadrícula,
    y asegurándose de que el emoji de la barra lateral esté presente al menos una vez en el tablero.
    """
    total_cells_per_row_or_col = mystate.GameDetails[2]  # Total de celdas por fila o columna según la dificultad

    # Seleccionar un emoji para la barra lateral de forma aleatoria
    sidebar_emoji_index = random.randint(0, len(mystate.emoji_bank) - 1)
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_index]

    sidebar_emoji_in_list = False  # Controla si el emoji de la barra lateral está en el tablero

    # Configurar emojis para cada celda del tablero
    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):
        if not mystate.plyrbtns[vcell]['isPressed']:  # Solo cambia los emojis de celdas no presionadas
            emoji_index = random.randint(0, len(mystate.emoji_bank) - 1)
            vemoji = mystate.emoji_bank[emoji_index]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji

            if vemoji == mystate.sidebar_emoji:
                sidebar_emoji_in_list = True

    # Asegurar que el emoji de la barra lateral está al menos una vez en el tablero
    if not sidebar_emoji_in_list:
        unpressed_cells = [cell for cell in range(1, (total_cells_per_row_or_col ** 2) + 1)
                           if not mystate.plyrbtns[cell]['isPressed']]
        if unpressed_cells:
            selected_cell = random.choice(unpressed_cells)
            mystate.plyrbtns[selected_cell]['eMoji'] = mystate.sidebar_emoji


def PreNewGame():
    """
       Prepara el juego para una nueva sesión, inicializando las celdas y los puntajes.

       Esta función se encarga de reiniciar todos los estados relevantes para comenzar un nuevo juego.
       Reinicia las celdas del juego, el puntaje del jugador, y selecciona de manera aleatoria los emojis
       que aparecerán en el tablero según la dificultad del juego. Asegura que todos los botones de
       la cuadrícula estén configurados para el inicio de una nueva partida.

       La función clasifica los emojis en varias categorías y selecciona una categoría de acuerdo a la
       dificultad establecida en los detalles del juego. Esta selección influye en la disposición inicial
       de los emojis en el tablero, impactando la experiencia de juego.
       """
    total_cells_per_row_or_col = mystate.GameDetails[
        2]  # Total de celdas por fila o columna, definido por la dificultad
    mystate.expired_cells = []  # Reinicia la lista de celdas expiradas
    mystate.myscore = 0  # Reinicia el puntaje del jugador

    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    random.seed()
    # Selección de categoría de emojis según la dificultad del juego
    if mystate.GameDetails[0] == 'Easy':
        # Asignar a mystate.emoji_bank el valor de una variable local cuyo nombre está almacenado en wch_bank
        # locals retorna un diccionario que contiene las variables definidas en el ámbito local donde se ejecuta
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]

    # Reinicia la información de los botones del juego
    mystate.plyrbtns = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        # vcell es la clave y corresponde a cada celda individual en la cuadrícula del juego.

        # 'isPressed': False: Un booleano que indica si la celda ha sido presionada. Inicialmente, está configurado en False, lo que significa que ninguna celda ha sido tocada al iniciar el juego.
        # 'isTrueFalse': False: True si la acción realizada en esa celda fue correcta, False en caso contrario
        # 'eMoji': '': Una cadena vacía que se usará para almacenar un emoji o símbolo que se mostrará en esa celda. Al inicio, no hay emojis asignados.
        mystate.plyrbtns[vcell] = {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''}


def score_emoji():
    """
       Determina el emoji a mostrar basado en la puntuación actual del jugador almacenada en `my_state.myscore`.

       Esta función evalúa el rango en el que se encuentra la puntuación del jugador y retorna un emoji correspondiente
       que refleja una retroalimentación visual instantánea al jugador sobre su desempeño.

       Returns:
           str: Un string de emoji que representa el estado emocional del jugador.

       Ejemplos:
           - Una puntuación de 0 retorna '😐', indicando una expresión neutral.
           - Puntuaciones negativas retornan emojis tristes, incrementando en tristeza a medida que la puntuación disminuye.
           - Puntuaciones positivas retornan emojis sonrientes, incrementando en alegría a medida que la puntuación aumenta.
       """
    if mystate.myscore == 0:
        return '😐'
    elif -5 <= mystate.myscore <= -1:
        return '😏'
    elif -10 <= mystate.myscore <= -6:
        return '☹️'
    elif mystate.myscore <= -11:
        return '😖'
    elif 1 <= mystate.myscore <= 5:
        return '🙂'
    elif 6 <= mystate.myscore <= 10:
        return '😊'
    elif mystate.myscore > 10:
        return '😁'


def NewGame():
    """
      Inicia una nueva partida del juego, restableciendo el tablero y preparando todos los componentes necesarios.

      Esta función se encarga de inicializar o reiniciar todas las configuraciones necesarias para comenzar un nuevo juego.
      Configura el tablero con nuevos emojis, restablece los puntajes y asegura que el entorno del juego esté listo para una nueva sesión.
      Además, gestiona la interfaz de usuario en la barra lateral para mostrar detalles relevantes del juego y maneja la interacción del usuario durante la partida.

      Proceso detallado:
      - Llama a `ResetBoard()` para preparar el tablero con emojis nuevos y aleatorios.
      - Ajusta el margen superior en la barra lateral para optimizar la visualización.
      - Muestra en la barra lateral el nivel de dificultad actual, el emoji objetivo y ofrece la posibilidad de reiniciar el juego.
      - Configura un temporizador de autorefrescamiento que penaliza al jugador si el tiempo se agota antes de realizar una selección.
      - Lee el leaderboard para mostrar los puntajes altos y permite al usuario interactuar con el tablero del juego.
      - Maneja la lógica de finalización del juego y transición entre diferentes pantallas de juego.
      """
    ResetBoard()  # Prepara el tablero con nuevos emojis
    total_cells_per_row_or_col = mystate.GameDetails[2]

    ReduceGapFromPageTop('sidebar')
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True)

        # Temporizador de autorefrescamiento que resta puntos si el tiempo se agota
        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0: mystate.myscore -= 1

        st.info(
            f"{score_emoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = Main
            st.rerun()

    # Lee y muestra el leaderboard
    Leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set Board Dafaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # make button face big

    # Configura y muestra los botones del tablero del juego de forma programatrica
    for i in range(1, (total_cells_per_row_or_col + 1)):
        # Configura las columnas para los botones del tablero.
        # Cada fila del tablero de juego está compuesta por un número de columnas igual al total de celdas por fila.
        # La variable 'tlst' define el espacio de cada columna, y luego se crea un objeto de columna para cada posición.

        tlst = ([1] * total_cells_per_row_or_col) + [2]  # 2 = espacio al lado derecho
        globals()['cols' + str(i)] = st.columns(tlst)

    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):

        # Itera sobre cada celda del tablero, configurando los botones y su comportamiento.
        # 'arr_ref' calcula la referencia de la fila actual basada en la celda y la cantidad de celdas por fila.
        # 'mval' es el índice del primer elemento en la fila actual.
        # Si un botón está presionado, muestra el resultado de la acción (correcto o incorrecto).
        # Si no está presionado, muestra el botón para ser seleccionado.

        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2) + 1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3) + 1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4) + 1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5) + 1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6) + 1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7) + 1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8) + 1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9) + 1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        globals()['cols' + arr_ref][vcell - mval] = globals()['cols' + arr_ref][vcell - mval].empty()
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)

            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)

        else:
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell - mval].button(vemoji, on_click=PressedCheck, args=(vcell,),
                                                             key=f"B{vcell}")

    st.caption('')  # vertical filler
    st.markdown(horizontal_bar, True)

    # Sección de escritura de puntajes y manejo de las interacciones del tablero
    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2):
        # Escribir en el leaderboard si todas las celdas han sido presionadas
        Leaderboard('write')

        # Evaluar el puntaje del jugador para determinar el resultado del juego
        if mystate.myscore > 0:
            st.balloons()  # Muestra animación de globos si el jugador tiene un puntaje positivo
        elif mystate.myscore <= 0:
            st.snow()  # Muestra animación de nieve si el puntaje es cero o negativo

        # Pausa antes de reiniciar o volver a la página principal
        tm.sleep(5)
        mystate.runpage = Main  # Cambia la página activa a la principal
        st.rerun()  # Reinicia la aplicación Streamlit para reflejar el cambio de página


def Main():
    """
        Configura y muestra la página principal del juego, incluyendo la selección de la dificultad, entrada del nombre del jugador,
        y la opción de iniciar un nuevo juego.

        Esta función actúa como la pantalla de inicio del juego, donde los usuarios pueden seleccionar opciones
        y configurar los detalles antes de comenzar una partida. Incluye configuraciones para la dificultad del juego,
        entrada para el nombre del jugador, y un botón para iniciar el juego.

        Proceso detallado:
        - Configura el ancho de la barra lateral y el estilo de los botones.
        - Muestra opciones para seleccionar el nivel de dificultad y para que el usuario ingrese su nombre y país.
        - Ofrece un botón para comenzar un nuevo juego, que al ser presionado, invocará la preparación del juego
          y transición a la pantalla de juego activa.
        - Inicializa la página con detalles básicos y ayuda visible para el usuario.
        """

    # Ajustar el estilo de la barra lateral y los botones
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    # Mostrar la página inicial con reglas e instrucciones
    InitialPage()
    # Configuración de la barra lateral para entradas de usuario y opciones
    with st.sidebar:
        # Selección de nivel de dificultad
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )

        # Entrada para el nombre del jugador y el país
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for Leaderboard')

        # Botón para iniciar un nuevo juego
        if st.button(f"🕹️ New Game", use_container_width=True):
            # Configurar intervalos de tiempo y tamaño de la cuadrícula basado en la dificultad seleccionada
            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # secs interval
                mystate.GameDetails[2] = 6  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # secs interval
                mystate.GameDetails[2] = 7  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # secs interval
                mystate.GameDetails[2] = 8  # total_cells_per_row_or_col

            # Crear el leaderboard si no existe, preparar el juego y cambiar a la pantalla de juego
            Leaderboard('create')

            PreNewGame()
            mystate.runpage = NewGame
            st.rerun()

        st.markdown(horizontal_bar, True)  # Barra decorativa horizontal


if 'runpage' not in mystate:
    mystate.runpage = Main
mystate.runpage()
