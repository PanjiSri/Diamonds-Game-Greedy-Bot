from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, clamp, position_equals


class Bana(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.diamonds = []

    def getDiamond_inRange(self, board: Board, pos1: Position, pos2: Position) -> List[GameObject]:
        x1 = pos1.x
        x2 = pos2.x
        y1 = pos1.y
        y2 = pos2.y

        dirX, dirY = clamp(x2 - x1, -1, 1), clamp(y2 - y1, -1, 1)
        if (dirY == 0):
            dirY += 1
        if (dirX == 0):
            dirX += 1
        print(dirX, dirY)
        diamonds = [d for d in board.game_objects if ((d.type == "DiamondGameObject") and (d.position.x in range(x1, x2+dirX, dirX)) and (d.position.y in range(y1, y2+dirY, dirY)))]
        print(len(diamonds))
        diamondBaru = [d.position for d in diamonds]

        for i in range(len(self.diamonds)):
            print(i,'X ', self.diamonds[i].x)
            print(i,'Y ', self.diamonds[i].y)
        print("Get Range")

        return diamondBaru
    
    def getDistance(self, pos1: Position, pos2: Position, byX: bool = True, byY: bool = True) -> int:
        jarak = 0
        if(byX):
            jarak += abs(pos1.x - pos2.x)
        if(byY):
            jarak += abs(pos1.y - pos2.y)
        return jarak

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        # Get base, red button, and diamonds in between
        base = board_bot.properties.base
        redButton = [d.position for d in board.game_objects if d.type == "DiamondButtonGameObject"][0]

        if(len(self.diamonds) == 0):
            self.diamonds.append(base)

        isRedButton = position_equals(current_position, self.diamonds[-1])
        isBase = position_equals(current_position, base)
        if (isBase or isRedButton):
            if (not(isRedButton and isBase)):
                self.diamonds = self.getDiamond_inRange(board, base, self.diamonds[-1])
            else:
                self.diamonds = self.getDiamond_inRange(board, base, redButton)
            

            if (self.getDistance(base, redButton, byY=False) > self.getDistance(base, redButton, byX=False)):
                self.diamonds = sorted(self.diamonds, key=lambda diamond: diamond.y)[0:4]
            else:
                self.diamonds = sorted(self.diamonds, key=lambda diamond: diamond.x)[0:4]

            self.diamonds = sorted(self.diamonds, key=lambda diamond: self.getDistance(diamond, current_position))
            if (not(isRedButton and isBase)):
                self.diamonds.append(base)
            else:
                self.diamonds.append(redButton)
        
        if (position_equals(current_position, self.diamonds[0])):
            self.diamonds.pop(0)

        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = self.diamonds[0]

        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y