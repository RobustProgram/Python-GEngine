import sys, os, pygame
import GEngineCore as Core
import BaseSprite

class EnemySprite(BaseSprite.Sprite):
    def __init__(self,enemytype,image,centerpoint,health,colorkey=None,size=24):
        BaseSprite.Sprite.__init__(self,image,centerpoint,colorkey,size)
        self.health = health
        self.type = enemytype
        self.xv = 1
        self.yv = 0
        self.falling = False

    def update(self,platforms,levelwidth,levelheight):
        if self.falling == True:
            self.yv += Core.G_C_GRAVITY_AMOUNT
            
        self.rect.left += self.xv
        self.Collision(self.xv,0,platforms)
        self.rect.top += self.yv
        self.falling = True
        self.Collision(0,self.yv,platforms)
        
        if(self.rect.top + 10 > levelheight):
            self.kill()
        
    def Collision(self,xv,yv,platforms):
        for p in platforms:
            if(pygame.sprite.collide_rect(self,p)):
                if(xv < 0):
                    self.rect.left = p.rect.right
                    self.xv *= -1
                elif(xv > 0):
                    self.rect.right = p.rect.left
                    self.xv *= -1
                if(yv > 0):
                    self.rect.bottom = p.rect.top
                    self.yv = 0
                    self.falling = False
                    self.jumping = False
                elif(yv < 0):
                    self.rect.top = p.rect.bottom
                    self.yv = 0
