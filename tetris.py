import tkinter as tk
import time
import random

win_width = 800  # ウインドウサイズ(x)
win_height = 600  # ウインドウサイズ(y)
win_center_x = win_width/2  # 画面中心(x)
win_center_y = win_height/2  # 画面中心(y)
root = tk.Tk()
root.title(u"テトリス")
root.geometry("800x600")
cv = tk.Canvas(root, width=win_width, height=win_height)  # キャンバスの作成
cv.pack()  # パック(配置)

l = 13  # ブロックサイズの半分
mino_type = 0  # 変数宣言だけ、値に意味無し
next_mino_type = 0  # 同上
next2_mino_type = 0  # 同上
next3_mino_type = 0  # 同上
hold_mino_type = 0  # 同上
hold_flag = 0  # HOLD確認用
gameover = 0  # gameoverの判断
interlock = 0  # インターロック(入力を同時に受け付けないようにする 0:unlock,1:rock)
time_start = 0  # 変数宣言だけ、値に意味無し
time_limit = 0.8  # 初期落下時間
game_level = 1  # 初期ゲームレベル
matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 0
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 1
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 2
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 3
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 4
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 5
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 6
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 7
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 8
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 9
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 10
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 11
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 12
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 13
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 14
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 15
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 16
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 17
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 18
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 19
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # x = 0 ~ 9 , y = 20
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # x = 0 ~ 9 , y = 21


class background:

    def __init__(self):
        global l
        self.x = 283  # 左上からおいていく
        self.y = 27  # 左上からおいていく

    def draw(self):  # フィールド及び固定されたミノの描画
        for i in range(0, 10):
            for j in range(2, 22):
                if matrix[j][i] == 0:
                    self.color = "gainsboro"
                if matrix[j][i] == 1:
                    self.color = "deepskyblue"
                if matrix[j][i] == 2:
                    self.color = "yellow"
                if matrix[j][i] == 3:
                    self.color = "lightgreen"
                if matrix[j][i] == 4:
                    self.color = "red"
                if matrix[j][i] == 5:
                    self.color = "blue"
                if matrix[j][i] == 6:
                    self.color = "orange"
                if matrix[j][i] == 7:
                    self.color = "purple"
                cv.create_rectangle((self.x-l)+2*i*l, (self.y-l)+2*j*l, (self.x+l) +
                                    2*i*l, (self.y+l)+2*j*l, fill=self.color, tag="block")

    def erase(self):  # フィールド及び固定されたミノの削除
        cv.delete("block")


class I_mino:

    global l, matrix, game_level, interlock

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [-1, 0],
                             [1, 0], [2, 0]]  # [x,y]の順であり、右回転の順
        self.mino_state_1 = [[1, 0], [1, -1], [1, 1], [1, 2]]
        self.mino_state_2 = [[0, 1], [-1, 1], [1, 1], [2, 1]]
        self.mino_state_3 = [[0, 0], [0, -1], [0, 1], [0, 2]]
        self.mino_state = self.mino_state_0  # 今のテトリミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のテトリミノの向き(次のミノの向き)
        self.mino_state_num = 0  # テトリミノの向きの番号
        self.color = "deepskyblue"  # テトリミノの色
        self.color_num = 1  # カラーナンバー

    def coordinate_transform(self, X, Y):  # 座標変換
        x = 283+26*X
        y = 27+26*Y
        return x, y

    def draw(self):  # テトリミノの描画
        x, y = self.coordinate_transform(self.X, self.Y)
        for i in self.mino_state:
            cv.create_rectangle(x-l+(2*l*i[0]), y-l+(2*l*i[1]), x+l+(
                2*l*i[0]), y+l+(2*l*i[1]), fill=self.color, tag="mino")
        self.rewrite_matrix(matrix, self.mino_state, self.color_num)

    def next_mino_draw(self):  # 次のテトリミノの描画
        x, y = self.coordinate_transform(15, 4)
        for i in self.mino_state_0:
            cv.create_rectangle(x-l+(2*l*i[0]), y-l+(2*l*i[1]), x+l+(
                2*l*i[0]), y+l+(2*l*i[1]), fill=self.color, tag="next_mino")

    def next2_mino_draw(self):  # 次々のテトリミノの描画
        x, y = self.coordinate_transform(15, 8)
        for i in self.mino_state_0:
            cv.create_rectangle(x-l+(2*l*i[0]), y-l+(2*l*i[1]), x+l+(
                2*l*i[0]), y+l+(2*l*i[1]), fill=self.color, tag="next_mino")

    def next3_mino_draw(self):  # 次々々のテトリミノの描画
        x, y = self.coordinate_transform(15, 12)
        for i in self.mino_state_0:
            cv.create_rectangle(x-l+(2*l*i[0]), y-l+(2*l*i[1]), x+l+(
                2*l*i[0]), y+l+(2*l*i[1]), fill=self.color, tag="next_mino")

    def hold_mino_draw(self):  # ホールドのテトリミノの描画
        x, y = self.coordinate_transform(-6, 4)
        for i in self.mino_state_0:
            cv.create_rectangle(x-l+(2*l*i[0]), y-l+(2*l*i[1]), x+l+(
                2*l*i[0]), y+l+(2*l*i[1]), fill=self.color, tag="hold_mino")

    def rewrite_matrix(self, matrix, mino_state, value):  # 座標情報の更新
        for i in mino_state:
            matrix[self.Y+i[1]][self.X+i[0]] = value

    def drop(self):  # テトリミノのドロップ
        global gameover
        self.rewrite_matrix(matrix, self.mino_state, 0)
        if (self.Y+self.mino_state[0][1] == 21 or
            self.Y+self.mino_state[1][1] == 21 or
            self.Y+self.mino_state[2][1] == 21 or
            self.Y+self.mino_state[3][1] == 21 or
            matrix[self.Y+1+self.mino_state[0][1]][self.X+self.mino_state[0][0]] != 0 or
            matrix[self.Y+1+self.mino_state[1][1]][self.X+self.mino_state[1][0]] != 0 or
            matrix[self.Y+1+self.mino_state[2][1]][self.X+self.mino_state[2][0]] != 0 or
                matrix[self.Y+1+self.mino_state[3][1]][self.X+self.mino_state[3][0]] != 0):

            self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            self.gameover()
            if gameover == 0:
                self.line_check()

        else:
            self.rewrite_matrix(matrix, self.mino_state, 0)
            self.Y += 1
            self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            self.erase()
            self.draw()

    def erase(self):  # テトリミノの描画の削除
        cv.delete("mino")
        cv.delete("mino")

    def get_mino_state(self, mino_state_num):  # テトリミノ回転向きの取得
        if self.mino_state_num == 0 or self.mino_state_num == 4:
            return self.mino_state_0
        if self.mino_state_num == 1:
            return self.mino_state_1
        if self.mino_state_num == 2:
            return self.mino_state_2
        if self.mino_state_num == 3 or self.mino_state_num == -1:
            return self.mino_state_3

    def left(self, event):  # テトリミノの左移動
        global interlock
        if gameover == 0 and interlock == 0:  # gameoverかつ処理中でなければ
            interlock = 1
            self.rewrite_matrix(matrix, self.mino_state, 0)
            if (0 <= self.X-1+self.mino_state[0][0] <= 9 and 0 <= self.Y+self.mino_state[0][1] <= 21 and
                0 <= self.X-1+self.mino_state[1][0] <= 9 and 0 <= self.Y+self.mino_state[1][1] <= 21 and
                0 <= self.X-1+self.mino_state[2][0] <= 9 and 0 <= self.Y+self.mino_state[2][1] <= 21 and
                    0 <= self.X-1+self.mino_state[3][0] <= 9 and 0 <= self.Y+self.mino_state[3][1] <= 21):
                if(matrix[self.Y+self.mino_state[0][1]][self.X-1+self.mino_state[0][0]] == 0 and
                   matrix[self.Y+self.mino_state[1][1]][self.X-1+self.mino_state[1][0]] == 0 and
                   matrix[self.Y+self.mino_state[2][1]][self.X-1+self.mino_state[2][0]] == 0 and
                   matrix[self.Y+self.mino_state[3][1]][self.X-1+self.mino_state[3][0]] == 0):
                    self.rewrite_matrix(matrix, self.mino_state, 0)
                    self.X -= 1
                    self.rewrite_matrix(
                        matrix, self.mino_state, self.color_num)
                    self.erase()
                    self.draw()
                else:
                    self.rewrite_matrix(
                        matrix, self.mino_state, self.color_num)
            else:
                self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            interlock = 0

    def right(self, event):  # テトリミノの右移動
        global interlock
        if gameover == 0 and interlock == 0:  # gameoverかつ処理中でなければ
            interlock = 1
            self.rewrite_matrix(matrix, self.mino_state, 0)
            if (0 <= self.X+1+self.mino_state[0][0] <= 9 and 0 <= self.Y+self.mino_state[0][1] <= 21 and
                0 <= self.X+1+self.mino_state[1][0] <= 9 and 0 <= self.Y+self.mino_state[1][1] <= 21 and
                0 <= self.X+1+self.mino_state[2][0] <= 9 and 0 <= self.Y+self.mino_state[2][1] <= 21 and
                    0 <= self.X+1+self.mino_state[3][0] <= 9 and 0 <= self.Y+self.mino_state[3][1] <= 21):
                if(matrix[self.Y+self.mino_state[0][1]][self.X+1+self.mino_state[0][0]] == 0 and
                   matrix[self.Y+self.mino_state[1][1]][self.X+1+self.mino_state[1][0]] == 0 and
                   matrix[self.Y+self.mino_state[2][1]][self.X+1+self.mino_state[2][0]] == 0 and
                   matrix[self.Y+self.mino_state[3][1]][self.X+1+self.mino_state[3][0]] == 0):

                    self.rewrite_matrix(matrix, self.mino_state, 0)
                    self.X += 1
                    self.rewrite_matrix(
                        matrix, self.mino_state, self.color_num)
                    self.erase()
                    self.draw()
                else:
                    self.rewrite_matrix(
                        matrix, self.mino_state, self.color_num)
            else:
                self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            interlock = 0

    def quick_drop(self, event):  # テトリミノの高速落下
        global time_start, interlock
        if gameover == 0 and interlock == 0:  # gameoverかつ処理中でなければ
            interlock = 1
            time_start -= 100
            score.score += 1*game_level
            score.delete()
            score.draw()
            interlock = 0

    def move(self):  # キーボードの入力の受付
        root.bind("<Right>", self.right)
        root.bind("<Left>", self.left)
        root.bind("<z>", self.rotate_L)
        root.bind("<x>", self.rotate_R)
        root.bind("<Down>", self.quick_drop)
        root.bind("<Up>", self.hard_drop)
        root.bind("<Control_L>", self.hold)

    def hard_drop(self, event):  # テトリミノのハードドロップ

        global time_start, interlock
        if gameover == 0 and interlock == 0:  # gameoverかつ処理中でなければ
            interlock = 1
            self.rewrite_matrix(matrix, self.mino_state, 0)
            while (0 <= self.Y+self.mino_state[0][1] <= 20 and
                   0 <= self.Y+self.mino_state[1][1] <= 20 and
                   0 <= self.Y+self.mino_state[2][1] <= 20 and
                   0 <= self.Y+self.mino_state[3][1] <= 20 and
                   matrix[self.Y+1+self.mino_state[0][1]][self.X+self.mino_state[0][0]] == 0 and
                   matrix[self.Y+1+self.mino_state[1][1]][self.X+self.mino_state[1][0]] == 0 and
                   matrix[self.Y+1+self.mino_state[2][1]][self.X+self.mino_state[2][0]] == 0 and
                   matrix[self.Y+1+self.mino_state[3][1]][self.X+self.mino_state[3][0]] == 0):

                self.Y += 1
                score.score += 1*game_level
            self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            time_start -= 10000
            score.delete()
            score.draw()
            self.erase()
            self.draw()
            interlock = 0

    def hold(self, event):  # テトリミノのホールド

        global hold_mino_type, mino_type, next_mino_type, hold_flag, interlock
        if gameover == 0 and hold_flag == 0 and interlock == 0:  # gameoverかつミノチェンジ後かつ処理中でなければ
            interlock = 1
            mino_type, hold_mino_type = hold_mino_type, mino_type
            if mino_type == 0:
                mino_select.select()
                next_mino.delete()
                next_mino.draw()
            hold_mino.delete()
            hold_mino.draw()
            self.erase()
            self.rewrite_matrix(matrix, self.mino_state, 0)
            self.__init__()
            mino_type.draw()
            hold_flag = 1
            interlock = 0

    def rotate_L(self, event):  # テトリミノの左回転
        global interlock
        if gameover == 0 and interlock == 0:  # gameoverかつ処理中でなければ
            interlock = 1
            self.rewrite_matrix(matrix, self.mino_state, 0)
            self.mino_state_temp = self.get_mino_state(self.mino_state_num-1)
            if (0 <= self.X+self.mino_state_temp[0][0] <= 9 and 0 <= self.Y+self.mino_state_temp[0][1] <= 21 and
                0 <= self.X+self.mino_state_temp[1][0] <= 9 and 0 <= self.Y+self.mino_state_temp[1][1] <= 21 and
                0 <= self.X+self.mino_state_temp[2][0] <= 9 and 0 <= self.Y+self.mino_state_temp[2][1] <= 21 and
                    0 <= self.X+self.mino_state_temp[3][0] <= 9 and 0 <= self.Y+self.mino_state_temp[3][1] <= 21):
                if(matrix[self.Y+self.mino_state_temp[0][1]][self.X+self.mino_state_temp[0][0]] == 0 and
                   matrix[self.Y+self.mino_state_temp[1][1]][self.X+self.mino_state_temp[1][0]] == 0 and
                   matrix[self.Y+self.mino_state_temp[2][1]][self.X+self.mino_state_temp[2][0]] == 0 and
                   matrix[self.Y+self.mino_state_temp[3][1]][self.X+self.mino_state_temp[3][0]] == 0):
                    self.mino_state_num -= 1
                    if self.mino_state_num == -1:
                        self.mino_state_num = 4
                    self.rewrite_matrix(matrix, self.mino_state, 0)
                    self.mino_state = self.mino_state_temp
                    self.rewrite_matrix(
                        matrix, self.mino_state, self.color_num)
                    self.erase()
                    self.draw()
            else:
                self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            interlock = 0

    def rotate_R(self, event):  # テトリミノの右回転
        global interlock
        if gameover == 0 and interlock == 0:  # gameoverかつ処理中でなければ
            interlock = 1
            self.rewrite_matrix(matrix, self.mino_state, 0)
            self.mino_state_temp = self.get_mino_state(self.mino_state_num+1)
            if (0 <= self.X+self.mino_state_temp[0][0] <= 9 and 0 <= self.Y+self.mino_state_temp[0][1] <= 21 and
                0 <= self.X+self.mino_state_temp[1][0] <= 9 and 0 <= self.Y+self.mino_state_temp[1][1] <= 21 and
                0 <= self.X+self.mino_state_temp[2][0] <= 9 and 0 <= self.Y+self.mino_state_temp[2][1] <= 21 and
                    0 <= self.X+self.mino_state_temp[3][0] <= 9 and 0 <= self.Y+self.mino_state_temp[3][1] <= 21):
                if(matrix[self.Y+self.mino_state_temp[0][1]][self.X+self.mino_state_temp[0][0]] == 0 and
                   matrix[self.Y+self.mino_state_temp[1][1]][self.X+self.mino_state_temp[1][0]] == 0 and
                   matrix[self.Y+self.mino_state_temp[2][1]][self.X+self.mino_state_temp[2][0]] == 0 and
                   matrix[self.Y+self.mino_state_temp[3][1]][self.X+self.mino_state_temp[3][0]] == 0):
                    self.mino_state_num += 1
                    if self.mino_state_num == 5:
                        self.mino_state_num = 1
                    self.rewrite_matrix(matrix, self.mino_state, 0)
                    self.mino_state = self.mino_state_temp
                    self.rewrite_matrix(
                        matrix, self.mino_state, self.color_num)
                    self.erase()
                    self.draw()
            else:
                self.rewrite_matrix(matrix, self.mino_state, self.color_num)
            interlock = 0

    def line_check(self):  # ラインチェック
        global game_level
        self.erase()
        line = []
        for i in range(0, 22):
            cnt = 0
            for j in range(0, 10):
                if matrix[i][j] == 0:
                    break
                else:
                    cnt += 1
            if cnt == 10:
                line.append(i)
        for i in line:
            del matrix[i]
            matrix.reverse()
            matrix.extend([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
            matrix.reverse()
        if len(line) == 1:  # 1列揃う
            score.score += 40*game_level
        elif len(line) == 2:  # 2列揃う
            score.score += 100*game_level
        elif len(line) == 3:  # 3列揃う
            score.score += 300*game_level
        elif len(line) == 4:  # 4列揃う
            score.score += 1200*game_level
        score.delete()
        score.draw()
        background.erase()
        background.draw()
        self.__init__()
        mino_select.select()
        next_mino.delete()
        next_mino.draw()
        mino_type.draw()

    def gameover(self):  # ゲームオーバー判定
        global gameover
        if (matrix[0][0] or matrix[0][1] or matrix[0][2] or matrix[0][3] or
            matrix[0][4] or matrix[0][5] or matrix[0][6] or matrix[0][7] or
            matrix[0][8] or matrix[0][9] or matrix[1][0] or matrix[1][1] or
            matrix[1][2] or matrix[1][3] or matrix[1][4] or matrix[1][5] or
                matrix[1][6] or matrix[1][7] or matrix[1][8] or matrix[1][9]):

            gameover = 1


class O_mino(I_mino):

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [1, 0], [
            0, -1], [1, -1]]  # [x,y]の順であり、右回転
        self.mino_state_1 = [[0, 0], [1, 0], [0, -1], [1, -1]]
        self.mino_state_2 = [[0, 0], [1, 0], [0, -1], [1, -1]]
        self.mino_state_3 = [[0, 0], [1, 0], [0, -1], [1, -1]]
        self.mino_state = self.mino_state_0  # 今のミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のミノの向き(次のミノの向き)
        self.mino_state_num = 0  # ミノの向きの番号
        self.matrix = matrix
        self.color = "yellow"
        self.color_num = 2


class S_mino(I_mino):

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [-1, 0],
                             [0, -1], [1, -1]]  # [x,y]の順であり、右回転
        self.mino_state_1 = [[0, 0], [1, 0], [1, 1], [0, -1]]
        self.mino_state_2 = [[0, 0], [1, 0], [-1, 1], [0, 1]]
        self.mino_state_3 = [[0, 0], [0, 1], [-1, 0], [-1, -1]]
        self.mino_state = self.mino_state_0  # 今のミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のミノの向き(次のミノの向き)
        self.mino_state_num = 0  # ミノの向きの番号
        self.matrix = matrix
        self.color = "lightgreen"
        self.color_num = 3


class Z_mino(I_mino):

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [1, 0], [
            0, -1], [-1, -1]]  # [x,y]の順であり、右回転
        self.mino_state_1 = [[0, 0], [0, 1], [1, 0], [1, -1]]
        self.mino_state_2 = [[0, 0], [0, 1], [-1, 0], [1, 1]]
        self.mino_state_3 = [[0, 0], [0, -1], [-1, 0], [-1, 1]]
        self.mino_state = self.mino_state_0  # 今のミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のミノの向き(次のミノの向き)
        self.mino_state_num = 0  # ミノの向きの番号
        self.matrix = matrix
        self.color = "red"
        self.color_num = 4


class J_mino(I_mino):

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [1, 0],
                             [-1, 0], [-1, -1]]  # [x,y]の順であり、右回転
        self.mino_state_1 = [[0, 0], [0, -1], [1, -1], [0, 1]]
        self.mino_state_2 = [[0, 0], [-1, 0], [1, 0], [1, 1]]
        self.mino_state_3 = [[0, 0], [0, -1], [0, 1], [-1, 1]]
        self.mino_state = self.mino_state_0  # 今のミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のミノの向き(次のミノの向き)
        self.mino_state_num = 0  # ミノの向きの番号
        self.matrix = matrix
        self.color = "blue"
        self.color_num = 5


class L_mino(I_mino):

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [1, 0],
                             [-1, 0], [1, -1]]  # [x,y]の順であり、右回転
        self.mino_state_1 = [[0, 0], [0, -1], [0, 1], [1, 1]]
        self.mino_state_2 = [[0, 0], [1, 0], [-1, 0], [-1, 1]]
        self.mino_state_3 = [[0, 0], [0, 1], [0, -1], [-1, -1]]
        self.mino_state = self.mino_state_0  # 今のミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のミノの向き(次のミノの向き)
        self.mino_state_num = 0  # ミノの向きの番号
        self.matrix = matrix
        self.color = "orange"
        self.color_num = 6


class T_mino(I_mino):

    def __init__(self):
        self.X = 4
        self.Y = 1
        self.mino_state_0 = [[0, 0], [1, 0],
                             [-1, 0], [0, -1]]  # [x,y]の順であり、右回転
        self.mino_state_1 = [[0, 0], [1, 0], [0, 1], [0, -1]]
        self.mino_state_2 = [[0, 0], [1, 0], [-1, 0], [0, 1]]
        self.mino_state_3 = [[0, 0], [0, 1], [-1, 0], [0, -1]]
        self.mino_state = self.mino_state_0  # 今のミノの向き
        self.mino_state_temp = self.mino_state_1  # 検証用のミノの向き(次のミノの向き)
        self.mino_state_num = 0  # ミノの向きの番号
        self.matrix = matrix
        self.color = "purple"
        self.color_num = 7


class mino_select:  # テトリミノのセレクト

    def __init__(self):
        global mino_type, next_mino_type, next2_mino_type, next3_mino_type
        self.dict_mino_type = {1: I_mino, 2: O_mino, 3: S_mino,
                               4: Z_mino, 5: J_mino, 6: L_mino, 7: T_mino}
        self.list = [1, 2, 3, 4, 5, 6, 7]
        num = random.choice(self.list)
        mino_type = self.dict_mino_type[num]  # 今のミノの形
        self.list.remove(num)

        num = random.choice(self.list)
        next_mino_type = self.dict_mino_type[num]  # 次のミノの形
        self.list.remove(num)

        num = random.choice(self.list)
        next2_mino_type = self.dict_mino_type[num]  # 次々のミノの形
        self.list.remove(num)

        num = random.choice(self.list)
        next3_mino_type = self.dict_mino_type[num]  # 次々々のミノの形
        self.list.remove(num)

    def select(self):
        global mino_type, next_mino_type, next2_mino_type, next3_mino_type, hold_flag
        if len(self.list) == 0:
            self.list = [1, 2, 3, 4, 5, 6, 7]
        mino_type = next_mino_type
        next_mino_type = next2_mino_type
        next2_mino_type = next3_mino_type
        num = random.choice(self.list)
        next3_mino_type = self.dict_mino_type[num]  # 次々々のミノの形
        self.list.remove(num)
        hold_flag = 0


class Hold_mino:  # ホールドテトリミノの描画

    def __init__(self):
        cv.create_text(130, 50, text="HOLD", font=('FixedSys', 35), tag="hold")

    def draw(self):
        global hold_mino_type
        if hold_mino_type != 0:
            hold_mino_type.hold_mino_draw()

    def delete(self):
        cv.delete("hold_mino")


class Next_mino:  # ネクストテトリミノの描画

    def __init__(self):
        cv.create_text(670, 50, text="NEXT", font=('FixedSys', 35), tag="next")

    def draw(self):
        next_mino_type.next_mino_draw()
        next2_mino_type.next2_mino_draw()
        next3_mino_type.next3_mino_draw()

    def delete(self):
        cv.delete("next_mino")


class Score:  # スコア

    def __init__(self):
        self.score = 0  # スコアの初期値
        cv.create_text(130, 280, text="Score", font=(
            'FixedSys', 35), tag="score_name")

    def draw(self):
        cv.create_text(130, 350, text=str(self.score),
                       font=('FixedSys', 35), tag="score")

    def delete(self):
        cv.delete("score")


class Level:  # レベル

    def __init__(self):
        global time_limit, game_level
        time_limit = 0.8
        game_level = 1
        cv.create_text(130, 500, text="Lv."+str(game_level),
                       font=('FixedSys', 35), tag="level")

    def draw(self):
        global time_limit, game_level
        if score.score < 1000:
            game_level = 1
            time_limit = 0.8
        elif 1000 <= score.score < 2000:
            game_level = 2
            time_limit = 0.7
        elif 2000 <= score.score < 5000:
            game_level = 3
            time_limit = 0.6
        elif 5000 <= score.score < 10000:
            game_level = 4
            time_limit = 0.5
        elif 10000 <= score.score < 15000:
            game_level = 5
            time_limit = 0.4
        elif 15000 <= score.score < 20000:
            game_level = 6
            time_limit = 0.3
        elif 20000 <= score.score < 30000:
            game_level = 7
            time_limit = 0.2
        elif 30000 <= score.score < 40000:
            game_level = 8
            time_limit = 0.1
        elif 40000 <= score.score:
            game_level = 9
            time_limit = 0.05
        cv.delete("level")
        cv.create_text(130, 500, text="Lv."+str(game_level),
                       font=('FixedSys', 35), tag="level")


class Window:  # ウィンドウを閉じる
    def close(self, event):
        root.destroy()


# インスタンス生成
I_mino = I_mino()
O_mino = O_mino()
S_mino = S_mino()
Z_mino = Z_mino()
J_mino = J_mino()
L_mino = L_mino()
T_mino = T_mino()
background = background()
level = Level()
score = Score()
next_mino = Next_mino()
hold_mino = Hold_mino()
mino_select = mino_select()
window = Window()

# 初期描画
background.draw()
mino_type.draw()
hold_mino.draw()
next_mino.draw()
score.draw()
level.draw()

# ゲームのメインループ
while gameover == 0:  # ゲームオーバでなければ
    time_start = time.time()
    while time.time()-time_start <= time_limit:  # 指定時間の間繰り返す
        mino_type.move()  # テトリミノの操作
        root.update()  # 描画の更新
        for i in matrix:
            print(i)
        print("\n")
    interlock = 1
    mino_type.drop()  # テトリミノの落下
    level.draw()  # スコアの更新
    root.update()  # 描画の更新
    interlock = 0
cv.create_text(win_center_x, win_center_y, text="gameover",
               font=('FixedSys', 100), tag="gameover")  # ゲームオーバの表示
cv.create_text(670, 560, text="Escで終了", font=('ＭＳ ゴシック', 30), tag="gameover")
root.bind("<Escape>", window.close)  # Escで閉じる

root.mainloop()
