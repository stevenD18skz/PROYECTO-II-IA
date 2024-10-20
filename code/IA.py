import math

class minmax:
    def __init__(self):
        self.nombre = "1"


    # Representación del tablero de 3 en raya
    def print_board(self, board):
        symbols = {0: '   ', 1: ' X ', 2: ' O '}  # Diccionario para mapear los valores a los símbolos
        for row in board:
            # Convertir cada fila a sus símbolos correspondientes y mostrar con separadores de |
            print('|'.join([symbols[cell] for cell in row]))
            print("-" * 12)  # Línea separadora entre filas


    # Comprobar si hay un ganador
    def check_winner(self, board):
        # Comprobar filas, columnas y diagonales
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != 0:
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != 0:
                return board[0][i]

        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]

        return None


    # Comprobar si el tablero está lleno
    def is_full(self, board):
        for row in board:
            if 0 in row:
                return False
        return True



    # Algoritmo Minimax
    def minimax(self, board, depth, is_maximizing, move=None):
        winner = self.check_winner(board)
        
        # Si la IA gana, devuelve +1
        if winner == 2:
            return 1
        
        # Si el humano gana, devuelve -1
        if winner == 1:
            return -1
        
        # Si es empate, devuelve 0
        if self.is_full(board):
            return 0

        if move is not None:
            print(f"Evaluando movimiento: {move}")
            self.print_board(board)

        # Jugador IA (maximizar)
        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2
                        score = self.minimax(board, depth + 1, False, move=(i, j))
                        board[i][j] = 0
                        best_score = max(score, best_score)
                        if move is not None:
                            print(f"Puntaje del movimiento {move}: {score}")
            return best_score


        # Jugador humano (minimizar)
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, depth + 1, True, move=(i, j))
                        board[i][j] = 0
                        best_score = min(score, best_score)
                        if move is not None:
                            print(f"Puntaje del movimiento {move}: {score}")
            return best_score




    # Encuentra el mejor movimiento para la IA
    def find_best_move(self, board):
        best_score = -math.inf
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = self.minimax(board, 0, False, move=(i, j))
                    board[i][j] = 0
                    print(f"Movimiento {(i, j)} tiene un puntaje de {score}")
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move





    # Función principal para jugar
    def play_game(self):
        # 0: Espacio vacío, 1: Humano (X), 2: IA (O)
        board = [[1, 2, 1],
                 [2, 1, 0],
                 [0, 0, 2]]

        while True:
            # Imprimir el tablero
            self.print_board(board)

            # Turno del humano
            print("Tu turno (X):")
            row = int(input("Ingresa la fila (0, 1, 2): "))
            col = int(input("Ingresa la columna (0, 1, 2): "))

            if board[row][col] != 0:
                print("Posición inválida. Intenta de nuevo.")
                continue

            board[row][col] = 1

            # Comprobar si el humano ha ganado
            if self.check_winner(board) == 1:
                print("¡Has ganado!")
                self.print_board(board)
                break

            # Comprobar si el tablero está lleno (empate)
            if self.is_full(board):
                print("¡Es un empate!")
                self.print_board(board)
                break

            # Turno de la IA
            print("Turno de la IA (O):")
            move = self.find_best_move(board)
            board[move[0]][move[1]] = 2

            # Comprobar si la IA ha ganado
            if self.check_winner(board) == 2:
                print("La IA ha ganado.")
                self.print_board(board)
                break

            # Comprobar si el tablero está lleno (empate)
            if self.is_full(board):
                print("¡Es un empate!")
                self.print_board(board)
                break

# Ejecutar el juego
m = minmax()
m.play_game()
