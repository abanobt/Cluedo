from game import CluedoGame

import random
import pygame

def main():
    # Initialize pygame
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Cluedo")

    game = CluedoGame()

    # Main loop
    game_loop(screen, game)

    pygame.quit()

def game_loop(screen, game):
    # Define colors
    BG = (0, 143, 213)

    is_running = True
    time = pygame.time.get_ticks()
    while is_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        curr_time = pygame.time.get_ticks()
        if curr_time - time > 2000:
            time = curr_time
            game.do_turn()
        # Draw
        screen.fill(BG)
        game.draw(screen)

        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main()
