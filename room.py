from enum import Enum

# Represents the id of the unique rooms in the game
class RoomId(Enum):
    Ballroom = 1,
    BilliardRoom = 2,
    Conservatory = 3,
    DiningRoom = 4,
    Hall = 5,
    Kitchen = 6,
    Library = 7,
    Lounge = 8,
    Study = 9

# Class to represent a room in the mansion
class Room:
    def __init__(self, roomid, connections):
        """
        Initializes a Room object.
        
        Parameters:
        - roomid (RoomId): The unique identifier for the room.
        - connections (list): A list of RoomId values representing rooms connected to this room.
        """
        self.id = roomid
        self.players = [] # The players that are in this room
        self.screen_position = ROOM_SCREEN_POSITIONS[roomid]
        self.connections = connections
        
    def draw(self, screen):
        """
        Draws the players currently in the room at the appropriate position on the screen.
        
        Parameters:
        - screen (pygame.Surface): The Pygame surface to render the players onto.
        """
        position = self.screen_position
        count = 0
        for player in self.players:
            screen.blit(player.image, position)
            if count >= 3:
                position = (position[0] - 90, position[1] + 30)
                count = 0
            else:
                position = (position[0] + 30, position[1])
            count = count + 1

# Mapping of RoomId values to their corresponding screen positions for rendering
ROOM_SCREEN_POSITIONS = {
    RoomId.Ballroom: (165, 15),
    RoomId.BilliardRoom: (315, 125),
    RoomId.Conservatory: (315, 15),
    RoomId.DiningRoom: (15, 165),
    RoomId.Hall: (165, 315),
    RoomId.Kitchen: (15, 15),
    RoomId.Library: (315, 240),
    RoomId.Lounge: (15, 315),
    RoomId.Study: (315, 355)
}
