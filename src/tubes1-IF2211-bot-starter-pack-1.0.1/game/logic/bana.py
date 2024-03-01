# import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
from typing import List


# By Profit
class Bana(BaseLogic):
    def __init__(self):
        self.is_position_red_button_moved = False
        self.list_most_diamonds_in_quadrant = []
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.current_position_red_button_x = None
        self.current_position_red_button_y = None

    # Bagi board menjadi 4 bagian/kuadran
    def get_most_diamonds_in_quadrant(self, board: Board) -> List[GameObject]:
        center_x = board.width // 2
        center_y = board.height // 2
        diamonds_quadrant_counts = [[], [], [], []]

        for diamond in board.diamonds:
            '''
            the positive numbers add to the right and bottom, and the index of the each square of width or height is 0-based
            '''
            # 0: top-left, 1: top-right, 2: bottom-left, 3: bottom-right
            quadrant = (diamond.position.x > center_x) + (diamond.position.y > center_y) * 2
            diamonds_quadrant_counts[quadrant].append(diamond)

        quadrant_max_diamonds = max(range(len(diamonds_quadrant_counts)), key=lambda i: len(diamonds_quadrant_counts[i]))

        return diamonds_quadrant_counts[quadrant_max_diamonds]

    def next_move(self, board_bot: GameObject, board: Board):
        if not self.list_most_diamonds_in_quadrant or self.goal_position == board_bot.position:
            self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)
        
        # Deklarasi board, posisi, sorted list diamond, teleport, red button
        props = board_bot.properties
        current_position = board_bot.position

        # get many of steps to base and time left
        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(board_bot.properties.milliseconds_left / 1000)
        # red_button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]
        
        if self.list_most_diamonds_in_quadrant == []:
            self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)
            list_diamonds = sorted(self.list_most_diamonds_in_quadrant, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
            diamond = list_diamonds[0]
        else:
            diamond = None

        # teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]

        if (self.list_most_diamonds_in_quadrant) or (current_position.x == diamond.position.x and current_position.y == diamond.position.y):
            self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)
            list_diamonds = sorted(self.list_most_diamonds_in_quadrant, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
            diamond = list_diamonds[0]

        # Pulang ke base
        if steps_to_base == time_left or props.diamonds == props.inventory_size or (diamond.properties.points == 2 and props.diamonds == props.inventory_size - 1):
            self.goal_position = props.base
        elif self.list_most_diamonds_in_quadrant:
            closest_diamond = min(
                self.list_most_diamonds_in_quadrant,
                key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)
            )
            self.goal_position = closest_diamond.position
        else:
            self.goal_position = None
            
        # Jalankan get direction
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        elif list_diamonds != [] and list_diamonds[0] != []:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                list_diamonds[0].position.x,
                list_diamonds[0].position.y,
            )
        return delta_x, delta_y