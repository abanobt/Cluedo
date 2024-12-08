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
        self.prev_action = ["", "", "", ""]
        self.awaiting_player_refutation = False

    def do_turn(self):
        turn = self.current_player_turn
        # For now all the players will be AI, but eventually one player will be the user
        player = self.players[turn]
        # if player.is_user:
            # action = input.get_user_action
            # if action == None:
                # return # player has not made action
        action = get_ai_action(self.players[turn], self.mansion)
        self.do_move(player, action)
        self.do_suggestion(player, action)
        self.do_accusation(player, action)
        self.current_player_turn = 0 if turn + 1 >= len(self.players) else turn + 1


    def do_move(self, player, action):
        if not action.want_move:
            self.prev_action[0] = "Prev: {0} did not move".format(player.get_name())
            return

        room = self.mansion.get_player_room(player)
        connections = room.get_connections()
        new_room = connections[action.move_room_index]
        self.mansion.move_player(player, new_room)
        self.prev_action[0] = "Prev: {0} moved from {1} to {2}".format(player.get_name(), room.get_name(), new_room.name)

    def do_suggestion(self, player, action):
        if not action.want_suggestion:
            self.prev_action[1] = "     and did not suggest"
            return
        self.prev_action[1] = "     and suggested {0}/{1}".format(action.suggestion_weapon.name, action.suggestion_char.name)
        index = self.current_player_index
        index = 0 if index + 1 >= len(self.players) else index + 1
        while index != self.current_player_index:
            other_player = self.players[index];
            # if other_player.is_user:
                #self.awaiting_player_refutation
                # return
            # else
            for card in other_player.cards:
                if ((isinstance(card, Weapon) and card == action.suggestion_weapon) or \
                    (isinstance(card, RoomId) and card == self.mansion.get_player_room(player)) or \
                    (isinstance(card, Character) and card == action.suggestion_char)):
                    other_player.see_card(card)
                    self.prev_action[3] = "Player {0} refuted suggestion with {1}".format(other_player.get_name(), card.name)
                    return
        self.prev_action[3] = "No player refued the suggestion"
        
            

    def do_accusation(self, player, action):
        if not action.want_accusation:
            self.prev_action[2] = "     and did not accuse"
            return
        self.prev_action[2] = "     and accused {0}/{1}".format(action.suggestion_weapon.name, action.suggestion_char.name)        

    def draw(self, screen):
        self.mansion.draw_board(screen)
        position = self.players[self.current_player_turn].draw_info(screen)
        position = position + 30
        for t in self.prev_action:
            draw_text(t, (160,255,200), (500, position), screen)
            position = position + 30
        draw_text("(DEBUG) Solution: {0}, {1}, {2}".format(self.solution[0].name, self.solution[1].name, self.solution[2].name), (200,200,200), (500, position), screen)


