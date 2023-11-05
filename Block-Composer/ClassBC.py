import pygame

class KeyboardHandler:
    def __init__(self):
        self.paused = False
        self.quit_game = False
        self.quit_yes = False
        self.start = False
        
    def handle_event(self, event, blocks, game_field):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
            if event.key == pygame.K_q:
                self.quit_game = not self.quit_game
            if event.key == pygame.K_y:
                if self.quit_game:
                    self.quit_yes = True
            if event.key == pygame.K_LEFT:
                if blocks[-1].column > 0:  # Wenn der Block nicht am linken Rand ist
                    blocks[-1].column -= 1  # Bewegen Sie den Block eine Spalte nach links
                    if blocks[-1].collides(game_field):  # überprüfen Sie, ob der Block mit dem Spielfeld kollidiert
                        blocks[-1].column += 1  # Wenn ja, bewegen Sie den Block eine Spalte nach rechts zurück
            elif event.key == pygame.K_RIGHT:
                # Fügen Sie hier den Code für die rechte Pfeiltaste hinzu
                pass
    pass