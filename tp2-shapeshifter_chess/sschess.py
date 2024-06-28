import gamelib
from random import randint, choice
import csv


CANTIDAD_COL = 8
CANTIDAD_FILAS = 8
PIEZAS = ('caballo', 'alfil', 'torre')
IMAGENES = ('img/caballo_blanco.gif', 'img/alfil_blanco.gif', 'img/torre_blanco.gif','img/caballo_rojo.gif', 'img/alfil_rojo.gif', 'img/torre_rojo.gif')
TECLA_ACEPTAR = 's'
TECLA_RECHAZAR = 'n'
TECLA_REINTENTAR = 'r'
JUEGO_NUEVO = 1

ALTO_VENTANA = 675
ANCHO_VENTANA = 600
ALTO_CASILLERO = 75
ANCHO_CASILLERO = 75
CUARTO_ANCHO_VENTANA = ANCHO_VENTANA // 4
CUARTO_ALTO_VENTANA = (ALTO_VENTANA - ALTO_CASILLERO) // 4
CENTRADO_IMAGEN = ANCHO_CASILLERO // 5

ALTO_IMG_FISCHER = 299
ANCHO_IMG_FISCHER = 480
MITAD_IMG_FISCHER_DOS = 123

POSICION_TEXTO_UNO = 125
POSICION_TEXTO_DOS = 500


def juego_empezar(diccionario_movimientos):
    """Se encarga de dibujar la pantalla inicial del juego y preguntarle al usuario si desea cargar una partida antigua, o empezar un juego nuevo.
    Si el usuario elige cargar una partida pero no se encuentra ninguna partida guardada, se envía un mensaje de error. Se devuelve el tablero, la pieza inicial
    junto a su posicion en el tablero, el diccionario y el numero de nivel actual. Estos serán creados desde 0 si el usuario decide empezar un juego nuevo
    y serán cargados desde un archivo si se elijió seguir una partida vieja """
    while gamelib.is_alive():
        gamelib.draw_begin()
        gamelib.draw_image('img/fischer.gif', ANCHO_VENTANA  // 2 - ANCHO_IMG_FISCHER, 0)
        gamelib.draw_image('img/fischer2.gif', MITAD_IMG_FISCHER_DOS, ALTO_IMG_FISCHER)
        gamelib.draw_text('SHAPE SHIFTER \n       CHESS!', 3 * CUARTO_ANCHO_VENTANA, CUARTO_ALTO_VENTANA , size=25, fill='purple')
        gamelib.draw_text(f' CARGAR\nPARTIDA? \n      {TECLA_ACEPTAR}/{TECLA_RECHAZAR}', CUARTO_ANCHO_VENTANA, 3 * CUARTO_ALTO_VENTANA, size=25, fill='purple')
        gamelib.draw_rectangle(0, ANCHO_VENTANA, ALTO_VENTANA - ALTO_CASILLERO, ALTO_VENTANA, outline='blue', width=3,  fill='blue')
        gamelib.draw_text('created by: martin_games', ANCHO_VENTANA // 2, ALTO_VENTANA - ALTO_CASILLERO // 2, size=20, fill='red')
        gamelib.draw_end()
        ev = gamelib.wait()
        ev.type == gamelib.EventType.KeyPress
        if ev.key.lower() == TECLA_RECHAZAR:  
            tablero, col, fila, pieza_inicial = juego_nuevo(JUEGO_NUEVO, diccionario_movimientos)
            return tablero, col, fila, pieza_inicial, JUEGO_NUEVO
        elif ev.key.lower() == TECLA_ACEPTAR:
            try:
                tablero, col, fila, pieza_inicial, n_nivel = cargar_juego()
                return tablero, col, fila, pieza_inicial, n_nivel
            except FileNotFoundError:
                gamelib.say("No hay ninguna partida guardada")
        


def crear_diccionario_movimientos():
    """Se devuelve un diccionario cuyas claves serán los nombres de las piezas del juego y los valores serán listas de movimientos representados como
    tuplas de acuerdo con el reglamento del ajedrez tradicional """

    diccionario_movimientos = {}
    with open('movimientos.csv') as f:
        for linea in f:
            campos = linea.rstrip().split(',')
            pieza = campos[0]
            dx, dy = map(int, campos[1].rstrip().split(';'))
            extensible = campos[2]
            diccionario_movimientos[pieza] = diccionario_movimientos.get(pieza, [])
            if extensible == 'true':
                for i in range(CANTIDAD_FILAS):
                    diccionario_movimientos[pieza].append((dx * (i + 1), dy * (i + 1)))           
            else:
                diccionario_movimientos[pieza].append((dx, dy)) 
        return diccionario_movimientos


def modificar_tablero(tablero, fila, col, pieza_inicial, diccionario_movimientos):
    """Se recibe una pieza junto a sus coordenadas, el tablero en el cual esta posicionada y un diccionario con los movimientos de las piezas.
        Esta función se encarga de elegir un movimiento al azar de la lista de movimientos perteneciente a la pieza recibida. Si el movimiento
        es legal se inserta una pieza aleatoria en el casillero donde iría a parar la pieza inicial si hiciera el movimiento elegido antes.
        Se devuelve el tablero con la nueva pieza, junto a la posicion de esta misma.  """
    while True:
        direccion = choice(diccionario_movimientos[pieza_inicial])
        fila_nueva = fila + direccion[1]
        col_nueva =  col + direccion[0]
        if not(col_nueva in range(CANTIDAD_COL) and fila_nueva in range(CANTIDAD_FILAS) and tablero[fila_nueva][col_nueva] not in PIEZAS):
            continue
        pieza_nueva = choice(PIEZAS)
        tablero[fila_nueva][col_nueva] = pieza_nueva
        return tablero, fila_nueva, col_nueva, pieza_nueva

 
def juego_mostrar(tablero, col, fila, casillas_posibles, nivel):
    '''dibuja la interfaz de la aplicación en la ventana'''
    gamelib.draw_begin()
    gamelib.draw_text('SHAPE SHIFTER \n       CHESS!', POSICION_TEXTO_UNO, ALTO_CASILLERO // 2, size=15, fill='purple')
    gamelib.draw_text('REINTENTAR: \n         "R"', POSICION_TEXTO_DOS, ALTO_CASILLERO // 2, size=15, fill='purple')
    gamelib.draw_text(f'NIVEL \n    {nivel}', ANCHO_VENTANA // 2, ALTO_CASILLERO // 2, size=15, fill='green')
    for i in range(1, CANTIDAD_COL):
        gamelib.draw_line(ANCHO_CASILLERO * i, ALTO_CASILLERO, ANCHO_CASILLERO * i, ALTO_VENTANA, fill='blue', width=2)
    for i in range(0, CANTIDAD_FILAS ):
        gamelib.draw_line(0, ALTO_CASILLERO * (i + 1), ANCHO_VENTANA , ALTO_CASILLERO * (i + 1), fill='blue', width=2)
    for i in range(CANTIDAD_FILAS):
        for j in range(CANTIDAD_COL):
            if (i, j) in casillas_posibles:
                gamelib.draw_rectangle(j * ANCHO_CASILLERO, ALTO_CASILLERO * (i + 1), ANCHO_CASILLERO * (j + 1), ALTO_CASILLERO * (i + 2), outline='red', width=3,  fill='')
            if tablero[i][j] in PIEZAS:
                if i == fila and j == col:
                    gamelib.draw_image(IMAGENES[PIEZAS.index(tablero[i][j]) + len(PIEZAS)], ANCHO_CASILLERO * j + CENTRADO_IMAGEN, ALTO_CASILLERO * (i + 1) + CENTRADO_IMAGEN)
                else:
                    gamelib.draw_image(IMAGENES[PIEZAS.index(tablero[i][j])], ANCHO_CASILLERO * j + CENTRADO_IMAGEN, ALTO_CASILLERO * (i + 1) + CENTRADO_IMAGEN)
    gamelib.draw_end()

def guardar_juego(tablero, col, fila, n_nivel):
    """Se escribe un archivo csv con la información del nivel actual """
    with open('partida_guardada.txt' , "w") as f:
        f.write(str(n_nivel) + "\n")
        for i in range(CANTIDAD_FILAS):
            info_fila = []
            for j in range(CANTIDAD_COL):
                info_fila.append(str(tablero[i][j]))
            f.write( ','.join(info_fila) + "\n")
        f.write(f"{col} , {fila}")

def cargar_juego():
    """Se lee un archivo csv con la información del último nivel jugado. Se procesa esta información y se devuelve el tablero, la pieza inicial 
    junto a su posicion y el numero del nivel que se cargó """
    tablero = []
    with open('partida_guardada.txt' , "r") as f:
        reader = csv.reader(f)
        n_nivel = next(reader)
        for linea in f:
            filas = []
            campos = linea.rstrip().split(',')
            for elementos in campos:
                filas.append(elementos)
            tablero.append(filas)
        col, fila = int(campos[0]), int(campos[1])
    return tablero, col, fila, tablero[fila][col], int(n_nivel[0])

def obtener_movimientos_disponibles(tablero, col, fila, pieza_actual, diccionario_movimientos):
    """Se recibe la pieza inicial, junto a su posición, el tablero del nivel actual y el diccionario que contiene sus movimientos.
    Se devuelve una lista de tuplas que contiene los casilleros del tablero (ocupados por otra pieza) a los que la pieza inicial podría moobtenerse """
    
    casillas_posibles = []
    coordenadas_marcadas = []
    for i in range(len(diccionario_movimientos[pieza_actual])):
        nueva_coordenada = (fila + diccionario_movimientos[pieza_actual][i][1], col + diccionario_movimientos[pieza_actual][i][0])
        casillas_posibles.append(nueva_coordenada)
    for i in range(CANTIDAD_FILAS):
        for j in range(CANTIDAD_COL):
            if (i,j) in casillas_posibles and tablero[i][j] in PIEZAS:
                coordenadas_marcadas.append((i, j))
    return coordenadas_marcadas


def juego_nuevo(n_nivel, diccionario_movimientos):
    '''inicializa el estado del juego para el numero de nivel dado'''
    tablero = [["" for j in range(CANTIDAD_COL)] for i in range(CANTIDAD_FILAS)] 
    col = randint(0, CANTIDAD_COL - 1 )
    fila = randint(0, CANTIDAD_FILAS - 1)
    tablero[fila][col] = choice(PIEZAS)
    col_nueva, fila_nueva, pieza_nueva = col, fila, tablero[fila][col]
    for i in range(n_nivel + 1):
        tablero, fila_nueva,col_nueva, pieza_nueva = modificar_tablero(tablero, fila_nueva, col_nueva, pieza_nueva, diccionario_movimientos)   
    guardar_juego(tablero, col, fila, n_nivel)
    return tablero, col, fila, tablero[fila][col]

def main():
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    diccionario_movimientos = crear_diccionario_movimientos()
    tablero, col, fila, pieza_actual, n_nivel = juego_empezar(diccionario_movimientos)
    while gamelib.is_alive():
        casillas_posibles = obtener_movimientos_disponibles(tablero, col, fila, pieza_actual, diccionario_movimientos)
        juego_mostrar(tablero, col, fila, casillas_posibles,n_nivel)
        contador_piezas = 0
        for i in range(CANTIDAD_FILAS):
                    for j in range(CANTIDAD_COL):
                        if tablero[i][j] in PIEZAS:
                            contador_piezas += 1
        if contador_piezas == 1:
            n_nivel += 1
            tablero, col, fila, pieza_actual= juego_nuevo(n_nivel, diccionario_movimientos)
        ev = gamelib.wait()
        if not ev:
            break
        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            click_x = ev.x // ANCHO_CASILLERO
            click_y = ev.y // ALTO_CASILLERO - 1
            if (click_y,click_x) in casillas_posibles:
                tablero[fila][col] = 0
                fila, col = click_y, click_x
                pieza_actual = tablero[fila][col]           
        elif ev.type == gamelib.EventType.KeyPress and ev.key.lower() == TECLA_REINTENTAR:
            tablero, col, fila, pieza_actual, n_nivel = cargar_juego()
            casillas_posibles = obtener_movimientos_disponibles(tablero, col, fila, pieza_actual, diccionario_movimientos)
            juego_mostrar(tablero, col, fila, casillas_posibles, n_nivel)

gamelib.init(main)