import copy
import math
import os
import random
import time


class jugador:
    def __init__(self, nombre, representacion):
        self.nombre = nombre
        self.score = 0
        self.bono = False
        self.representacion = representacion
    
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
        return f"Jugador: {self.nombre}, Puntuación: {self.score}, Bono: {"X2" if self.bono else "X1"}"




class MiClase:
    def __init__(self, dificultad="facil"):
        #MAQUINA JUGADOR
        self.player = jugador("STEVEN", "HB")
        self.maquina = jugador("MACHINE", "HW")
        self.turno = self.player


        #ATRIBUTOS ENTORNO
        self.tablero = self.generate_grid()
        self.tablero = [
            [   0,    0, 0, 0, 0,  0,    0, 0],
            [   0, 4, 0, 0, 0,  0,    0,    0],
            [   0,    5, 0, 0, 0,  0,    0,    0],
            [   4,    0, 0, 0, 0,  0, 0,    0],
            [   0,    0, 'HB', 0, 0,  0,    0,    0],
            [   3,    0, 0,     0, 'HW', 0,   0,    0],
            [   0,    0, 0,     0, 0,  0,    0,    0],
            [0,    0, 0, 0,  0,  0,    0,    12],
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
        self.datos_ia = {
            "facil": [3],
            "media": [5],
            "avanzada": [7]
        }
        self.dificultad = dificultad



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
        print(self.maquina)
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
        # Verificar si quedan casillas con puntos en el tablero
        puntos_disponibles = any(isinstance(value, int) and value > 0 for row in self.tablero for value in row)

        # Si ya no quedan puntos, declarar ganador
        if not puntos_disponibles:
            if self.player.score > self.maquina.score:
                self.winner = self.player.representacion
            elif self.maquina.score > self.player.score:
                self.winner = self.maquina.representacion
            else:
                self.winner = "DRAW"
        else:
            pass




    def calculate_available_moves(self):
        posibles_movimientos = []
        for i in range(8):
            pocision_caballo = self.find_position(self.turno.representacion)
            movimiento = (self.directions[i][1], self.directions[i][2])
            resultado = tuple(a + b for a, b in zip(pocision_caballo, movimiento))
            posibles_movimientos.append(resultado)
        
        resultado = [t for t in posibles_movimientos if all(0 <= x <= 7 for x in t)]

        final = []
        for i in resultado:
            if self.tablero[i[0]][i[1]] not in [ self.player.representacion,  self.maquina.representacion]:
                final.append(i)

        return final



 
    def moveHorse(self, tupla = ""):
        if tupla not in self.calculate_available_moves():
            self.alert = "Movimiento invalido"
            return

        fila_actual, columna_actual = self.find_position(self.turno.representacion)
        nueva_fila, nueva_columna = tupla
        valor = self.tablero[nueva_fila][nueva_columna]


        #MOVER EL CABALLO
        self.tablero[fila_actual][columna_actual] = 0
        self.tablero[nueva_fila][nueva_columna] = self.turno.representacion


        #HACER LOS PASOS NECESARIOS SI LA CASILLA NO ES VACIA
        if isinstance(valor, int) and valor != 0:
            self.turno.setScore(valor)
            
        elif valor == "x2":
            self.turno.bono = True


        #CAMBIAR DE TURNO
        if self.turno.representacion == self.player.representacion:
            self.turno = self.maquina
        
        else:
            self.turno = self.player

        self.alert = ""
   





    # Encuentra el mejor movimiento para la IA
    def find_best_move(self):
        self.alert = "sdafafasddddddddddddddddddd"
        best_score = -math.inf
        best_move = None
        avalible = self.calculate_available_moves()


        # MOVER EL CABALLO  
        for i, pos in enumerate(avalible):
            # Simular la jugada de la IA
            game_clone = copy.deepcopy(self)
            game_clone.moveHorse(pos)


            # Calcular el valor de esta jugada
            score = self.minimax(game_clone, 2, False)


            #actualizar el mejor nodo
            if score > best_score:
                best_score = score
                best_move = pos

        return best_move
    



    def minimax(self, board, depth, is_maximizing, move=None):
        winner = board.check_winner()
        
        if depth == self.datos_ia[self.dificultad][0]:
            return board.player.score - board.maquina.score
        
        # Si la IA gana, devuelve +1
        if winner == 2:
            return 1000
        
        # Si el humano gana, devuelve -1
        if winner == 1:
            return -1000
        
        # Si es empate, devuelve 0
        #if board.is_full(board):
        #    return 0

        #if move is not None:
            #print(f"Evaluando movimiento: {self.tablero}")
            

        # Jugador IA (maximizar)
        if is_maximizing:
            avalible = board.calculate_available_moves()
            best_score = -math.inf

            # MOVER EL CABALLO  
            for i, pos in enumerate(avalible):
                # Simular la jugada de la IA
                game_clone = copy.deepcopy(board)
                game_clone.moveHorse(pos)

                #calcular nodo
                score = game_clone.minimax(game_clone, depth + 1, False)
                #print(f"{"    "*depth}{depth} ==> Puntaje del movimiento 🏮🏮🏮{pos}: {score}")

                best_score = max(score, best_score)
            
            return best_score


        # Jugador humano (minimizar)
        else:
            avalible = board.calculate_available_moves()
            best_score = math.inf

            # MOVER EL CABALLO  
            for i, pos in enumerate(avalible):
                # Simular la jugada de la IA
                game_clone = copy.deepcopy(board)
                game_clone.moveHorse(pos)

                #calcular nodo
                score = game_clone.minimax(game_clone, depth + 1, True)

                best_score = min(score, best_score)
                #print(f"{"    "*depth}{depth} ==> Puntaje del movimiento 🏮🏮🏮{pos}: {score}")
            
            return best_score
        





    def set_difficulty(self, dif):
        self.dificultad = dif
