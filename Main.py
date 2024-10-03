import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtGui import (
    QIcon,
    QFont,
    QPixmap,
    QPalette,
    QColor,
    QCursor
)
from PyQt6.QtCore import (
    Qt,
    QSize
)
import random

# 预设一些全局变量
# 胜局
win_count = 0
# 败局
lose_count = 0
# 局数
play_round = 0
# 上一次玩家输入
previous_input = None
# 玩家本次输入
player_choice = None
# AI本次输入
computer_choice = None

# 第0、1、2个子列表分别为石头、剪刀、布的出拳顺序所对应的次数。例如：先出石头，后出布，则为 long_term_memory[0][1]
long_term_memory_count = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
short_term_memory = []

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构造相对于脚本目录的图片路径
# 石头
rock_image = os.path.join(script_dir, "./assets/rock.png")
rock_AI_image = os.path.join(script_dir, "./assets/rock_AI.png")

# 剪刀
scissors_image = os.path.join(script_dir, "./assets/scissors.png")
scissors_AI_image = os.path.join(script_dir, "./assets/scissors_AI.png")

# 布
paper_image = os.path.join(script_dir, "./assets/paper.png")
paper_AI_image = os.path.join(script_dir, "./assets/paper_AI.png")


def long_term_memory_count_algorithm():
    """
    实现长期记忆算法以预测玩家下一次的出拳。

    该函数根据玩家之前的出拳计数预测玩家的下一次出拳。

    示例:
        假设玩家上一次出拳为石头，且长期记忆为 [[7, 8, 9], [1, 2, 3], [4, 5, 6]]，
        则该函数将返回 1，表示布（两个参数对应的索引：0为石头，1为布，2为剪刀）。

    返回:
        int: 预测的下一次出拳，取值如下：
            - 0：石头
            - 1：布
            - 2：剪刀
    """
    # Step 1: 获取子列表
    sublist = long_term_memory_count[previous_input]

    # Step 2: 找到最大元素
    max_value = max(sublist)

    # Step 3: 找到最大元素的位置
    max_index = sublist.index(max_value)

    return (max_index)


def user_to_ai(AI_Prediction):
    """
    将AI判断的玩家可能出拳选择转换为AI的出拳选择。

    当玩家出拳的情况为：
        - 如果玩家出石头（0），AI会选择剪刀（2）
        - 如果玩家出布（1），AI会选择石头（0）
        - 如果玩家出剪刀（2），AI会选择布（1）

    参数:
        AI_Prediction (int): AI对玩家出拳的预测，取值为 0（石头）、1（布）、2（剪刀）。

    返回:
        int: AI的出拳选择，取值为 0、1 或 2，分别对应石头、布和剪刀。

    示例:
        >>> user_to_ai(0)  # 玩家出拳为石头
        2  # AI选择剪刀
        >>> user_to_ai(1)  # 玩家出拳为布
        0  # AI选择石头
        >>> user_to_ai(2)  # 玩家出拳为剪刀
        1  # AI选择布
    """
    return (AI_Prediction + 2) % 3


def random_rps():
    """
    随机生成一个石头、剪刀、布的选择。

    随机生成一个石头、剪刀、布的选择作为AI的选择。

    参数：
        无

    返回:
        int: 随机选择的出拳，取值为 0（石头）、1（剪刀）、2（布）。

    示例：
        random_rps()
    """
    return random.randint(0, 2)


def convert_number_to_rps(input_number):
    """
    使用字典将数字输入转换为石头、剪刀、布的字符串表示。

    根据输入的数字，返回对应的出拳选项如下：
        - 0 -> 石头
        - 1 -> 剪刀
        - 2 -> 布

    参数:
        input_number (int): 要转换的数字，取值应为0、1或2。

    返回:
        str: 对应的出拳字符串，若输入无效返回 "无效输入"。

    示例:
        >>> convert_number_to_rps(0)
        "石头"
        >>> convert_number_to_rps(1)
        "剪刀"
        >>> convert_number_to_rps(2)
        "布"
        >>> convert_number_to_rps(3)
        "无效输入"
    """
    rps_dict = {0: "石头", 1: "剪刀", 2: "布"}
    return rps_dict.get(input_number, "无效输入")  # 使用 get 方法，找不到键返回 "无效输入"


def check_win(user_input, AI_input):
    """
    判断石头剪刀布游戏的输赢。

    通过比较玩家和AI的出拳选择来判断石头剪刀布游戏的输赢。

    参数:
        user_input（int）: 玩家选择的数字。取值如下：0为石头，1为剪刀，2为布。
        AI_input（int）: AI选择的数字。取值如下：0为石头，1为剪刀，2为布。

    返回:
        无

    示例:
        check_win(0, 1)
        # 玩家赢
    """
    # 设置全局变量
    global lose_count, win_count, play_round
    play_round += 1

    '''print(f"AI出：{convert_number_to_rps(AI_input)}")'''

    if user_input == AI_input:
        # 平局
        '''print("平局")'''
    elif (AI_input + 1) % 3 == user_input:
        # 玩家输
        lose_count += 1
        '''print(
            f"\033[1;31;5m输！\033[0m败局：{lose_count}；胜局：{win_count}；胜率：{round(win_count/play_round*100, 3)}%")'''
    else:
        # 玩家赢
        win_count += 1
        '''print(
            f"\033[1;32;5m赢\033[0m。胜局：{win_count}；败局：{lose_count}；胜率：{round(win_count/play_round*100, 3)}%")

    print("-----------------------------------------------")'''


def AI():
    """
    让AI决定使用何种算法，并返回AI的出拳选择。

    根据当前的游戏轮次，AI将决定其出拳方式：
    - 如果游戏轮次小于或等于 3，AI将随机选择出拳（石头、剪刀或布）。
    - 在其他情况下，AI将使用玩家的出拳历史（通过长远记忆算法）来预测玩家的下一次出拳。

    注：目前“让AI决定使用何种算法”的功能尚未实现。

    参数：
        无

    返回:
        int: AI的出拳选择，取值为 0（石头）、1（剪刀）、2（布）。

    示例:
        >>> AI()  # AI的出拳可能为 0、1 或 2，根据当前轮次
    """
    if play_round <= 3:
        return random_rps()
    elif True:
        return user_to_ai(long_term_memory_count_algorithm())


def update_long_term_memory_and_count(user_input):
    """
    更新长期记忆以记录玩家的出拳选择

    该函数通过将玩家的当前出拳与之前的出拳进行比较，更新长期记忆的数据结构，以便在未来的游戏中使用。

    参数:
        user_input（int）: 玩家的出拳。取值为 0（石头）、1（布）、2（剪刀）

    返回：
        无

    示例：
        update_long_term_memory_and_count(0)  # 玩家出拳为石头
    """
    # 设置全局变量
    global long_term_memory_count, previous_input

    if previous_input is not None:
        long_term_memory_count[previous_input][user_input] += 1

    previous_input = user_input


def update_short_term_memory(user_input):  # TODO：实现短期记忆算法
    """
    更新短期记忆

    TODO

    参数:
        user_input（int）: 玩家的出拳。取值为 0（石头）、1（布）、2（剪刀）

    返回：
        无

    示例：
    update_short_term_memory(0)
    """
    # 设置全局变量
    global short_term_memory, previous_input


def play(user_input):
    """
    执行一轮石头剪刀布游戏。

    根据玩家的出拳和AI的出拳选择，判断游戏结果，并更新长期记忆。

    参数:
        user_input (int): 玩家的出拳选择，取值为 0（石头）、1（剪刀）、2（布）。

    返回:
        None: 此函数不返回任何值，但会更新游戏状态和长期记忆。

    示例:
        >>> play(0)  # 玩家选择石头
    """
    # 设置全局变量
    global player_choice, computer_choice

    AI_choice = AI()
    check_win(user_input, AI_choice)
    update_long_term_memory_and_count(user_input)

    player_choice = user_input
    computer_choice = AI_choice


class RPSUI (QWidget):
    """
    石头剪刀布游戏玩家界面类。

    该类创建一个图形玩家界面，允许玩家参与石头剪刀布游戏，
    显示当前轮次、玩家和AI的得分，并有石头、剪刀、布的选择按钮。

    属性:
    无

    方法:
    initUI(): 初始化玩家界面，包括窗口设置、布局和按钮等组件。

    示例:
        app = QApplication(sys.argv)
        window = RPSUI()
        window.show()
        sys.exit(app.exec())
    """
    # 设置全局变量
    global play_round, player_choice, computer_choice

    def __init__(self):
        # 调用父类的构造函数，以确保父类的初始化逻辑得以执行
        super().__init__()

        # 设置窗口的图标为指定的图标文件
        self.setWindowIcon(QIcon(paper_image))

        # 初始化用户界面
        self.initUI()

    def initUI(self):
        # 设置窗口大小
        width = 900   # 宽度
        height = 600  # 高度
        self.resize(width, height)

        # 将窗口置于屏幕中央
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        x = (screen_size.width() - width) // 2
        y = (screen_size.height() - height) // 2

        # 设置窗口标题和大小
        self.setWindowTitle("人机游戏-石头剪刀布")
        self.setGeometry(x, y, width, height)

        # 主布局
        main_layout = QVBoxLayout()

        # 局数显示
        self.round_label = QLabel(f"Round {play_round}", self)
        self.round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置字体样式为大号加粗文本
        self.round_label.setStyleSheet("font-size: 40px; font-weight: bold;")
        main_layout.addWidget(self.round_label)

        # 添加一个伸缩项，增加间距
        main_layout.addStretch()

        # 玩家和AI的出拳显示与得分
        middle_layout = QHBoxLayout()

        # 玩家部分
        player_layout = QVBoxLayout()

        # 玩家图片显示
        self.player_image = QLabel(self)
        self.player_image.setPixmap(QPixmap(paper_image))
        self.player_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_layout.addWidget(self.player_image)

        # 玩家得分显示
        self.player_score_label = QLabel(f"{win_count}", self)
        self.player_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_score_label.setStyleSheet("font-size: 25px;")
        player_layout.addWidget(self.player_score_label)

        # 添加玩家部分至中间布局
        middle_layout.addLayout(player_layout)

        # AI部分
        ai_layout = QVBoxLayout()

        # AI图片显示
        self.ai_image = QLabel(self)
        self.ai_image.setPixmap(QPixmap(paper_AI_image))
        self.ai_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ai_layout.addWidget(self.ai_image)

        # AI得分显示
        self.ai_score_label = QLabel(f"{lose_count}", self)
        self.ai_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ai_score_label.setStyleSheet("font-size: 25px;")
        ai_layout.addWidget(self.ai_score_label)

        # 添加AI部分至中间布局
        middle_layout.addLayout(ai_layout)

        # 添加“玩家和AI的出拳显示与得分”部分至主页面
        main_layout.addLayout(middle_layout)

        # 添加一个伸缩项，增加间距
        main_layout.addStretch()

        # 按钮组布局
        button_layout = QHBoxLayout()

        def create_button(icon_path, callback):
            button = QPushButton(self)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(60, 60))
            # 设置自定义样式，背景透明，字体颜色等
            # 设置鼠标光标为手型
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 150);  /* 白色黑色 */
                    border: 1px solid rgba(255, 189, 66, 120);  /* 边框 */
                    border-radius: 10px;  /* 圆角 */
                    width: 100px; /* 宽度 */
                    height: 100px; /* 高度 */

                }
                QPushButton:hover {
                    background-color: rgb(255, 189, 66);  /* 悬停时更深的色彩 */
                }
            """
            )
            button.clicked.connect(callback)
            return button

        # 设置“石头”按钮
        rock_button = create_button(rock_image, lambda: [play(0), update_UI()])
        button_layout.addWidget(rock_button)

        # 设置“剪刀”按钮
        scissors_button = create_button(
            scissors_image, lambda: [play(1), update_UI()])
        button_layout.addWidget(scissors_button)

        # 设置“布”按钮
        paper_button = create_button(
            paper_image, lambda: [play(2), update_UI()])
        button_layout.addWidget(paper_button)

        # 将按钮组添加至主页面
        main_layout.addLayout(button_layout)

        # 设置主布局
        self.setLayout(main_layout)

        def update_UI():
            """
            更新石头剪刀布游戏UI界面

            更新局数显示，玩家、AI显示图片、得分

            参数：
                无

            返回：
                无

            示例：
                update_UI()
            """
            # 设置字典：将玩家、AI的出拳转换为对应的图片
            user_image_dict = {0: rock_image,
                               1: scissors_image, 2: paper_image}
            AI_image_dict = {0: rock_AI_image,
                             1: scissors_AI_image, 2: paper_AI_image}

            # 将玩家、AI的出拳转换为对应的图片
            user_image = user_image_dict.get(player_choice, "无效输入")
            AI_image = AI_image_dict.get(computer_choice, "无效输入")

            # 更新玩家、AI显示图片
            self.player_image.setPixmap(QPixmap(user_image))
            self.ai_image.setPixmap(QPixmap(AI_image))

            # 更新轮数显示
            self.round_label.setText(f"Round {play_round}")

            # 更新玩家、AI得分显示
            self.player_score_label.setText(f"{win_count}")
            self.ai_score_label.setText(f"{lose_count}")


# 主程序部分
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RPSUI()
    game.show()
    sys.exit(app.exec())
