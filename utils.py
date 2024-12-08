import pygame

FONT = None

def draw_text(text, color, position, screen):
    global FONT
    if FONT == None:
        FONT = pygame.font.Font(None, 20)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.topleft = position
    screen.blit(text_surface, text_rect)

def draw_button(text, position, size, screen):
    mouse = pygame.mouse.get_pos()
    is_hovering = mouse[0] > position[0] and mouse[0] < position[0] + size[0] \
            and mouse[1] > position[1] and mouse[1] < position[1] + size[1]
    pygame.draw.rect(screen, (0,100,200) if is_hovering else (0,0,0), [position[0],position[1],size[0],size[1]])
    global FONT
    if FONT == None:
        FONT = pygame.font.Font(None, 25)
    text_surface = FONT.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (position[0] + (size[0] - text_rect.width) / 2, position[1] + (size[1] - text_rect.height) / 2)
    screen.blit(text_surface, text_rect)
    return is_hovering

