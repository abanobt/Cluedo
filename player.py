from enum import Enum
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

    def draw(self, screen, position):
        screen.blit(self.image, position)

    def get_name(self):
        return self.id.name

    def __eq__(self, other):
        return self.id == other.id

PLAYER_IMAGES = {
    PlayerId.Red: "player_red.png",
    PlayerId.Yellow: "player_yellow.png",
    PlayerId.White: "player_white.png",
    PlayerId.Green: "player_green.png",
    PlayerId.Blue: "player_blue.png",
    PlayerId.Purple: "player_purple.png"
}