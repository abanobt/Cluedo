from enum import Enum
from weapon import Weapon
from room import RoomId
from character import Character
from utils import draw_text
import pygame

# Enum to represent player identifiers (with color-coded IDs)
class PlayerId(Enum):
    Red = 1,
    Yellow = 2,
    White = 3,
    Green = 4,
    Blue = 5,
    Purple = 6

# Class to represent a player in the game
class Player:
    def __init__(self, playerid, dealt_cards):
        """
        Initializes a Player object.
        
        Parameters:
        - playerid (PlayerId): The ID corresponding to the player (e.g., Red, Yellow).
        - dealt_cards (list): Cards dealt to this player at the start of the game.
        """
        self.id = playerid
        self.image = pygame.image.load(PLAYER_IMAGES[playerid])
        self.cards = dealt_cards
        self.knowledge = PlayerKnowledge(dealt_cards)
        self.is_disqualified = False
        
    def no_refutation(self, weapon, room, suspect):
        """
        Updates player's knowledge when no player has refuted their suggestion.
        
        Parameters:
        - weapon (Weapon): The weapon suggested.
        - room (RoomId): The room suggested.
        - suspect (Character): The suspect suggested.
        """
        if (room not in self.cards):
            self.knowledge.solution_found(weapon, room, suspect)

    def draw_info(self, screen):
        """
        Draws player-specific information (current player, cards, knowledge) on the screen.
        
        Parameters:
        - screen (pygame.Surface): The Pygame surface to render the text onto.
        
        Returns:
        - int: The updated vertical position after drawing the information.
        """
        position = 15
        draw_text("Current Player: {0}".format(self.id.name), (255,255,255), (500, position), screen)
        position = position + 30
        text = "    Cards: "
        for card in self.cards:
            text = text + card.name + ", "
        draw_text(text, (255,255,255), (500, position), screen)
        position = position + 30
        position = self.knowledge.draw_info(screen, position)
        return position

    def __eq__(self, other):
        """
        Checks if two players are equal based on their IDs.
        """
        if other is None:
            return False
        return self.id == other.id

class PlayerKnowledge:
    def __init__(self, cards):
        """
        Initializes a PlayerKnowledge object.
        
        Parameters:
        - cards (list): The initial set of cards the player was dealt.
        """
        self.known_weapons = set(e for e in cards if isinstance(e, Weapon))
        self.known_rooms = set(e for e in cards if isinstance(e, RoomId))
        self.known_suspects = set(e for e in cards if isinstance(e, Character))

    def add_card(self, card):
        """
        Adds a card to the player's knowledge base.
        
        Parameters:
        - card: The card to add (can be a Weapon, RoomId, or Character).
        """
        if isinstance(card, Weapon):
            self.known_weapons.add(card)
        
        if isinstance(card, RoomId):
            self.known_rooms.add(card)

        if isinstance(card, Character):
            self.known_suspects.add(card)

    def solution_found(self, weapon, room, suspect):
        """
        Marks all options except the provided ones as known.
        
        Parameters:
        - weapon (Weapon): The confirmed weapon.
        - room (RoomId): The confirmed room.
        - suspect (Character): The confirmed suspect.
        """
        self.known_weapons = set(e for e in Weapon)
        self.known_weapons.remove(weapon)
        self.known_rooms = set(e for e in RoomId)
        self.known_rooms.remove(room)
        self.known_suspects = set(e for e in Character)
        self.known_suspects.remove(suspect)

    def get_knowledge_diff(self):
        """
        Returns the difference between all possibilities and known items.
        
        Returns:
        - tuple: (unknown weapons, unknown rooms, unknown suspects)
        """
        return (set(e for e in Weapon) - self.known_weapons, set(e for e in RoomId) - self.known_rooms, set(e for e in Character) - self.known_suspects)
    
    def draw_info(self, screen, position):
        """
        Draws known information (weapons, rooms, suspects) on the screen.
        
        Parameters:
        - screen (pygame.Surface): The Pygame surface to render the text onto.
        - position (int): The vertical position to start rendering.
        
        Returns:
        - int: The updated vertical position after drawing.
        """
        position = self.draw_info_section("KnownWeapons: ", screen, self.known_weapons, position)
        position = self.draw_info_section("KnownRooms: ", screen, self.known_rooms, position)
        position = self.draw_info_section("KnownSuspects: ", screen, self.known_suspects, position)
        return position
    
    def draw_info_section(self, text, screen, items, position):
        """
        Draws a category of known information (weapons, rooms, or suspects).
        
        Parameters:
        - text (str): The label for the information (e.g., "KnownWeapons: ").
        - screen (pygame.Surface): The Pygame surface to render the text onto.
        - items (set): The items to display.
        - position (int): The vertical position to start rendering.
        
        Returns:
        - int: The updated vertical position after drawing.
        """
        for item in items:
            text = text + item.name + ", "
        draw_text(text, (255,200,0), (500, position), screen) 
        position = position + 30
        return position

# Mapping of PlayerId to corresponding player images
PLAYER_IMAGES = {
    PlayerId.Red: "player_red.png",
    PlayerId.Yellow: "player_yellow.png",
    PlayerId.White: "player_white.png",
    PlayerId.Green: "player_green.png",
    PlayerId.Blue: "player_blue.png",
    PlayerId.Purple: "player_purple.png"
}
