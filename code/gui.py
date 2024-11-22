import pygame
from main import *

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

# Clase para el Tablero de Smart Horses
# Clase para el Tablero de Smart Horses
class SmartHorsesBoard:
    def __init__(self):
        # Cargar las imágenes de los caballos
        self.white_knight = pygame.image.load('./image/HW.png')
        self.black_knight = pygame.image.load('./image/HB.png')
        
        # Escalar las imágenes al tamaño de las casillas
        self.white_knight = pygame.transform.scale(self.white_knight, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_knight = pygame.transform.scale(self.black_knight, (SQUARE_SIZE, SQUARE_SIZE))
        
        # Tablero de juego
        self.back = MiClase(dificultad="media")



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
                if value == 'HW':
                    win.blit(self.white_knight, rect.topleft)
                    if self.back.maquina.bono:
                        pygame.draw.ellipse(win, PASTEL_GOLD, rect.inflate(10, 10), 6)

                elif value == 'HB':
                    win.blit(self.black_knight, rect.topleft)
                    if self.back.player.bono:
                        pygame.draw.ellipse(win, PASTEL_GOLD, rect.inflate(10, 10), 6)

                elif (x, y) in avalible_moves and isinstance(value, int) and value != 0:
                    pygame.draw.rect(win, PASTEL_COMBINATION_AVALIBLE_NUMBER, rect)
                    self.draw_text(win, str(value), rect.center, TEXT_COLOR_AVALIBLE)
                elif (x, y) in avalible_moves and value == 'x2':
                    pygame.draw.rect(win, PASTEL_COMBINATION_AVALIBLE_BONO, rect)
                    self.draw_text(win, 'x2', rect.center, TEXT_COLOR_AVALIBLE)
                elif (x, y) in avalible_moves:
                    pygame.draw.rect(win, PASTEL_GREEN, rect)
                    self.draw_text(win, 'F', rect.center)
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
        if self.back.winner == 'HW':
            text = "¡Gana el Caballo Blanco!"
        elif self.back.winner == 'HB':
            text = "¡Gana el Caballo Negro!"
        else:
            text = "¡Es un empate!"

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(BOARD_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        win.blit(overlay, (0, 0))
        win.blit(text_surface, text_rect)



    def get_square_under_mouse(self, pos):
        if self.back.winner:  # Si ya hay un ganador, no permitir más movimientos
            return
        
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        self.back.moveHorse(tupla=(row, col))
        self.back.check_winner()  # Verificar si hay un ganador


        if self.back.turno.representacion == "HB":
            move = self.back.find_best_move()
            self.back.moveHorse(tupla=move)
            self.back.check_winner()  # Verificar si hay un ganador


        return (row, col)





# Clase para manejar la interfaz de datos
class InfoPanel:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)



    def draw(self, win, turn, score_white, score_black, alert):
        # Fondo del panel de información
        pygame.draw.rect(win, INFO_BG_COLOR, (BOARD_WIDTH, 0, INFO_WIDTH, INFO_HEIGHT))

        # Texto de información
        self.draw_text(win, f"Turn: {'White' if turn == 'HW' else 'Black'}", (BOARD_WIDTH + 20, 50))
        self.draw_text(win, f"White Score: {score_white}", (BOARD_WIDTH + 20, 150))
        self.draw_text(win, f"Black Score: {score_black}", (BOARD_WIDTH + 20, 250))

        if alert:
            self.draw_text(win, f"Aviso: {alert}", (BOARD_WIDTH + 20, 350))



    def draw_text(self, win, text, pos):
        text_surface = self.font.render(text, True, TEXT_COLOR)
        win.blit(text_surface, pos)






# Función principal para ejecutar el juego
def main():
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Smart Horses")
    
    board = SmartHorsesBoard()
    info_panel = InfoPanel()
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not board.back.winner:
                pos = pygame.mouse.get_pos()
                if pos[0] < BOARD_WIDTH:
                    row, col = board.get_square_under_mouse(pos)
                    #print(f"Se hizo clic en la casilla: ({row}, {col})")

        # Dibujar el tablero y el panel de información
        board.draw(win)
        info_panel.draw(win, board.back.turno.representacion, board.back.maquina.score, board.back.player.score, board.back.alert)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
