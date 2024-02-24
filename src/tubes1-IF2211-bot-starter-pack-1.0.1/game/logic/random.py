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

        # Get diamond, teleport, red button, and bot position - DEBUG DUDE
        diamond = board.diamonds[0]
        teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        # red_button = [d for d in board.game_objects if d.type == "RedButtonGameObject"]

        bot1 = board.bots[-1]
        # base1 = board.bots[-1].properties.base
        
        bot2 = board.bots[0]
        # base2 = board.bots[1].properties.base
    
        print("diamond:", diamond.position.x, diamond.position.y)
        print("teleport:", teleport[0].position.x, teleport[0].position.y)
        # print("red button:", red_button[0].position.x, red_button[0].position.y)
        
        print("bot 1:", bot1.position.x, bot1.position.y)
        # print("base 1:", base1.x, base1.y)
        print("bot 2:", bot2.position.x, bot2.position.y)
        # print("base 2:", base2.x, base2.y)
        
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
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
