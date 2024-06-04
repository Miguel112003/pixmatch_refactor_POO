import json
import os

from settings import LEADERBOARD_FILE_NAME, FILES_PATH


class LeaderBoardManager:
    """
    Clase para manejar el leaderboard del juego. Guarda y lee el leaderboard en un archivo JSON.
    """

    def __init__(self):
        self.leaderboard_file_name_path = os.path.join(FILES_PATH, LEADERBOARD_FILE_NAME)

    def create_leader_board(self):
        if os.path.isfile(self.leaderboard_file_name_path) == False:
            tmpdict = {}
            # Crea el archivo de leaderboard vacío
            json.dump(tmpdict, open(self.leaderboard_file_name_path, 'w'))  # write file

    def read_leader_board(self):
        """
        Lee el archivo de leaderboard y retorna el diccionario con la información de los jugadores.
        Returns: Diccionario con la información de los jugadores y su puntaje tal y como se encuentra en el archivo JSON.

        """
        if os.path.isfile(self.leaderboard_file_name_path):
            leaderboard = json.load(open(self.leaderboard_file_name_path))
            return leaderboard  # Se retorna el diccionario con el leaderboard
        else:
            # Controla el caso en el que e lederboard no existe
            raise Exception("Leaderboard file does not exist")

    def sort_leader_board_data(self, leaderboard_dicc):
        """
        Ordena el diccionario del leaderboard de mayor a menor puntaje.
        Args:
                leaderboard_dicc: diccionario con la información de los jugadores
        Returns: diccionario ordenado de mayor a menor puntaje
        """
        # Item[1] es el diccionario con la información del jugador
        sorted_items = sorted(leaderboard_dicc.items(), key=lambda dicc_item: dicc_item[1]['HighestScore'],
                              reverse=True)
        # Crea un nuevo diccionario con las claves actualizadas
        leaderboard_dicc = {}
        for i, item in enumerate(sorted_items, start=1):
            # item[1] representa el diccionario con la información del jugador
            leaderboard_dicc[str(i)] = item[1]
        return leaderboard_dicc

    def update_leader_board(self, player, MAX_PLAYERS):
        """
        Actualiza el leaderboard con el puntaje del jugador actual. Siempre y cuando el puntaje del jugador actual sea mayor al puntaje mínimo del leaderboard y no se haya llegado al máximo de jugadores en el leaderboard.
        Args:
            player: jugador actual
            MAX_PLAYERS: maximo de jugadores en el leaderboard (Esta siempre es la constante definida en settings para la cantidad maxima en el leaderboard)
        """
        leaderboard_dicc = self.read_leader_board()
        leaderboard_dict_lngth = len(leaderboard_dicc)

        if leaderboard_dict_lngth >= MAX_PLAYERS:  # Se llegó al máximo de jugadores en el leaderboard
            leaderboard_min_score = min(leaderboard_dicc.values(), key=lambda x: x['HighestScore'])['HighestScore']
            if player.score > leaderboard_min_score:
                # El puntaje del jugador actual supera al puntaje mínimo del leaderboard
                # Solo se dejan en el diccionario los máximos cuatro elementos
                leaderboard_dicc = self.sort_leader_board_data(leaderboard_dicc)
                leaderboard_dicc.popitem()  # Elimina el elemento con el menor puntaje
                leaderboard_dicc[str(leaderboard_dict_lngth)] = {'NameCountry': player.player_name_country,
                                                                  'HighestScore': player.score}
        else:
            leaderboard_dicc[str(leaderboard_dict_lngth + 1)] = {'NameCountry': player.player_name_country,
                                                                 'HighestScore': player.score}

        # Ordena el leaderboard de mayor a menor puntaje
        leaderboard_dicc = self.sort_leader_board_data(leaderboard_dicc)
        # Guarda en disco
        json.dump(leaderboard_dicc, open(self.leaderboard_file_name_path, 'w'))
