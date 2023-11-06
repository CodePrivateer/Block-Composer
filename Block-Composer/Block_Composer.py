import pygame
import random
import EventHandlerClass

# Spielkonfiguration
import Const
link_rect = None

# Blocks
THE_BLOCKS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 1]],
]

class Block:
    def __init__(self, column):
        self.column = column
        self.row = 0
        self.shape = random.choice(THE_BLOCKS)
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        self.reached_bottom = False

    def draw(self):
        for r in range(len(self.shape)):
            for c in range(len(self.shape[r])):
                if self.shape[r][c] == 1:
                    pygame.draw.rect(screen, self.color,
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
    def __init__(self):
        self.field = [[None for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)] for _ in range(Const.SCREEN_HEIGHT // Const.BLOCK_SIZE)]

    def add_block(self, block):
        for r, c in block.get_occupied_cells():
            self.field[r][c] = block.color

    def remove_full_rows(self):
        removed_rows = 0  # Initialisieren Sie die Zählvariable
        for r in range(Const.SCREEN_HEIGHT // Const.BLOCK_SIZE):
            if all(self.field[r][c] is not None for c in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)):
                del self.field[r]
                self.field.insert(0, [None for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)])
                removed_rows += 1  # Erhöhen Sie die Zählvariable um eins
        return removed_rows  # Geben Sie die Anzahl der entfernten Reihen zur�ck

    def draw(self):
        for r in range(len(self.field)):
            for c in range(len(self.field[r])):
                color = self.field[r][c]
                if color is not None:
                    pygame.draw.rect(screen, color,
                                     (c*Const.BLOCK_SIZE,
                                      r*Const.BLOCK_SIZE,
                                      Const.BLOCK_SIZE-2,
                                      Const.BLOCK_SIZE-2))
        
    def reset_field(self):  # Methode zum Zurücksetzen des Spielfelds
            self.field = [[None for _ in range(Const.SCREEN_WIDTH // Const.BLOCK_SIZE)] for _ in range(Const.SCREEN_HEIGHT // Const.BLOCK_SIZE)]
        
    def print_field(self):
        for i, row in enumerate(self.field):
            print(f"Zeile {i}: {row}")

# Initialisiere Pygame
pygame.init()
screen = pygame.display.set_mode((Const.SCREEN_WIDTH + Const.SCORE_AREA_WIDTH, Const.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Erstellen Sie eine Liste von Blöcken und fügen Sie den ersten Block hinzu
game_field = GameField()  # Erstellen Sie ein GameField-Objekt
blocks = [Block(5)]
    
# Initialisiere Keyboard_handler Klasse
event_handler = EventHandlerClass.EventHandler()

def draw_surface(s_width, s_height, alpha, color, pos_x, pos_y):
    s = pygame.Surface((s_width, s_height))  # Erstellen Sie eine Oberfläche
    s.set_alpha(alpha)  # Stellen Sie die Transparenz auf 50%
    s.fill(color)  # Füllen Sie die Oberfläche mit Dunkelblau
    screen.blit(s, (pos_x,pos_y))  # Blit die Oberfläche auf den Bildschirm

def draw_text(text, size, color, x, y, centered=True):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    if centered:
        screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
    else:
        screen.blit(text_surface, (x, y))
        
def draw_link(text, size, color, x, y, centered=True):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_rect  # Rückgabe des Rechtecks für Kollisionserkennung

def game_over_screen():
    draw_surface(Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT, 128, (0,0,128), 0, 0)
    draw_text("Game Over", 72, (255, 255, 255), Const.SCREEN_WIDTH // 2 , Const.SCREEN_HEIGHT // 4)
    draw_text("Press key to play", 36, (255, 255, 255), Const.SCREEN_WIDTH // 2 , Const.SCREEN_HEIGHT // 2)

def score_screen(points, highscore, lines, level):
    global link_rect  # Deklarieren Sie link_rect als global innerhalb der Funktion
    draw_surface(Const.SCORE_AREA_WIDTH, Const.SCREEN_HEIGHT, 128, (0,0,128), Const.SCREEN_WIDTH ,0)
    draw_text(str(points).zfill(4) + " Points", 36,(200,200,200),Const.SCREEN_WIDTH +10 ,10 ,centered=False)
    draw_text(str(lines).zfill(4) + " Lines",36,(200,200,200),Const.SCREEN_WIDTH +10 ,50 ,centered=False)
    draw_text(str(level).zfill(4) + " Level",36,(200,200,200),Const.SCREEN_WIDTH +10 ,90 ,centered=False)
    draw_text(str(highscore).zfill(4) + " Highscore",36,(255,200,200),Const.SCREEN_WIDTH +10 ,130 ,centered=False)
    draw_text("Left Arrow > Shift left",24,(200,200,200),Const.SCREEN_WIDTH +10 ,210 ,centered=False)
    draw_text("Right Arrow > Shift Right",24,(200,200,200),Const.SCREEN_WIDTH +10 ,250 ,centered=False)
    draw_text("Down Arrow Key > Fast place",24,(200,200,200),Const.SCREEN_WIDTH +10 ,290 ,centered=False)
    draw_text("Space Key > rotate",24,(200,200,200),Const.SCREEN_WIDTH +10 ,330 ,centered=False)
    draw_text("'p' Key Pause",24,(200,200,200),Const.SCREEN_WIDTH +10 ,370 ,centered=False)
    draw_text("'q' Quit Game ",24,(200,200,200),Const.SCREEN_WIDTH +10 ,410 ,centered=False)
    link_rect = draw_link("Block-Composer on Github", 16, (200,200,200), Const.SCREEN_WIDTH +10 ,530 ,centered=False)

def pause_screen():
    draw_surface(Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT, 128,(0,0,128),0 ,0)
    draw_text("Game Paused",72,(255 ,255 ,255),Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //4)
    draw_text("Press 'p' key to play",36,(255 ,255 ,255),Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //2)

def start_screen():
    draw_surface(Const.SCREEN_WIDTH ,Const.SCREEN_HEIGHT ,128 ,(0 ,0 ,128) ,0 ,0)
    draw_text("Block-Composer",64 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //4)
    draw_text("Press key to play",36 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //2)

def quit_screen():
    draw_surface(Const.SCREEN_WIDTH ,Const.SCREEN_HEIGHT ,128 ,(0 ,0 ,128) ,0 ,0)
    draw_text("Quit Game?",72 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //4)
    draw_text("Press y key to quit",36 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //2)

def save_highscore(highscore):
    try:
        with open('highscore.txt', 'w') as file:
            file.write(str(highscore))
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def load_highscore():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        print("Die Datei highscore.txt existiert nicht.")
        return 0
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return 0

def game_quit(points,highscore, lines, level):

    if points > highscore:  # Wenn die Punkte h�her sind als der Highscore, setzen Sie den Highscore auf die Punkte
        highscore = points
        save_highscore(highscore)
    game_field.reset_field()  # Setzen Sie das Spielfeld zurück
    game_over_screen()  # Zeigen Sie den Game Over-Bildschirm an
    score_screen(points, highscore, lines, level)  # Zeigen Sie das Scoreboard an
    return highscore

def game_level(points, lines, level):
    # Berechnen Sie die erwarteten Level basierend auf Punkten und Linien
    expected_level_points = (points // (Const.LEVEL_POINTS * level)) + 1
    expected_level_lines = (lines // (Const.LEVEL_LINES * level)) + 1

    # W�hlen Sie das h�chste erwartete Level aus
    expected_level = max(expected_level_points, expected_level_lines)

    # Wenn das erwartete Level h�her ist als das aktuelle Level und kleiner oder gleich 5, erhöhen Sie das Level
    if expected_level > level and level < 5:
        level = expected_level
    print (level)
    return int(level)
    
# Spiel Loop
def spiel():
    counter = 0
    state = {
        'paused': False,
        'quit_game': False,
        'quit_yes': False,
        'start': False,
        'speed': 1,
        'level': 1,
        'restart_game': False,
        'start_timer': False,
        'start_screen_timer': False,
    }

    points = 0  # Initialisieren Sie die Punkte
    highscore = load_highscore()  # Initialisieren Sie den Highscore
    lines = 0
    background = pygame.image.load('background.jpeg')  # Laden Sie das Hintergrundbild
    background.set_alpha(128)  # erh�hen der Transparenz des Hintergrundbildes
    background = pygame.transform.smoothscale(background, (650, 600))  # Skalieren Sie das Bild auf 650x600
     
    while True: # Spiel loop
        if state['start_timer'] or state['start'] == False:
            screen.fill((0,0,0))
            screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
            score_screen(points, highscore, lines, state['level'])  
            start_screen()
            pygame.display.flip()
            event_handler.handle_start_event(state, link_rect)
            state['start_timer'] = False
            
        screen.fill((0,0,0))
        screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
        game_field.draw()  # Zeichnen Sie das Spielfeld
        if state['paused']:
            pause_screen()
            score_screen(points, highscore, lines, state['level'])
        if state['quit_game'] and not state['quit_yes']:
            quit_screen()
            score_screen(points, highscore, lines, state['level'])
            pygame.display.flip()
        events = pygame.event.get()    
        event_handler.handle_mouse_event(events, link_rect)
        event_handler.handle_keyboard_event(events, blocks, game_field, state)

        while not state['paused'] and not state['quit_game'] and not state['quit_yes']:
            for block in blocks[:]:  # Erstellen Sie eine Kopie der Liste für die Iteration
                block.draw()  # Zeichnen Sie den Block
                if counter % (40 // state['speed']) == 0: 
                    if not block.reached_bottom:  # überprüfen Sie, ob der Block den Boden noch nicht erreicht hat
                        block.row += 1  # Bewegen Sie den Block eine Zeile nach unten
                        if block.collides(game_field):  # überprüfen Sie, ob der Block mit dem Spielfeld kollidiert
                            block.row -= 1  # Bewegen Sie den Block eine Zeile nach oben
                            block.reached_bottom = True  # Setzen Sie reached_bottom auf True, da der Block den Boden erreicht hat
                            points += Const.POINTS_BLOCK  # Erhöhen Sie die Punkte um die Punkte für einen Block
                            game_field.add_block(block)  # Fügen Sie den Block zum Spielfeld hinzu
                            removed_rows = game_field.remove_full_rows()  # Entfernen Sie volle Reihen vom Spielfeld und speichern Sie die Anzahl der entfernten Reihen
                            if removed_rows is not None:  # überprüfen Sie, ob Reihen entfernt wurden
                                points += removed_rows * Const.POINTS_ROW  # Erhöhen Sie die Punkte um die Anzahl der entfernten Reihen multipliziert mit den Punkten pro Reihe
                                lines += removed_rows
                            state['level'] = game_level(points, lines, state['level'])
                            blocks.remove(block)  # Entfernen Sie den Block aus der Liste
                            new_block = Block(5)  # Erstellen Sie einen neuen Block
                            state['speed'] = 1 * state['level']                       
                            if new_block.collides(game_field):  # überprüfen Sie, ob der neue Block mit dem Spielfeld kollidiert
                                highscore = game_quit(points, highscore, lines, state['level'])
                                points = 0
                                lines = 0
                                pygame.display.flip()  
                                event_handler.handle_gameover_event(state, blocks, new_block)
                            else:
                                blocks.append(new_block)  # Fügen Sie den neuen Block zur Liste hinzu, wenn er nicht mit dem Spielfeld kollidiert       
            counter += 1
            score_screen(points, highscore, lines, state['level'])
            break
        if state['quit_yes']: # Das Spiel wurde vom Spieler beendet
            screen.fill((0,0,0))
            screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
            highscore = game_quit(points,highscore,lines, state['level'])
            points = 0
            lines = 0
            pygame.display.flip()
            event_handler.handle_gameover_event(state, blocks, new_block)
            state['quit_yes'] = False
            state['quit_game'] = False 
      
        pygame.display.flip()
        clock.tick(60)

spiel()
pygame.quit()
