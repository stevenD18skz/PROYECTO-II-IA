import copy
import math
import os
import random
import time
from collections import deque



class jugador:
    def __init__(self, nombre, representacion, profundidad):
        self.nombre = nombre
        self.score = 0
        self.bono = False
        self.representacion = representacion

        self.datos_ia = {
            "facil": [3, "f"],
            "media": [5, "m"],
            "avanzada": [7, "v"]
        }
        self.datos_inteligencia = self.datos_ia[profundidad]


    
    def setScore(self, new_score):
        if self.bono:
            self.score += new_score * 2
            self.bono = False
        
        else:
            self.score += new_score * 1



    # Método para clonar el jugador
    def clone(self):
        new_player = jugador(self.nombre, self.representacion)
        new_player.score = self.score
        new_player.bono = self.bono
        return new_player



    def __str__(self):
        return f"Jugador: {self.nombre}, Puntuación: {self.score}, Bono: {"X2" if self.bono else "X1"}, Nivel IA {self.datos_inteligencia[1]}"
    
    

    def set_difficulty(self, dif):
        self.datos_inteligencia = self.datos_ia[dif]






class Game:
    def __init__(self):
        #MAQUINA JUGADOR
        self.player = jugador("STEVEN", "HB", "media")
        self.maquina = jugador("MACHINE", "HW", "media")
        self.turno = self.maquina


        #ATRIBUTOS ENTORNO
        self.tablero = self.generate_grid()
        self.tablero = [
            [   0,    0, 0, 0, 0,  0,    0, 0],
            [   0, 0, 0, 0, 0,  0,    0,    0],
            [   0,    0, 0, 'HB', 0,  0,    0,    0],
            [   4,    0, 0, 0, 0,  0, 0,    0],
            [   0,    0, 0, 0, 0,  0,    0,    0],
            [   3,    0, 0,     0, 'HW', 0,   0,    0],
            [   0,    0, 0,     0, 0,  0,    0,    0],
            [0,    0, 0, 0,  0,  0,    0,    9],
        ]
        self.directions = [
            ("L arriba derecha", -2, 1),  # Dos hacia atrás, una a la derecha
            ("L derecha arriba", -1, 2),  # Una hacia atrás, dos a la derecha
            ("L derecha abajo", 1, 2),  # Una hacia adelante, dos a la derecha
            ("L abajo derecha", 2, 1),  # Dos hacia adelante, una a la derecha
            ("L abajo izquierda", 2, -1),  # Dos hacia adelante, una a la izquierda
            ("L izquierda abajo", 1, -2),  # Una hacia adelante, dos a la izquierda
            ("L izquierda arriba", -1, -2),  # Una hacia atrás, dos a la izquierda
            ("L arriba izquierda", -2, -1),  # Dos hacia atrás, una a la izquierda
        ]



        #ATRIBUTOS JUEGO
        self.alert = ""
        self.winner = None


        #OPTIMIZACION
        self.avalibe_points = 10
        self.positions_horse = {
            self.player.representacion:  self.find_position(self.player.representacion),
            self.maquina.representacion: self.find_position(self.maquina.representacion)
        }




    def generate_grid(self):
        # Crear un tablero vacío de 8x8
        grid = [[0 for _ in range(8)] for _ in range(8)]
        
        # Generar posiciones aleatorias para las 10 casillas de puntos (de 1 a 10)
        points = list(range(1, 11))
        random.shuffle(points)
        
        # Colocar las casillas con puntos en el tablero
        for point in points:
            while True:
                x, y = random.randint(0, 7), random.randint(0, 7)
                if grid[x][y] == 0:
                    grid[x][y] = point
                    break
        
        # Generar posiciones aleatorias para los 4 símbolos x2
        for _ in range(4):
            while True:
                x, y = random.randint(0, 7), random.randint(0, 7)
                if grid[x][y] == 0:
                    grid[x][y] = "x2"
                    break
        
        # Generar posiciones aleatorias para los caballos de maquina y player
        for horse in [self.maquina.representacion, self.player.representacion]:
            while True:
                x, y = random.randint(0, 7), random.randint(0, 7)
                if grid[x][y] == 0:
                    grid[x][y] = horse
                    break
        
        
        return grid





    def find_position(self, object_value):
        for x, row in enumerate(self.tablero):
            for y, value in enumerate(row):
                if value == object_value:
                    return (x, y)





    def check_winner(self):
        # Si ya no quedan puntos, declarar ganador
        if not self.avalibe_points:
            if self.player.score > self.maquina.score:
                self.winner = self.player.representacion
            elif self.maquina.score > self.player.score:
                self.winner = self.maquina.representacion
            else:
                self.winner = "DRAW"





    def calculate_available_moves(self, dec=""):
        posibles_movimientos = []
        who = self.turno.representacion if not dec else dec
        pocision_caballo = self.positions_horse[who]

        for i in range(8):
            movimiento = (self.directions[i][1], self.directions[i][2])
            resultado = tuple(a + b for a, b in zip(pocision_caballo, movimiento))
            posibles_movimientos.append(resultado)
        
        resultado = [t for t in posibles_movimientos if all(0 <= x <= 7 for x in t)]

        final = []
        for i in resultado:
            if self.tablero[i[0]][i[1]] not in [ self.player.representacion,  self.maquina.representacion]:
                final.append(i)

        return final






    def moveHorse(self, tupla = "", isIA = False):
        if not isIA:
            if tupla not in self.calculate_available_moves():
                self.alert = "Movimiento invalido"
                return False


        fila_actual, columna_actual = self.positions_horse[self.turno.representacion]
        nueva_fila, nueva_columna = tupla
        valor = self.tablero[nueva_fila][nueva_columna]



        #MOVER EL CABALLO
        self.tablero[fila_actual][columna_actual] = 0
        self.tablero[nueva_fila][nueva_columna] = self.turno.representacion

        self.positions_horse[self.turno.representacion] = (nueva_fila, nueva_columna)



        #HACER LOS PASOS NECESARIOS SI LA CASILLA NO ES VACIA
        if isinstance(valor, int) and valor != 0:
            self.turno.setScore(valor)
            self.avalibe_points -= 1
            
        elif valor == "x2":
            self.turno.bono = True


        #CAMBIAR DE TURNO
        if self.turno.representacion == self.player.representacion:
            self.turno = self.maquina
        else:
            self.turno = self.player

        self.alert = ""
        return True
    

   



    # Encuentra el mejor movimiento para la IA
    def find_best_move(self):
        inicio = time.time()
        self.alert = "IA PENSANDO"

        best_score = -math.inf
        best_move = None
        avalible = self.calculate_available_moves()


        # MOVER EL CABALLO  
        for i, pos in enumerate(avalible):
            # Simular la jugada de la IA
            game_clone = copy.deepcopy(self)
            game_clone.moveHorse(pos, True)


            # Calcular el valor de esta jugada
            score = self.minimax(game_clone, 2, False, princi=self.turno.representacion, profundidad_maxima=self.turno.datos_inteligencia[0])


            #actualizar el mejor nodo
            if score > best_score:
                best_score = score
                best_move = pos



        final = time.time()
        #print(f"tiempo total {final - inicio}")
        return best_move
    
    



    def calculate_heuristica(self):
        # Calcular el puntaje basado en heurística
        score = 0

        score += (self.maquina.score - self.player.score) * 3
        


        # Posición actual del caballo de la IA
        ia_pos = self.positions_horse[self.maquina.representacion]
        max_valor = float('-inf')  # Inicializa con el menor valor posible
        posicion = None  # Para almacenar la posición del valor máximo

        for fila in range(8):
            for col in range(8):
                valor = self.tablero[fila][col]
                # Verifica si es un número antes de compararlo
                if isinstance(valor, (int, float)) and valor > max_valor:
                    max_valor = valor
                    posicion = (fila, col)
        

        print(max_valor, posicion)

        def knight_distance(start, target):
            if start == target:
                return 0

            # BFS
            queue = deque([(start[0], start[1], 0)])  # (x, y, distancia actual)
            visited = set()
            visited.add(start)

            while queue:
                x, y, dist = queue.popleft()

                for name, dy, dx in self.directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx <= 7 and 0 <= ny <= 7:  # Dentro del tablero
                        if (nx, ny) == target:
                            return dist + 1
                        
                        #if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))

            return -1  # No alcanzable (no debería ocurrir en ajedrez estándar)
        

        pasos = knight_distance(ia_pos, posicion)
        print(f" pasos === {pasos}")
        score -= pasos



        self.pintarTrablero()
        return score





    def minimax(self, board, depth, is_maximizing, alpha=-math.inf, beta=math.inf, 
                princi=None, profundidad_maxima=3):
        
        board.check_winner()

        if board.winner:
            # Condición de victoria o empate
            if board.winner == princi:
                return 1000
            elif board.winner == "DRAW":
                return 0
            else:
                return -1000
            

        if depth == profundidad_maxima:
            if princi == board.maquina.representacion:
                scorte_final =  board.calculate_heuristica() #board.maquina.score - board.player.score #
            
            else:
                scorte_final = board.player.score # - board.maquina.score


            
            input(f"final score => {scorte_final}=====\n\n\n")#-8
        
            return scorte_final

    


        if is_maximizing:
            avalible = board.calculate_available_moves()
            best_score = -math.inf
            for pos in avalible:
                game_clone = copy.deepcopy(board)
                game_clone.moveHorse(pos, True)

                score = game_clone.minimax(game_clone, depth + 1, False, alpha, beta, 
                                           princi, profundidad_maxima)

                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:pass

            return best_score
        


        #mueve el contricante
        else:
            avalible = board.calculate_available_moves()
            best_score = math.inf

            for pos in avalible:
                game_clone = copy.deepcopy(board)
                game_clone.moveHorse(pos, True)

                score = game_clone.minimax(game_clone, depth + 1, True, alpha, beta, 
                                           princi, profundidad_maxima)

                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:pass

            return best_score




    def pintarTrablero(self, depth=0):
        posibles_movimientos = []
        for i in range(8):
            pocision_caballo = self.find_position(self.turno.representacion)
            movimiento = (self.directions[i][1], self.directions[i][2])
            resultado = tuple(a + b for a, b in zip(pocision_caballo, movimiento))
            posibles_movimientos.append(resultado)

        
        #os.system('cls')
        print(f"{"    "*depth}{self.turno.representacion}")
        print(f"{"    "*depth}{self.player}")

        print(f"{"    "*depth}{self.maquina}")

        for x, row in enumerate(self.tablero):
            print(f"{"    "*depth}", end="")
            for y, value in enumerate(row):
                if value == 'HW':
                    # Imprimir "H" en verde
                    print(f"\033[91m{value:<2}\033[0m", end="  ")

                elif value == 'HB':
                    # Imprimir "H" en verde
                    print(f"\033[92m{value:<2}\033[0m", end="  ")

                elif (x, y) in posibles_movimientos:
                    print(f"\033[92m{value:<2}\033[0m", end="  ")

                elif value == 'x2':
                    # Imprimir "H" en verde
                    print(f"\033[93m{value:<2}\033[0m", end="  ")
                
                elif value != 0:
                    print(f"\033[96m{value:<2}\033[0m", end="  ")

                else:
                    print(f"\033[90m{value:<2}\033[0m", end="  ")

            print("")