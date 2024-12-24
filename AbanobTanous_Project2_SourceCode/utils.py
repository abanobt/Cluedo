import pygame

FONT = None

def draw_text(text, color, position, screen):
    """
    Renders text onto a Pygame screen at the specified position.
    
    Parameters:
    - text (str): The string to be rendered.
    - color (tuple): RGB tuple specifying the color of the text (e.g., (255, 255, 255) for white).
    - position (tuple): The (x, y) position where the text will be drawn on the screen.
    - screen (pygame.Surface): The Pygame surface on which the text will be rendered.
    """
    global FONT
    if FONT == None:
        FONT = pygame.font.Font(None, 22)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.topleft = position
    screen.blit(text_surface, text_rect)

