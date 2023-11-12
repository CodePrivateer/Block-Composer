import pygame
import EventHandlerClass
import ScreenHandlerClass
import ComponentClass
import time

# Spielkonfiguration
import Const
link_rect = None

# Initialisiere Pygame
pygame.init()
screen = pygame.display.set_mode((Const.SCREEN_WIDTH + Const.SCORE_AREA_WIDTH, Const.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# initialisiere ScreenHandler Klasse
screen_handler = ScreenHandlerClass.ScreenHandler(screen)

# Erstellen Sie eine Liste von Blöcken und fügen Sie den ersten Block hinzu
game_field = ComponentClass.GameField(screen)  # Erstellen Sie ein GameField-Objekt
    
# Initialisiere Keyboard_handler Klasse
event_handler = EventHandlerClass.EventHandler()

# Funktionen
def draw_start_screen(screen, background, state):
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    screen_handler.score_screen(state)
    screen_handler.start_screen()
    screen_handler.link_screen()
    pygame.display.flip()
    
def draw_pause_screen(state):
    screen_handler.pause_screen()
    screen_handler.score_screen(state)
    screen_handler.link_screen()

def draw_quit_screen(state):
    screen_handler.quit_screen()
    screen_handler.score_screen(state)
    screen_handler.link_screen()
    pygame.display.flip()
    
def draw_game(screen, background, game_field, state):
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    game_field.draw()
    screen_handler.score_screen(state)
    screen_handler.link_screen()
    
def handle_events(block, game_field, state, link_rect):
    events = pygame.event.get()    
    event_handler.handle_mouse_event(events, link_rect)
    event_handler.handle_keyboard_event(events, block, game_field, state)

def reset_game(state, game_field, screen_handler, background, component_handler):
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
    state['highscore'] = component_handler.game_quit(state, game_field, screen_handler)
    state['points'] = 0
    state['lines'] = 0
    pygame.display.flip()
    #block = ComponentClass.Block(Const.START_COLUMN,screen)  # Erstellen Sie einen neuen Block    
    event_handler.handle_gameover_event(state, link_rect)
    state['quit_yes'] = False
    state['quit_game'] = False 

def remove_rows(state, game_field):
    removed_rows = game_field.remove_full_rows()  # Entfernen Sie volle Reihen vom Spielfeld und speichern Sie die Anzahl der entfernten Reihen
    if removed_rows is not None:  # überprüfen Sie, ob Reihen entfernt wurden
        state['points'] += removed_rows * Const.POINTS_ROW  # Erhöhen Sie die Punkte um die Anzahl der entfernten Reihen multipliziert mit den Punkten pro Reihe
        state['lines'] += removed_rows

def block_move(state, block, component_handler, game_field, background):
    if not block.reached_bottom:  # überprüfen Sie, ob der Block den Boden noch nicht erreicht hat
        block.row += 1  # Bewegen Sie den Block eine Zeile nach unten
        if block.collides(game_field):  # überprüfen Sie, ob der Block mit dem Spielfeld kollidiert
            block.row -= 1  # Bewegen Sie den Block eine Zeile nach oben
            block.reached_bottom = True  # Setzen Sie reached_bottom auf True, da der Block den Boden erreicht hat
            state['points'] += Const.POINTS_BLOCK  # Erhöhen Sie die Punkte um die Punkte für einen Block
            game_field.add_block(block)  # Fügen Sie den Block zum Spielfeld hinzu
            remove_rows(state, game_field)
            state['level'] = component_handler.game_level(state)
            block = ComponentClass.Block(Const.START_COLUMN,screen)  # Erstellen Sie einen neuen Block
            state['speed'] = 1 + state['level']                       
            if block.collides(game_field):  # überprüfen Sie, ob der neue Block mit dem Spielfeld kollidiert
                reset_game(state, game_field, screen_handler, background, component_handler)
            return block
    return block

# Spiel Loop
def spiel():
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
        'points': 0,
        'highscore': 0,
        'lines': 0,
    }
    
    # Initialisiere ComponentClass Klasse
    component_handler = ComponentClass.ComponentHandler()
    
    # Initialisiere die start time
    start_time = time.time()
        
    block = ComponentClass.Block(Const.START_COLUMN, screen)  # Erstellen Sie eine einzelne Block-Instanz
    state['highscore'] = component_handler.load_highscore()  # Initialisieren Sie den Highscore
    background = pygame.image.load('background.jpeg')  # Laden Sie das Hintergrundbild
    background.set_alpha(128)  # erh�hen der Transparenz des Hintergrundbildes
    background = pygame.transform.smoothscale(background, (650, 600))  # Skalieren Sie das Bild auf 650x600
    link_rect = screen_handler.link_screen()
    print(link_rect)

    while True: # Spiel loop
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if state['start_timer'] or state['start'] == False:
            draw_start_screen(screen, background, state)
            event_handler.handle_start_event(state, link_rect)
            state['start_timer'] = False
        
        draw_game(screen, background, game_field, state)
        
        if state['paused']:
            draw_pause_screen()
        if state['quit_game'] and not state['quit_yes']:
            draw_quit_screen(state)

        handle_events(block, game_field, state, link_rect)

        if not state['paused'] and not state['quit_game'] and not state['quit_yes']:
            block.draw()  # Zeichnen Sie den Block
            if elapsed_time >= 1 / state['speed']:
                block = block_move(state, block, component_handler, game_field, background)
                start_time = time.time()  # Setzen Sie den Timer zurück           
            screen_handler.score_screen(state)
        
            if state['quit_yes']: # Das Spiel wurde vom Spieler beendet
                reset_game(state, game_field, screen_handler, background, component_handler)
      
            pygame.display.flip()
            clock.tick(60)

spiel()
pygame.quit()