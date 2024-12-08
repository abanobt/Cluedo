from weapon import Weapon
from character import Character
from collections import deque
import random

class Action:
    def __init__(self, want_move, move_room_index, want_accusation, want_suggestion, suggestion_weapon, suggestion_char):
        self.want_move = want_move
        self.move_room_index = move_room_index
        self.want_accusation = want_accusation
        self.want_suggestion = want_suggestion
        self.suggestion_weapon = suggestion_weapon
        self.suggestion_char = suggestion_char

def get_ai_action(aiplayer, mansion):
    knowledge_diff = aiplayer.knowledge.get_knowledge_diff()
    if is_solution_known(knowledge_diff):
        return get_action_towards_solution(aiplayer, mansion, knowledge_diff[0][0], knowledge_diff[1][0], knowledge_diff[2][0])
    return Action(True, 0, False, True, random.choice([e for e in Weapon]), random.choice([e for e in Character]))

def is_solution_known(knowledge_diff):
        return len(knowledge_diff[0]) == 1 and \
               len(knowledge_diff[1]) == 1 and \
               len(knowledge_diff[2]) == 1

def get_action_towards_solution(aiplayer, mansion, solution_weapon, solution_room, solution_suspect):
    room = mansion.get_player_room(aiplayer)
    # Player is in the solution room
    if room.id == solution_room:
        return Action(False, 0, True, False, solution_weapon, solution_char)

    connections = room.get_connections()
    move_room_index = 0
    for connection in connections:
        # Player is connected to solution room
        if connection.id == solution_room:
            return Action(True, move_room_index, True, False, solution_weapon, solution_char)
        move_room_index = move_room_index + 1

    # Player is not connected to solution room
    next_room = find_path_to_room(room, solution_room)
    move_room_index = 0
    for connection in connections:
        if connection.id == next_room:
            return Action(True, move_room_index, False, False, solution_weapon, solution_char)
        move_room_index = move_room_index + 1

# BFS algorithm to find shortest path from one room to another
def find_path_to_room(start_room, goal_room_id):
    queue = deque([(start_room, [start_room])])
    visited = set()
    while queue:
        current_node, path = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node.id == goal_room_id:
            return path[1] # return the second element in the path, which is the next node to move to
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None

    
# TODO: Clue logic
# class Clue:
