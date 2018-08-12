import sys, os, pygame
import GEngineCore as Core
import BaseSprite

class PlayerSprite(BaseSprite.Sprite):
    def __init__(self,image,centerpoint,colorkey=None,size=24):
        BaseSprite.Sprite.__init__(self,image,centerpoint,colorkey,size)
        self.size = size
        self.spawnpoint = centerpoint
        self.life = 3
        self.kills = 0
        self.xv = 0
        self.yv = 0
        self.falling = False
        self.jumping = False
        self.HorSpeed = int(Core.ConfigData.ReturnData("horizontal_speed"))
        self.VertSpeed = int(Core.ConfigData.ReturnData("vertical_speed"))
        self.dead = False
        
    def update(self,platforms,enemygroup,levelwidth,levelheight,controlled = True):
        self.Keys = pygame.key.get_pressed()
        if self.falling == True:
            self.yv += Core.G_C_GRAVITY_AMOUNT

        if(controlled == True):
            if self.Keys[pygame.K_LEFT]:
                self.xv = -self.HorSpeed
            elif self.Keys[pygame.K_RIGHT]:
                self.xv = self.HorSpeed
            else:
                self.xv = 0
            if self.Keys[pygame.K_UP] and self.jumping != True:
                self.yv = -self.VertSpeed
                self.jumping = True
            if self.Keys[pygame.K_DOWN] and Core.G_C_GRAVITY == False:
                self.yv = self.VertSpeed

        self.rect.left += self.xv
        if not(platforms == None):
            self.Collision(self.xv,0,platforms)
        self.rect.top += self.yv
        self.falling = True
        if not(platforms == None):
            self.Collision(0,self.yv,platforms)

        if not(enemygroup == None):
            self.UpdateStatus(enemygroup,levelwidth,levelheight)

    def Collision(self,xv,yv,platforms):
        for p in platforms:
            if(pygame.sprite.collide_rect(self,p)):
                if(xv < 0):
                    self.rect.left = p.rect.right
                elif(xv > 0):
                    self.rect.right = p.rect.left
                if(yv > 0):
                    self.rect.bottom = p.rect.top
                    self.yv = 0
                    self.falling = False
                    self.jumping = False
                elif(yv < 0):
                    self.rect.top = p.rect.bottom
                    self.yv = 0

    #updates the current status of the player
    #whether he collided with a sprite killing it or killing himself
    def UpdateStatus(self,enemygroup,levelwidth,levelheight):
        if(self.rect.top + 10 > levelheight):
            self.Died()
        elif(len(pygame.sprite.spritecollide(self,enemygroup,0)) > 0):
            collidedy = pygame.sprite.spritecollide(self,enemygroup,0)[0].rect.top
            if (self.rect.bottom > collidedy + self.size/2):
                self.Died()
            else:
                self.yv *= -1
                pygame.sprite.spritecollide(self,enemygroup,0)[0].kill()
                self.kills += 1

    #sets the died property to True
    #deduces a point from the life attribute
    def Died(self):
        self.dead = True
        self.life -= 1
        self.yv = -5

    def Respawn(self):
        self.yv = 0
        self.xv = 0
        self.rect.center = self.spawnpoint

    def DeathAnimation(self):
        self.xv = 0
        self.update(None,None,None,False)
        
