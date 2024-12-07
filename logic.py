from weapon import Weapon
from character import Character

import random

class Action:
	def __init__(self):
		# TOOD: For now the AI is behaving randomly, but eventually there will be logic to it
		self.want_move=random.choice([True, False])
		self.move_room_index=random.choice([0, 1])
		self.suggestion_weapon=random.choice([e for e in Weapon])
		self.suggestion_char=random.choice([e for e in Character])

# TODO: Clue logic
# class Clue: