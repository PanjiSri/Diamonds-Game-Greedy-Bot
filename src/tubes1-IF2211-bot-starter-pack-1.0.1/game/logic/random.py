# import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
from typing import List


class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    '''
    5 komponen:
    1. Diamonds: Untuk memenangkan pertandingan, kita harus mengumpulkan diamond ini sebanyak-banyaknya dengan melewati/melangkahinya. Terdapat 2 jenis diamond yaitu diamond biru dan diamond merah. Diamond merah bernilai 2 poin, sedangkan yang biru bernilai 1 poin. Diamond akan di-regenerate secara berkala dan rasio antara diamond merah dan biru ini akan berubah setiap regeneration.
    2. Red Button/Diamond Button: Ketika red button ini dilewati/dilangkahi, semua diamond (termasuk red diamond) akan di-generate kembali pada board dengan posisi acak. Posisi red button ini juga akan berubah secara acak jika red button ini dilangkahi. 
    3. Teleporters: Terdapat 2 teleporter yang saling terhubung satu sama lain. Jika bot melewati sebuah teleporter maka bot akan berpindah menuju posisi teleporter yang lain. 
    4. Bots and Bases: Pada game ini kita akan menggerakkan bot untuk mendapatkan diamond sebanyak banyaknya. Semua bot memiliki sebuah Base dimana Base ini akan digunakan untuk menyimpan diamond yang sedang dibawa. Apabila diamond disimpan ke base, score bot akan bertambah senilai diamond yang dibawa dan inventory (akan dijelaskan di bawah) bot menjadi kosong
    5. Inventory: Bot memiliki inventory yang berfungsi sebagai tempat penyimpanan sementara diamond yang telah diambil. Inventory ini memiliki kapasitas maksimum sehingga sewaktu waktu bisa penuh. Agar inventory ini tidak penuh, bot bisa menyimpan isi inventory ke base agar inventory bisa kosong kembali. 
    '''

    quadrant = 0

    # Bagi board menjadi 4 bagian/kuadran
    def get_quadrant_max_diamonds(board: Board) -> int:
        diamonds_quadrant_counts = [[], [], [], []] 

        # Mendapatkan posisi tengah board
        center_x = board.width // 2
        center_y = board.height // 2

        for diamond in board.diamonds:
            quadrant =  1 if diamond.position.x >= center_x and diamond.position.y >= center_y else \
                        2 if diamond.position.x < center_x and diamond.position.y >= center_y else \
                        3 if diamond.position.x < center_x and diamond.position.y < center_y else \
                        4
            diamonds_quadrant_counts[quadrant-1].append(diamond)

        quadrant_max_diamonds = diamonds_quadrant_counts.index(max((len(a) for a in diamonds_quadrant_counts), default=None) + 1)

        return quadrant_max_diamonds


    def next_move(self, board_bot: GameObject, board: Board):
        global quadrant

        # Deklarasi board, posisi, sorted list diamond, teleport, red button
        props = board_bot.properties
        current_position = board_bot.position
        list_diamonds = sorted(board.diamonds, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
        teleport = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        red_button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]
        diamonds = list_diamonds[0]

        # print bot position
        print(f"Bot position: {current_position.x}, {current_position.y}")

        # get many of steps to base and time left
        steps_to_base = abs(current_position.x - props.base.x) + abs(current_position.y - props.base.y)
        time_left = int(board_bot.properties.milliseconds_left / 1000)

        # jika diamond yang dikumpulkan berjumlah 4 dan bot akan mengambil diamond merah, maka ia akan mencari diamond berikutnya (indeks daftar diamond berikutnya)
        # MASIH UNSOLVED!
        # if props.diamonds == 4 and diamonds.type == "RedDiamondGameObject" and len(list_diamonds) > 1:
        #     # Skip red diamond kalo sudah punya 4 diamonds
        #     self.goal_position = list_diamonds[1].position

        # if len(list_diamonds) > 0:
            #  self.goal_position = list_diamonds[0].position
            #  for diamond in list_diamonds:
            #      if diamond.position.x >= center_x and diamond.position.y >= center_y and quadrant_max_diamonds == 1:
            #          self.goal_position = diamond.position
            #          break
            #      elif diamond.position.x < center_x and diamond.position.y >= center_y and quadrant_max_diamonds == 2:
            #          self.goal_position = diamond.position
            #          break
            #      elif diamond.position.x < center_x and diamond.position.y < center_y and quadrant_max_diamonds == 3:
            #          self.goal_position = diamond.position
            #          break
            #      elif diamond.position.x >= center_x and diamond.position.y < center_y and quadrant_max_diamonds == 4:
            #          self.goal_position = diamond.position
            #          break

        if (steps_to_base == time_left) or props.diamonds == 5 or props.diamonds == 4:
            # Pulang ke base
            self.goal_position = board_bot.properties.base
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
        else:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                diamonds.position.x,
                diamonds.position.y,
            )

        return delta_x, delta_y