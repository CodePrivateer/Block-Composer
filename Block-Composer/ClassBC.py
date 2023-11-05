import pygame
import Const

class KeyboardHandler:       
    def handle_event(self, event, blocks, game_field, state):
        if event.key == pygame.K_p:
            state['paused'] = not state['paused']
        if event.key == pygame.K_q:
            state['quit_game'] = not state['quit_game']
        if event.key == pygame.K_y:
            if state['quit_game']:
                state['quit_yes'] = True
        if event.key == pygame.K_LEFT:  # Wenn die gedr�ckte Taste die linke Pfeiltaste ist
            if blocks[-1].column > 0:  # Wenn der Block nicht am linken Rand ist
                blocks[-1].column -= 1  # Bewegen Sie den Block eine Spalte nach links
                if blocks[-1].collides(game_field):  # �berpr�fen Sie, ob der Block mit dem Spielfeld kollidiert
                    blocks[-1].column += 1  # Wenn ja, bewegen Sie den Block eine Spalte nach rechts zur�ck
        elif event.key == pygame.K_RIGHT:  # Wenn die gedr�ckte Taste die rechte Pfeiltaste ist
            if blocks[-1].column < Const.SCREEN_WIDTH / Const.BLOCK_SIZE - len(blocks[-1].shape[0]):  # Wenn der Block nicht am rechten Rand ist
                blocks[-1].column += 1  # Bewegen Sie den Block eine Spalte nach rechts
                if blocks[-1].collides(game_field):  # �berpr�fen Sie, ob der Block mit dem Spielfeld kollidiert
                    blocks[-1].column -= 1  # Wenn ja, bewegen Sie den Block eine Spalte nach links zur�ck
        elif event.key == pygame.K_SPACE:  # Wenn die gedr�ckte Taste die Leertaste ist
            blocks[-1].rotate(game_field)  # Drehen Sie den Block und �bergeben Sie das Spielfeld an die rotate-Methode zur Kollisionspr�fung
        elif event.key == pygame.K_DOWN:  # Wenn die gedr�ckte Taste die Pfeiltaste nach unten ist
            state['speed'] = 10 * state['level']  # Erh�hen Sie die Geschwindigkeit, mit der der Block f�llt
    
    def handle_start_event(self, event, blocks, game_field, state):
        while True:
            pygame.time.wait(100)  # Warten Sie 100 Millisekunden
            for event in pygame.event.get():  # Durchlaufen Sie alle aufgetretenen Ereignisse
                if event.type == pygame.QUIT:  # Wenn das Ereignis QUIT ist (z.B. Schlie�en des Fensters)
                    return  # Beenden Sie die Funktion
                elif event.type == pygame.KEYDOWN:  # Wenn das Ereignis ein Tastendruck ist
                    state['start'] = not state['start']
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Wenn das Ereignis ein Mausklick ist
                    if state['link_rect'].collidepoint(pygame.mouse.get_pos()):  # Wenn der Mausklick innerhalb des link_rect ist
                        webbrowser.open("https://github.com/CodePrivateer/Block-Composer")  # �ffnen Sie den Webbrowser mit der angegebenen URL
            if state['start']:
                break