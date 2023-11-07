import pygame
import EventHandlerClass
import ScreenHandlerClass
import ComponentClass

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

# Initialisiere ComponentClass Klasse
component_handler = ComponentClass.ComponentHandler()
  
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
        'points': 0,
        'highscore': 0,
        'lines': 0,
    }

    block = ComponentClass.Block(5, screen)  # Erstellen Sie eine einzelne Block-Instanz
    state['highscore'] = component_handler.load_highscore()  # Initialisieren Sie den Highscore
    background = pygame.image.load('background.jpeg')  # Laden Sie das Hintergrundbild
    background.set_alpha(128)  # erh�hen der Transparenz des Hintergrundbildes
    background = pygame.transform.smoothscale(background, (650, 600))  # Skalieren Sie das Bild auf 650x600
     
    while True: # Spiel loop
        if state['start_timer'] or state['start'] == False:
            screen.fill((0,0,0))
            screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
            screen_handler.score_screen(state)  
            screen_handler.start_screen()
            pygame.display.flip()
            event_handler.handle_start_event(state, link_rect)
            state['start_timer'] = False
            
        screen.fill((0,0,0))
        screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
        game_field.draw()  # Zeichnen Sie das Spielfeld
        if state['paused']:
            screen_handler.pause_screen()
            screen_handler.score_screen(state)
        if state['quit_game'] and not state['quit_yes']:
            screen_handler.quit_screen()
            screen_handler.score_screen(state)
            pygame.display.flip()
        events = pygame.event.get()    
        event_handler.handle_mouse_event(events, link_rect)
        event_handler.handle_keyboard_event(events, block, game_field, state)

        while not state['paused'] and not state['quit_game'] and not state['quit_yes']:
            block.draw()  # Zeichnen Sie den Block
            if counter % (40 // state['speed']) == 0: 
                if not block.reached_bottom:  # überprüfen Sie, ob der Block den Boden noch nicht erreicht hat
                    block.row += 1  # Bewegen Sie den Block eine Zeile nach unten
                    if block.collides(game_field):  # überprüfen Sie, ob der Block mit dem Spielfeld kollidiert
                        block.row -= 1  # Bewegen Sie den Block eine Zeile nach oben
                        block.reached_bottom = True  # Setzen Sie reached_bottom auf True, da der Block den Boden erreicht hat
                        state['points'] += Const.POINTS_BLOCK  # Erhöhen Sie die Punkte um die Punkte für einen Block
                        game_field.add_block(block)  # Fügen Sie den Block zum Spielfeld hinzu
                        removed_rows = game_field.remove_full_rows()  # Entfernen Sie volle Reihen vom Spielfeld und speichern Sie die Anzahl der entfernten Reihen
                        if removed_rows is not None:  # überprüfen Sie, ob Reihen entfernt wurden
                            state['points'] += removed_rows * Const.POINTS_ROW  # Erhöhen Sie die Punkte um die Anzahl der entfernten Reihen multipliziert mit den Punkten pro Reihe
                            state['lines'] += removed_rows
                        state['level'] = component_handler.game_level(state)
                        block = ComponentClass.Block(5,screen)  # Erstellen Sie einen neuen Block
                        state['speed'] = 1 * state['level']                       
                        if block.collides(game_field):  # überprüfen Sie, ob der neue Block mit dem Spielfeld kollidiert
                            state['highscore'] = component_handler.game_quit(state, game_field, screen_handler)
                            state['points'] = 0
                            state['lines'] = 0
                            pygame.display.flip()  
                            event_handler.handle_gameover_event(state, link_rect)
            counter += 1
            screen_handler.score_screen(state)
            break
        if state['quit_yes']: # Das Spiel wurde vom Spieler beendet
            screen.fill((0,0,0))
            screen.blit(background, (0, 0))  # Zeichnen Sie das Hintergrundbild
            state['highscore'] = component_handler.game_quit(state, game_field, screen_handler)
            state['points'] = 0
            state['lines'] = 0
            pygame.display.flip()
            block = ComponentClass.Block(5,screen)  # Erstellen Sie einen neuen Block    
            event_handler.handle_gameover_event(state, link_rect)
            state['quit_yes'] = False
            state['quit_game'] = False 
      
        pygame.display.flip()
        clock.tick(60)

spiel()
pygame.quit()
