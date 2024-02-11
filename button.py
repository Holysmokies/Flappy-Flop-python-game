import pygame
import draw
import load
import Flap_flop_game

from os.path import isfile, join


class Button():
    def __init__(self, x, y, image, name, scale):
        self.image = pygame.image.load(join("assets", "Menu", "Buttons", image))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.scaled = pygame.transform.scale(self.image, (int(self.width * scale), int(self.height * scale)))
        self.rect = pygame.Rect(x, y, self.width * scale, self.height * scale)
        self.name = name
        self.scale = scale
        self.clicked = False
        self.drawn = False

    def draw_button(self, surface):
        action = False
        #draw button
        surface.blit(self.scaled, (self.rect.x, self.rect.y))

        mouse_position = pygame.mouse.get_pos() 
        #check mouseover
        if self.rect.collidepoint(mouse_position) and self.drawn == True:
            draw.draw_text(self.name, 35, (255,255,255), mouse_position[0] + 20, mouse_position[1] - 35, True, surface = surface)
            #check for mouseclick
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        #once mouse is released, restores clicked status to unclicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action 
    


class level_button():
    def __init__(self, x, y, width, height, color, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.name = name
        self.clicked = False
        self.drawn = False

    def draw_lvl_btn(self, surface):
        action = False
        pygame.draw.rect(surface, self.color, self.rect, 0, 4)
        mouse_position = pygame.mouse.get_pos() 

        #check mouseover
        if self.rect.collidepoint(mouse_position) and self.drawn == True:
            pygame.draw.rect(surface, (255,255,0), self.rect, 0, 4)
            #check for mouseclick
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        #once mouse is released, restores clicked status to unclicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        pygame.draw.rect(surface, (0,0,0), self.rect, 3, 4)
        return action 



class talent_button():
    def __init__(self, x, y, width, height, color, name, talent_point_requirement):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.name = name
        self.clicked = False
        self.drawn = False
        self.req = talent_point_requirement

    def draw_lvl_btn(self, surface, available_points, talents):
        action = False
        pygame.draw.rect(surface, self.color, self.rect, 0, 4)
        
        mouse_position = pygame.mouse.get_pos()
        if self.name == "Max  Health":
            for i in range(0, 3):
                pygame.draw.rect(surface, (255,0,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 3, 4)
            for i in range(0, talents[0]):
                pygame.draw.rect(surface, (0,255,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 3, 4)
        elif self.name == "Level Time":
            for i in range(0, 2):
                pygame.draw.rect(surface, (255,0,0), (self.rect.x + (self.rect.width/2)*(i), self.rect.y + 153 , self.rect.width / 2, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x + (self.rect.width/2)*(i), self.rect.y + 153 , self.rect.width / 2, self.rect.height / 7), 3, 4)
            for i in range(0, talents[2]):
                pygame.draw.rect(surface, (0,255,0), (self.rect.x + (self.rect.width/2)*(i), self.rect.y + 153 , self.rect.width / 2, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x + (self.rect.width/2)*(i), self.rect.y + 153 , self.rect.width / 2, self.rect.height / 7), 3, 4)
        elif self.name == "Jump Upgrade":
            for i in range(0, 1):
                pygame.draw.rect(surface, (255,0,0), (self.rect.x, self.rect.y + 153 , self.rect.width, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x, self.rect.y + 153 , self.rect.width, self.rect.height / 7), 3, 4)
            for i in range(0, talents[3]):
                pygame.draw.rect(surface, (0,255,0), (self.rect.x, self.rect.y + 153 , self.rect.width, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x, self.rect.y + 153 , self.rect.width, self.rect.height / 7), 3, 4)
        elif self.name == "Run  Speed":
            for i in range(0, 3):
                pygame.draw.rect(surface, (255,0,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 3, 4)
            for i in range(0, talents[1]):
                pygame.draw.rect(surface, (0,255,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 0, 4)
                pygame.draw.rect(surface, (0,0,0), (self.rect.x + (self.rect.width/3)*(i), self.rect.y + 153 , self.rect.width / 3, self.rect.height / 7), 3, 4)
        
        
        #check mouseover
        if self.rect.collidepoint(mouse_position) and self.drawn == True:
            if self.req > available_points:
                draw.draw_text("This upgrade requires "+str(self.req)+" available talent points", 35, (255,50, 50),
                    load.Width / 4.4, load.Height - load.Height / 5, None, surface=load.window)
                #check for mouseclick
                
            else:
                pygame.draw.rect(surface, (0,255,0), self.rect, 0, 4)
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
        #once mouse is released, restores clicked status to unclicked
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        draw.draw_text(self.name, 30, (255,255,255), self.rect.left + self.rect.width / 5,
                        self.rect.top + self.rect.height / 2.9, surface=load.window)
        pygame.draw.rect(surface, (0,0,0), self.rect, 3, 4)
        return action 