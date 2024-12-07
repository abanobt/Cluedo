from enum import Enum

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

class Room:
    def __init__(self, roomid, connections):
        self.id = roomid
        self.players = [] # The players that are in this room
        self.screen_position = ROOM_SCREEN_POSITIONS[roomid]
        self.connections = connections

    def get_connections(self):
        return self.connections

    def has_player(self, player):
        return player in self.players

    def move_player_in(self, player):
        self.players.append(player)

    def move_player_out(self, player):
        self.players.remove(player)

    def get_name(self):
        return self.id.name
        
    def draw(self, screen):
        position = self.screen_position
        count = 0
        for player in self.players:
            player.draw(screen, position)
            if count >= 3:
                position = (position[0] - 90, position[1] + 30)
                count = 0
            else:
                position = (position[0] + 30, position[1])
            count = count + 1

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