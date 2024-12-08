from game import CluedoGame
from utils import *
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
    # Define colors
    BG = (0, 143, 213)

    is_running = True
    game_winner = None
    time = pygame.time.get_ticks()
    while is_running:
        screen.fill(BG)

        mouse_down = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

        if game_winner == None:
            do_turn = draw_button("Next", (10, 500), (100, 60), screen) and mouse_down
            curr_time = pygame.time.get_ticks()
            if do_turn:
                time = curr_time
                game_winner = game.do_turn()
                
        # Draw
        game.draw(screen)
        if game_winner != None:
            draw_text(f"Player {game_winner.id.name} won the game, the solution was {game.solution[0].name}, {game.solution[1].name}, and {game.solution[2].name}", (100,255,100), (10, 500), screen)

        # Update display
        pygame.display.flip()

    pygame.quit()
    

if __name__ == "__main__":
    main()
