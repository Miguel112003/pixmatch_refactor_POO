import random
import streamlit as st
from models.board import Board
from models.leaderboard_manager import LeaderBoardManager
from models.player import Player
from settings import EMOJIS_CATEGORIES_EASY, EMOJIS_CATEGORIES_MEDIUM, EMOJIS_CATEGORIES_HARD, \
    DIFFICULTY_LEVELS_OPTIONS, MAX_LEADERBOARD_PLAYERS


class GameController:
    def __init__(self):
        """
          Inicializa el controlador del juego con los valores predeterminados.
        """
        self.selected_difficulty = None
        self.current_player = None
        self.emoji_bank = []
        self.target_emoji = None
        self.game_status = None
        self.board = None
        self.leaderboard_ranking = {}  # Diccionario con el ranking del leaderboard
        self.leaderboard_manager = LeaderBoardManager()


    def pick_emoji_bank(self):
        """
         Selecciona un banco de emojis basado en la dificultad seleccionada.
        """
        random.seed()
        # Version mejorada de la selección de categoría de emojis según la dificultad del juego
        difficulty_emoji_map = {
            'Easy': EMOJIS_CATEGORIES_EASY,
            'Medium': EMOJIS_CATEGORIES_MEDIUM,
            'Hard': EMOJIS_CATEGORIES_HARD
        }

        difficulty_name = self.selected_difficulty['name']
        if difficulty_name in difficulty_emoji_map:
            # Define el banco de emojis
            self.emoji_bank = random.choice(difficulty_emoji_map[difficulty_name])

    def choose_sidebar_emoji(self):
        """
        Selecciona un emoji al azar para la barra lateral.
        """

        sidebar_emoji_index = random.randint(0, len(self.emoji_bank) - 1)
        self.target_emoji = self.emoji_bank[sidebar_emoji_index]

    def reset_board(self):
        """
            Reinicia el tablero del juego, configurando emojis aleatorios en cada celda de la cuadrícula,
            y asegurándose de que el emoji de la barra lateral esté presente al menos una vez en el tablero.
            """
        # Seleccionar un emoji para la barra lateral de forma aleatoria
        self.choose_sidebar_emoji()

        sidebar_emoji_in_list = False  # Controla si el emoji de la barra lateral está en el tablero

        # Configurar emojis para cada celda del tablero que no ha sido presionada
        unpressed_cells_list = self.board.get_unpressed_cells()
        for unpressed_cell in unpressed_cells_list:
            emoji_index = random.randint(0, len(self.emoji_bank) - 1)
            emoji = self.emoji_bank[emoji_index]
            # Actualiza el emoji de la celda
            self.board.cells_map[unpressed_cell].emoji_img = emoji
            if emoji == self.target_emoji:
                sidebar_emoji_in_list = True

        # Asegurar que el emoji de la barra lateral está al menos una vez en el tablero
        if not sidebar_emoji_in_list:
            if len(self.board.get_unpressed_cells()) > 0:
                selected_cell = random.choice(unpressed_cells_list)
                # Asigna el emoji de la barra lateral a la celda seleccionada
                self.board.cells_map[selected_cell].emoji_img = self.target_emoji

    def pre_new_game(self, selected_difficulty, player_name_country, board_size_option):
        """
               Prepara el juego para una nueva sesión, inicializando las celdas y los puntajes.

               Esta función se encarga de reiniciar todos los estados relevantes para comenzar un nuevo juego.
               Reinicia las celdas del juego y selecciona de manera aleatoria los emojis
               que aparecerán en el tablero según la dificultad del juego. Asegura que todos los botones de
               la cuadrícula estén configurados para el inicio de una nueva partida.
        """
        self.selected_difficulty = DIFFICULTY_LEVELS_OPTIONS[selected_difficulty]
        self.current_player = Player(player_name_country)
        # Inicializa el tablero
        self.board = Board(board_size_option)

        # Selecciona el banco de emojis
        self.pick_emoji_bank()

        # Reinicia la información de los botones del juego
        self.board.prepare_board()

        # Indica que el juego esta activo
        self.game_status = 'ACTIVE'

        # Crea el leaderboard si no existe y el jugador puso el nombre
        if self.current_player.player_name_country != "":
            self.leaderboard_manager.create_leader_board()

    def new_game(self):

        # Reinicia el tablero del juego
        self.reset_board()

        # Lee el leaderboard si se recibió el nombre del jugador
        if self.current_player.player_name_country != "":
            self.leaderboard_ranking = self.leaderboard_manager.read_leader_board()

        # Verificar si el juego ha terminado o todavía sigue activo
        self.verify_game_status()

    def play(self, cell_idx):
        """
        Verifica si el emoji seleccionado por el jugador coincide con el emoji objetivo.
        Actualiza el puntaje del jugador en consecuencia.
        Args:
            cell_idx:
        """
        cell = self.board.cells_map[cell_idx]
        cell.verify_emoji_match(self.target_emoji)
        if cell.verification_result == True:
            self.current_player.increase_score(self.selected_difficulty['points_by_difficulty'])
        elif cell.verification_result == False:
            self.current_player.decrease_score()

        # Agrega la celda a la lista de celdas que ya fueron usadas
        self.board.add_expired_cell(cell_idx)

    def verify_game_status(self):
        """
             Verifica si el juego sigue en curso, si el jugador ha ganado o perdido.
             Ademas verifica si el jugador sigue por debajo del numero de errores maximos, en caso de
             haber superdado la cantidad pierde automaticamente.
        Returns:
           'ACTIVE' si el juego sigue en curso, 'WIN' si el jugador ha ganado, 'LOOSE' si el jugador ha perdido.
        """
        # Determino el numero maximo de fallos
        max_failures = self.board.total_cells // 2 + 1
        # Obtengo los fallos del jugador
        player_failures = sum(1 for cell in self.board.cells_map.values() if cell.verification_result == False)

        if player_failures >= max_failures:
            self.game_status = 'LOOSE'

        # Y mantengo la logica de la version anterior:
        elif self.board.count_pending_cells() == 0:
            if self.current_player.score < 0:
                self.game_status = 'LOOSE'
            elif self.current_player.score > 0:
                self.game_status = 'WIN'
                # Actualiza el leaderboard solo si gana
                self.leaderboard_manager.update_leader_board(player=self.current_player,
                                                             MAX_PLAYERS=MAX_LEADERBOARD_PLAYERS)
        else:
            self.game_status = 'ACTIVE'
        return self.game_status