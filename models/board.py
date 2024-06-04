from models.board_cell import BoardCell
import random

class Board:
    """
    Clase que representa el tablero de juego con celdas y emojis. Util para mantener la información del tablero
    """

    def __init__(self, board_size):
        self.cells_map = {}
        self.expired_cells_idx_list = []
        self.board_size = board_size
        self.total_cells = board_size ** 2  # El tamaño del tablero es el cuadrado del tamaño de la cuadrícula

    def prepare_board(self):
        """
        Según la dificultad parametrizada prepara el tablero de juego creando
        un objeto de celda para cada celda en el tablero.
        Cada celda tiene un índice unico y su casilla de verificación inicia en None
        """
        cont_row = 0
        cont_col = 0
        for vcell in range(self.total_cells):
            # Crea un objeto de celda y lo agrega al mapa de celdas del tablero
            self.cells_map[vcell] = BoardCell(cell_idx=vcell, row=cont_row, col=cont_col)
            cont_col += 1
            # Verifica si se ha completado una fila
            if cont_col >= self.board_size:
                cont_col = 1  # Reinicia el contador de columnas cada vez que termina una fila
                cont_row += 1  # Incrementa el contador de filas para indicar que va en la fila siguiente

    def get_unpressed_cells(self):
        """
        Retorna una lista de celdas no presionadas que es la diferencia entre las celdas expiradas y las celdas totales del tablero
        """
        all_cells = self.cells_map.keys()
        unpressed_cells = list(set(all_cells) - set(self.expired_cells_idx_list))
        return unpressed_cells

    def count_pending_cells(self):
        """
        Retorna la cantidad de celdas pendientes que no han sido presionadas
        """
        pending_cells = self.total_cells - len(self.expired_cells_idx_list)
        return pending_cells

    def get_cell_by_idx(self, idx):
        return self.cells_map.get(idx)

    def add_expired_cell(self, idx):
        # Busca la celda
        cell = self.cells_map.get(idx)
        if cell is not None:
            # Agrega el índice de la celda a la lista de celdas expiradas
            # Con el índice se puede recuperar del mapa el resto de la información de la celda
            self.expired_cells_idx_list.append(idx)
        else:
            # TODO agregar excepcion, pq la celda no existe
            pass
