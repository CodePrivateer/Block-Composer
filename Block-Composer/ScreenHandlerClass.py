import pygame
import Const

class ScreenHandler:
    def __init__(self, screen):
        self.screen = screen
        
    def draw_surface(self, s_width, s_height, alpha, color, pos_x, pos_y):
        s = pygame.Surface((s_width, s_height))  # Erstellen Sie eine Oberfl�che
        s.set_alpha(alpha)  # Stellen Sie die Transparenz auf 50%
        s.fill(color)  # F�llen Sie die Oberfl�che mit Dunkelblau
        self.screen.blit(s, (pos_x,pos_y))  # Blit die Oberfl�che auf den Bildschirm

    def draw_text(self, text, size, color, x, y, centered=True):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        if centered:
            self.screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
        else:
            self.screen.blit(text_surface, (x, y))
        
    def draw_link(self, text, size, color, x, y, centered=True):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect  # R�ckgabe des Rechtecks f�r Kollisionserkennung

    def game_over_screen(self):
        self.draw_surface(Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT, 128, (0,0,128), 0, 0)
        self.draw_text("Game Over", 72, (255, 255, 255), Const.SCREEN_WIDTH // 2 , Const.SCREEN_HEIGHT // 4)
        self.draw_text("Press key to play", 36, (255, 255, 255), Const.SCREEN_WIDTH // 2 , Const.SCREEN_HEIGHT // 2)

    def score_screen(self, state):
        self.draw_surface(Const.SCORE_AREA_WIDTH, Const.SCREEN_HEIGHT, 128, (0,0,128), Const.SCREEN_WIDTH ,0)
        self.draw_text(str(state['points']).zfill(4) + " Points", 36,(200,200,200),Const.SCREEN_WIDTH +10 ,10 ,centered=False)
        self.draw_text(str(state['lines']).zfill(4) + " Lines",36,(200,200,200),Const.SCREEN_WIDTH +10 ,50 ,centered=False)
        self.draw_text(str(state['level']).zfill(4) + " Level",36,(200,200,200),Const.SCREEN_WIDTH +10 ,90 ,centered=False)
        self.draw_text(str(state['highscore']).zfill(4) + " Highscore",36,(255,200,200),Const.SCREEN_WIDTH +10 ,130 ,centered=False)
        self.draw_text("Left Arrow > Shift left",24,(200,200,200),Const.SCREEN_WIDTH +10 ,210 ,centered=False)
        self.draw_text("Right Arrow > Shift Right",24,(200,200,200),Const.SCREEN_WIDTH +10 ,250 ,centered=False)
        self.draw_text("Down Arrow Key > Fast place",24,(200,200,200),Const.SCREEN_WIDTH +10 ,290 ,centered=False)
        self.draw_text("Space Key > rotate",24,(200,200,200),Const.SCREEN_WIDTH +10 ,330 ,centered=False)
        self.draw_text("'p' Key Pause",24,(200,200,200),Const.SCREEN_WIDTH +10 ,370 ,centered=False)
        self.draw_text("'q' Quit Game ",24,(200,200,200),Const.SCREEN_WIDTH +10 ,410 ,centered=False)

    def link_screen(self):
        link_rect = self.draw_link("Block-Composer on Github", 16, (200,200,200), Const.SCREEN_WIDTH +10 ,530 ,centered=False)
        return link_rect       

    def pause_screen(self):
        self.draw_surface(Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT, 128,(0,0,128),0 ,0)
        self.draw_text("Game Paused",72,(255 ,255 ,255),Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //4)
        self.draw_text("Press 'p' key to play",36,(255 ,255 ,255),Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //2)

    def start_screen(self):
        self.draw_surface(Const.SCREEN_WIDTH ,Const.SCREEN_HEIGHT ,128 ,(0 ,0 ,128) ,0 ,0)
        self.draw_text("Block-Composer",64 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //4)
        self.draw_text("Press key to play",36 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //2)

    def quit_screen(self):
        self.draw_surface(Const.SCREEN_WIDTH ,Const.SCREEN_HEIGHT ,128 ,(0 ,0 ,128) ,0 ,0)
        self.draw_text("Quit Game?",72 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //4)
        self.draw_text("Press y key to quit",36 ,(255 ,255 ,255) ,Const.SCREEN_WIDTH //2 ,Const.SCREEN_HEIGHT //2)




