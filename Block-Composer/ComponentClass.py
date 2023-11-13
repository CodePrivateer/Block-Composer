from typing import Self
import Const
import random
import pygame

class ComponentHandler(object):
       
    def game_quit(self, state, game_field, screen_handler):

        if state['points'] > state['highscore']:  # Wenn die Punkte h�her sind als der Highscore, setzen Sie den Highscore auf die Punkte
            state['highscore'] = state['points']
            self.save_highscore(state['highscore'])
        game_field.reset_field()  # Setzen Sie das Spielfeld zurück
        screen_handler.game_over_screen()  # Zeigen Sie den Game Over-Bildschirm an
        screen_handler.score_screen(state)  # Zeigen Sie das Scoreboard an
        return state['highscore']
    
    def game_level(self, state):
        # Berechnen Sie die erwarteten Level basierend auf Punkten und Linien
        expected_level_points = (state['points'] // (Const.LEVEL_POINTS * state['level'])) + 1
        expected_level_lines = (state['lines'] // (Const.LEVEL_LINES * state['level'])) + 1

        # W�hlen Sie das h�chste erwartete Level aus
        expected_level = max(expected_level_points, expected_level_lines)

        # Wenn das erwartete Level h�her ist als das aktuelle Level und kleiner oder gleich 5, erhöhen Sie das Level
        if expected_level > state['level'] and state['level'] < 5:
            state['level'] = expected_level
        return int(state['level'])

    def save_highscore(self, highscore):
        try:
            with open('highscore.txt', 'w') as file:
                file.write(str(highscore))
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

    def load_highscore(self):
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            print("Die Datei highscore.txt existiert nicht.")
            return 0
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return 0

class Block:
    def __init__(self, column, screen):
        self.column = column
        self.screen = screen
        self.row = 0
        self.shape = random.choice(Const.THE_BLOCKS)
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        self.reached_bottom = False

    def draw(self):
        for r in range(len(self.shape)):
            for c in range(len(self.shape[r])):
                if self.shape[r][c] == 1:
                    pygame.draw.rect(self.screen, self.color,
                                     (self.column*Const.BLOCK_SIZE+c*Const.BLOCK_SIZE,
                                      self.row*Const.BLOCK_SIZE+r*Const.BLOCK_SIZE,
                                      Const.BLOCK_SIZE-2,
                                      Const.BLOCK_SIZE-2))
    
    def collides(self, game_field):
        for r in range(len(self.shape)):
            for c in range(len(self.shape[r])):
                if self.shape[r][c] == 1:
                    # überprüfen Sie, ob der Block den Boden erreicht hat oder einen anderen Block berührt
                    if self.row + r >= Const.SCREEN_HEIGHT / Const.BLOCK_SIZE or self.column + c >= Const.SCREEN_WIDTH / Const.BLOCK_SIZE or \
                       self.row + r < 0 or self.column + c < 0 or game_field.field[self.row + r][self.column + c] is not None:
                        return True
        return False

    def get_occupied_cells(self):
        return [(self.row + r, self.column + c) for r in range(len(self.shape)) for c in range(len(self.shape[r])) if self.shape[r][c] == 1]
       
    def rotate(self, game_field):
        old_shape = self.shape.copy()
        self.shape = [list(x)[::-1] for x in zip(*self.shape)]
        if self.collides(game_field):  # überprüfen Sie die Kollision mit dem GameField
            self.shape = old_shape

class GameField:
    def __init__(self, screen):
        self.screen = screen
        self.field = [[None for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)] for _ in range(Const.SCREEN_HEIGHT // Const.BLOCK_SIZE)]

    def add_block(self, block):
        for r, c in block.get_occupied_cells():
            self.field[r][c] = block.color

    def remove_full_rows(self):
        removed_rows = 0  # Initialisieren Sie die Zählvariable
        for r in range(Const.SCREEN_HEIGHT // Const.BLOCK_SIZE):
            if all(self.field[r][c] is not None for c in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)):
                # Lassen Sie die Reihe blinken, bevor Sie sie entfernen
                for _ in range(3):  # Ändern Sie die Anzahl der Wiederholungen, um die Anzahl der Blinkvorgänge zu ändern
                    self.field[r] = [None if cell is None else (255, 255, 255) for cell in self.field[r]]  # Ändern Sie die Farbe der Zellen in der Reihe in Weiß
                    self.draw()  # Zeichnen Sie das Spielfeld
                    pygame.display.flip()  # Aktualisieren Sie den Bildschirm
                    pygame.time.delay(100)  # Warten Sie eine halbe Sekunde
                    self.field[r] = [(0, 0, 0, 0) for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)]  # Ändern Sie die Farbe der Zellen in der Reihe in Transparent
                    self.draw()  # Zeichnen Sie das Spielfeld
                    pygame.display.flip()  # Aktualisieren Sie den Bildschirm
                    pygame.time.delay(100)  # Warten Sie eine halbe Sekunde

                # Entfernen Sie die Reihe
                del self.field[r]
                self.field.insert(0, [None for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)])
                removed_rows += 1  # Erhöhen Sie die Zählvariable um eins
        return removed_rows  # Geben Sie die Anzahl der entfernten Reihen zurück


    def draw(self):
        for r in range(len(self.field)):
            for c in range(len(self.field[r])):
                color = self.field[r][c]
                if color is not None:
                    pygame.draw.rect(self.screen, color,
                                     (c*Const.BLOCK_SIZE,
                                      r*Const.BLOCK_SIZE,
                                      Const.BLOCK_SIZE-2,
                                      Const.BLOCK_SIZE-2))
        
    def reset_field(self):  # Methode zum Zurücksetzen des Spielfelds
            self.field = [[None for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)] for _ in range(Const.SCREEN_HEIGHT // Const.BLOCK_SIZE)]
        
    def print_field(self):
        for i, row in enumerate(self.field):
            print(f"Zeile {i}: {row}")
            
class SoundHandler:
    def __init__(self):
        self.block_down_sound = pygame.mixer.Sound('block_down.wav')
        self.line_remove_sound = pygame.mixer.Sound('line_remove.wav')
    # Spielen Sie den Soundeffekt ab, wenn eine Aktion ausgeführt wird
    def action_performed(self, action):
        if action == 'block_down':
            self.block_down_sound.set_volume(0.5) # Lautstärke auf 50%
            self.block_down_sound.play()
        elif action == 'line_remove':
            self.line_remove_sound.set_volume(0.5) # Lautstärke auf 50%
            self.line_remove_sound.play()