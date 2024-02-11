import pygame
from os.path import isfile, join
from os import listdir
import draw

pygame.init()

#window settings (top caption, dimensions, fps)
pygame.display.set_caption("Flippy Flop")
Width, Height = 1000, 800
FPS = 60
window = pygame.display.set_mode((Width, Height))
player_velocity = 5
MAX_LEVEL = 0

#each small square is 8 pixels pygame.Rect(starting x, starting y, for x pixels, for y pixels)
#48x48 blocks (96 size)
concrete = (0,0, 48, 48)
wood = (0, 64, 48, 48)
leaf = (0, 128, 48, 48)
green_grass = (96, 0, 48, 48)
orange_grass = (96, 64, 48, 48)
pink_grass = (96, 128, 48, 48)
brick = (272, 64, 48, 48)

#thin bridges (48x4)
gold_bridge = (272, 0, 48, 4)
bronze_bridge = (272, 16, 48, 4)
silver_bridge = (272, 32, 48, 4)

#metallic blocks 
#1 - 48x16
#2 - 16x16
#3 - 32x32
#4 - 16x48
bronze_long = (192, 0, 48, 16)
bronze_small = (192, 16, 16, 16)
bronze_med = (208, 16, 32, 32)
bronze_tall = (240, 0, 16, 48)

silver_long = (192, 64, 48, 16)
silver_small = (192, 80, 16, 16)
silver_med = (208, 80, 32, 32)
silver_tall = (240, 64, 16, 48)

lego_long = (192, 128, 48, 16)
lego_small = (192, 144, 16, 16)
lego_med = (208, 144, 32, 32)
lego_tall = (240, 128, 16, 48)

gold_long = (272, 128, 48, 16)
gold_small = (272, 144, 16, 16)
gold_med = (288, 144, 32, 32)
gold_tall = (320, 128, 16, 48)



def flip_x(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False, dir3=None):
    all_sprites = {}
    #load every single file in directory
    if dir3 == None:
        path = join("assets", dir1, dir2)
    else:
        path = join("assets", dir1, dir2, dir3)

    images = [f for f in listdir(path) if isfile(join(path, f))]
    for image in images:
        #creates sheet, appends path, and removes unused pixels for sprite sheet
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        #splits sheet into width of individual animation frames based on width
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)

            #blit = draw (so below draws only the specific animation frame of the sheet)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            #we want multidirectional sprites (falling/running/jumping left and right)
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip_x(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(block_tuple):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((block_tuple[2],  block_tuple[3]), pygame.SRCALPHA, 32)
    rect = pygame.Rect(block_tuple[0], block_tuple[1], block_tuple[2], block_tuple[3])
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_floor(block_tuple):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((block_tuple[2], block_tuple[3]), pygame.SRCALPHA, 32)
    #removing some pixels from left of block so they tile without edges
    rect = pygame.Rect(block_tuple[0]+2, block_tuple[1], block_tuple[2], block_tuple[3])
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_item(width, height, folder, subfolder=None, name=None):
    if subfolder != None and name != None:
        path = join("assets", "Items", folder, subfolder, name)
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(0,0, width, height)
        surface.blit(image, (0,0), rect)
        return 0, pygame.transform.scale2x(surface)

    if subfolder == None and name != None:
        sprites = load_sprite_sheets("Items", folder, width, height)
        return 1, sprites


def get_background(name, Width, Height):
    #sets image for background tiling (ENSURE PATH IS CORRECT!!)
    image = pygame.image.load(join("assets", "Background", name))

    #_ means we do not care about this value, width and height are the pixel values of our chosen image
    _, _, width, height = image.get_rect()
    tiles = []

    #creates specified positions for background tiles to be placed
    for i in range(Width // width + 1):
        for j in range(Height // height + 1):
            pos = (i * width, j * height) 
            tiles.append(pos)

    return tiles, image 