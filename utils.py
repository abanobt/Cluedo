import pygame

FONT = None

def draw_text(text, color, position, screen):
    global FONT
    if FONT == None:
        FONT = pygame.font.Font(None, 25)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.topleft = position
    screen.blit(text_surface, text_rect)

