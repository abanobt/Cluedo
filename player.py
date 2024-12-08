from enum import Enum
from weapon import Weapon
from room import RoomId
from character import Character
from utils import draw_text
import pygame

class PlayerId(Enum):
    Red = 1,
    Yellow = 2,
    White = 3,
    Green = 4,
    Blue = 5,
    Purple = 6

class Player:
    def __init__(self, playerid, dealt_cards):
        self.id = playerid
        self.image = pygame.image.load(PLAYER_IMAGES[playerid])
        self.cards = dealt_cards
        self.knowledge = PlayerKnowledge(dealt_cards)

    def see_card(self, card):
        self.knowledge.add_card(card)

    def draw(self, screen, position):
        screen.blit(self.image, position)

    def draw_info(self, screen):
        position = 15
        draw_text("Current Player: {0}".format(self.get_name()), (255,255,255), (500, position), screen)
        position = position + 30
        text = "    Cards: "
        for card in self.cards:
            text = text + card.name + ", "
        draw_text(text, (255,255,255), (500, position), screen)
        position = position + 30
        position = self.knowledge.draw_info(screen, position)
        return position

    def get_name(self):
        return self.id.name

    def __eq__(self, other):
        return self.id == other.id

class PlayerKnowledge:
    def __init__(self, cards):
        self.known_weapons = set(e for e in cards if isinstance(e, Weapon))
        self.known_rooms = set(e for e in cards if isinstance(e, RoomId))
        self.known_suspects = set(e for e in cards if isinstance(e, Character))

    def add_card(self, card):
        if isinstance(card, Weapon):
            self.known_weapons.add(card)
        
        if isinstance(card, RoomId):
            self.known_rooms.add(card)

        if isinstance(card, Character):
            self.known_suspects.add(card)

    def get_knowledge_diff(self):
        return (set(e for e in Weapon) - self.known_weapons, set(e for e in RoomId) - self.known_rooms, set(e for e in Character) - self.known_suspects)
    
    def draw_info(self, screen, position):
        text = "KnownWeapons: "
        for weapon in self.known_weapons:
            text = text + weapon.name + ", "
        draw_text(text, (255,100,255), (500, position), screen) 
        position = position + 30

        text = "KnownRooms: "
        for room in self.known_rooms:
            text = text + room.name + ", "
        draw_text(text, (255,100,255), (500, position), screen) 
        position = position + 30    

        text = "KnownSuspects: "
        for suspect in self.known_suspects:
            text = text + suspect.name + ", "
        draw_text(text, (255,100,255), (500, position), screen) 
        position = position + 30
        return position

PLAYER_IMAGES = {
    PlayerId.Red: "player_red.png",
    PlayerId.Yellow: "player_yellow.png",
    PlayerId.White: "player_white.png",
    PlayerId.Green: "player_green.png",
    PlayerId.Blue: "player_blue.png",
    PlayerId.Purple: "player_purple.png"
}
