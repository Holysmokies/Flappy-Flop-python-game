import pygame
import load
#import player_char
#import draw


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width * 2, height * 2)
        self.image = pygame.Surface((width * 2, height * 2), pygame.SRCALPHA)
        self.name = name

    def draw(self, window, offset_x, offset_y):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))  


class Block(Object):
    def __init__(self, x, y, size_x, size_y, block_tuple):
        super().__init__(x, y, size_x, size_y)
        block = load.get_block(block_tuple)
        self.image.blit(block,(0, 0))
        self.mask = pygame.mask.from_surface(self.image)



class Floor(Object):
    def __init__(self, x, y, size_x, size_y, block_tuple):
        super().__init__(x, y, size_x, size_y)
        block = load.get_floor(block_tuple)
        self.image.blit(block,(0, 0))
        self.mask = pygame.mask.from_surface(self.image)



class item(Object):
    ANIMATION_DELAY = 3



class pointer(Object):
    def __init__(self, x, y, width, height, folder, subf, name):
        super().__init__(x, y, width, height, name)
        self.item = load.load_sprite_sheets("Items", folder, dir3=subf, width=width, height=height)
        self.image = self.item["Start (Idle)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.vanish = 0



class fruit(Object):
    ANIMATION_DELAY = 4
    
    def __init__(self, x, y, width, height, folder, subf, name):
        super().__init__(x, y, width, height, name)
        self.item = load.load_sprite_sheets("Items", folder, width=width, height=height)
        self.image = self.item[name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = name
        self.collected = False
        self.vanish = 0
    
    def touch(self):
        self.collected = True
        self.animation_count = 0
        self.animation_name = "Collected"
        

    def loop(self):
        if self.collected:
            if self.vanish < load.FPS:
                self.ANIMATION_DELAY = 10
                self.vanish += 1
                sprites = self.item[self.animation_name]
                sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
                self.image = sprites[sprite_index]
                self.animation_count += 1

                self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
                self.mask = pygame.mask.from_surface(self.image)

                if self.animation_count // self.ANIMATION_DELAY > len(sprites):
                    self.animation_count = 0
        else:
            sprites = self.item[self.animation_name]
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.image = sprites[sprite_index]
            self.animation_count += 1

            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)

            if self.animation_count // self.ANIMATION_DELAY > len(sprites):
                self.animation_count = 0


class Goal(Object):
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height, folder, subf):
        super().__init__(x, y, width, height, 'goal')
        self.goal = load.load_sprite_sheets("Items", dir2=folder, width= width, height=height, dir3=subf)
        self.image = self.goal["Checkpoint (No Flag)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Checkpoint (No Flag)"
        self.vanish = 0
    
    def touch(self):
        self.animation_name = "Checkpoint (Flag Out) (64x64)"
        
    def idle(self):
        self.animation_name = "Checkpoint (Flag Idle)(64x64)"

    def loop(self):
        sprites = self.goal[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Confetti(Object):
    def __init__(self, x, y, size_x, size_y, block_tuple):
        super().__init__(x, y, size_x, size_y)
        confetti = load.get_confetti(block_tuple)
        self.image.blit(confetti, (0,0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire_trap(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height,):
        super().__init__(x, y, width, height, 'fire')
        self.fire = load.load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"
    
    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0



class Projectile(Object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = load.player_velocity * 2

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
    
