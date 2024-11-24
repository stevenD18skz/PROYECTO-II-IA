import pygame
from game import *

# Inicializar Pygame
pygame.init()

# Configuraciones básicas
BOARD_WIDTH, BOARD_HEIGHT = 600, 600  # Tamaño del tablero
INFO_WIDTH, INFO_HEIGHT = 300, 600    # Tamaño de la barra lateral para datos
WINDOW_WIDTH = BOARD_WIDTH + INFO_WIDTH  # Tamaño total de la ventana
WINDOW_HEIGHT = BOARD_HEIGHT

ROWS, COLS = 8, 8  # Filas y columnas del tablero
SQUARE_SIZE = BOARD_WIDTH // COLS  # Tamaño de cada casilla

# Colores pastel
PASTEL_LIGHT = (255, 239, 213)  # Color claro del tablero
PASTEL_DARK = (189, 183, 107)   # Color oscuro del tablero
PASTEL_YELLOW = (253, 253, 150) # Casillas con puntos
PASTEL_GOLD = (250, 218, 94)    # Casillas x2
PASTEL_GREEN = (100, 218, 50)   # Casillas DISPONIBLES
PASTEL_COMBINATION_AVALIBLE_NUMBER = (100, 100, 100)   # Casillas CON NUMERO DISPONIBLE
PASTEL_COMBINATION_AVALIBLE_BONO = (200, 100, 100)   # Casillas CON BONO X2 DISPONIBLE
TEXT_COLOR = (105, 105, 105)    # Color del texto (gris oscuro)
TEXT_COLOR_AVALIBLE = (170, 170, 170)    # Color del texto (gris claro)
INFO_BG_COLOR = (245, 245, 245) # Color de fondo para la barra de datos

# Colores para los turnos
WARM_LIGHT = (255, 200, 150)  # Color cálido claro (para la máquina)
WARM_DARK = (255, 160, 120)   # Color cálido oscuro (para la máquina)
COOL_LIGHT = (150, 200, 255)  # Color frío claro (para el jugador)
COOL_DARK = (120, 160, 255)   # Color frío oscuro (para el jugador)


# Clase para el Tablero de Smart Horses
class SmartHorsesBoard:
    def __init__(self):
        # Tablero de juego
        self.back = Game()

        # Cargar las imágenes de los caballos
        self.white_knight = pygame.image.load(f'./image/{self.back.maquina.representacion}.png')
        self.black_knight = pygame.image.load(f'./image/{self.back.player.representacion}.png')
        
        # Escalar las imágenes al tamaño de las casillas
        self.white_knight = pygame.transform.scale(self.white_knight, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_knight = pygame.transform.scale(self.black_knight, (SQUARE_SIZE, SQUARE_SIZE))





    def draw_text(self, win, text, pos, color=TEXT_COLOR):
        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        win.blit(text_surface, text_rect)




    def draw(self, win):
        win.fill(PASTEL_LIGHT)
        avalible_moves = self.back.calculate_available_moves()

        for x, row in enumerate(self.back.tablero):
            for y, col in enumerate(row):
                if (x + y) % 2 == 0:
                    color = PASTEL_LIGHT
                else:
                    color = PASTEL_DARK

                rect = pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(win, color, rect)

                value = col

                # Imágenes de los caballos
                if value == self.back.maquina.representacion:
                    win.blit(self.white_knight, rect.topleft)
                    if self.back.maquina.bono:
                        pygame.draw.ellipse(win, PASTEL_GOLD, rect.inflate(10, 10), 6)

                elif value == self.back.player.representacion:
                    win.blit(self.black_knight, rect.topleft)
                    if self.back.player.bono:
                        pygame.draw.ellipse(win, PASTEL_GOLD, rect.inflate(10, 10), 6)

                # Movimientos disponibles según el turno
                elif (x, y) in avalible_moves:
                    if self.back.turno == self.back.maquina:
                        # Turno de la máquina: colores cálidos
                        if isinstance(value, int) and value != 0:
                            pygame.draw.rect(win, WARM_DARK, rect)
                            self.draw_text(win, str(value), rect.center, TEXT_COLOR_AVALIBLE)
                        elif value == 'x2':
                            pygame.draw.rect(win, WARM_LIGHT, rect)
                            self.draw_text(win, 'x2', rect.center, TEXT_COLOR_AVALIBLE)
                        else:
                            pygame.draw.rect(win, WARM_LIGHT, rect)
                            self.draw_text(win, 'F', rect.center)
                    elif self.back.turno == self.back.player:
                        # Turno del jugador: colores fríos
                        if isinstance(value, int) and value != 0:
                            pygame.draw.rect(win, COOL_DARK, rect)
                            self.draw_text(win, str(value), rect.center, TEXT_COLOR_AVALIBLE)
                        elif value == 'x2':
                            pygame.draw.rect(win, COOL_LIGHT, rect)
                            self.draw_text(win, 'x2', rect.center, TEXT_COLOR_AVALIBLE)
                        else:
                            pygame.draw.rect(win, COOL_LIGHT, rect)
                            self.draw_text(win, 'F', rect.center)

                # Casillas normales (sin movimientos disponibles)
                elif value == 'x2':
                    pygame.draw.rect(win, PASTEL_GOLD, rect)
                    self.draw_text(win, 'x2', rect.center)
                elif isinstance(value, int) and value != 0:
                    pygame.draw.rect(win, PASTEL_YELLOW, rect)
                    self.draw_text(win, str(value), rect.center)

        # Verificar si hay un ganador
        if self.back.winner:
            self.display_winner(win)

 




    def display_winner(self, win):
        # Crear una superficie oscura que cubra el tablero
        overlay = pygame.Surface((BOARD_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Color negro con transparencia

        # Mostrar mensaje de victoria
        font = pygame.font.SysFont(None, 64)
        if self.back.winner == self.back.maquina.representacion:
            text = f"¡Gana el Caballo {self.back.maquina.representacion}!"
        elif self.back.winner == self.back.player.representacion:
            text = f"¡Gana el Caballo {self.back.player.representacion}!"
        else:
            text = "¡Es un empate!"

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(BOARD_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        win.blit(overlay, (0, 0))
        win.blit(text_surface, text_rect)





    def get_square_under_mouse(self, pos ): 
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE

        # Mover ficha del jugador
        return self.back.moveHorse(tupla=(row, col))
         
         

        






# Modificación del InfoPanel para incluir la dificultad
class InfoPanel:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, win, turn, score_white, score_black, alert, back_info, difficulty):
        # Fondo del panel de información
        pygame.draw.rect(win, INFO_BG_COLOR, (BOARD_WIDTH, 0, INFO_WIDTH, INFO_HEIGHT))

        # Texto de información
        self.draw_text(win, f"Turn: {back_info.back.maquina.representacion if turn == back_info.back.maquina.representacion else back_info.back.player.representacion}", (BOARD_WIDTH + 20, 50))
        self.draw_text(win, f"White Score: {score_white}", (BOARD_WIDTH + 20, 100))
        self.draw_text(win, f"Black Score: {score_black}", (BOARD_WIDTH + 20, 150))
        self.draw_text(win, f"Dificultad: {difficulty}", (BOARD_WIDTH + 20, 200))  # Mostrar dificultad seleccionada

        if alert:
            self.draw_text(win, f"Aviso: {alert}", (BOARD_WIDTH + 20, 10))

    def draw_text(self, win, text, pos):
        text_surface = self.font.render(text, True, TEXT_COLOR)
        win.blit(text_surface, pos)


class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)



def main():
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Smart Horses")
    
    board = SmartHorsesBoard()
    info_panel = InfoPanel()
    clock = pygame.time.Clock()

    # Define botones
    easy_button = Button(630, BOARD_HEIGHT - 340, 150, 50, "Fácil", (144, 238, 144), (0, 100, 0), lambda: set_difficulty("facil"))
    medium_button = Button(630, BOARD_HEIGHT - 260, 150, 50, "Media", (173, 216, 230), (0, 0, 139), lambda: set_difficulty("media"))
    hard_button = Button(630, BOARD_HEIGHT - 180, 150, 50, "Difícil", (255, 182, 193), (139, 0, 0), lambda: set_difficulty("avanzada"))
    start_button = Button(630, BOARD_HEIGHT - 100, 150, 50, "Start", (240, 230, 140), (139, 69, 19), lambda: set_difficulty)  # Botón de Start

    buttons = [easy_button, medium_button, hard_button, start_button]
    game_started = False  # Variable para rastrear si el juego ha comenzado
    difficulty_selected = False  # Variable para verificar si ya se eligió la dificultad
    current_difficulty = "N/A"  # Variable para almacenar la dificultad actual
    machine_thinking = True

    def set_difficulty(difficulty):
        nonlocal current_difficulty, difficulty_selected
        board.back.set_difficulty(difficulty)
        if difficulty == "facil":
            current_difficulty = "Fácil"
        elif difficulty == "media":
            current_difficulty = "Media"
        elif difficulty == "avanzada":
            current_difficulty = "Difícil"
        difficulty_selected = True

    blink_timer = 0  # Temporizador para el efecto parpadeante

    while True:
        clock.tick(30)
        blink_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if not game_started:
                    # Habilitar selección de dificultad antes de iniciar el juego
                    for button in buttons:
                        if button.is_clicked(pos):
                            button.action()

                    # Iniciar el juego sólo si ya se seleccionó una dificultad
                    if start_button.is_clicked(pos) and difficulty_selected:
                        game_started = True  # Marcar el inicio del juego

                elif game_started:
                    if board.back.turno == board.back.player.representacion:
                        print("si es el movimiento del jugador")

                    # Movimiento del jugador solo si el juego ya comenzó
                    elif pos[0] < BOARD_WIDTH and not board.back.winner and not machine_thinking:
                        if board.get_square_under_mouse(pos):
                            machine_thinking = True  # Indicar que la máquina debe pensar en el próximo ciclo



        # Dibujar el tablero, panel de información y botones
        board.draw(win)
        info_panel.draw(win, board.back.turno.representacion, board.back.maquina.score, board.back.player.score, board.back.alert, board, current_difficulty)

        # Dibujar botones
        for button in buttons:
            # Deshabilitar botones de dificultad si ya comenzó el juego
            if game_started:
                button.color = (200, 200, 200)  # Cambiar a un color apagado
                button.text_color = (100, 100, 100)  # Color del texto desactivado
                button.action = None  # Deshabilitar acción
            button.draw(win)


        # Proceso del turno de la máquina
        if machine_thinking and not board.back.winner and  game_started:
            board.back.alert = "Pensando..."
            pygame.display.flip()  # Mostrar el estado de "Pensando..." antes de calcular el movimiento

            move = board.back.find_best_move()
            board.back.moveHorse(move, True)
            board.back.check_winner()
            board.back.alert = None  # Limpiar alerta
            machine_thinking = False


        # Fondo negro con texto parpadeante antes de que comience el juego
        if not game_started:
            # Fondo negro solo en la región del tablero
            overlay = pygame.Surface((BOARD_WIDTH, WINDOW_HEIGHT))  # Tamaño del área del tablero
            overlay.set_alpha(245)  # Establecer la transparencia (255 es opaco, 0 es totalmente transparente)
            overlay.fill((10, 10, 10))  # Color del fondo negro
            win.blit(overlay, (0, 0))  # Dibujar la superficie en la ventana
                    
            
            # Efecto de parpadeo
            if (blink_timer // 30) % 2 == 0:  # Alternar visibilidad cada 15 frames
                font = pygame.font.SysFont(None, 64)
                text_surface = font.render("Esperando...", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(BOARD_WIDTH // 2, BOARD_HEIGHT // 2))
                win.blit(text_surface, text_rect)
                
        pygame.display.flip()



 


if __name__ == "__main__":
    main()
