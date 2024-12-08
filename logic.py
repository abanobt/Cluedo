from weapon import Weapon
from character import Character
from collections import deque
import random

class Action:
    def __init__(self, want_move, move_room, want_accusation, want_suggestion, suggestion_weapon, suggestion_char):
        self.want_move = want_move
        self.move_room = move_room
        self.want_accusation = want_accusation
        self.want_suggestion = want_suggestion
        self.suggestion_weapon = suggestion_weapon
        self.suggestion_char = suggestion_char

def get_ai_action(aiplayer, mansion):
    knowledge_diff = aiplayer.knowledge.get_knowledge_diff()
    if is_solution_known(knowledge_diff):
        return get_action_towards_solution(aiplayer, mansion, knowledge_diff[0].pop(), knowledge_diff[1].pop(), knowledge_diff[2].pop())
    next_room = determine_next_move(mansion, mansion.get_player_room(aiplayer), aiplayer)
    return Action(True, mansion.rooms[next_room], False, True, determine_next_suggestion_weapon(aiplayer, knowledge_diff), determine_next_suggestion_suspect(aiplayer, knowledge_diff))

def is_solution_known(knowledge_diff):
        return len(knowledge_diff[0]) == 1 and \
               len(knowledge_diff[1]) == 1 and \
               len(knowledge_diff[2]) == 1

def get_action_towards_solution(aiplayer, mansion, solution_weapon, solution_room, solution_suspect):
    room = mansion.get_player_room(aiplayer)
    # Player is in the solution room
    if room.id == solution_room:
        return Action(False, 0, True, False, solution_weapon, solution_suspect)

    for connection in room.get_connections():
        # Player is connected to solution room
        if connection == solution_room:
            return Action(True, connection, True, False, solution_weapon, solution_suspect)

    # Player is not connected to solution room
    next_room = find_path_to_room(room, solution_room)
    return Action(True, mansion.rooms[next_room], False, False, solution_weapon, solution_suspect)

# BFS algorithm to find shortest path from one room to another
def find_path_to_room(start_room, goal_room_id):
    queue = deque([(start_room.id, [start_room.id])])
    visited = set()
    while queue:
        current_node, path = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node == goal_room_id:
            return path[1] # return the second element in the path, which is the next node to move to
        for neighbor in mansion.rooms[current_node].get_connections():
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None
    
# BFS algorithm to find path to closest unknown room
def determine_next_move(mansion, start_room, aiplayer):
    queue = deque([(start_room.id, [start_room.id])])
    visited = set()
    while queue:
        current_node, path = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node != start_room.id and current_node not in aiplayer.knowledge.known_rooms:
            return path[1] # return the second element in the path, which is the next node to move to
        for neighbor in mansion.rooms[current_node].get_connections():
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return start_room.id
    
def determine_next_suggestion_weapon(aiplayer, knowledge_diff):
    return random.choice(list(knowledge_diff[0]))
    
def determine_next_suggestion_suspect(aiplayer, knowledge_diff):
    return random.choice(list(knowledge_diff[2]))


