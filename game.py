from mansion import Mansion
from character import Character
from weapon import Weapon
from room import RoomId
from player import PlayerId
from player import Player
from logic import Action
#from logic import Clue

import pygame
import random

class CluedoGame:
    def __init__(self):
        character_cards = [c for c in Character]
        room_cards = [r for r in RoomId]
        weapon_cards = [w for w in Weapon]

        # Randomly select one character, one weapon, and one room to be the solution to the murder
        self.solution = (random.choice(character_cards), random.choice(room_cards), random.choice(weapon_cards))

        # Remove the solution cards
        character_cards.remove(self.solution[0]) 
        room_cards.remove(self.solution[1]) 
        weapon_cards.remove(self.solution[2])
        
        # Place the remaining cards into a pile and shuffle
        cards = character_cards + room_cards + weapon_cards
        random.shuffle(cards)

        self.players = []
        self.current_player_turn = 0 # The index of the player whose turn it is to goo
        for playerid in PlayerId:
            dealt_cards = cards[0:3] # Deal the top three cards from the pile
            del cards[0:3] # Remove the dealt cards
            self.players.append(Player(playerid, dealt_cards))

        self.mansion = Mansion(self.players)
        self.font = pygame.font.Font(None, 25)
        self.prev_action = ""

    def do_turn(self):
        turn = self.current_player_turn
        # For now all the players will be AI, but eventually one player will be the user
        self.ai_do_turn(self.players[turn])
        # player_do_turn()
        self.current_player_turn = 0 if turn + 1 >= len(self.players) else turn + 1
        return

    # The AI will take its turn
    def ai_do_turn(self, player):
        action = Action()
        self.ai_do_move(player, action)
        self.ai_do_suggestion(player, action)
        return
	
    # The AI will move to another room
    def ai_do_move(self, player, action):
        if not action.want_move:
            self.prev_action = "Prev: {0} did not move".format(player.get_name())
            return

        room = self.mansion.get_player_room(player)
        connections = room.get_connections()
        new_room = connections[action.move_room_index]
        self.mansion.move_player(player, new_room)
        self.prev_action = "Prev: {0} moved from {1} to {2}".format(player.get_name(), room.get_name(), new_room.name)
        return

    def ai_do_suggestion(self, player, action):
        self.prev_action = self.prev_action + " and suggested {0}/{1}".format(action.suggestion_weapon.name, action.suggestion_char.name)
        # TODO: resolve suggestion
        # player_with_clue = self.find_player_with_clue(player, action)
        # clue = Clue(player, action, player_with_clue)
        # player.give_clue(clue)
        return

    def ai_do_accusation(self, player, action):
        # TODO
        return

    def draw(self, screen):
        self.mansion.draw_board(screen)
        text = "Current Player: {0}".format(self.players[self.current_player_turn].get_name())
        draw_text(text, self.font, (255,255,255), (500, 15), screen)
        text = self.prev_action
        draw_text(text, self.font, (160,255,200), (500, 42), screen)
        #TODO: remove this
        text = "(DEBUG) Solution: {0}, {1}, {2}".format(self.solution[0].name, self.solution[1].name, self.solution[2].name)
        draw_text(text, self.font, (200,200,200), (500, 69), screen)

# TODO: move to utils
def draw_text(text, font, color, position, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect() 
    text_rect.topleft = position
    screen.blit(text_surface, text_rect)
