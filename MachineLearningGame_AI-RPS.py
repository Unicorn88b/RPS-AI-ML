print("猜拳游戏，填汝欲出者，譬如：石头。欲退则曰：退出")
print("-----------------------------------------------")
win = 0
lose = 0
list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 分别为石头、剪刀、布
FirstInput = int()
SecondInput = ""


def find_max_index(UserInput):
    # Step 1: 获取子列表
    first_list = list[UserInput]

    # Step 2: 找到最大元素
    max_value = max(first_list)

    # Step 3: 找到最大元素的位置
    max_index = first_list.index(max_value)

    return (max_index)


def UserInput_to_AIinput(AIchoice):
    if AIchoice == 0:
        return 2
    elif AIchoice == 1:
        return 0
    else:
        return 1


def convert_number_to_rps(number):
    if number == 0:
        return "石头"
    elif number == 1:
        return "剪刀"
    elif number == 2:
        return "布"


def convert_rps_to_number(rps):
    if rps == "石头":
        return 0
    elif rps == "剪刀":
        return 1
    elif rps == "布":
        return 2


def check_win(UserInput, AIinput):
    """
    判断石头剪刀布的输赢。

    Args:
        UserInput: 用户选择的数字，0为石头，1为剪刀，2为布。
        AIinput: AI选择的数字，0为石头，1为剪刀，2为布。
    """

    print("AI出：{}".format(convert_number_to_rps(AIinput)))

    # 判定平局
    if UserInput == AIinput:
        print("平局")
        print("-----------------------------------------------")
        return

    # 判定用户输的情况
    if (UserInput == 0 and AIinput == 2) or \
       (UserInput == 1 and AIinput == 0) or \
       (UserInput == 2 and AIinput == 1):
        global lose
        lose += 1
        print("\033[1;31;5m输！\033[0m败局：", lose)
        print("-----------------------------------------------")
        return

    # 否则用户赢
    global win
    win += 1
    print("\033[1;32;5m赢\033[0m。胜局：", win)
    print("-----------------------------------------------")
    return


def AI(UserInput):
    AIchoice = find_max_index(UserInput)
    AIchoice = UserInput_to_AIinput(AIchoice)
    check_win(UserInput, AIchoice)


def save_list(UserInput):
    global FirstInput
    global SecondInput
    global list
    SecondInput = UserInput
    if FirstInput != "":
        list[FirstInput][SecondInput] += 1
    FirstInput = UserInput


while True:
    UserInput = input("汝欲出：")
    if UserInput in ["0", "1", "2"]:
        UserInput = int(UserInput)
        AI(UserInput)

    elif UserInput in ["石头", "剪刀", "布"]:
        UserInput = convert_rps_to_number(UserInput)
        AI(UserInput)
        save_list(UserInput)
        # print(list)

    elif "退出" in UserInput:
        lose_text = R'''
   ____                                 ___                          _   _   _ 
  / ___|   __ _   _ __ ___     ___     / _ \  __   __   ___   _ __  | | | | | |
 | |  _   / _` | | '_ ` _ \   / _ \   | | | | \ \ / /  / _ \ | '__| | | | | | |
 | |_| | | (_| | | | | | | | |  __/   | |_| |  \ V /  |  __/ | |    |_| |_| |_|
  \____|  \__,_| |_| |_| |_|  \___|    \___/    \_/    \___| |_|    (_) (_) (_)
'''
        print("\033[1;31;5m", lose_text, "\033[0m")
        break

    else:
        print("汝瞎乎？抑汝天质之卑耶？")
        print("-----------------------------------------------")
