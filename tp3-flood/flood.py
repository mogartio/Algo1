from random import randint

DIRECCIONES = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla.
        """
        self.tablero = [[0 for j in range(ancho)] for i in range(alto)]
        self.alto = alto
        self.ancho = ancho
        self.lista_casillas_iguales = []
       
    def mezclar_tablero(self, n_colores):
        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Argumentos:
            n_colores (int): Cantidad maxima de colores a incluir en la grilla.
        """
        alto, ancho = self.dimensiones()
        self.tablero = [[randint(0, n_colores - 1)for j in range(ancho)]for i in range(ancho)]

    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.

        Devuelve:
            Color asignado.
        """
        return self.tablero[fil][col]

    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.
        La secuencia tendrá todos los colores posibles que fueron utilizados
        para generar el tablero, sin importar cuántos de estos colores queden
        actualmente en el tablero.

        Devuelve:
            iterable: secuencia ordenada de colores.
        """
        alto, ancho = self.dimensiones()
        tablero = self.tablero
        colores_posibles = []
        for i in range(alto):
            for j in range(ancho):
                if tablero[i][j] not in colores_posibles:
                    colores_posibles.append(tablero[i][j])
        return colores_posibles

    def dimensiones(self):
        """
        Dimensiones de la grilla (filas y columnas)

        Devuelve:
            (int, int): alto y ancho de la grilla en ese orden.
        """
        return (self.alto, self.ancho)

    def es_coordenada_valida(self, dy, dx):
        """
        Recibe dos int que representan coordenadas. Se devuelve True si dichas coordenadas estan dentro del tablero y False de no ser así
        """

        return dy in range(0, self.alto) and dx in range(0, self.ancho)
        

    def cambiar_color(self, color_nuevo, dy, dx):
        """
        Asigna el nuevo color al Flood de la grilla. Es decir, a todas las
        coordenadas que formen un camino continuo del mismo color comenzando
        desde la coordenada origen en (0, 0) se les asignará `color_nuevo`

        Argumentos:
            color_nuevo: Valor del nuevo color a asignar al Flood.
        """
        alto, ancho = self.dimensiones()
        color_viejo = self.obtener_color(dy, dx)
        tablero = self.tablero
        while True:
            if color_nuevo == color_viejo:
                break
            tablero[dy][dx] = color_nuevo
            for direcccion in DIRECCIONES:
                dx_nueva = dx + direcccion[0]
                dy_nueva = dy + direcccion[1]
                if not self.es_coordenada_valida(dy_nueva, dx_nueva):
                    continue
                if tablero[dy_nueva][dx_nueva] == color_viejo:
                    self.cambiar_color(color_nuevo, dy_nueva, dx_nueva)
            return 

    def clonar(self):
        """
        Devuelve:
            Flood: Copia del Flood actual
        """
        clon_flood = Flood(
        alto = self.alto,
        ancho = self.ancho
            )
        tablero = [[self.tablero[i][j] for j in range(self.ancho)]for i in range(self.alto)]
        clon_flood.tablero = tablero
        return clon_flood

    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color

        Devuelve:
            bool: True si toda la grilla tiene el mismo color
        """
        # Parte 4: Tu código acá...
        color_inicial = self.obtener_color(0, 0)
        alto, ancho = self.dimensiones()
        for i in range(alto):
            for j in range(ancho):
                if self.tablero[i][j] != color_inicial:
                    return False
        return True

    def calcular_bloques_transformados(self, color_inicial, dy, dx):
        """
        Se modifica el atributo lista_casillas_iguales, que indica cuantas casillas conectadas a la casilla en (0, 0) son del mismo color que esta.
        """
        alto, ancho = self.dimensiones()
        tablero = self.tablero
        self.cambiar_color(color_inicial, 0, 0)
        while True:
            if (dy, dx) not in self.lista_casillas_iguales:
                self.lista_casillas_iguales.append((dy, dx))
            for direcccion in DIRECCIONES:
                dx_nueva = dx + direcccion[0]
                dy_nueva = dy + direcccion[1]
                if not self.es_coordenada_valida(dy_nueva, dx_nueva):
                    continue
                if tablero[dy_nueva][dx_nueva] == color_inicial and (dy_nueva, dx_nueva) not in self.lista_casillas_iguales:
                    self.calcular_bloques_transformados(color_inicial, dy_nueva, dx_nueva)
            return 
    
    def colores_a_comparar(self):
        """
        Se devuelve una lista que contiene los colores que todavía están presentes en el tablero
        """
        colores_posibles = self.obtener_posibles_colores()
        alto, ancho = self.dimensiones()
        tablero = self.tablero
        colores_a_comparar = []
        for color in colores_posibles:
            for i in range(alto):
                if color in colores_a_comparar:
                        break
                for j in range(ancho):
                    if color in colores_a_comparar:
                        break
                    if tablero[i][j] in colores_posibles and tablero[i][j]:
                        colores_a_comparar.append(color)
                        break
        return colores_a_comparar

    def comparar_colores(self):
        """
        Se fija cuales son los colores que todavía pertenecen al tablero, para cada uno de esos colores se fija en la posición actual para 
        cual de estos colores el atributo lista_casillas_iguales tiene más elementos y devuelve dicho color
        """
        color_optimo = 0
        maximas_casillas = 0
        colores_a_comparar = self.colores_a_comparar()
        for color in colores_a_comparar:
            clon_flood = self.clonar()
            clon_flood.calcular_bloques_transformados(color, 0, 0)
            if len(clon_flood.lista_casillas_iguales) > maximas_casillas:
                color_optimo = color
                maximas_casillas = len(clon_flood.lista_casillas_iguales)
        return color_optimo