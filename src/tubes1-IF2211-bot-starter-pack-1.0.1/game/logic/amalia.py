from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

# By Density
class Amalia(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        # Analisis sort diamond berdasarkan points / jarak (densitas)
        list_diamonds = sorted(board.diamonds, key=lambda diamond: (diamond.properties.points / (abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))) if (abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)) != 0 else 1, reverse=True)

        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(board_bot.properties.milliseconds_left / 1000)
        diamond = list_diamonds[0]
        base = board_bot.properties.base

        if (props.diamonds == props.inventory_size) or (steps_to_base == time_left) or (diamond.properties.points == 2 and props.diamonds == props.inventory_size-1):
            # Pulang ke base
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                base.x,
                base.y,
            )
        else:
            # Ambil diamond
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                diamond.position.x,
                diamond.position.y,
            )
        return delta_x, delta_y