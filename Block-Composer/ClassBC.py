import pygame
import Const

class KeyboardHandler:       
    def handle_event(self, event, blocks, game_field, state):
        if event.type == pygame.KEYDOWN:
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