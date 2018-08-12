"""
    GEngineCore.pyw contains all of the necessary code
    functions and variables that will be used by all other
    pyw files.
"""
import pygame, os, sys
import DataParser as Config
import LevelParser as Level

"""
    Global usable variables
"""
G_C_LEVEL = []
G_C_CURRENTLEVEL = 0
G_C_DIFFICULTY = 0
G_C_GRAVITY = True
G_C_GRAVITY_AMOUNT = 0.9
G_C_BLOCK_SIZE = 0
G_C_LEVEL_DIRECTORY = []
ConfigData = Config.GEngineConfig()


"""
    Global usable functions
"""
def Load_Image(name,colorkey=None,size=24):
    #Loads the images and their prereqs
    try:
        image = pygame.image.load(name)
    except (pygame.error):
        print('Cannot load image:' + str(name))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    image = pygame.transform.scale(image,(size,size))
    return image, image.get_rect()

def Load_Level_List():
    file = open("EngineDataFile/EngineConfig/GEngineLevels.txt")
    for a in file:
        G_C_LEVEL_DIRECTORY.append(a)

def Load_Level(directory):
    G_C_Level = Level.GameLevel(directory)
    Block = G_C_Level.GetData("Tile")
    Sprite = G_C_Level.GetData("Sprite")
    Data = G_C_Level.GetData("Data")
    return Block, Sprite, Data
