import random
import time as tm

import streamlit as st
from PIL import Image

from settings import HORIZONTAL_BAR_HTML_TEMPLATE, PURPLE_BUTTON_HTML_TEMPLATE, \
    IMAGES_PATH, TARGET_EMOJI_HTML_TEMPLATE, MAX_LEADERBOARD_PLAYERS, DIFFICULTY_LEVELS_OPTIONS


def draw_instructions():
    # Detalles y ayuda del juego
    instruccions_html_text = f"""<span style="font-size: 26px;">
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
    game_help_image_path = IMAGES_PATH + random.choice(
        ["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    game_help_image = Image.open(game_help_image_path).resize((550, 550))
    sc2.image(game_help_image, use_column_width='auto')

    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)
    sc1.markdown(instruccions_html_text, unsafe_allow_html=True)
    st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)

    # Detalles del autor
    author_details = "<strong>Happy  play: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_details, unsafe_allow_html=True)
    st.info("Modified by: Luisa Rincon y Yo :D")


def draw_main_page(gui_controller):
    # Ajustar el estilo de la barra lateral y los botones
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(PURPLE_BUTTON_HTML_TEMPLATE, unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)

        # Cargar y mostrar el logo del juego en la barra lateral
        sidebar_logo = Image.open(IMAGES_PATH + 'sidebarlogo.jpg').resize((300, 390))
        st.image(sidebar_logo, use_column_width='auto')

    # Mostrar la página inicial con reglas e instrucciones
    draw_instructions()

    # Configuración de la barra lateral para entradas de usuario y opciones
    with st.sidebar:
        # Selección de nivel de dificultad
        selected_difficulty = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=0,
                                       horizontal=True, )
        st.write(f'La dificultad seleccionada fue {selected_difficulty}')

        # Obtener las opciones de tamaño de tablero según la dificultad seleccionada
        board_size_options = DIFFICULTY_LEVELS_OPTIONS[selected_difficulty]['board_size_options']

        # Permitir al usuario seleccionar el tamaño del tablero
        board_size_options = st.radio('Board Size:', options=board_size_options, index=0, horizontal=True, key='board_size')

        # La opcion de autorefresco
        autorefresh_option = st.checkbox("Enable Autorefresh", key="autorefresh_option")

        # Entrada para el nombre del jugador y el país
        player_name_country = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                            help='Optional input only for Leaderboard')
        # Botón para iniciar un nuevo juego
        if st.button(f"🕹️ New Game", use_container_width=True):
            gui_controller.pre_new_game_gui(selected_difficulty, player_name_country, board_size_options, autorefresh_option)

        st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)  # Barra decorativa horizontal


def draw_new_game_board(gui_controller):
    reduce_gap_from_page_top('sidebar')
    # Dibujar la barra lateral que tiene el emoji a buscar y el botón de regreso
    draw_lateral_bar_new_game(gui_controller)

    # Dibujar el ranking del leaderboard
    draw_leaderboard_ranking(gui_controller)

    st.subheader("Picture Positions:")
    st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)
    # Set Board Defaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # make button face big

    # Dibujar la matriz del tablero
    gui_controller.new_game_gui()

    st.caption('')  # vertical filler
    st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)

    # Lógica para controlar mensajes de fin de juego cuando se ha terminado
    draw_end_game_info(gui_controller)


def draw_end_game_info(gui_controller):
    """
    Muestra un mensaje de victoria o derrota cuando termina el juego.
    """
    if gui_controller.game_controller.game_status != 'ACTIVE':
        # Mostrar mensaje de victoria o derrota
        if gui_controller.game_controller.game_status == 'WIN':
            gui_controller.draw_game_won_page()
        elif gui_controller.game_controller.game_status == 'LOOSE':
            st.error("😢 You lost! 😢")
            st.snow()  # Muestra animación de nieve si el puntaje es cero o negativo
        tm.sleep(5)
        gui_controller.back_to_main()
    else:
        pass  # No se hace nada si el juego sigue activo


def draw_lateral_bar_new_game(gui_controller):
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {gui_controller.game_controller.current_player.player_name_country}")
        st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)
        st.markdown(TARGET_EMOJI_HTML_TEMPLATE.replace('|fill_variable|', gui_controller.game_controller.target_emoji),
                    True)

        st.info(gui_controller.get_score_and_pending_cells_values())

        st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            gui_controller.back_to_main()


def draw_leaderboard_ranking(gui_controller):
    # Crear una lista con el ancho de las columnas
    # La primera columna tiene un ancho fijo de 2
    # Las columnas restantes tienen un ancho dinámico de 1
    column_widths = [2] + [1] * MAX_LEADERBOARD_PLAYERS

    # Crear las columnas en Streamlit
    columns = st.columns(column_widths)

    leaderboard = gui_controller.game_controller.leaderboard_ranking

    # La primera columna enunciara el texto de ganadores por eso es columns[0
    columns[0].write('🏆 Past winners:')
    for idx, (key, value) in enumerate(leaderboard.items()):
        if idx < MAX_LEADERBOARD_PLAYERS:
            columns[idx + 1].write(f"'🥇' | {value['NameCountry']}: {value['HighestScore']}")


def reduce_gap_from_page_top(section_to_adjust):
    if section_to_adjust == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ",
                    True)  # Ajusta el espacio en la página principal
    elif section_to_adjust == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ",
                    True)  # Ajusta el espacio en la barra lateral
    elif section_to_adjust == 'all':
        # Ajusta el espacio tanto en la página principal como en la barra lateral
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)
