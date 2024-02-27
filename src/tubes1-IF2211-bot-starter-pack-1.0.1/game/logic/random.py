# import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
from typing import List


class RandomLogic(BaseLogic):
    def __init__(self):
        self.is_position_red_button_moved = False
        self.list_most_diamonds_in_quadrant = []
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.current_position_red_button_x = None
        self.current_position_red_button_y = None

    '''
    5 komponen:
    1. Diamonds: Untuk memenangkan pertandingan, kita harus mengumpulkan diamond ini sebanyak-banyaknya dengan melewati/melangkahinya. Terdapat 2 jenis diamond yaitu diamond biru dan diamond merah. Diamond merah bernilai 2 poin, sedangkan yang biru bernilai 1 poin. Diamond akan di-regenerate secara berkala dan rasio antara diamond merah dan biru ini akan berubah setiap regeneration.
    2. Red Button/Diamond Button: Ketika red button ini dilewati/dilangkahi, semua diamond (termasuk red diamond) akan di-generate kembali pada board dengan posisi acak. Posisi red button ini juga akan berubah secara acak jika red button ini dilangkahi. 
    3. Teleporters: Terdapat 2 teleporter yang saling terhubung satu sama lain. Jika bot melewati sebuah teleporter maka bot akan berpindah menuju posisi teleporter yang lain. 
    4. Bots and Bases: Pada game ini kita akan menggerakkan bot untuk mendapatkan diamond sebanyak banyaknya. Semua bot memiliki sebuah Base dimana Base ini akan digunakan untuk menyimpan diamond yang sedang dibawa. Apabila diamond disimpan ke base, score bot akan bertambah senilai diamond yang dibawa dan inventory (akan dijelaskan di bawah) bot menjadi kosong
    5. Inventory: Bot memiliki inventory yang berfungsi sebagai tempat penyimpanan sementara diamond yang telah diambil. Inventory ini memiliki kapasitas maksimum sehingga sewaktu waktu bisa penuh. Agar inventory ini tidak penuh, bot bisa menyimpan isi inventory ke base agar inventory bisa kosong kembali. 
    '''

    # Bagi board menjadi 4 bagian/kuadran
    def get_most_diamonds_in_quadrant(self, board: Board) -> List[GameObject]:
        center_x = board.width // 2
        center_y = board.height // 2
        diamonds_quadrant_counts = [[], [], [], []]

        for diamond in board.diamonds:
            '''
            the positive numbers add to the right and bottom, and the index of the each square of width or height is 0-based
            '''
            # 0: top-left, 1: top-right, 2: bottom-left, 3: bottom-right
            quadrant = (diamond.position.x > center_x) + (diamond.position.y > center_y) * 2
            diamonds_quadrant_counts[quadrant].append(diamond)

        quadrant_max_diamonds = max(range(len(diamonds_quadrant_counts)), key=lambda i: len(diamonds_quadrant_counts[i]))

        return diamonds_quadrant_counts[quadrant_max_diamonds]

    def next_move(self, board_bot: GameObject, board: Board):
        if not self.list_most_diamonds_in_quadrant or self.goal_position == board_bot.position:
            self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)
        
        # Deklarasi board, posisi, sorted list diamond, teleport, red button
        props = board_bot.properties
        current_position = board_bot.position

        # get many of steps to base and time left
        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(board_bot.properties.milliseconds_left / 1000)
        # red_button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]
        
        if self.list_most_diamonds_in_quadrant == []:
            self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)
            list_diamonds = sorted(self.list_most_diamonds_in_quadrant, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
            diamonds = list_diamonds[0]
        else:
            diamonds = None

        # teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]

        if (self.list_most_diamonds_in_quadrant) or (current_position.x == diamonds.position.x and current_position.y == diamonds.position.y):
            self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)
            list_diamonds = sorted(self.list_most_diamonds_in_quadrant, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
            diamonds = list_diamonds[0]
        
        # Pulang ke base
        if steps_to_base == time_left or props.diamonds >= props.inventory_size:
            self.goal_position = props.base
        elif self.list_most_diamonds_in_quadrant:
            closest_diamond = min(
                self.list_most_diamonds_in_quadrant,
                key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)
            )
            self.goal_position = closest_diamond.position
        else:
            self.goal_position = None
            
        # Jalankan get direction
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        elif list_diamonds != [] and list_diamonds[0] != []:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                list_diamonds[0].position.x,
                list_diamonds[0].position.y,
            )
        # else:
        #     delta_x, delta_y = get_direction(
        #         current_position.x,
        #         current_position.y,
        #         diamonds.position.x,
        #         diamonds.position.y,
        #     )
        return delta_x, delta_y


    '''
    def next_move(self, board_bot: GameObject, board: Board):
        if not self.is_position_red_button_moved:
                self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)

        props = board_bot.properties
        current_position = board_bot.position

        if self.list_most_diamonds_in_quadrant:
            list_diamonds = sorted(self.list_most_diamonds_in_quadrant, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
            diamonds = list_diamonds[0]
        else:
            diamonds = None

        # Logic for red button movement (Placeholder for actual implementation)
        # is_position_red_button_moved = check_if_red_button_moved(board)

        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(props.milliseconds_left / 1000)

        # Decide goal position based on various conditions
        if diamonds and ((steps_to_base <= time_left) or props.diamonds >= 4):
            self.goal_position = props.base
        elif diamonds:
            self.goal_position = diamonds.position

        # Determine the direction to move towards the goal position
        if self.goal_position:
            delta_x, delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
        elif diamonds:  # Move towards the closest diamond if there's no specific goal
            delta_x, delta_y = get_direction(current_position.x, current_position.y, diamonds.position.x, diamonds.position.y)
        else:
            delta_x, delta_y = 0, 0  # Stay in place if there are no diamonds

        # jika diamond yang dikumpulkan berjumlah 4 dan bot akan mengambil diamond merah, maka ia akan mencari diamond berikutnya (indeks daftar diamond berikutnya)
        # MASIH UNSOLVED!
        # if props.diamonds == 4 and diamonds.type == "RedDiamondGameObject" and len(list_diamonds) > 1:
        #     # Skip red diamond kalo sudah punya 4 diamonds
        #     self.goal_position = list_diamonds[1].position

                # if the red button's position is different from the previous position, then the red button has been moved -> is_position_red_button_moved = True
        # if self.current_position_red_button_x and (self.current_position_red_button_x != red_button[0].position.x or self.current_position_red_button_y != red_button[0].position.y):
        #     self.is_position_red_button_moved = True

        # self.current_position_red_button_x = red_button[0].position.x
        # self.current_position_red_button_y = red_button[0].position.y

        # if self.is_position_red_button_moved or self.list_most_diamonds_in_quadrant == []:
        #     self.list_most_diamonds_in_quadrant = self.get_most_diamonds_in_quadrant(board)

        
        
        return delta_x, delta_y
    '''