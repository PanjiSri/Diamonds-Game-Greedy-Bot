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

        #INI BUAT TESTING
        arr_bot = board.bots
        # print("lokasi -1", arr_bot[-1].position.x, arr_bot[-1].position.y)
        # print("lokasi 0", arr_bot[0].position.x, arr_bot[0].position.y)
        # print("lokasi 1", arr_bot[1].position.x, arr_bot[1].position.y)
        # print("lokasi sekarang", current_position.x, current_position.y)

        list_diamonds = board.diamonds

        arr_1 = []

        for diamond in list_diamonds:

            filtered_bots = [bot for bot in arr_bot if not(bot.position.x == current_position.x and bot.position.y == current_position.y)]

            list_robot_terdekat = sorted(filtered_bots, key=lambda bots: abs(bots.position.x - diamond.position.x) + abs(bots.position.y - diamond.position.y))

            if filtered_bots:
                arr_1.append((diamond, list_robot_terdekat[0]))
                
        # print("lokasi sekarang", current_position.x, current_position.y)
        # print("x: ", arr_1[0][1].position.x, "y: ", arr_1[0][1].position.y)
        
        arr_2 = []

        for elemen in arr_1:

              distance_to_us = abs(elemen[0].position.x - current_position.x) + abs(elemen[0].position.y - current_position.y)

              selisih = distance_to_us -  (abs(elemen[1].position.x - elemen[0].position.x) + abs(elemen[1].position.y - elemen[0].position.y))

              arr_2.append((elemen[0], selisih, distance_to_us))

        # print("x bot: ", current_position.x, "y bot: ", current_position.y)
        # print("x: ", arr_2[0][0].position.x, "y: ", arr_2[0][0].position.y)
        # print("selisih", arr_2[0][1])
        # print("jarak ke kita", arr_2[0][2])
    
        filtered_arr_2 = [elem for elem in arr_2 if elem[1] < 0] 


        if filtered_arr_2 != []:

            min_distance_elem = min(filtered_arr_2, key=lambda elem: elem[2]) 

            selected_goal = min_distance_elem[0]

        #     min_selisih_elem = min(filtered_arr_2, key=lambda elem: (elem[1], elem[2]))

        #     selected_diamond = min_selisih_elem[0]
            
        else:
             selected_goal = base
    
        # #teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        # #print(diamond.position.x + " " + diamond.position.y)
        # #print(teleport.position.x + " " + teleport.position.y)
        # # Analyze new state
        if props.diamonds == 5 or props.diamonds == 4:
        #     # Move to base
             base = board_bot.properties.base
             self.goal_position = base

        else:
        #     # Just roam around
             self.goal_position = None

        if self.goal_position:
             # We are aiming for a specific position, calculate delta
             delta_x, delta_y = get_direction(
                 current_position.x,
                 current_position.y,
                 self.goal_position.x,
                 self.goal_position.y,
             )
        # #[1,2,3]
        # #
        else:
        #     # Roam around
        #     # delta = self.directions[self.current_direction]
             delta_x, delta_y = get_direction(
                 current_position.x,
                 current_position.y,
                 selected_goal.position.x,
                 selected_goal.position.y,
             )
            # delta_x = delta[0]
            # delta_y = delta[1]
            # if random.random() > 0.6:
            #     self.current_direction = (self.current_direction + 1) % len(
            #         self.directions
            #     )
        # return delta_x, delta_y
        return delta_x, delta_y