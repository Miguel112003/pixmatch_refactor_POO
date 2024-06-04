# Ejercicio de migración parte 2

## Migración a objetos

### Objetivo

Incorporar el paradigma de programación orientada a objetos (OOP) y transformar la aplicación en una aplicación en
Streamlit
para favorcer la mantenibilidad del código fuente.

## Código original

* Ver el código fuente del proyecto https://github.com/shakamoushie/pixmatch/blob/main/pixmatch.py . Este proyecto tiene
  un clone del proyecto original
* Interactuar con el juego para entener las funcionalidades principales https://pixmatchgame.streamlit.app
* Instalar el proyecto en su computador local. Escriba desde la línea de comandos y ubicado en la carpeta raíz del
  proyecto `pip install -r requirements.txt`. Note que si no tiene un ambiente virtual primero debe configurarlo.
* Ejecutar el juego localmente. Escriba en consola `streamlit run docs/legacy_version/pixmatch.py`. Su navegador debería
  abrir el juego
  ![img.png](docs/img/ejecucion.png)

## Código orientado a objetos

* Este código fuente cumple las mismas funcionalidades que el código legacy pero tiene orientación a objetos
* **Análisis del código actual**
    * Compare la lógica del método ```PreNewGame``` en el código original y en el nuevo código orientado a objetos.
      Identifique como esta separada la lógica relacionada con la visualización con la lógica de negocio
    * Identifique en la versión orientada a objetos en qué puntos se controla la lectura y escritura del leaderboard.
      Considere que una restricción es que solo se escribe y se lee el leaderboard si el jugador escribe su nombre

### Por hacer

1. Agregar lógica para que si el jugador a fallado en más del 50% + 1 de las celdas el juego termine
2. Ajuste el código para que el leaderboard sea de cuatro jugadores. Observe la diferencia entre ajustarlo en el código
   anterior y en esta nueva versión de código. Note como un diseño mejorado facilita el mantenimiento
2. Agregar nueva página para que cuando se gana se muestre una página con un mensaje grande que indica que el jugador ha
   ganado y los globos. En esta página se debe mostrar el puntaje del jugador, y un botón para reiniciar un nuevo juego
   (Pagina limpia)

3. Agregar un bonus aleatorio en alguna celda del juego. Este bonus cambia de posición en cada interacción y cuando se
   descubre suma 5 puntos al puntaje del jugador. Si el bonus se descubre se le avisa al jugador y se vuelve a ubicar en
   las celdas que no han sido destapadas, siempre y cuando falten más del 20% de las celdas por destapar. El botón que
   destapó el bonus debe tener un icono que lo identifique
4. Ajustar parametrización de dificultad para poder cambiar el tamaño del tablero predefinido por dificultad
5. Ajustar parametrización inicial para activar o desactivar el autorefresco de la página. Por defecto debe estar
   desactivado
6. **RETO:** Me gustaría que los botones que muestran los emojis fueran más grandes. Esto implica interacción con html. ¿Cómo
   haría esto?

## Diagrama del proyecto

```mermaid
classDiagram
    class GameController {
        -selected_difficulty
        -current_player
        -emoji_bank
        -target_emoji
        -game_status
        -board
        -leaderboard_ranking
        +pick_emoji_bank()
        +choose_sidebar_emoji()
        +reset_board()
        +pre_new_game(selected_difficulty, player_name_country)
        +new_game()
        +verify_game_status()
        +play(cell_idx)
    }
    class GUIController {
        -game_controller
        -run_page
        -st_matrix
        +main()
        +pre_new_game_gui(selected_difficulty, player_name_country)
        +new_game_gui()
        +get_emoji_for_score()
        +get_score_and_pending_cells_values()
        +get_refresh_interval()
        +back_to_main()
    }
    class Board {
        -cells_map
        -expired_cells_list
        -board_size
        -total_cells 
        +prepare_board()
        +get_unpressed_cells()
        +count_pending_cells()
        +get_cell_by_idx()
        +add_expired_cell(cell_idx)
    }
    class BoardCell {
        -cell_idx
        -verification_result
        -row = 0
        -col = 0
        -emoji_img: string
        +BoardCell(cell_idx,row,col)
        +verify_emoji_match(target_emoji)
    }
    class LeaderBoardManager {
        -leaderboard_file_name_path
    
        +create_leader_board()
        +read_leader_board()
        +sort_leader_board_data()
        +update_leader_board(player, MAX_PLAYERS)
    }
    class Player {
        -player_name_country
        -score
        
        +Player(player_name_country)
        +get_player_info(
        +increase_score(difficulty_points)
        +decrease_score()
    }
    class MainView {
        +draw_instructions()
        +draw_main_page(gui_controller)
        +draw_new_game_board(gui_controller)
        +draw_end_game_info(gui_controller)
        +draw_lateral_bar_new_game(gui_controller)
        +reduce_gap_from_page_top(section_to_adjust)
    }
    class App {
        +main()
    }
    GUIController --> GameController : has
    Board <-- GameController : has
    Board o-- BoardCell : has
    GameController --> Player : has
    GameController ..> LeaderBoardManager : uses
    LeaderBoardManager ..> Player : uses
    MainView ..> GameController : uses
    GUIController <..> MainView : uses
    App ..> GUIController : launches
```

Editor:https://diagrams.helpful.dev/s/s:MAdFfNUs

### Diagrama de secuencia que representa la interacción cuando se da click en new game
```mermaid
sequenceDiagram
    participant GUIController as GUIController
    participant GameController as GameController
    participant Board as Board
    participant main_view as main_view

    GUIController->>GameController: pre_new_game(selected_difficulty, player_name_country)
    GameController->>GameController: selected_difficulty = DIFFICULTY_LEVELS_OPTIONS[selected_difficulty]
    GameController->>GameController: current_player = Player(player_name_country)
    GameController->>Board: board = Board(selected_difficulty['board_size'])
    GameController->>GameController: pick_emoji_bank()
    GameController->>Board: prepare_board()
    GameController->>GameController: game_status = 'ACTIVE'
    GameController->>GameController: create_leader_board()
    GUIController->>GUIController: run_page = 'new_game'
    GUIController->>GUIController: rerun()
    GUIController->>GameController: new_game()
    GameController->>GameController: reset_board()
    GameController->>GameController: read_leader_board()
    GameController->>GameController: verify_game_status()
    GUIController->>main_view: draw_new_game_board(self)
```