import pygame
import load
import draw

FPS = 60

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load.load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    
    DMG_IMMUNE = False

    def __init__(self, x, y, width, height, exp, talents):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.health = 3
        
        self.victory = False
        self.low_grav = False
        self.low_grav_timer = 0
        self.coins = 0
        self.lvl_timer = 0
        self.in_level = False
        self.countdown = False
        self.experience = exp
        self.player_level = 1
        self.talent_points = talents[4]
        self.used_talent_points = talents[5]
        self.health_talent_point = talents[0]
        self.run_speed_talent_point = talents[1]
        self.level_time_talent_point = talents[2]
        self.jump_talent_point = talents[3]
        self.MAX_HEALTH = 3 + self.health_talent_point
        self.ANIMATION_DELAY = 5 - self.run_speed_talent_point
        
    def check_level(self):
        if self.experience > 1000:
            self.player_level = 8
        elif self.experience > 750:
            self.player_level = 7
        elif self.experience > 550:
            self.player_level = 6
        elif self.experience > 400:
            self.player_level = 5
        elif self.experience > 300:
            self.player_level = 4
        elif self.experience > 250:
            self.player_level = 3
        elif self.experience > 50:
            self.player_level = 2

        if self.talent_points + self.used_talent_points != self.player_level - 1:
            self.talent_points = self.player_level - self.used_talent_points - 1
    
    def level_up(self):
        level_before = self.player_level
        self.check_level()
        level_after = self.player_level
        if level_before == level_after:
            return (False, 0) 
        else:
            change = level_after - level_before
            return (True, change)


    def timer_active(self):
        if not self.victory:
            if self.countdown:
                self.lvl_timer += 1

    def victorious(self):
        self.victory = True

    def make_hit(self):
        if not self.DMG_IMMUNE:
            self.hit = True
            self.health -= 1
            self.hit_count = 0

    def heal(self):
        self.health = self.MAX_HEALTH
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel - self.run_speed_talent_point/2
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel + self.run_speed_talent_point/2
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * (6.1 + self.jump_talent_point / 3)
        self.animation_count = 0
        self.jump_count += 1
        self.fall_count = 0
    
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.fall_count = 0
        self.y_vel = 0

    def moon_grav(self):
        self.low_grav = True

    def loop(self, fps):
        if self.low_grav_timer > 0:
            self.y_vel += min(0.15, (self.fall_count / FPS) * self.GRAVITY)
        else:
            self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)

        self.timer_active()

        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
            self.DMG_IMMUNE = True
        if self.hit_count == FPS:
            self.hit = False
            self.hit_count = 0
            self.DMG_IMMUNE = False

        if self.low_grav:
            self.low_grav_timer += 1
        if self.low_grav_timer == FPS * 5:
            self.low_grav = False
            self.low_grav_timer = 0
        
        self.fall_count += 1
        self.update_sprite()
        
    def update_sprite(self):
        #base state
        sprite_sheet = "idle"

       
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0 and self.jump_count == 1:
            sprite_sheet = "jump"
        elif self.y_vel < 0 and self.jump_count == 2:
            sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY*2:
            sprite_sheet = "fall" 

        #if moving but not jumping
        elif self.x_vel != 0:
                sprite_sheet = "run"
        #specifies which direction to pull correct sprites (recall the flip ---> run_left, etc...)
        sprite_sheet_direction = sprite_sheet + "_" + self.direction
        #creates a list of sprites for animation 
        sprites = self.SPRITES[sprite_sheet_direction]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, window, offset_x, offset_y):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))