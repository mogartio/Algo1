from random import randint

CANTIDAD_FILAS = 4
CANTIDAD_COL = 4
NUMERO_MEZCLAS = 1000
JUEGO_PERDIDO = NUMERO_MEZCLAS * 5
ARRIBA = 'W'
ABAJO = 'S'
IZQUIERDA = 'A'
DERECHA = 'D'
TECLA_SALIR = 'O'
MOVIMIENTOS = (ARRIBA, ABAJO, IZQUIERDA, DERECHA)
TECLAS_VALIDAS = (ARRIBA, ABAJO, IZQUIERDA, DERECHA, TECLA_SALIR)
DIRECCION = ((ARRIBA,1,0), (ABAJO,-1,0), (IZQUIERDA,0,1), (DERECHA,0,-1))


def inicializar_tablero(filas, columnas):
	"""Recibe dos números enterosque representan la cantidad de filas y columnas respectivamente. Devuelve una lista que contiene la misma 
	cantidad de listas adentro suyo que el valor "filas"le pasamos, a la vez estas listas van a estar compuestas por una cantidad de elementos
	igual al valor "columnas" que le pasamos. """
	
	tablero = [[1 + j + i * CANTIDAD_COL for j in range(CANTIDAD_COL)] for i in range(CANTIDAD_FILAS)]			
	return mezclar_tablero(tablero)



def mezclar_tablero(tablero):

	"""Recibe una lista que representa un tablero con una cantidad predefinida de filas y columnas.Luego de haber
		intercambiado sus elementos una cantidad predeterminada de veces de forma tal que el tablero resultante pueda ser utilizado
		 en el juego Fifteen, se devuelve la lista y se imprime su informacion por pantalla"""
	
	for i in range(NUMERO_MEZCLAS):

		movimiento = MOVIMIENTOS[randint(0, 3)]
		while not es_movimiento_valido(tablero,movimiento):
			movimiento = MOVIMIENTOS[randint(0, 3)]
		hacer_movimiento(tablero, movimiento)

	imprimir_tablero(tablero, 0)
	return tablero

def	imprimir_tablero(tablero, contador_movimientos):
	"""Recibe el tablero junto a un numero entera que representa cuantos movimientos se han realizado en el transcurso del juego.
	La función imprime la información del juego por pantalla """

	print(f"\nCONTROLES : {ARRIBA},{ABAJO},{IZQUIERDA},{DERECHA} \nSALIR : {TECLA_SALIR} \nSE HAN REALIZADO {contador_movimientos} MOVIMIENTOS")

	for i in range (CANTIDAD_FILAS):	
		for j in range (CANTIDAD_COL):
			if tablero[i][j] == CANTIDAD_COL * CANTIDAD_FILAS:
				print(" ", end= "	|")
			else:
				print(tablero[i][j], end= "	|")
		print()



def buscar_vacio(tablero):
	"""Recibe al tablero y devuelve dos numeros enteros que representan las coordenadas del casillero vacío del tablero """

	for i in range(CANTIDAD_FILAS):
		for j in range(CANTIDAD_COL):
			if tablero[i][j] == CANTIDAD_COL * CANTIDAD_FILAS:
				return i,j


	
def es_movimiento_valido(tablero, movimiento):
	"""Recibe la lista que representa al tablero y un caracter que representa el movimiento que se quiere realizar.
		Se devuelve True si dicho movimiento es compatible con el tablero recibido según las reglas del Fifteen 
		se devuelve False de no ser así"""
	
	coordenada = buscar_vacio(tablero)
	borde = (CANTIDAD_FILAS, CANTIDAD_COL)

	for i in range(4):
		if movimiento in DIRECCION[i]:
			if (coordenada[0] + DIRECCION[i][1]) % borde[0] != coordenada[0] + DIRECCION[i][1]:
				return False
			elif (coordenada[1] + DIRECCION[i][2]) % borde[1] != coordenada[1] + DIRECCION[i][2]:
				return False
	return True


def hacer_movimiento(tablero,movimiento):

	"""Recibe la lista que representa al tablero y un caracter que representa un movimiento que debe ser compatible con dicho tablero 
		según las reglas del juego. Se muta la lista de forma tal que se intercambian las coordenadas del casillero vacío con otro elemento de 
		coordenadas adyacentes.	"""

	fila_actual, col_actual = buscar_vacio(tablero)[0], buscar_vacio(tablero)[1]

	for i in range(4):
		if movimiento in DIRECCION[i]:
			tablero[fila_actual][col_actual], tablero[fila_actual + DIRECCION[i][1]][col_actual + DIRECCION[i][2]] = (  
				tablero[fila_actual + DIRECCION[i][1]][col_actual + DIRECCION[i][2]], tablero[fila_actual][col_actual])

def esta_ganado(tablero):
	"""Recibe el tablero y devuelve True si está ordenado de menor a mayor y False de no ser así"""

	for i in range(CANTIDAD_FILAS):
		for j in range(CANTIDAD_COL - 1):
			if tablero[i][j] > tablero[i][j+1]:
				return False
		if i != CANTIDAD_FILAS - 1 and tablero[i][0] > tablero[i+1][0]:
			return False
	return True



