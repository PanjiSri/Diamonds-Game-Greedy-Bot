import random
from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, clamp


class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def getDiamond_inRange(self, board: Board, pos1: Position, pos2: Position) -> List[GameObject]:
        dirX, dirY = clamp(pos1.x - pos2.x, -1, 1), clamp(pos1.y - pos2.y, -1, 1)
        diamonds = [d for d in board.game_objects if ((d.type == "DiamondGameObject") and (d.position.x in range(pos1.x, pos2.x, dirX)) and (d.position.y in range(pos1.y, pos2.y, dirY)))]
        return diamonds
    
    def getDistance(self, pos1: Position, pos2: Position) -> int:
        return (abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y))

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        # Get base, red button, and diamonds in between
        base = board_bot.properties.base
        redButton = [d.position for d in board.game_objects if d.type == "DiamondButtonGameObject"][0]
        
        diamonds = self.getDiamond_inRange(board, base, redButton)
        diamonds = sorted(diamonds, key=lambda diamond: self.getDistance(diamond.position, current_position))
        
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = None

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return 0,1
