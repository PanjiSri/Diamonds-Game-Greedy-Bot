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
        # diamond = board.diamonds[0]
        current_position = board_bot.position
        list_diamonds = sorted(board.diamonds, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))

        for diamond in list_diamonds:
            # print distance of each diamond from bot
            print("distance of each diamond from bot")
            print('(' + str(abs(diamond.position.x - current_position.x)) + ',' + str(abs(diamond.position.y - current_position.y)) + ')')

            # print position of each diamond
            print("position of all diamonds")
            print('('+str(diamond.position.x) + ','+ str(diamond.position.y)+ ')')

        diamonds = list_diamonds[0]
        
        #teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]
    
        #print(diamond.position.x + " " + diamond.position.y)
        #print(teleport.position.x + " " + teleport.position.y)
        # Analyze new state
        if props.diamonds == 5 or props.diamonds == 4:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base

        else:
            # Just roam around
            self.goal_position = None

        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        #[1,2,3]
        #
        else:
            # Roam around
            # delta = self.directions[self.current_direction]
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                diamonds.position.x,
                diamonds.position.y,
            )
            # delta_x = delta[0]
            # delta_y = delta[1]
            # if random.random() > 0.6:
            #     self.current_direction = (self.current_direction + 1) % len(
            #         self.directions
            #     )
        return delta_x, delta_y