import pygame

def draw(window, background, bg_image, player=None, objects=None, offset_x=None, offset_y=None, items=None):
    for tile in background:
        window.blit(bg_image, tile)

    if objects != None:
        for obj in objects:
            obj.draw(window, offset_x, offset_y)

    if items != None:
        for item in items:
            item.draw(window, offset_x, offset_y)

    if player != None:
        player.draw(window, offset_x, offset_y)

def draw_text(text, size, text_color, x, y, boxed=None, dx=None, dy=None, surface=None):
    #BACKGROUND (SHADOW) 8514oem Regular, System Bold, Terminal, 
    font_bg = pygame.font.SysFont("Agency FB", size + 2, False)
    image_bg = font_bg.render(text, True, (0,0,0))
    rect_bg = pygame.Rect(x - 8, y+1, image_bg.get_width() + 20, image_bg.get_height() + 4)
    #FOREGROUND (FONT)
    font_fg = pygame.font.SysFont("Agency FB", size + 2, False)
    image_fg = font_fg.render(text, True, text_color)
    rect_fg = pygame.Rect(x - 8, y+1, image_fg.get_width() + 20, image_fg.get_height() + 4)

    if boxed == None:
    #draws background and foreground, offsetting background for 'shadow' effect
        if dx == None and dy == None:
            surface.blit(image_bg, (x + 3, y + 3))
            surface.blit(image_fg, (x, y))

        elif dx == None:
            surface.blit(image_bg, (x + 3, y - dy + 3))
            surface.blit(image_fg, (x, y - dy))
        elif dy == None:
            surface.blit(image_bg, (x - dx + 3, y + 3))
            surface.blit(image_fg, (x - dx, y))
        else:
            surface.blit(image_bg, (x - dx + 3, y - dy + 3))
            surface.blit(image_fg, (x - dx, y - dy))

    elif boxed:
        pygame.draw.rect(surface, (0,150,255), rect_fg, 0, 3)
        pygame.draw.rect(surface, (0,0,0), rect_bg, 3, 3)
        if dx == None and dy == None:
            surface.blit(image_bg, (x + 3, y + 3))
            surface.blit(image_fg, (x, y))
        elif dx == None:
            surface.blit(image_bg, (x + 3, y - dy + 3))
            surface.blit(image_fg, (x, y - dy))
        elif dy == None:
            surface.blit(image_bg, (x - dx + 3, y + 3))
            surface.blit(image_fg, (x - dx, y))
        else:
            surface.blit(image_bg, (x - dx + 3, y - dy + 3))
            surface.blit(image_fg, (x - dx, y - dy))
