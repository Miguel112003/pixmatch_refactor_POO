import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

from controllers.game_controller import GameController
from settings import PRESSED_EMOJI_HTML_TEMPLATE
from view.main_view import draw_main_page, draw_new_game_board


class GUIController:
    def __init__(self):

        if 'my_state' not in st.session_state:
            self.game_controller = GameController()
            # Agregar las variables que necesitan

            self.run_page = 'main'  # Asigna el método main a la variable run_page para ejecutarse
            self.st_matrix ={} # Controla las columnas y fila a dibujar en streamlit
            self.autorefresh_option = False
            # Variable necesaria para mantener el estado
            st.session_state['my_state'] = self

        else:
            # Si ya existe en la sesión, entonces actualiza los valores
            self.game_controller = st.session_state.my_state.game_controller
            self.st_matrix = st.session_state.my_state.st_matrix
            self.run_page = st.session_state.my_state.run_page
            self.autorefresh_option = st.session_state.my_state.autorefresh_option

    def initialize_columns(self):

        # Crea las columnas
        for i in range(self.game_controller.board.board_size):
            # Define el espacio para cada columna
            # Configura las columnas para los botones del tablero.
            # Cada fila del tablero de juego está compuesta por un número de columnas igual al total de celdas por fila.
            # La ultima columna tiene un ancho fijo de [2] para dar espacio al lado derecho
            columns_list = ([1] * self.game_controller.board.board_size) + [2]  # 2 = espacio al lado derecho

            # Agrega las columnas al diccionario que representa las filas del tablero
            self.st_matrix[i] = st.columns(columns_list)

    def main(self):
        if self.run_page == 'main':
            draw_main_page(self)
        elif self.run_page == 'new_game':
            if self.game_controller.game_status == 'WIN':  # Agregamos esta condición para verificar si el jugador ganó
                self.draw_game_won_page()
            else:
                self.game_controller.new_game()
                draw_new_game_board(self)

    def pre_new_game_gui(self, selected_difficulty, player_name_country, board_size_option, autorefresh_option):
        # Inicializa el tablero
        self.game_controller.pre_new_game(selected_difficulty, player_name_country, board_size_option)
        # Actualiza la página a la vista del tablero de juego
        st.session_state.my_state.run_page = 'new_game'
        # Al haber puesto el estado como 'new_game' y volver a correr el codigo ahora en main se ejecuta otra situacion
        st.rerun()
        # Guarda el estado del autorefrescamiento en la sesión
        st.session_state.my_state.autorefresh_option = autorefresh_option

    def new_game_gui(self):
        # Dibuja las columnas de juego en streamlit
        self.initialize_columns()
        cell_cont = 0

        # Variable para controlar si se ha encontrado el bonus
        bonus_found = False

        # Agrega los botones a las columnas según corresponda en el juego
        for row in range(self.game_controller.board.board_size):
            st_row_to_draw = self.st_matrix[row]
            for col in range(self.game_controller.board.board_size):
                cell_to_draw = self.game_controller.board.cells_map[cell_cont]
                st_cell_to_draw = st_row_to_draw[col].empty()

                # Verificar si la celda es el bonus y aún no se ha encontrado
                if not bonus_found and random.random() < 0.05:  # Probabilidad del 5% de que sea un bonus
                    bonus_found = True
                    self.game_controller.board.cells_map[cell_cont].is_bonus = True
                    bonus_icon = "🎁"
                    st_cell_to_draw.button(bonus_icon, on_click=self.handle_bonus, args=(cell_cont,),
                                           key=f"B{cell_cont}")
                # Si la celda no es el bonus, proceder como antes
                else:
                    # Aquí empieza el juego... el resto es pintar y preparar variables
                    if cell_to_draw.verification_result is None:
                        vemoji = cell_to_draw.emoji_img
                        st_cell_to_draw.button(vemoji, on_click=self.game_controller.play,
                                               args=(cell_cont,),
                                               key=f"B{cell_cont}")
                    elif cell_to_draw.verification_result == True:
                        st_cell_to_draw.markdown(
                            PRESSED_EMOJI_HTML_TEMPLATE.replace('|fill_variable|', '✅️'), unsafe_allow_html=True)
                    elif cell_to_draw.verification_result == False:
                        st_cell_to_draw.markdown(
                            PRESSED_EMOJI_HTML_TEMPLATE.replace('|fill_variable|', '❌'), unsafe_allow_html=True)
                cell_cont += 1

        # Lógica para autorefrescar la página y cambiar el score si pasado un tiempo no se ha seleccionado nada
        self.autorefresh_page()

    def handle_bonus(self, cell_idx):
        """
        Maneja la interacción cuando se descubre el bonus en una celda.
        Args:
            cell_idx: El índice de la celda donde se encuentra el bonus.
        """
        if self.game_controller.board.cells_map[cell_idx].is_bonus:
            # Aumenta el puntaje del jugador
            self.game_controller.current_player.increase_score(5)
            # Mostrar mensaje de bonus encontrado
            st.write("🎉 ¡Has encontrado un bonus! Ganaste 5 puntos adicionales.")
            # Remover el bonus de la celda actual
            self.game_controller.board.cells_map[cell_idx].is_bonus = False
            # Volver a ubicar el bonus si es necesario
            self.relocate_bonus()
        else:
            # Si la celda no es el bonus, no se hace nada
            pass
    def relocate_bonus(self):
        """
        Vuelve a ubicar el bonus en una celda no descubierta, si es posible.
        """
        if self.game_controller.board.count_pending_cells() / self.game_controller.board.total_cells > 0.2:
            # Si queda más del 20% de las celdas por descubrir, volver a ubicar el bonus
            cell_cont = random.randint(0, self.game_controller.board.total_cells - 1)
            while self.game_controller.board.cells_map[cell_cont].verification_result is not None:
                cell_cont = random.randint(0, self.game_controller.board.total_cells - 1)
            # Marcar la nueva celda como el bonus
            self.game_controller.board.cells_map[cell_cont].is_bonus = True

    def autorefresh_page(self):
        """
        Lógica para autorefrescar la página y cambiar el score si pasado un tiempo no se ha seleccionado nada.
        """
        # Temporizador de autorefrescamiento que resta puntos si el tiempo se agota pendiente por agregar
        aftimer = st_autorefresh(interval=(self.get_refresh_interval()), key="aftmr")

        if aftimer > 0:
            # Se agotó el tiempo para seleccionar un emoji, entonces reduce el puntaje del jugador
            self.game_controller.current_player.decrease_score()

    def get_emoji_for_score(self):
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

        if self.game_controller.current_player.score == 0:
            return '😐'
        elif -5 <= self.game_controller.current_player.score <= -1:
            return '😏'
        elif -10 <= self.game_controller.current_player.score <= -6:
            return '☹️'
        elif self.game_controller.current_player.score <= -11:
            return '😖'
        elif 1 <= self.game_controller.current_player.score <= 5:
            return '🙂'
        elif 6 <= self.game_controller.current_player.score <= 10:
            return '😊'
        elif self.game_controller.current_player.score > 10:
            return '😁'

    def get_score_and_pending_cells_values(self):
        return f"{self.get_emoji_for_score()} Score: {self.game_controller.current_player.score} | Pending: {self.game_controller.board.count_pending_cells()}"

    def get_refresh_interval(self):
        """
        Obtiene el intervalo de tiempo en milisegundos para el autorefrescamiento de la página.
        """
        return self.game_controller.selected_difficulty['sec_interval_for_autogen'] * 1000

    def back_to_main(self):
        """
        Regresa a la página principal del juego.
        """
        st.session_state.my_state.run_page = 'main'
        st.rerun()

    def draw_game_won_page(self):
        """
        Dibujamos una pagina cuando el player gana el juego asi bien insano
        """
        # Esta es una referencia a un video, por eso no es el mismo mensajito con gorros de fiesta.
        st.subheader("TU!!! Okay 👍")
        st.balloons()
        # Aqui entre nosotros, porque existe una funcion de globos en St? era necesario?
        st.write(f"Your final score: {self.game_controller.current_player.score}")
        if st.button("🔄 Play Again", key="play_again_button"):
            self.back_to_main()