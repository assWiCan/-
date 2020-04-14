import numpy as np
import random as rd

chessboard = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 0, 0, 0, 1, 0, 0, 0],
                       [0, 1, 0, 0, 0, 1, 0, 1],
                       [0, 0, 1, 0, 0, 0, 1, 0],
                       [0, 0, 0, 1, 0, 0, 0, 0]])


# 统计每行的皇后数
def ColCount(chessboard):
    colnum = np.zeros(8, dtype=int)
    for col in range(0, 8):
        num = 0
        for row in range(0, 8):
            if chessboard[col][row] == 1:
                num = num + 1
        colnum[col] = num
    return colnum


# 统计每列的皇后数
def RowCount(chessboard):
    rownum = np.zeros(8, dtype=int)
    for row in range(0, 8):
        num = 0
        for col in range(0, 8):
            if chessboard[col][row] == 1:
                num = num + 1
        rownum[row] = num
    return rownum


# 统计每条副对角线的皇后数
def CdiagonalCount(chessboard):
    cdiagonalnum = np.zeros(15, dtype=int)
    row = 0
    col = 0
    for cdiagonal in range(0, 15):
        num = 0
        if cdiagonal < 8:
            row = cdiagonal
            col = cdiagonal - row
            while True:
                if chessboard[row][col] == 1:
                    # print('row:{} col:{}'.format(row, col))
                    num = num + 1
                    # print('mdiagonal:{} num:{}'.format(mdiagonal, num))
                if row == 0:
                    break
                row = row - 1
                col = cdiagonal - row
            cdiagonalnum[cdiagonal] = num
        else:
            row = 7
            col = cdiagonal - row
            while 0 <= row <= 7 and 0 <= col <= 7:
                if chessboard[row][col] == 1:
                    num = num + 1
                row = row - 1
                col = cdiagonal - row
            cdiagonalnum[cdiagonal] = num

    return cdiagonalnum


# 统计每条主对角线皇后数
def MdiagonalCount(chessboard):
    mdiagonalnum = np.zeros(15, dtype=int)
    for c in range(-7, 8):
        num = 0
        for iteam in chessboard.diagonal(c):
            if iteam == 1:
                num = num + 1
        mdiagonalnum[c + 7] = num
    return mdiagonalnum


# 冲突评估函数
def DashCount(chessboard):
    dash_of_col = 0
    for colnum in ColCount(chessboard):
        if colnum != 0:
            dash_of_col = dash_of_col + colnum * (colnum - 1) * 0.5

    dash_of_row = 0
    for rownum in RowCount(chessboard):
        if rownum != 0:
            dash_of_row = dash_of_row + rownum * (rownum - 1) * 0.5

    dash_of_mdiagonal = 0
    for mdiagonalnum in MdiagonalCount(chessboard):
        if mdiagonalnum != 0:
            dash_of_mdiagonal = dash_of_mdiagonal + mdiagonalnum * (mdiagonalnum - 1) * 0.5

    dash_of_cdiagonal = 0
    for cdiagonalnum in CdiagonalCount(chessboard):
        if cdiagonalnum != 0:
            dash_of_cdiagonal = dash_of_cdiagonal + cdiagonalnum * (cdiagonalnum - 1) * 0.5
    return int(dash_of_col + dash_of_row + dash_of_mdiagonal + dash_of_cdiagonal)


# 生成下一步冲突图
def GetNextDashCount(chessboard):
    dash_map = np.zeros((8, 8), dtype=int)
    for col in range(0, 8):
        for row in range(0, 8):
            temp_chessboard = np.copy(chessboard)
            if temp_chessboard[row][col] != 1:
                for i in range(8):
                    if temp_chessboard[i][col] == 1:
                        temp_chessboard[i][col] = 0
                        temp_chessboard[row][col] = 1
                        break
                dash_map[row][col] = DashCount(temp_chessboard)
            else:
                dash_map[row][col] = -1
    return dash_map


# 寻找下一步的最优解并调整为最优解的状态,随机从最优解集中选取一组解
def FindANdMove(chessboard):
    dash_map = GetNextDashCount(chessboard)
    best_move = dash_map[0][0]
    best_row = 0
    best_col = 0
    best_sol_set = []
    for row in range(8):
        for col in range(8):
            if 0 <= dash_map[row][col] < best_move:
                best_move = dash_map[row][col]
                best_row = row
                best_col = col
    for row in range(8):
        for col in range(8):
            if dash_map[row][col] == best_move:
                best_sol_set.append([row, col])
    next_move = rd.randint(0, len(best_sol_set)-1)
    best_row = best_sol_set[next_move][0]
    best_col = best_sol_set[next_move][1]
    for switch_mark in range(8):
        if chessboard[switch_mark][best_col] == 1:
            chessboard[switch_mark][best_col] = 0
            print('交换({},{})和({},{})'.format(switch_mark, best_col, best_row, best_col))
            break
    chessboard[best_row][best_col] = 1


# print('每行皇后数：{}'.format(ColCount(chessboard)))
# print('每列皇后数：{}'.format(RowCount(chessboard)))
# print('每条主对角线皇后数：{}'.format(MdiagonalCount(chessboard)))
# print('每条副对角线皇后数：{}'.format(CdiagonalCount(chessboard)))
# print('当前状态冲突总数:{}'.format(DashCount(chessboard)))
# print('下一步状态冲突情况:\n{}'.format(GetNextDashCount(chessboard)))
# print(chessboard)
# FindANdMove(chessboard)
# print(chessboard)

while True:
    FindANdMove(chessboard)
    if DashCount(chessboard) == 0:
        print(chessboard)
        break
