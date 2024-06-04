# Cambios realizados
Aqui profundizo en que cambios hice para tener control ya que es un señor programa.

## Agregar lógica para que si el jugador a fallado en más del 50% + 1 de las celdas el juego termine
### Archivo game_controller.py
```python
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
```
Aqui el cambio que se realizo fue añadir una pareja de variables para determinar el numero maximo de errores
y otra para obtener la cantidad actual de errores al momento de invocar al metodo, en caso de que se cumpla el
criterio de perder, se asigna el estado de 'LOOSE' y pues ocurre normal la logica de perder.


## Ajuste el código para que el leaderboard sea de cuatro jugadores
### Archivo leaderboard_manager.py
Aqui cambie la logica en mayor medida, ya que ahora cuando el leadeboard esta lleno (4 players) verifico que el puntaje
del player actual sea mayor que el mas bajo del leaderboard, en caso tal pues elimino al mas bajo y meto al nuevo al leaderboard
Sin embargo hay un pequeñito bug que el emoticon de cada posicion del leaderboard es una medalla de oro, pero en el fondo
no somos todos ganadores de experiencia? para reflexionar.

```python
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
```

### Archivo settings.py
Se modifico la constante de maxima cantidad de jugadores en el leaderboard para que sea igual a 4 (Antes era 5)
```python
MAX_LEADERBOARD_PLAYERS = 4  # Settings
```

# Agregar nueva página para que cuando se gana se muestre una página con un mensaje grande que indica que el jugador ha ganado y los globos...
### Archivo gui_controller.py
Se creo una nueva funcion para la pagina nueva de victoria, no tiene nada de especial
```python
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
```

### Archivo main_view.py
Se modifico este archivo para que cuando se gane el juego se llame a la funcion que pinta la pantalla de victoria
```python
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

```
# Agregar un bonus aleatorio en alguna celda del juego
Dios como odie esta...
### Archivo gui_controller.py
```python
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

```
Tambien cree otras dos funciones para manejar lo del bonus
```python
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
```
Segun yo funciona

# Ajustar parametrización de dificultad para poder cambiar el tamaño del tablero predefinido por dificultad
Este me costo

### Archivo game_controller.py
Modifique el metodo pre_new_game para que ahora reciba un parametro mas, este parametro sera para posteriormente elegir
el tamaño del tablero, independiente de la dificultad.
```python
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
```
### Archivo gui_controller.py
Se añade el parametro al metodo:
```python
    def pre_new_game_gui(self, selected_difficulty, player_name_country, board_size_option):
        # Inicializa el tablero
        self.game_controller.pre_new_game(selected_difficulty, player_name_country, board_size_option)
        # Actualiza la página a la vista del tablero de juego
        st.session_state.my_state.run_page = 'new_game'
        # Al haber puesto el estado como 'new_game' y volver a correr el codigo ahora en main se ejecuta otra situacion
        st.rerun()
```
### Archivo "main_view.py"
Aqui se modifico la barra lateral para añadir el seleccionador de tamaños.
```python
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

        # Entrada para el nombre del jugador y el país
        player_name_country = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                            help='Optional input only for Leaderboard')
        # Botón para iniciar un nuevo juego
        if st.button(f"🕹️ New Game", use_container_width=True):
            gui_controller.pre_new_game_gui(selected_difficulty, player_name_country, board_size_options)

        st.markdown(HORIZONTAL_BAR_HTML_TEMPLATE, True)  # Barra decorativa horizontal

```
Y creo que eso fue todo, espero...

# Ajustar parametrización inicial para activar o desactivar el autorefresco de la página
No entiendo este del todo, pero vamos a ver que me dice copilot al respecto.

5 min despues...

Pues segun entiendo se refiere como al dinamismo de la pagina? que no se actualice sola, no entiendo del todo pero voy a
hacerlo, no se ve tan complejo.

### Archivo main_view.py
Añadi otro elemento, un checkbox para el tema del autorefresco, y lo paso como parametro
```python
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
```

### Archivo gui_controller.py
Aqui añado otro parametro al pre_new_game_gui para manejar lo del autorefresh.

```python
    def pre_new_game_gui(self, selected_difficulty, player_name_country, board_size_option, autorefresh_option):
        # Inicializa el tablero
        self.game_controller.pre_new_game(selected_difficulty, player_name_country, board_size_option)
        # Actualiza la página a la vista del tablero de juego
        st.session_state.my_state.run_page = 'new_game'
        # Al haber puesto el estado como 'new_game' y volver a correr el codigo ahora en main se ejecuta otra situacion
        st.rerun()
        # Guarda el estado del autorefrescamiento en la sesión
        st.session_state.my_state.autorefresh_option = autorefresh_option
```
Tambien se modifica el metodo de new_game_gui:
```python
    def new_game_gui(self):
        # Dibuja las columnas de juego en streamlit
        self.initialize_columns()
        cell_cont = 0

        # Agrega los botones a las columnas segun corresponda en el juego
        for row in range(self.game_controller.board.board_size):
            st_row_to_draw = self.st_matrix[row]
            for col in range(self.game_controller.board.board_size):
                cell_to_draw = self.game_controller.board.cells_map[cell_cont]
                st_cell_to_draw = st_row_to_draw[col].empty()
                # Aqui empieza el juego... el resto es pintar y preparar variables
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

        # Verificar si el autorefrescamiento está habilitado
        if st.session_state.my_state.autorefresh_option:
            # Lógica para autorefrescar la página y cambiar el score si pasado un tiempo no se ha seleccionado nada
            self.autorefresh_page()

```
Y naturalmente añadi el nuevo elemento del mystate, aunque no estoy seguro si esta funcionando del todo... no se si era 
este el requerimiento.

```python
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

```