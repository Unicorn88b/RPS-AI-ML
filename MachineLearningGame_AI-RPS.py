import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox
)
from PyQt6.QtGui import (
    QIcon,
    QFont,
    QPixmap)
from PyQt6.QtCore import Qt
import random

# 预设一些全局变量
win_count = 0
lose_count = 0
play_round = 0
previous_input = None

# 第0、1、2个子列表分别为石头、剪刀、布的出拳顺序所对应的次数。例如：先出石头，后出布，则为 long_term_memory[0][1]
long_term_memory_count = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
short_term_memory = []

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构造相对于脚本目录的图片路径
image_path = os.path.join(script_dir, 'rock.png')


def long_term_memory_algorithm():
    '''
    长期记忆算法

    通过查找石头、剪刀、布的出拳顺序所对应的次数来预判玩家下一次的出拳
    若 long_term_memory = [[7, 8, 9], [1, 2, 3], [4, 5, 6]]，假如玩家上一次出拳为石头，那么TA下一次出拳最有可能是布（因为在 long_term_memory[0] 中，第二个项的值最大）
    '''
    if play_round <= 2:
        return random.randint(0, 2)

    # Step 1: 获取子列表
    sublist = long_term_memory_count[previous_input]

    # Step 2: 找到最大元素
    max_value = max(sublist)

    # Step 3: 找到最大元素的位置
    max_index = sublist.index(max_value)

    return (max_index)


def user_to_ai(AIchoice):
    '''
    将用户的可能输出转为AI的输出

    0->2，1->0，2->1
    '''
    return (AIchoice + 2) % 3


def random_rps():
    return random.randint(0, 2)


def convert_number_to_rps(input_number):
    '''
    使用字典对输入进行转换

    0->石头，1->剪刀，2->布
    '''
    rps_dict = {0: "石头", 1: "剪刀", 2: "布"}
    return rps_dict.get(input_number, "无效输入")  # 使用 get 方法，找不到键返回 "无效输入"


def convert_rps_to_number(rps):
    '''
    即将弃用
    '''
    if rps == "石头":
        return 0
    elif rps == "剪刀":
        return 1
    elif rps == "布":
        return 2


def check_win(user_input, AI_input):
    """
    判断石头剪刀布的输赢。

    Args:
        user_input: 用户选择的数字，0为石头，1为剪刀，2为布。
        AI_input: AI选择的数字，0为石头，1为剪刀，2为布。
    """
    # 设置全局变量
    global lose_count, win_count, play_round
    play_round += 1

    print(f"AI出：{convert_number_to_rps(AI_input)}")

    if user_input == AI_input:
        # 平局
        print("平局")
    elif (AI_input + 1) % 3 == user_input:
        # 玩家输
        lose_count += 1
        print(
            f"\033[1;31;5m输！\033[0m败局：{lose_count}；胜局：{win_count}；胜率：{round(win_count/play_round*100, 3)}%")
    else:
        # 玩家赢
        win_count += 1
        print(
            f"\033[1;32;5m赢\033[0m。胜局：{win_count}；败局：{lose_count}；胜率：{round(win_count/play_round*100, 3)}%")

    print("-----------------------------------------------")


def AI():
    '''
    让AI决定使用何种算法，并返回AI的出拳

    注：“让AI决定使用何种算法”的功能目前暂未实现
    '''
    if play_round <= 3:
        return random_rps()
    elif True:
        return user_to_ai(long_term_memory_algorithm())


def update_long_term_memory(user_input):
    '''
    更新长期记忆

    Args:
        user_input: 用户的出拳
    '''
    # 设置全局变量
    global long_term_memory_count, previous_input

    if previous_input is not None:
        long_term_memory_count[previous_input][user_input] += 1

    previous_input = user_input


def update_short_term_memory(user_input):  # TODO：实现短期记忆算法
    '''
    更新短期记忆

    Args:
        user_input: 用户的出拳
    '''
    # 设置全局变量
    global short_term_memory, previous_input


def play(user_input):
    AI_choice = AI()
    check_win(user_input, AI_choice)
    update_long_term_memory(user_input)


class RPSUI (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("石头剪刀布")
        self.setWindowIcon(QIcon("icon.png"))

        self.round = 1
        self.player_score = 0
        self.ai_score = 0

        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('石头剪刀布游戏')
        self.setGeometry(100, 100, 400, 300)

        # 主布局
        main_layout = QVBoxLayout()

        # 局数显示
        self.round_label = QLabel(f'Round {self.round}', self)
        self.round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.round_label)

        # 添加一个伸缩项，增加间距
        main_layout.addStretch()

        # 玩家和AI的出拳显示与得分
        middle_layout = QHBoxLayout()

        # 玩家部分
        player_layout = QVBoxLayout()

        self.player_image = QLabel(self)
        self.player_image.setPixmap(QPixmap(image_path).scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.player_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_layout.addWidget(self.player_image)

        self.player_score_label = QLabel(f'{self.player_score}', self)
        self.player_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_layout.addWidget(self.player_score_label)

        middle_layout.addLayout(player_layout)

        # AI部分
        ai_layout = QVBoxLayout()

        self.ai_image = QLabel(self)
        self.ai_image.setPixmap(QPixmap(image_path).scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.ai_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ai_layout.addWidget(self.ai_image)

        self.ai_score_label = QLabel(f'{self.ai_score}', self)
        self.ai_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ai_layout.addWidget(self.ai_score_label)

        middle_layout.addLayout(ai_layout)

        main_layout.addLayout(middle_layout)

        # 添加一个伸缩项，增加间距
        main_layout.addStretch()

        # 按钮组布局
        button_layout = QHBoxLayout()

        rock_button = QPushButton(self)
        rock_button.setIcon(QIcon('rock.svg'))
        rock_button.setIconSize(self.player_image.size())
        rock_button.clicked.connect(lambda: play(0))
        button_layout.addWidget(rock_button)

        paper_button = QPushButton(self)
        paper_button.setIcon(QIcon('paper.svg'))
        paper_button.setIconSize(self.player_image.size())
        paper_button.clicked.connect(lambda: play(1))
        button_layout.addWidget(paper_button)

        scissors_button = QPushButton(self)
        scissors_button.setIcon(QIcon('scissors.svg'))
        scissors_button.setIconSize(self.player_image.size())
        scissors_button.clicked.connect(lambda: play(2))
        button_layout.addWidget(scissors_button)

        main_layout.addLayout(button_layout)

        # 设置主布局
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RPSUI()
    game.show()
    sys.exit(app.exec())
