from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class Panji(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):

        def position_equals(a: Position, b: Position):
             return a.x == b.x and a.y == b.y

        props = board_bot.properties

        tombol_merah = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]   

        teleportasi = [d for d in board.game_objects if d.type == "TeleportGameObject"]    

        current_position = board_bot.position

        #INI BUAT TESTING
        arr_bot = board.bots

        list_diamonds = board.diamonds

        arr_1 = []

        arr_1_teleport = []

        for diamond in list_diamonds:

            filtered_bots = [bot for bot in arr_bot if not(bot.position.x == current_position.x and bot.position.y == current_position.y)]

            list_robot_terdekat = sorted(filtered_bots, key=lambda bots: abs(bots.position.x - diamond.position.x) + abs(bots.position.y - diamond.position.y))

            if filtered_bots:
                arr_1.append((diamond, list_robot_terdekat[0]))

                
            teleport_terdekat = sorted(teleportasi, key=lambda teleport: abs(teleport.position.x - diamond.position.x) + abs(teleport.position.y - diamond.position.y))

            list_robot_terdekat_teleportasi = sorted(filtered_bots, key=lambda bots: abs(bots.position.x - teleport_terdekat[1].position.x) + abs(bots.position.y - teleport_terdekat[1].position.y))

            if filtered_bots:
                arr_1_teleport.append((diamond, list_robot_terdekat_teleportasi[0]))

        
        arr_2 = []

        arr_2_teleportasi = []

        for elemen in arr_1:
              
              #ini buat jarak biasa

              distance_to_us = abs(elemen[0].position.x - current_position.x) + abs(elemen[0].position.y - current_position.y)

              selisih = distance_to_us -  (abs(elemen[1].position.x - elemen[0].position.x) + abs(elemen[1].position.y - elemen[0].position.y))

              arr_2.append((elemen[0], selisih, distance_to_us, 1))

 
        for elemen in arr_1_teleport:
              #ini buat jarak teleportasi

              teleport_terdekat = sorted(teleportasi, key=lambda teleport: abs(teleport.position.x - diamond.position.x) + abs(teleport.position.y - diamond.position.y))

              distance_to_us_teleportasi =  ((abs(elemen[0].position.x - teleport_terdekat[0].position.x) + abs(elemen[0].position.y - teleport_terdekat[0].position.y)) + (abs(teleport_terdekat[1].position.x - current_position.x) + abs(teleport_terdekat[1].position.y - current_position.y)))      

              selisih_teleportasi = distance_to_us_teleportasi - ((abs(elemen[0].position.x - teleport_terdekat[0].position.x) + abs(elemen[0].position.y - teleport_terdekat[0].position.y)) + (abs(teleport_terdekat[1].position.x - elemen[1].position.x) + abs(teleport_terdekat[1].position.y - elemen[1].position.y)))     

              arr_2_teleportasi.append((elemen[0], selisih_teleportasi, distance_to_us_teleportasi, 2))        


        arr_2 = arr_2 + arr_2_teleportasi                                                                           


        filtered_arr_2 = []
        filtered_arr_2 = [elem for elem in arr_2 if elem[1] < 0] 

        #print("selisih", filtered_arr_2[0][1])
        print("lokasi TM", tombol_merah[0].position.x, tombol_merah[0].position.y)

        selected_goal = tombol_merah[0]

        print("panjang", len(filtered_arr_2))

        if len(filtered_arr_2) > 0 and filtered_arr_2 != []:

            print("dia masuk sini teleport")

            min_distance_elem = max(filtered_arr_2, key=lambda elem: elem[0].properties.points / elem[2]) 

            if min_distance_elem[3] == 1:
                selected_goal = min_distance_elem[0]
                if not(position_equals(selected_goal.position, current_position)):
                    selected_goal = min_distance_elem[0]
                else:
                    selected_goal = tombol_merah[0]
            else:
                 
                 lokasi_teleport = sorted(teleportasi, key=lambda teleport: abs(teleport.position.x - current_position.x) + abs(teleport.position.y - current_position.y))

                 selected_goal = lokasi_teleport[0]
                 if not(position_equals(selected_goal.position, current_position)):
                    selected_goal = lokasi_teleport[0]
                 else:
                    selected_goal = tombol_merah[0]
            
        else:
             print("dia masuk tombol merah")
             selected_goal = tombol_merah[0]
    
        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(board_bot.properties.milliseconds_left / 1000)

        if (props.diamonds == 5) or (steps_to_base == time_left) or (selected_goal.type == "DiamondGameObject" and selected_goal.properties.points == 2 and props.diamonds == 4) or props.diamonds == 5:

             base = board_bot.properties.base

             jarak_bot_ke_teleport = sorted(teleportasi, key=lambda teleport: (abs(teleport.position.x - current_position.x) + abs(teleport.position.y - current_position.y)))

             jarak_base_biasa = abs(base.x - current_position.x) + abs(base.y - current_position.y)

             jarak_base_teleportasi = ((abs(current_position.x - jarak_bot_ke_teleport[0].position.x) + abs(current_position.y - jarak_bot_ke_teleport[0].position.y)) + (abs(jarak_bot_ke_teleport[1].position.x - base.x) + abs(jarak_bot_ke_teleport[1].position.y - base.y)))

             if jarak_base_biasa <= jarak_base_teleportasi:
                  
                self.goal_position = base
            
             else:

                self.goal_position = teleportasi[0].position

        else:

             self.goal_position = None

        if self.goal_position:

             delta_x, delta_y = get_direction(
                 current_position.x,
                 current_position.y,
                 self.goal_position.x,
                 self.goal_position.y,
             )

        else:

             delta_x, delta_y = get_direction(
                 current_position.x,
                 current_position.y,
                 selected_goal.position.x,
                 selected_goal.position.y,
             )

        filtered_arr_2 = []
        
        print("tes")
        return delta_x, delta_y 