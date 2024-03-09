from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class Logic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        def clamp(n, smallest, largest):
            return max(smallest, min(n, largest))

        def position_equals(a: Position, b: Position):
             return a.x == b.x and a.y == b.y
        
        def get_direction_Adv(current_x: int, current_y: int, dest_x: int, dest_y: int, avoidList = []):
            listBaru = [(a.position.x, a.position.y) for a in avoidList]
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
        
        def getDistance(pos1: Position, pos2: Position, listTele = []):
            if (listTele != []):
                listTeleport = sorted(listTele, key=lambda teleport: teleport.properties.pair_id)
                min_dist = 0
                min_idx = 0

                for i in range(0, len(listTeleport), 2):
                    dist_tele1 = getDistance(pos1, listTeleport[i].position)[0] + getDistance(pos2, listTeleport[i+1].position)[0]
                    dist_tele2 = getDistance(pos1, listTeleport[i+1].position)[0] + getDistance(pos2, listTeleport[i].position)[0]

                    if (dist_tele1 < dist_tele2):
                        if (dist_tele1 < min_dist):
                            min_dist = dist_tele1
                            min_idx = i
                    else:
                        if (dist_tele2 < min_dist):
                            min_dist = dist_tele2
                            min_idx = i+1

                return (min_dist, min_idx)
            else:
                jarak = abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
                return (jarak, -1)

        # Algo Tackle
        current_position = board_bot.position
        isTackle = False
        isWait = False
        list_enemy = []
        list_Teleport = []
        for d in board.game_objects:
            if (d.type == "BotGameObject"):
                jarak = getDistance(current_position, d.position)[0]
                if (jarak != 0):
                    list_enemy.append(d)
                elif (jarak == 1 and board_bot.properties.can_tackle):
                    self.goal_position = d.position
                    isTackle = True
                    break
                elif (jarak == 2):
                    isWait = True

        if (not(isTackle)):
            if (isWait):
                return 0,0
            props = board_bot.properties
            list_redButt = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]
            list_Teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]
            if (props.diamonds == 4):
                list_diamonds = [d for d in board.game_objects if (d.type == "DiamondGameObject" and d.properties.points == 1)]
            else:
                list_diamonds = board.diamonds

            # Algo Back Home On Time
            (steps_to_base, isTele) = getDistance(current_position, props.base)
            (steps_to_base_tele, idxTele) = getDistance(current_position, props.base, list_Teleport)
            
            if (steps_to_base_tele < steps_to_base):
                steps_to_base = steps_to_base_tele
                isTele = idxTele

            time_left = int(board_bot.properties.milliseconds_left / board.minimum_delay_between_moves)

            if (props.diamonds == props.inventory_size) or (steps_to_base == time_left+1):
                base = props.base

                if (isTele == -1):
                    self.goal_position = base
                else:
                    telePos = list_Teleport[isTele].position
                    if not(position_equals(telePos, current_position)):
                        self.goal_position = telePos
                        list_Teleport.pop(isTele)
                    else:
                        self.goal_position = base

            # Algo Searching for Goal
            else:
                pair_dia_dist = [] # # List of Tuple (diamond, distance to us, mode identifier)
                
                for diamond in list_diamonds:
                    if (list_enemy):
                        # Calculate Distance Diamond to Us
                        (distance_to_us, identifier) = getDistance(diamond.position, current_position)
                        (distance_to_us_tele, idxTele) = getDistance(diamond.position, current_position, list_Teleport)

                        if (distance_to_us_tele < distance_to_us):
                            distance_to_us = distance_to_us_tele
                            identifier = idxTele

                        # Find Closest Enemy to Diamond
                        distance_to_enemy = 0
                        for i in list_enemy:
                            a = getDistance(i.position, diamond.position)[0]
                            b = getDistance(i.position, diamond.position, list_Teleport)[0]
                            if ((a != 0 and a < distance_to_enemy) or distance_to_enemy == 0):
                                distance_to_enemy = a
                            if ((b != 0 and b < distance_to_enemy) or distance_to_enemy == 0):
                                distance_to_enemy = b
                        
                        # Filtered Possible Diamond to Target
                        selisih = distance_to_us - distance_to_enemy
                        if selisih < 0 and distance_to_us != 0:
                            if (identifier < 0):
                                pair_dia_dist.append((diamond, distance_to_us, identifier))
                            else:
                                pair_dia_dist.insert(0, (diamond, distance_to_us, identifier))

                if pair_dia_dist != []:
                    # Choose Diamond by Density
                    min_distance_elem = sorted(pair_dia_dist, key=lambda elem: ((elem[0].properties.points / elem[1]), -(elem[1])))[0]

                    if min_distance_elem[2] == -1:
                        self.goal_position = min_distance_elem[0].position
                    else:
                        self.goal_position = list_Teleport.pop([min_distance_elem[2]]).position

                # No Possible Diamond
                else:
                    self.goal_position = list_redButt[0].position
            
        delta_x, delta_y = get_direction_Adv(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y, list_Teleport)
            
        return delta_x, delta_y