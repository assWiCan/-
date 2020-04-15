import random as rd

import time

start = time.time()


chessboard = [2, 4, 7, 4, 8, 5, 5, 2]
chessboard_population = [[2, 4, 7, 4, 8, 5, 5, 2],
                         [3, 2, 7, 5, 2, 4, 1, 1],
                         [2, 4, 4, 1, 5, 1, 2, 4],
                         [3, 2, 5, 4, 3, 2, 1, 3]]


# 计算不相互共计皇后数
def NoDashCount(chessboard):
    no_dash_num = 0
    for queen in range(len(chessboard)):
        for compare_queen in range(queen, len(chessboard)):
            if (chessboard[queen] != chessboard[compare_queen] and queen != compare_queen) and \
                    ((chessboard[queen] - chessboard[compare_queen] >= 0 or chessboard[queen] - chessboard[
                        compare_queen] != queen - compare_queen) and queen != compare_queen) and \
                    (chessboard[queen] - chessboard[compare_queen] <= 0 or chessboard[compare_queen] - chessboard[
                        queen] != queen - compare_queen):
                no_dash_num = no_dash_num + 1
    return no_dash_num


# 按照概率随机抽取一个父辈样本
def RandPick(chessboard_population):
    rand_pick_list = []
    for i in range(len(chessboard_population)):
        for j in range(0, NoDashCount(chessboard_population[i])):
            rand_pick_list.append(i)
    choosen = rd.randint(0, len(rand_pick_list) - 1)
    # print(len(rand_pick_list))
    return chessboard_population[rand_pick_list[choosen]]


# 两个父辈杂交生成一个新的后代样本
def Mix(chessboard_a, chessboard_b):
    choke_point = rd.randint(1, len(chessboard_a) - 2)
    child = []
    for i in range(0, choke_point):
        child.append(chessboard_a[i])
    for i in range(choke_point, len(chessboard_a)):
        child.append(chessboard_b[i])
    return child


# 概率变异
def Heteromorphosis(child):
    if_change = rd.randint(0, 9)
    if if_change == 7:
        heteromorphosis_point = rd.randint(0, len(child) - 1)
        child[heteromorphosis_point] = rd.randint(1, 8)
    return child


new_times = 0
flag = 0
step = 0
while True:
    chessboard_population.append(Heteromorphosis(Mix(RandPick(chessboard_population), RandPick(chessboard_population))))
    if new_times % 100 == 0:
        print('=====================================', new_times)
        print('种群规模:',len(chessboard_population))
        for chessboard in chessboard_population:
            if NoDashCount(chessboard) == 28:
                flag = -1
                print(chessboard)
                break
            if NoDashCount(chessboard) < 21 + step:
                chessboard_population.remove(chessboard)
    if new_times % 1000 == 0 and step<=26:
        step = step + 0.3
    if flag == -1:
        break
    new_times = new_times + 1
end = time.time()
print(end-start)
