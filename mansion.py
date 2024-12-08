from room import Room
from room import RoomId
import pygame
import random

class Mansion :
    def __init__(self, players):
        """
        Initialize the mansion with its rooms and randomly assign players to starting rooms.
        """
        # Define rooms and their connections
        self.rooms = {
            RoomId.Ballroom: Room(RoomId.Ballroom, [RoomId.Kitchen, RoomId.Conservatory]),
            RoomId.Conservatory: Room(RoomId.Conservatory, [RoomId.Ballroom, RoomId.BilliardRoom]),
            RoomId.BilliardRoom: Room(RoomId.BilliardRoom, [RoomId.Conservatory, RoomId.Library]),
            RoomId.Library: Room(RoomId.Library, [RoomId.BilliardRoom, RoomId.Study]),
            RoomId.Study: Room(RoomId.Study, [RoomId.Library, RoomId.Hall]),
            RoomId.Hall: Room(RoomId.Hall, [RoomId.Study, RoomId.Lounge]),
            RoomId.Lounge: Room(RoomId.Lounge, [RoomId.Hall, RoomId.DiningRoom]),
            RoomId.DiningRoom: Room(RoomId.DiningRoom, [RoomId.Lounge, RoomId.Kitchen]),
            RoomId.Kitchen: Room(RoomId.Kitchen, [RoomId.DiningRoom, RoomId.Ballroom])
        }
        
        # Place each player in a random starting position
        room_values = list(self.rooms.values())
        for player in players:
            rand_room = random.choice(room_values)
            rand_room.players.append(player)

        # Load the mansion background image
        self.background_image = pygame.image.load("mansion.png")

    def get_player_room(self, player):
        """
        Find and return the room where the specified player is located.
        """
        for roomid in self.rooms:
            room = self.rooms[roomid]
            if player in room.players:
                return room

    def move_player(self, player, new_room):
        """
        Move a player from their current room to a new room.
        """
        old_room = self.get_player_room(player)
        old_room.players.remove(player)
        new_room.players.append(player)

    def draw_board(self, screen):
        """
        Render the mansion board and its rooms on the screen.
        """
        screen.blit(self.background_image, (0, 0)) 
        for room in self.rooms:
            self.rooms[room].draw(screen)

