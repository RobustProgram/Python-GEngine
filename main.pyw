import sys, os ,pygame
import BaseSprite
import EnemySprite
import Player
import GEngineCore as Core
import Menu
import TextScreen
from pygame.locals import *

class GEngine:
    def __init__(self,WIDTH=640,HEIGHT=480):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.caption = pygame.display.set_caption("GEngine")
        self.Running = True
        self.clock = pygame.time.Clock()

    def GEngineLoop(self):
        self.GEngineInitialization()
        main_MenuRunning = True
        main_GameRunning = False
        main_InstructionsRunning = False
        main_MenuButtonResults = -1
        main_Cutscene = False
        
        while self.Running == True:
            self.clock.tick(60)
            self.mouse_event = 0
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            if main_GameRunning == True:
                self.GEngineDebugText()
                #updates the player and enemies
                if(main_Cutscene == False):
                    self.EnemyGroup.update(self.CollisionBlocks,self.width,self.height)
                    self.Player.update(self.CollisionBlocks,self.EnemyGroup,self.width,self.height)
                    if(self.Player.dead == True):
                        main_Cutscene = True
                        a=0
                elif(main_Cutscene == True):
                    if(a == 0):
                        a += 1
                        pygame.mixer.init()
                        pygame.mixer.music.load("EngineDataFile/Sounds/death.mp3")
                        pygame.mixer.music.play()
                    self.Player.DeathAnimation()
                    if(pygame.mixer.music.get_busy() == False):
                        self.Player.dead = False
                        self.Player.Respawn()
                        self.Block_Group.empty()
                        self.CollisionBlocks.empty()
                        self.EnemyGroup.empty()
                        self.GEngineGenerateSprites(False)
                        self.GEngineGenerateTile()
                        main_Cutscene = False
                    

                self.EnemyGroup.draw(self.screen)
                self.Player_Group.draw(self.screen)
                self.Block_Group.draw(self.screen)
                    
            else:
                if main_MenuRunning == True:
                    main_MenuButtonResults = self.GameMenu.drawButtons(event)
                    if main_MenuButtonResults == 0:
                        main_MenuRunning = False
                        self.GEngineGenerateSprites()
                        self.GEngineGenerateTile()
                        main_GameRunning = True
                    elif main_MenuButtonResults == 2:
                        main_MenuRunning = False
                        main_InstructionsRunning = True
                        
                if main_InstructionsRunning == True:
                    main_MenuButtonResults = self.GameText.drawText(event)
                    if main_MenuButtonResults == 0:
                        main_InstructionsRunning = False
                        main_MenuRunning = True


            pygame.display.flip()

    def GEngineInitialization(self):
        #This is where you put the initial
        #functions that will run once

        self.Running = True
        Core.G_C_BLOCK_SIZE = int(Core.ConfigData.ReturnData("BLOCK_SIZE"))
        Core.G_C_GRAVITY_AMOUNT = float(Core.ConfigData.ReturnData("GRAVITY_AMOUNT"))
        Core.Load_Level_List()
        self.level, self.sprites, self.leveldimensions = Core.Load_Level(Core.G_C_LEVEL_DIRECTORY[0])
        x,y = self.leveldimensions[0]
        self.gamewidth = int(x)
        self.gameheight = int(y)
        self.Block_Group = pygame.sprite.Group()
        self.CollisionBlocks = pygame.sprite.Group()
        self.Player_Group = pygame.sprite.Group()
        self.EnemyGroup = pygame.sprite.Group()
        #-----------------------------------
        self.GameMenu = Menu.GMenu(0,['New Game','Load Game','Instructions','Quit'],100,25,self.screen,"EngineDataFile/Images/menu_logo.png")
        self.GameText = TextScreen.TextScreen(["Return"],"Jump and win",self.screen)

    def GEngineGenerateSprites(self,generatePlayer = True):
        for a in self.sprites:
            x,y,t,_ = a
            x = int(x)
            y = int(y)
            t = int(t)
            if(t == 0) and (generatePlayer == True):
                centerpoint = ((x - (Core.G_C_BLOCK_SIZE/2)),(y - (Core.G_C_BLOCK_SIZE/2)))
                self.Player = Player.PlayerSprite("EngineDataFile/Images/player.png",centerpoint,-1)
                self.Player_Group.add((self.Player))
            if(t == 1):
                centerpoint = ((x - (Core.G_C_BLOCK_SIZE/2)),(y - (Core.G_C_BLOCK_SIZE/2)))
                self.Enemy = EnemySprite.EnemySprite(0,"EngineDataFile/Images/soldier.png",centerpoint,1000,-1)
                self.EnemyGroup.add((self.Enemy))
                print(self.EnemyGroup)
    
    def GEngineGenerateTile(self):
        for a in self.level:
            x,y,t,s = a
            x = int(x)
            y = int(y)
            t = int(t)
            if(t == 1):
                centerpoint = ((x - (Core.G_C_BLOCK_SIZE/2)),(y - (Core.G_C_BLOCK_SIZE/2)))
                self.Block = BaseSprite.Sprite("EngineDataFile/Images/block.png",centerpoint,None,Core.G_C_BLOCK_SIZE)
                if(s == "True"):
                    self.CollisionBlocks.add(self.Block)
                self.Block_Group.add((self.Block))

    def GEngineDebugText(self):
        stringtext = ["Player Life","Player Kills","Player Hor Speed","Player Vert Speed","Gravity","Player Y"]
        stringtext2 = [self.Player.life,self.Player.kills,self.Player.xv,self.Player.yv,Core.G_C_GRAVITY_AMOUNT,self.Player.rect.top]
        _,y = self.screen.get_size()
        startingy = y - (len(stringtext) * 15)
        debugfont = pygame.font.SysFont("monospace",15)
        for a in range(len(stringtext)):
            temp = debugfont.render(stringtext[a] + " " + str(stringtext2[a]),1,(255,255,0))
            self.screen.blit(temp,(0,startingy + 15 * a))

if __name__ == "__main__":
    MainGame = GEngine()
    MainGame.GEngineLoop()
