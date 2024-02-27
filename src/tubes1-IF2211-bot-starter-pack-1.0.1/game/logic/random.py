import random
from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        list_diamonds = sorted(board.diamonds, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))

        for diamond in list_diamonds:
            # print distance of each diamond from bot
            print(f"distance of a diamond from bot: {abs(diamond.position.x - current_position.x)}, {abs(diamond.position.y - current_position.y)}")

            # print position of each diamond
            print(f"position of a diamond: ({diamond.position.x}, {diamond.position.y})")

        # teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]
    
        # Analyze new state
        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(board_bot.properties.milliseconds_left / 1000)

        if (props.diamonds == props.inventory_size) or (steps_to_base == time_left):  # belum tackle punya bobot 4 dan ketemu red diamond
            # Pulang ke base
            base = board_bot.properties.base
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                base.x,
                base.y,
            )
        else:
            # Ambil diamond
            diamond = list_diamonds[0]
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                diamond.position.x,
                diamond.position.y,
            )
            if delta_x == delta_y:
                diamond = list_diamonds[1]
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    diamond.position.x,
                    diamond.position.y,
                )
        return delta_x, delta_y