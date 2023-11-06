import pygame
import Const
import webbrowser

class EventHandler:       
    def handle_keyboard_event(self, events, blocks, game_field, state):
        for event in events:  # Durchlaufen Sie alle aufgetretenen Ereignisse
            if event.type == pygame.QUIT:  # Wenn das Ereignis QUIT ist (z.B. Schließen des Fensters)
                pygame.quit()  # Beenden Sie die Funktion
            elif event.type == pygame.KEYDOWN:  # Wenn das Ereignis ein Tastendruck ist
                if event.key == pygame.K_p:
                    state['paused'] = not state['paused']
                if event.key == pygame.K_q:
                    state['quit_game'] = not state['quit_game']
                if event.key == pygame.K_y:
                    if state['quit_game']:
                        state['quit_yes'] = True
                if event.key == pygame.K_LEFT:  # Wenn die gedrückte Taste die linke Pfeiltaste ist
                    if blocks[-1].column > 0:  # Wenn der Block nicht am linken Rand ist
                        blocks[-1].column -= 1  # Bewegen Sie den Block eine Spalte nach links
                        if blocks[-1].collides(game_field):  # überprüfen Sie, ob der Block mit dem Spielfeld kollidiert
                            blocks[-1].column += 1  # Wenn ja, bewegen Sie den Block eine Spalte nach rechts zurück
                elif event.key == pygame.K_RIGHT:  # Wenn die gedrückte Taste die rechte Pfeiltaste ist
                    if blocks[-1].column < Const.SCREEN_WIDTH / Const.BLOCK_SIZE - len(blocks[-1].shape[0]):  # Wenn der Block nicht am rechten Rand ist
                        blocks[-1].column += 1  # Bewegen Sie den Block eine Spalte nach rechts
                        if blocks[-1].collides(game_field):  # überprüfen Sie, ob der Block mit dem Spielfeld kollidiert
                            blocks[-1].column -= 1  # Wenn ja, bewegen Sie den Block eine Spalte nach links zurück
                elif event.key == pygame.K_SPACE:  # Wenn die gedrückte Taste die Leertaste ist
                    blocks[-1].rotate(game_field)  # Drehen Sie den Block und übergeben Sie das Spielfeld an die rotate-Methode zur Kollisionsprüfung
                elif event.key == pygame.K_DOWN:  # Wenn die gedrückte Taste die Pfeiltaste nach unten ist
                    state['speed'] = 10 * state['level']  # Erhöhen Sie die Geschwindigkeit, mit der der Block fällt
                    
    def handle_mouse_event(self, events, link_rect):
        for event in events:  # Durchlaufen Sie alle aufgetretenen Ereignisse
            if event.type == pygame.QUIT:  # Wenn das Ereignis QUIT ist (z.B. Schließen des Fensters)
                pygame.quit()  # Beenden Sie die Funktion
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Wenn das Ereignis ein Mausklick ist
                if link_rect.collidepoint(pygame.mouse.get_pos()):  # Wenn der Mausklick innerhalb des link_rect ist
                    webbrowser.open("https://github.com/CodePrivateer/Block-Composer")  # Öffnen Sie den Webbrowser mit der angegebenen URL   
                    
    def handle_start_event(self, state, link_rect):
        event_handler = EventHandler()
        while True:
            pygame.time.wait(100)  # Warten Sie 100 Millisekunden
            events = pygame.event.get()
            for event in events:  # Durchlaufen Sie alle aufgetretenen Ereignisse
                if event.type == pygame.QUIT:  # Wenn das Ereignis QUIT ist (z.B. Schließen des Fensters)
                    pygame.quit()  # Beenden Sie die Funktion
                elif event.type == pygame.KEYDOWN:  # Wenn das Ereignis ein Tastendruck ist
                    state['start'] = not state['start']
            event_handler.handle_mouse_event(events, link_rect)
            if state['start']:
                break

    def handle_gameover_event(self, state, blocks, new_block):
        state['restart_game'] = False 
        while True:
            pygame.time.wait(100)  # Warten Sie 100 Millisekunden
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  
                elif event.type == pygame.KEYDOWN:  
                    blocks.append(new_block)  # Fügen Sie den neuen Block zur Liste hinzu und starten Sie das Spiel neu
                    state['restart_game'] = True  
                    break  
            if state['restart_game']:  
                break  

            
