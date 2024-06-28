from logica import *

def main():

	contador_movimientos = 0
	tablero = inicializar_tablero(CANTIDAD_FILAS, CANTIDAD_COL)


	while contador_movimientos < JUEGO_PERDIDO and not esta_ganado(tablero):
		movimientos = input("POR FAVOR INGRESAR UN MOVIMIENTO VALIDO: ")
		movimientos = movimientos.upper()

		if TECLA_SALIR in movimientos:
			break

		for movimiento in (movimientos):
			
			if es_movimiento_valido(tablero, movimiento):
				hacer_movimiento(tablero, movimiento)
				contador_movimientos += 1
		
			else:
				print(f"\nEL MOVIMIENTO INGRESADO NO ES VALIDO.\n\nPOR FAVOR INGRESE UN MOVIMIENTO VALIDO : {ARRIBA},{ABAJO},{IZQUIERDA},{DERECHA} ")
				
		imprimir_tablero(tablero, contador_movimientos)

	if esta_ganado(tablero):
		print("EL JUEGO HA SIDO VENCIDO, SOS UNA PERSONA INGENIOSA Y PERSEVERANTE.")

	else:
		print("EL JUEGO TE HA DERROTADO, QUE VERGONZOSO...")

main()


