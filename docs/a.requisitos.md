## Requisitos Funcionales y Criterios de Aceptación

## Requisitos Funcionales y Criterios de Aceptación

### 1. Configuración de Nivel de Dificultad

**Requisito:** El sistema debe permitir a los jugadores seleccionar el nivel de dificultad antes de comenzar el juego.

**Criterios de Aceptación:**

- Opciones de dificultad fácil, medio y difícil disponibles para selección.
- La configuración de dificultad debe influir en la mecánica del juego, como la frecuencia de regeneración de imágenes y
  la puntuación.
- Tiempos de regeneración específicos:
    - Fácil: cada 8 segundos.
    - Medio: cada 6 segundos.
    - Difícil: cada 5 segundos.

### 2. Inicialización del Tablero

**Requisito:** Al comenzar un juego, el sistema debe inicializar el tablero con un conjunto aleatorio de imágenes basado
en la dificultad seleccionada.

**Criterios de Aceptación:**

- El tablero debe ser llenado con imágenes de emojis que corresponden a la dificultad elegida.
- La imagen objetivo debe ser seleccionada aleatoriamente y mostrada en la barra lateral.

### 3. Parametrización del Nombre del Jugador y País

**Requisito:** El sistema debe permitir a los jugadores ingresar su nombre y país antes de comenzar el juego.

**Criterios de Aceptación:**

- Debe existir un campo de texto para que los jugadores ingresen su nombre y país.
- Es posible que los campos de nombre y país estén vacíos, pero en ese caso no se muestra el _Leaderboard_
- La información del jugador debe persistir durante la sesión de juego.

### 4. Visualización de Instrucciones del Juego

**Requisito:** El sistema debe proporcionar una sección donde los jugadores puedan leer las instrucciones del juego
antes de comenzar a jugar.

**Criterios de Aceptación:**

- Debe existir una opción para que los jugadores seleccionen y vean las instrucciones del juego.
- Las instrucciones deben cubrir aspectos esenciales del juego como las reglas y cómo se juega.
- Las instrucciones deben ser visibles sin interferir con la interfaz principal del juego.

### 5. Interfaz de Usuario y Visualización de Componentes

**Requisito:** La interfaz de usuario debe mostrar todos los componentes necesarios para jugar.
****
**Criterios de Aceptación:**

- El tablero de juego, las opciones de juego y la barra lateral deben estar visibles.
- Los botones y opciones de juego deben esta disponibles

### 6. Gestión de Puntaje y Validación de Respuestas

**Requisito:** El sistema debe actualizar el puntaje del jugador en tiempo real basándose en las selecciones correctas o
incorrectas.

**Criterios de Aceptación:**

- Incremento de puntaje para respuestas correctas según la dificultad.
- Decremento de puntaje por respuestas incorrectas.
- Casillas seleccionadas no deben ser reutilizables.
- Al seleccionar correctamente una figura, debe mostrarse un indicador visual positivo, como un color verde o un icono
  de verificación.
- Al seleccionar incorrectamente, debe mostrarse un indicador visual negativo, como un color rojo o un icono de cruz.

### 7. Registro y Visualización del Leaderboard

**Requisito:** El sistema debe registrar y mostrar un leaderboard con los puntajes más altos.

**Criterios de Aceptación:**

- El leaderboard debe actualizarse con el nombre del jugador y el puntaje.
- Solo los tres mejores puntajes deben ser visibles.
- Los puntajes deben ser persistentes entre sesiones de juego.

### 8. Regeneración Automática de Imágenes Objetivo

**Requisito:** Las imágenes objetivo deben regenerarse automáticamente en intervalos específicos.

**Criterios de Aceptación:**

- La regeneración automática debe ocurrir en los intervalos definidos.
- Cada regeneración debe ajustarse a la dificultad del juego.
- La regeneración debe penalizar el puntaje del jugador como respuesta fallida, si el jugador no ha seleccionado ninguna
  imagen.

### 9. Funcionalidad de Reinicio de Juego

**Requisito:** Debe haber una opción para reiniciar el juego.

**Criterios de Aceptación:**

- Un botón de reinicio debe estar visible y funcionar correctamente.
- Al presionar el botón de reinicio, el estado del juego debe volver a su estado inicial.
- Debe ser posible reiniciar la configuración de dificultad y otros ajustes.

## Diagrama de flujo

![diagrama_flujo.png](img%2Fdiagrama_flujo.png)

## Inventario de funciones actuales

- **`ReduceGapFromPageTop(wch_section = 'main page')`**: Esta función se utiliza para reducir el espacio desde la parte
  superior de la página.
- **`Leaderboard(what_to_do)`**: Esta función se utiliza para manejar las operaciones de la tabla de líderes, como
  crear, leer y escribir.
- **`InitialPage()`**: Esta función se utiliza para configurar y mostrar la página inicial del juego.
- **`ReadPictureFile(wch_fl)`**: Esta función se utiliza para leer un archivo de imagen.
- **`PressedCheck(vcell)`**: Esta función se utiliza para verificar si un botón ha sido presionado y realizar las
  acciones correspondientes.
- **`ResetBoard()`**: Esta función se utiliza para restablecer el tablero del juego a su estado inicial.
- **`PreNewGame()`**: Esta función se utiliza para preparar el estado inicial del juego antes de comenzar un nuevo
  juego.
- **`score_emoji()`**: Esta función se utiliza para determinar el emoji de la puntuación que se mostrará en la barra
  lateral.
- **`NewGame()`**: Esta función se utiliza para iniciar un nuevo juego, configurar el tablero del juego y manejar la
  lógica del juego.
- **`Main()`**: Esta es la función principal que se ejecuta al inicio del programa. Se encarga de configurar la interfaz
  de usuario y mostrar la página inicial.