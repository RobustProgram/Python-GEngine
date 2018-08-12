import pygame
import GEngineCore as Core

class Sprite(pygame.sprite.Sprite):
    def __init__(self,image,centerPoint,colorkey=None,size=24):
        pygame.sprite.Sprite.__init__(self)
        #Image and Rect are set here
        self.image,rect = Core.Load_Image(image,colorkey,size)
        self.rect = self.image.get_rect()
        #Moves the rect to the center
        self.rect.center = centerPoint
