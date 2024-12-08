from game import CluedoGame
from utils import *
import random
import pygame
import pygame_gui

def main():
    # Initialize pygame
    pygame.init()

    # Create and set up the game window
    pygame.display.set_caption("Cluedo")
    screen = pygame.display.set_mode((1280, 720))
    gui_manager = pygame_gui.UIManager((1280, 720))
    
    # Create background surface and set its color
    background = pygame.Surface((1280, 720))
    background.fill((0, 143, 213))
 
    game = CluedoGame() 
        
    # Create a "Next Turn" button
    next_turn_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 530), (100, 50)),  # Position and size of the button
        text='Next Turn',  # Button label
        manager=gui_manager  # Assign to the GUI manager
    )
    
    # Game loop variables
    is_running = True
    game_winner = None
    clock = pygame.time.Clock()
    
    while is_running:
        time_delta = clock.tick(60)/1000.0

        next_turn_clicked = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == next_turn_button:
                    next_turn_clicked = True
            gui_manager.process_events(event)
        
        gui_manager.update(time_delta)  # Update GUI state
        
        # Draw the background onto the screen
        screen.blit(background, (0, 0))
        
        # If the game is ongoing and "Next Turn" was clicked, progress the game
        if game_winner is None and next_turn_clicked:
            game_winner = game.do_turn()  # Execute the current player's turn and check for a winner
        

        game.draw(screen)
        
        # If there's a winner, display their name and the solution on the screen
        if game_winner is not None:
            draw_text(
                f"Player {game_winner.id.name} won the game, the solution was {game.solution[0].name}, {game.solution[1].name}, and {game.solution[2].name}",
                (100, 255, 100),  # Green color for success message
                (10, 500),  # Position on the screen
                screen
            )

        # Draw the GUI elements onto the screen
        gui_manager.draw_ui(screen)
        
        # Update the display with the new frame
        pygame.display.update()

    pygame.quit()  # Clean up and close the game window
    

if __name__ == "__main__":
    main()
