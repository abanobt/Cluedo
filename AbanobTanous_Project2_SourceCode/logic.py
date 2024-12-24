from weapon import Weapon
from character import Character
from collections import deque
import random

class Action:
    def __init__(self, want_move, move_room, want_accusation, want_suggestion, suggestion_weapon, suggestion_char):
        """
        Represents an action that a player can take during their turn.
        - want_move: Boolean, whether the player wants to move to another room.
        - move_room: The room the player wants to move to (if moving).
        - want_accusation: Boolean, whether the player wants to make an accusation.
        - want_suggestion: Boolean, whether the player wants to make a suggestion.
        - suggestion_weapon: The weapon involved in the suggestion.
        - suggestion_char: The character involved in the suggestion.
        """
        self.want_move = want_move
        self.move_room = move_room
        self.want_accusation = want_accusation
        self.want_suggestion = want_suggestion
        self.suggestion_weapon = suggestion_weapon
        self.suggestion_char = suggestion_char

def get_ai_action(aiplayer, mansion):
    """
    Determines the AI's action for its turn.
    - If the AI knows the solution, it attempts to move towards the solution room and make an accusation.
    - Otherwise, it explores the mansion and makes a suggestion to gather more information.
    """
    knowledge_diff = aiplayer.knowledge.get_knowledge_diff()
    
    # If the solution is fully known, move towards the solution and accuse
    if is_solution_known(knowledge_diff):
        return get_action_towards_solution(
            aiplayer, mansion,
            knowledge_diff[0].pop(),  # Weapon
            knowledge_diff[1].pop(),  # Room
            knowledge_diff[2].pop()   # Suspect
        )
    
    # Otherwise, determine the next move and make a suggestion
    next_room = determine_next_move(mansion, mansion.get_player_room(aiplayer), aiplayer)
    return Action(
        True,
        mansion.rooms[next_room],
        False,
        True,
        determine_next_suggestion_weapon(aiplayer, knowledge_diff),
        determine_next_suggestion_suspect(aiplayer, knowledge_diff)
    )

def is_solution_known(knowledge_diff):
    """
    Checks if the AI has identified the solution based on its knowledge.
    Returns True if only one possible weapon, room, and suspect remain.
    """
    return len(knowledge_diff[0]) == 1 and \
           len(knowledge_diff[1]) == 1 and \
           len(knowledge_diff[2]) == 1

def get_action_towards_solution(aiplayer, mansion, solution_weapon, solution_room, solution_suspect):
    """
    Determines the AI's action when it knows the solution.
    - If already in the solution room, make an accusation.
    - If adjacent to the solution room, move into it and accuse.
    - Otherwise, find the shortest path to the solution room.
    """
    room = mansion.get_player_room(aiplayer)
    
    # Player is in the solution room
    if room.id == solution_room:
        return Action(False, 0, True, False, solution_weapon, solution_suspect)

    # If connected to the solution room, move directly there and accuse
    for connection in room.connections:
        if connection == solution_room:
            return Action(True, connection, True, False, solution_weapon, solution_suspect)

    # Player is not connected to solution room
    next_room = find_path_to_room(room, solution_room)
    return Action(True, mansion.rooms[next_room], False, False, solution_weapon, solution_suspect)

def find_path_to_room(start_room, goal_room_id):
    """
    Uses BFS to find the shortest path from the current room to the target room.
    Returns the next step in the path.
    """
    queue = deque([(start_room.id, [start_room.id])])
    visited = set()
    
    while queue:
        current_node, path = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        
        if current_node == goal_room_id:
            return path[1] # return the second element in the path, which is the next node to move to
            
        for neighbor in mansion.rooms[current_node].connections:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                
    return None
    
def determine_next_move(mansion, start_room, aiplayer):
    """
    Uses BFS to find the closest unexplored room and returns the next step towards it.
    """
    queue = deque([(start_room.id, [start_room.id])])
    visited = set()
    
    while queue:
        current_node, path = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        
        if current_node != start_room.id and current_node not in aiplayer.knowledge.known_rooms:
            return path[1] # return the second element in the path, which is the next node to move to
            
        for neighbor in mansion.rooms[current_node].connections:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                
    return start_room.id
    
def determine_next_suggestion_weapon(aiplayer, knowledge_diff):
    """
    Selects a weapon from the AI's unknown weapon list for a suggestion.
    """
    return random.choice(list(knowledge_diff[0]))
    
def determine_next_suggestion_suspect(aiplayer, knowledge_diff):
    """
    Selects a suspect from the AI's unknown suspect list for a suggestion.
    """
    return random.choice(list(knowledge_diff[2]))

