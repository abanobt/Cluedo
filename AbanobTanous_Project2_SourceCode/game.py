from mansion import Mansion
from character import Character
from weapon import Weapon
from room import RoomId
from player import PlayerId
from player import Player
from logic import Action
from logic import get_ai_action
from utils import *

import pygame
import random

class CluedoGame:
    def __init__(self):
        """
        Initialize the Cluedo game and setups the game start state.
        """
        character_cards = [c for c in Character]
        room_cards = [r for r in RoomId]
        weapon_cards = [w for w in Weapon]

        # Randomly select one character, one weapon, and one room to be the solution to the murder
        self.solution = (random.choice(character_cards), random.choice(room_cards), random.choice(weapon_cards))

        # Remove the solution cards
        character_cards.remove(self.solution[0]) 
        room_cards.remove(self.solution[1]) 
        weapon_cards.remove(self.solution[2])
        
        # Combine remaining cards and shuffle them
        cards = character_cards + room_cards + weapon_cards
        random.shuffle(cards)
        
        # Deal cards evenly to players
        self.players = []
        self.current_player_turn = 0 # The index of the player whose turn it is to go
        for playerid in PlayerId:
            dealt_cards = cards[0:3] # Deal the top three cards from the pile
            del cards[0:3] # Remove the dealt cards
            self.players.append(Player(playerid, dealt_cards))

        self.mansion = Mansion(self.players)
        self.prev_action = ["", "", "", ""]

    def do_turn(self):
        """
        Execute the current player's turn. This includes moving, making suggestions, 
        and possibly making an accusation.
        """
        turn = self.current_player_turn
        player = self.players[turn]

        # Skip the turn if the player is disqualified
        if player.is_disqualified:
            self.current_player_turn = 0 if turn + 1 >= len(self.players) else turn + 1
            return

        # Determine AI action for the turn
        action = get_ai_action(player, self.mansion)

        # Handle movement, suggestion, and accusation actions
        self.do_move(player, action)
        self.do_suggestion(player, action)
        result = self.do_accusation(player, action)

        # Check if the game ends with a correct accusation
        if result == 1:
            return player  # Return the winning player

        # Update to the next player's turn
        self.current_player_turn = 0 if turn + 1 >= len(self.players) else turn + 1
        return None


    def do_move(self, player, action):
        """
        Handle the player's movement action.
        """
        if not action.want_move:
            self.prev_action[0] = f"Last turn: Player {player.id.name} did not move"
            return

        # Get the player's current room and move them to the desired room
        room = self.mansion.get_player_room(player)
        self.mansion.move_player(player, action.move_room)
        self.prev_action[0] = f"Last turn: Player {player.id.name} moved from {room.id.name} to {action.move_room.id.name}"

    def do_suggestion(self, player, action):
        """
        Handle the player's suggestion action.
        """
        if not action.want_suggestion:
            self.prev_action[1] = "     and did not suggest"
            self.prev_action[3] = "No player refuted the suggestion"
            return
        
        self.prev_action[1] = f"     and suggested {action.suggestion_weapon.name} with {action.suggestion_char.name}"
        
        index = self.current_player_turn
        index = 0 if index + 1 >= len(self.players) else index + 1
        
        while index != self.current_player_turn:
            other_player = self.players[index];
            random.shuffle(other_player.cards)
            for card in other_player.cards:
                if ((isinstance(card, Weapon) and card == action.suggestion_weapon) or \
                    (isinstance(card, RoomId) and card == self.mansion.get_player_room(player).id) or \
                    (isinstance(card, Character) and card == action.suggestion_char)):
                    player.knowledge.add_card(card)
                    self.prev_action[3] = f"Player {other_player.id.name} refuted suggestion with {card.name}"
                    return
            index = 0 if index + 1 >= len(self.players) else index + 1
        
        # No refuation
        player.no_refutation(action.suggestion_weapon, self.mansion.get_player_room(player).id, action.suggestion_char)
        self.prev_action[3] = "No player refuted the suggestion"

    def do_accusation(self, player, action):
        """
        Handle the player's accusation action.
        """
        if not action.want_accusation:
            self.prev_action[2] = "     and did not accuse"
            return
            
        # Check the validity of the accusation
        solution_suspect, solution_room, solution_weapon = self.solution
        if self.mansion.get_player_room(player).id == solution_room and \
           action.suggestion_weapon == solution_weapon and \
           action.suggestion_char == solution_suspect:
            self.prev_action[2] = f"     and correctly accused {action.suggestion_char.name} with {action.suggestion_weapon.name}"
            return 1 # Game over, player wins
        
        # False accusation disqualifies the player
        self.prev_action[2] = f"     and falsely accused {action.suggestion_weapon.name} with {action.suggestion_char.name}"
        player.is_disqulified = True
        return 0      

    def draw(self, screen):
        """
        Render the game board and UI elements on the screen.
        """
        self.mansion.draw_board(screen)
        position = self.players[self.current_player_turn].draw_info(screen)
        position = position + 30
        for t in self.prev_action:
            draw_text(t, (160,255,200), (500, position), screen)
            position = position + 30
        draw_text(f"Solution: {self.solution[0].name}, {self.solution[1].name}, {self.solution[2].name}", (200,200,200), (500, position), screen)


