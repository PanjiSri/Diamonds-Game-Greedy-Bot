# Algoritma Nabrak Orang, Pulang Tepat Waktu

import random
from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import clamp, position_equals


class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.diamonds = []

    def getDiamond_inRange(self, board: Board, pos1: Position, pos2: Position) -> List[GameObject]:
        x1, x2 = pos1.x, pos2.x
        y1, y2 = pos1.y, pos2.y

        dirX, dirY = clamp(x1 - x2, -1, 1), clamp(y1 - y2, -1, 1)
        diamonds = [d.position for d in board.game_objects if ((d.type == "DiamondGameObject") and (d.position.x in range(x1, x2+dirX, dirX)) and (d.position.y in range(y1, y2+dirY, dirY)))]
        
        if(len(diamonds) < 2):
            if (abs(x1-x2) > abs(y1-y1)):
                if(y2 == 0 or y2 == board.height-1):
                    y1 -= dirY
                else:
                    y2 += dirY
            else:
                if(x2 == 0 or x2 == board.width-1):
                    x1 -= dirX
                else:
                    x2 += dirX
            diamonds = self.getDiamond_inRange(board, )
        return diamonds
    
    def getDistance(self, pos1: Position, pos2: Position, byX: bool = True, byY: bool = True) -> int:
        jarak = 0
        if(byX):
            jarak += abs(pos1.x - pos2.x)
        if(byY):
            jarak += abs(pos1.y - pos2.y)
        return jarak

    def get_direction_Adv(current_x: int, current_y: int, dest_x: int, dest_y: int, avoidList):
        listBaru = [(a.x, a.y) for a in avoidList]
        delta_x = clamp(dest_x - current_x, -1, 1)
        delta_y = clamp(dest_y - current_y, -1, 1)
        if delta_x != 0:

            isBlocked = False
            if (delta_y != 0 and dest_x-delta_x == current_x):
                for i in range(current_y, dest_y+delta_y, delta_y):
                    if ((current_x + delta_x, i) in listBaru):
                        isBlocked = True

            if (isBlocked or (current_x + delta_x, current_y) in listBaru):
                delta_x = 0
                if delta_y == 0:
                    if (current_y != 0 and not((current_x, current_y-1) in listBaru)):
                        delta_x, delta_y = 0, -1
                    else:
                        delta_x, delta_y = 0, 1
            else:
                delta_y = 0
        if delta_x == 0:
            if ((current_x, current_y+delta_y) in listBaru):
                if (current_x != 0 and not((current_x-1, current_y) in listBaru)):
                    delta_x, delta_y = -1, 0
                else:
                    delta_x, delta_y = 1, 0

        return delta_x, delta_y
    
    

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        # Get base, red button, and diamonds in between
        base = board_bot.properties.base
        redButton = [d.position for d in board.game_objects if d.type == "DiamondButtonGameObject"][0]
        teleporter = [d.position for d in board.game_objects if d.type == "TeleportGameObject"]

        if(len(self.diamonds) == 0):
            self.diamonds.append(base)
        
        isRedButton = position_equals(current_position, self.diamonds[-1])
        isBase = position_equals(current_position, base)
        if (isBase or isRedButton):
            if (not(isRedButton and isBase)):
                self.diamonds = self.getDiamond_inRange(board, base, self.diamonds[-1])
            else:
                self.diamonds = self.getDiamond_inRange(board, base, redButton)
            

            if (self.getDistance(base, redButton, byY=False) < self.getDistance(base, redButton, byX=False)):
                self.diamonds = sorted(self.diamonds, key=lambda diamond: diamond.y)[0:5]
            else:
                self.diamonds = sorted(self.diamonds, key=lambda diamond: diamond.x)[0:5]

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
            delta_x, delta_y = self.get_direction_Adv(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
                teleporter,
            )
        return delta_x, delta_y