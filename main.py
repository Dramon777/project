import codecs
import sys
from random import randint

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QDesktopWidget, QLabel, QPushButton
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from collections import deque

game_sys_lang = 'Eng'
game_mod = None
wnd_menu = None
wnd_error = None
wnd_of_rules = None
text_rules = None
wnd_of_playing = None
wnd_of_choosing_dice_color = None
wnd_win = None
dice_value = None
dice_color = ''
dices_colors = {
    'white': {
        1: "dices/1_w.png",
        2: "dices/2_w.png",
        3: "dices/3_w.png",
        4: "dices/4_w.png",
        5: "dices/5_w.png",
        6: "dices/6_w.png"
    },
    'black': {
        1: "dices/1_b.png",
        2: "dices/2_b.png",
        3: "dices/3_b.png",
        4: "dices/4_b.png",
        5: "dices/5_b.png",
        6: "dices/6_b.png"
    }
}

# расположения всех треугольников

triangles = {
    0: [195, 787],
    1: [285, 787],
    2: [372, 787],
    3: [460, 787],
    4: [547, 787],
    5: [635, 787],
    6: [765, 787],
    7: [855, 787],
    8: [940, 787],
    9: [1028, 787],
    10: [1115, 787],
    11: [1200, 787],
    12: [1200, 35],
    13: [1112, 35],
    14: [1025, 35],
    15: [937, 35],
    16: [847, 35],
    17: [757, 35],
    18: [630, 35],
    19: [545, 35],
    20: [455, 35],
    21: [370, 35],
    22: [280, 35],
    23: [190, 35]
}


# Нейронная сеть
class BackgammonNN(nn.Module):
    def __init__(self):
        super(BackgammonNN, self).__init__()
        self.fc1 = nn.Linear(24 * 2, 128)  # 24 позиции на поле, 2 игрока
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 24 * 2)  # 24 позиции * 2 кубика

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x.view(-1, 24, 2)  # Формат: [batch_size, 24 позиции, 2 кубика]


# Инициализация нейронной сети
model = BackgammonNN()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Очередь для хранения данных (состояния и ходы)
training_data = deque(maxlen=10000)  # Ограничим размер очереди


# Функция для преобразования состояния игрового поля в вектор
def state_to_vector(cells):
    vector = np.zeros(24 * 2)
    for i, cell in enumerate(cells):
        if len(cell) > 0:
            if 'reddd' in cell[0].objectName():
                vector[i] = len(cell)
            else:
                vector[i + 24] = len(cell)
    return torch.FloatTensor(vector)


# Функция для выбора хода с помощью нейронной сети
def choose_move_with_nn(cells, player_color, first_dice, second_dice):
    state_vector = state_to_vector(cells)
    model.eval()
    with torch.no_grad():
        output = model(state_vector.unsqueeze(0))  # Добавляем batch dimension
    output = output.squeeze(0).numpy()  # Убираем batch dimension

    # Выбираем ходы для текущего игрока
    if player_color == 'reddd':
        possible_moves = output[:24]  # Ходы для красных
    else:
        possible_moves = output[24:]  # Ходы для белых

    # Проверяем, есть ли допустимые ходы
    if np.all(possible_moves == 0):
        print("No valid moves found by the neural network. Using random move.")
        return generate_random_move(cells, player_color, first_dice, second_dice)

    # Выбираем ход с максимальной оценкой
    move_index = np.argmax(possible_moves)
    current_position = move_index // 2  # Текущая позиция фишки
    dice_index = move_index % 2  # Индекс кубика (0 или 1)

    # Получаем значение кубика
    dice_value = first_dice if dice_index == 0 else second_dice

    return [current_position, dice_value]


# Генерация случайного хода
def generate_random_move(cells, player_color, first_dice, second_dice):
    valid_moves = []
    for i, cell in enumerate(cells):
        if len(cell) > 0 and player_color in cell[0].objectName():
            if first_dice != -1000:
                target_pos = (i + first_dice) % 24
                if len(cells[target_pos]) == 0 or player_color in cells[target_pos][0].objectName():
                    valid_moves.append([i, first_dice])
            if second_dice != -1000:
                target_pos = (i + second_dice) % 24
                if len(cells[target_pos]) == 0 or player_color in cells[target_pos][0].objectName():
                    valid_moves.append([i, second_dice])

    if len(valid_moves) == 0:
        return None
    return valid_moves[randint(0, len(valid_moves) - 1)]


# Функция для сохранения данных (состояние и ход)
def save_training_data(state, move):
    training_data.append((state, move))


# Функция для обучения модели
def train_model():
    if len(training_data) < 100:  # Обучаем, если накопилось достаточно данных
        return

    # Преобразуем данные в тензоры
    states = torch.stack([data[0] for data in training_data])
    moves = torch.FloatTensor([data[1] for data in training_data])

    # Обучаем модель
    model.train()
    optimizer.zero_grad()
    outputs = model(states)
    loss = criterion(outputs, moves)
    loss.backward()
    optimizer.step()

    print(f"Model trained. Loss: {loss.item()}")

    # Очищаем данные после обучения
    training_data.clear()


# Функция для сохранения модели
def save_model(filename="backgammon_model.pth"):
    torch.save(model.state_dict(), filename)
    print(f"Model saved to {filename}")


# Функция для загрузки модели
def load_model(filename="backgammon_model.pth"):
    if os.path.exists(filename):
        model.load_state_dict(torch.load(filename))
        print(f"Model loaded from {filename}")
    else:
        print("No saved model found. Starting from scratch.")


# правила

def open_rules():
    global wnd_of_rules
    wnd_menu.hide()
    wnd_of_rules = Rules()
    wnd_of_rules.show()


# функция обновления окна

def updater(self):
    global wnd_menu
    self.close()
    wnd_menu = Menu()
    wnd_menu.show()


# доп функция смены языка

def switch_lang(language):
    global game_sys_lang
    game_sys_lang = language


# функция центрирования окна

def centering(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())


# функция установки белого цвета у кубиков
def chose_color_white():
    global dice_color
    dice_color = 'white'
    print(dice_color)


# функция установки белого цвета у кубиков
def chose_color_black():
    global dice_color
    dice_color = 'black'
    print(dice_color)


# функция установки белого цвета у кубиков
def chose_color_both():
    global dice_color
    dice_color = 'both'
    print(dice_color)


# функция базовых настроек каждого окна

def set_args(self, w, h):
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                        QtCore.Qt.WindowStaysOnTopHint)
    self.setFixedSize(w, h)
    centering(self)
    QtWidgets.QApplication.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 255))
    palette.setColor(QPalette.WindowText, QColor(50, 50, 50))
    palette.setColor(QPalette.Button, QColor(180, 200, 255))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(230, 230, 255))
    palette.setColor(QPalette.AlternateBase, QColor(255, 250, 250))
    QtWidgets.QApplication.setPalette(palette)


# функция отображения окна ошибка в связи с невыбранностью режима игры

def error_of_game_mod(self1):
    global wnd_error
    if game_sys_lang == 'Eng':
        wnd_error = Error('<b>Wrong game mod</b>')
    else:
        wnd_error = Error('<b>Ошибка игрового режима</b>')
    self1.hide()
    wnd_error.show()


# функция отображения окна ошибка в связи с невыбранностью цвета кубиков
def error_of_dice_color(self1):
    global wnd_error
    if game_sys_lang == 'Eng':
        wnd_error = Error('<b>Wrong dice color</b>')
    else:
        wnd_error = Error('<b>Ошибка цвета кубиков</b>')
    self1.hide()
    wnd_error.show()


# функция выбора режима игры игрока против бота
def vsBot():
    global game_mod
    game_mod = 'bot'
    print(game_mod)


# функция выбора режима игры 1 на 1
def one_vs_one():
    global game_mod
    game_mod = '1vs1'
    print(game_mod)


# окно ошибки

class Error(QtWidgets.QWidget):
    def __init__(self, wrong):
        super().__init__()
        self.wrong = wrong
        self.ok_button = None
        self.lbl = None
        self.setupUI()

    def setupUI(self):
        set_args(self, 400, 110)
        self.setObjectName("error")
        self.lbl = QLabel(self)

        # вывод ошибки

        if game_sys_lang == 'Eng':
            self.lbl.setText(f'<b>Error: {self.wrong}!</b>')
        else:
            self.lbl.setText(f'<b>Ошибка: {self.wrong}!</b>')
        self.lbl.setStyleSheet("font-size: 18px;")
        self.lbl.move(5, 10)

        # кнопка "ок", для обозначения, что пользовватель ознакоммился с ошибкой

        self.ok_button = QtWidgets.QPushButton("ОК", self)
        self.ok_button.setGeometry(QtCore.QRect(90, 50, 220, 55))
        self.ok_button.setStyleSheet("font-size: 16px;")

        self.ok_button.clicked.connect(self.back)

    # функция закрытия окна и открытия меню

    def back(self):
        wnd_menu.show()
        self.close()


class GameEnd(QtWidgets.QWidget):
    def __init__(self, winner):
        super().__init__()
        self.txt_lbl = None
        self.back_menu = None
        self.winner = winner
        self.setupUI()

    def setupUI(self):
        wnd_of_playing.hide()
        set_args(self, 300, 100)

        self.txt_lbl = QLabel(self)
        if game_sys_lang == 'Рус':
            self.txt_lbl.setText(f"{'Белые' if self.winner == 'white' else 'Красные'} одержали победу!!!")
            self.back_menu = QPushButton('Вернуться в меню', self)
        else:
            self.txt_lbl.setText(f"{'White' if self.winner == 'white' else 'Red'} won!!!")
            self.back_menu = QPushButton('Back to menu', self)

        self.txt_lbl.setStyleSheet('font-size: 20px;')
        self.txt_lbl.move(20 if game_sys_lang == 'Рус' else 95, 10)

        self.back_menu.setStyleSheet('font-size: 20px;')
        self.back_menu.move(85 if game_sys_lang == 'Eng' else 65, 50)
        self.back_menu.clicked.connect(self.back)

    def back(self):
        global game_mod
        game_mod = None
        wnd_menu.show()
        self.close()
        wnd_of_playing.close()


# окно игры

class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.bg_lbl = None
        self.bg_pixmap = None
        self.button_back = None
        self.button_throw_dice = None
        self.wnd_of_exit = None

        # обязательные 2 кубика
        self.lbl_dice1 = None
        self.pixmap_dice1 = None
        self.lbl_dice2 = None
        self.pixmap_dice2 = None

        # необязательные 2 кубика
        self.lbl_dice3 = None
        self.pixmap_dice3 = None
        self.lbl_dice4 = None
        self.pixmap_dice4 = None

        self.first_dice = 0
        self.second_dice = 0
        self.red_chips = None
        self.white_chips = None
        self.is_same = False
        self.cells = None
        self.helper = None
        self.but_size = None

        self.can_move_but1 = None
        self.can_move_but2 = None

        self.throwing_r = False
        self.throwing_w = False

        self.fl_w = False
        self.fl_r = False

        self.can_throw_but1 = None
        self.can_throw_but2 = None

        self.player_color_now = ''
        self.moving_player = None
        self.num_of_last_pushed_but = ''
        self.butplay = None
        self.was = False

        self.success = False
        self.setupUI()

    def setupUI(self):
        set_args(self, 1700, 873)

        # игровое поле
        self.bg_lbl = QLabel(self)
        self.bg_pixmap = QPixmap("Game_desk.png")
        self.bg_lbl.setPixmap(self.bg_pixmap)
        self.bg_lbl.move(0, 0)

        self.moving_player = QLabel(self)
        self.moving_player.setStyleSheet("font-size: 20px;")
        self.moving_player.setGeometry(1445, 600, 260, 30)

        if game_sys_lang == 'Рус':
            # текст, уведомляющий игрока(-ов) о том, чтобы бросить кубики
            self.moving_player.setText('Бросьте кубики')

            # кнопка броска кубиков
            self.button_throw_dice = QtWidgets.QPushButton("Кинуть кубики", self)

            # кнопка выхода из игры в главное меню
            self.button_back = QtWidgets.QPushButton("Выход", self)

        else:
            # текст, уведомляющий игрока(-ов) о том, чтобы бросить кубики
            self.moving_player.setText('Throw the dice')

            # кнопка броска кубиков
            self.button_throw_dice = QtWidgets.QPushButton("Throw the dice", self)

            # кнопка выхода из игры в главное меню
            self.button_back = QtWidgets.QPushButton("Leave", self)

        # настройка кнопки выхода в меню из игры

        self.button_back.setGeometry(QtCore.QRect(1441, 800, 258, 73))
        self.button_back.setStyleSheet("font-size: 24px;")
        self.button_back.clicked.connect(self.back)

        # настройка кнопки бросания кубиков

        self.button_throw_dice.setGeometry(QtCore.QRect(1441, 727, 258, 73))
        self.button_throw_dice.setStyleSheet("font-size: 24px;")

        self.button_throw_dice.clicked.connect(self.throwed)

        self.but_size = QPixmap('red_chip.png').size()
        self.cells = []
        self.helper = [[], []]

        # начальная генерация фишек
        for i in range(1, 16):
            # создание и отображение красных фишек
            chip1 = self.create_chip('r', i)
            chip1.move(195, 787 - (52 * i) + 52)

            # создание и отображение белых фишек
            chip2 = self.create_chip('w', i)
            chip2.move(1200, (52 * i) - 17)

            chip1.clicked.connect(lambda checked, chip=chip1: self.travel(chip))
            chip2.clicked.connect(lambda checked, chip=chip2: self.travel(chip))

            self.helper[0].insert(0, chip1)
            self.helper[1].insert(0, chip2)

        # внутренняя реализация игрового поля вида:
        # <красные фишки> <треугольник> <треугольник> ... <треугольник> <белые фишки>
        # (20 треугольников, в каждом из которых по 1 кнопке, на которую можно будет нажимать для ходов, 1 треугольник под белые фишки, 1 треугольник под красные фишки)

        self.cells.append(self.helper[0])
        self.cells = self.cells + [[], [], [], [], [], [], [], [], [], [], []]
        self.cells.append(self.helper[1])
        self.cells = self.cells + [[], [], [], [], [], [], [], [], [], [], []]

        # отчистка вспомогательного списка
        self.helper.clear()

        self.butplay = QtWidgets.QPushButton('PLAY GAME' if game_sys_lang == 'Eng' else 'Начать игру', self)
        self.butplay.setStyleSheet("font-size: 35px;")
        self.butplay.setGeometry(QtCore.QRect(1441, 654, 258, 73))
        self.butplay.clicked.connect(self.play)

    def play(self):
        self.butplay.hide()
        global game_mod
        if game_mod == '1vs1':
            self.play_1vs1()
        else:
            self.play_vs_bot()

    # игра 1 на 1
    def play_1vs1(self):
        self.player_color_now = 'reddd' if randint(1, 2) == 1 else 'white'

        if game_sys_lang == 'Рус':
            self.moving_player.setText(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'}, бросьте кубики!")
        else:
            self.moving_player.setText(f"{'Red' if self.player_color_now == 'reddd' else 'White'}, throw dices!")

        while True:
            # Проверяем, не закончилась ли игра
            if self.is_game_end(self.player_color_now):
                global wnd_win
                wnd_win = GameEnd(self.player_color_now)
                wnd_win.show()

            # self.button_throw_dice.setEnabled(True)

            # Ожидание броска кубиков
            QtWidgets.QApplication.processEvents()  # Позволяем интерфейсу обновляться
            while self.button_throw_dice.isEnabled():
                QtWidgets.QApplication.processEvents()

            # После броска кубиков начинаем ход
            self.button_throw_dice.setEnabled(False)
            if game_sys_lang == 'Рус':
                self.moving_player.setText(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'}, ходите!")
            else:
                self.moving_player.setText(f"{'Red' if self.player_color_now == 'reddd' else 'White'}, make move!")

            # Проверяем, есть ли доступные ходы
            available_moves = self.check_available_moves()
            if not available_moves:
                print(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'} не могут сделать ход.")
                self.change_player()
                self.first_dice = self.second_dice = -1000
                self.button_throw_dice.setEnabled(True)
                continue

    def check_available_moves(self):
        if self.first_dice == -1000 and self.second_dice == -1000:
            print('Dices are empty')
            return False

        for i, cell in enumerate(self.cells):
            if len(cell) == 0:
                continue

            if self.player_color_now not in cell[0].objectName():
                continue

            pos = self.on_desk(cell[0])

            # Проверка на возможность выбрасывания фишек
            if (self.player_color_now in cell[0].objectName() and
                    (self.fl_r and self.player_color_now == 'reddd') or
                    (self.fl_w and self.player_color_now == 'white')):
                pos = 6 - (pos % 6)
                if self.first_dice == pos:
                    return True
                elif self.first_dice < pos:
                    continue
                else:
                    if self.nothing_before(pos, cell[0]):
                        return True

            # Проверка на возможность обычного хода
            if self.first_dice != -1000:
                target_pos = (pos + self.first_dice) % 24
                if len(self.cells[target_pos]) == 0 or self.player_color_now in self.cells[target_pos][0].objectName():
                    return True

            if self.second_dice != -1000:
                target_pos = (pos + self.second_dice) % 24
                if len(self.cells[target_pos]) == 0 or self.player_color_now in self.cells[target_pos][0].objectName():
                    return True

        return False

    # меняем цвета ходящего игрока
    def change_player(self):
        self.player_color_now = 'white' if 'reddd' == self.player_color_now else 'reddd'
        print(f'Color has changed to {self.player_color_now}')

        # Уведомляем текущего игрока о необходимости бросить кубики
        self.moving_player.setText(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'}, бросьте кубики!")

    # Игра против бота
    def play_vs_bot(self):
        while True:
            # Проверяем, не закончилась ли игра
            if self.is_game_end(self.player_color_now):
                global wnd_win
                wnd_win = GameEnd(self.player_color_now)
                wnd_win.show()
                break

            # Ожидание броска кубиков
            QtWidgets.QApplication.processEvents()
            while self.button_throw_dice.isEnabled():
                QtWidgets.QApplication.processEvents()

            # После броска кубиков начинаем ход
            self.button_throw_dice.setEnabled(False)
            if game_sys_lang == 'Рус':
                self.moving_player.setText(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'}, ходите!")
            else:
                self.moving_player.setText(f"{'Red' if self.player_color_now == 'reddd' else 'White'}, make move!")

            # Если ходит бот
            if self.player_color_now == 'white':
                move = choose_move_with_nn(self.cells, self.player_color_now, self.first_dice, self.second_dice)
                if move is None:
                    print("Bot cannot make a move. Skipping turn.")
                    self.change_player()
                    self.first_dice = self.second_dice = -1000
                    self.button_throw_dice.setEnabled(True)
                    continue

                self.make_move(move)
            else:
                # Ожидание хода игрока
                QtWidgets.QApplication.processEvents()
                while self.button_throw_dice.isEnabled():
                    QtWidgets.QApplication.processEvents()

            # Проверяем, есть ли доступные ходы
            available_moves = self.check_available_moves()
            if not available_moves:
                print(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'} не могут сделать ход.")
                self.change_player()
                self.first_dice = self.second_dice = -1000
                self.button_throw_dice.setEnabled(True)
                continue

        def make_move(self, move):
            if move is None:
                print("Invalid move. Skipping.")
                return

            current_position, dice_value = move

            # Проверяем, что текущая позиция и кубик допустимы
            if current_position < 0 or current_position >= 24:
                print(f"Invalid current position: {current_position}")
                return

            if dice_value not in [self.first_dice, self.second_dice]:
                print(f"Invalid dice value: {dice_value}")
                return

            # Вычисляем целевую позицию
            target_position = (current_position + dice_value) % 24

            # Проверяем, можно ли сделать ход на целевую позицию
            target_cell = self.cells[target_position]
            if len(target_cell) > 1 and self.player_color_now not in target_cell[0].objectName():
                print("Cannot move to this position: enemy has more than one chip.")
                return

            # Перемещаем фишку
            self.make_move(move)
            print(f"Moved chip from position {current_position} to position {target_position} using dice {dice_value}")

    # проверка на то, выиграл ли игрок с цветом <color>
    def is_game_end(self, color):
        for i in self.cells:
            if len(i) == 0:
                continue
            if color in i[0].objectName():
                return False
        return True

    # функция выхода в меню
    def back(self):
        self.wnd_of_exit = Exit('game')
        self.wnd_of_exit.show()

    # функция броска кубиков
    def throwed(self):
        global dice_value
        self.button_throw_dice.setEnabled(False)
        if not self.lbl_dice1 is None:
            self.lbl_dice1.clear()
        if not self.lbl_dice2 is None:
            self.lbl_dice2.clear()
        if not self.lbl_dice3 is None:
            self.lbl_dice3.clear()
        if not self.lbl_dice4 is None:
            self.lbl_dice4.clear()
        global dice_color

        # бросок кубиков + защита от спама кнопки

        self.first_dice = randint(1, 6)
        self.second_dice = randint(1, 6)
        print(self.first_dice, self.second_dice)

        # отображение кубиков на панели справа

        self.lbl_dice1 = QLabel(self)
        self.lbl_dice2 = QLabel(self)

        # настройка первого кубика

        self.pixmap_dice1 = QPixmap(dices_colors[dice_color if dice_color != 'both' else 'white'][self.first_dice])

        # настройка второго кубика

        self.pixmap_dice2 = QPixmap(dices_colors[dice_color if dice_color != 'both' else 'black'][self.second_dice])

        if self.first_dice == self.second_dice:
            self.lbl_dice3 = QLabel(self)
            self.lbl_dice4 = QLabel(self)

            self.pixmap_dice3 = QPixmap(dices_colors[dice_color if dice_color != 'both' else 'white'][self.first_dice])
            self.pixmap_dice3 = self.pixmap_dice3.scaled(110, 110, QtCore.Qt.KeepAspectRatio)
            self.lbl_dice3.setPixmap(self.pixmap_dice3)
            self.lbl_dice3.move(1450, 155)

            self.pixmap_dice4 = QPixmap(dices_colors[dice_color if dice_color != 'both' else 'black'][self.second_dice])
            self.pixmap_dice4 = self.pixmap_dice4.scaled(110, 110, QtCore.Qt.KeepAspectRatio)
            self.lbl_dice4.setPixmap(self.pixmap_dice4)
            self.lbl_dice4.move(1580, 155)

            # доп настройка ПЕРВОГО кубика, если выпало одинковое число

            self.pixmap_dice1 = self.pixmap_dice1.scaled(110, 110, QtCore.Qt.KeepAspectRatio)
            self.lbl_dice1.setPixmap(self.pixmap_dice1)
            self.lbl_dice1.move(1450, 20)

            # доп настройка ВТОРОГО кубика, если выпало одинковое число

            self.pixmap_dice2 = self.pixmap_dice2.scaled(110, 110, QtCore.Qt.KeepAspectRatio)
            self.lbl_dice2.setPixmap(self.pixmap_dice2)
            self.lbl_dice2.move(1580, 20)

            self.lbl_dice3.show()
            self.lbl_dice4.show()

        else:
            self.lbl_dice1.setPixmap(self.pixmap_dice1)
            self.lbl_dice2.setPixmap(self.pixmap_dice2)
            self.lbl_dice1.move(1470, 5)
            self.lbl_dice2.move(1470, 230)

        self.lbl_dice1.show()
        self.lbl_dice2.show()

    # функция создания фишки
    def create_chip(self, c, num):
        but = QtWidgets.QPushButton(self)
        if c != 'none':
            pix = QPixmap('red_chip.png' if c == 'r' else ('white_chip.png' if c == 'w' else 'green_chip.png'))
            but.setIcon(QIcon(pix))
            but.setIconSize(self.but_size)
        but.setFixedSize(self.but_size)
        but.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }" if c != "none" else "QPushButton { background-color: red; }")
        but.setObjectName(f'chip_{"white" if c == "w" else ("reddd" if c == "r" else "field")}_{str(num)}')
        return but

    # вспомогательная объединяющая функция для движения
    def travel(self, but1):
        # Проверка, что фишка принадлежит текущему игроку
        player_color = 'reddd' if 'reddd' in but1.objectName() else 'white'
        if player_color != self.player_color_now:
            print("Нельзя ходить вражеской фишкой!")
            return

        # Проверка на последнюю нажатую кнопку
        if (self.num_of_last_pushed_but and self.num_of_last_pushed_but[-2:] == but1.objectName()[-2:] and
            self.num_of_last_pushed_but[:5] in but1.objectName()) or self.first_dice == 0:
            print('\n')
            return
        print('This button is another than before')

        pos1 = self.on_desk(but1)

        # Удаление предыдущих подсказок, если они есть
        if self.num_of_last_pushed_but:
            self.clearer()
        print('Helps are cleared')

        cnt = 0
        for i in range(6, 12) if 'white' in but1.objectName() else range(18, 24):
            cnt += len(self.cells[i])

        if self.first_dice != -1000:
            # Создание подсказки для первого кубика
            self.can_move_but1 = self.create_chip('g', -1)
            self.move_chip(but1, pos1, self.first_dice, self.can_move_but1)

            # Создание подсказки для выбрасывания от первого кубика
            self.can_throw_but1 = self.create_chip('g', -2)
            self.move_chip(but1, pos1, self.first_dice, self.can_throw_but1)

        if self.second_dice != -1000:
            # Создание подсказки для второго кубика
            self.can_move_but2 = self.create_chip('g', -1)
            self.move_chip(but1, pos1, self.second_dice, self.can_move_but2)

            # Создание подсказки для выбрасывания от второго кубика
            self.can_throw_but2 = self.create_chip('g', -2)
            self.move_chip(but1, pos1, self.second_dice, self.can_throw_but2)

    # двигаем фишку-подсказку
    def move_chip(self, but1, pos1, dice, move_button):
        # если кубик выброшен до этого
        if dice == -1000:
            return
        target_pos = pos1 + dice
        # Проверка выхода за пределы игрового поля, при недостижении состояния выбрасывания
        if '-1' in move_button.objectName():
            if (('white' in but1.objectName() and target_pos % 24 > 11 and -1 < pos1 < 12) or
                    ('reddd' in but1.objectName() and target_pos > 23)):
                print('The chip is out of range before move and can\'t throw\n')
                return

            self.num_of_last_pushed_but = but1.objectName()[5:10] + but1.objectName()[-2:]
            print('The chip is NOT out of range after move')

            player_color, enemy_color = ('reddd', 'white') if 'reddd' in but1.objectName() else ('white', 'reddd')

            if self.cells[target_pos % 24]:
                if player_color in self.cells[target_pos % 24][0].objectName():
                    direction = -52 if target_pos % 24 < 12 else 52
                    move_button.move(self.cells[target_pos % 24][0].x(), self.cells[target_pos % 24][0].y() + direction)
                    print("Enemy's chip NOT in the position")
                else:
                    print("Enemy's chip in the position\n")
                    return  # вражеская фишка на позиции
            else:
                x, y = triangles[target_pos % 24][0], triangles[target_pos % 24][1]
                move_button.move(x, y)
                print('The position is empty')

            move_button.show()
            move_button.clicked.connect(lambda: self.mover(pos1, dice, move_button))
            print('HELP WAS CREATED')

        elif self.can_throw_but1 is not None:
            cnt = sum(len(self.cells[i]) for i in (range(6, 12) if 'white' in but1.objectName() else range(18, 24)))
            print(cnt)

            if not self.fl_r and 'reddd' in but1.objectName() and target_pos > 23 and cnt == 15:
                self.fl_r = True

            if not self.fl_w and 'white' in but1.objectName() and target_pos > 11 and cnt == 15:
                self.fl_w = True

            if (self.fl_r and 'reddd' in but1.objectName()) or (self.fl_w and 'white' in but1.objectName()):
                self.helper.clear()
                print('Start throwing')
                self.num_of_last_pushed_but = but1.objectName()[5:10] + but1.objectName()[-2:]

                pos = 6 - (pos1 % 6)
                if dice == pos:
                    print('==')
                    self.throw(but1, pos1, move_button)
                    print(move_button.x(), move_button.y())
                elif dice < pos:
                    print('<')
                    return
                else:
                    print('>')
                    if self.nothing_before(pos1, but1):
                        self.throw(but1, pos1, move_button)
                        print(move_button.x(), move_button.y())
                    else:
                        return
        else:
            return

    # смотрим нет ли фишек перед текущей(длф выбрасывания с дома)
    def nothing_before(self, pos, but1):
        if 'reddd' in but1.objectName():
            a = self.cells[18:24]
        else:
            a = self.cells[6:12]
        for i in range(0, pos % 6):
            if len(a[i]) > 0 and ('reddd' if 'reddd' in but1.objectName() else 'white') in a[i][
                0].objectName():  # если есть фишка слева от позиции выбранной И ЭТА ФИШКА НЕ ВРАЖЕСКАЯ
                return False
        return True

    # двигаем игровую фишку
    def mover(self, pos, dice, to_pos):
        print(self.first_dice, self.second_dice, self.first_dice + pos, self.second_dice + pos)
        target_pos = pos + dice
        m = self.cells[pos][0]
        del self.cells[pos][0]
        self.cells[target_pos % 24] = [m] + self.cells[target_pos % 24]
        x, y = to_pos.x(), to_pos.y()
        self.cells[target_pos % 24][0].move(x, y)
        print('The chip moved to position')
        self.clearer()
        print('Helps are cleared')
        print('\n')
        # удаляем поочерёдно кубики, которыми ходим
        # если выпали одинаковые кубики
        if self.first_dice == self.second_dice and self.lbl_dice3 is not None:
            if self.lbl_dice4 is not None:
                self.lbl_dice4.clear()
                self.lbl_dice4 = None
            elif self.lbl_dice3 is not None:
                self.lbl_dice3.clear()
                self.lbl_dice3 = None
        else:  # если кубики разные, или перестало выполняться условие для одинаковых кубиков
            if dice == self.second_dice:
                if self.lbl_dice2 is not None:
                    self.lbl_dice2.clear()
                    self.second_dice = -1000
                    self.lbl_dice2 = None
            elif self.lbl_dice1 is not None:
                self.lbl_dice1.clear()
                self.first_dice = -1000
                self.lbl_dice1 = None

    # номер лунки, в которой находится текущая фишка
    def on_desk(self, but):
        for i, cell in enumerate(self.cells):
            if but in cell:
                return i
        return -1

    # очистка игрового поля от подсказок
    def clearer(self):
        # Проверка и удаление каждой подсказки
        if hasattr(self, 'can_move_but1') and self.can_move_but1 is not None:
            self.can_move_but1.hide()
        if hasattr(self, 'can_move_but2') and self.can_move_but2 is not None:
            self.can_move_but2.hide()
        if hasattr(self, 'can_throw_but1') and self.can_throw_but1 is not None:
            self.can_throw_but1.hide()
        if hasattr(self, 'can_throw_but2') and self.can_throw_but2 is not None:
            self.can_throw_but2.hide()
        self.num_of_last_pushed_but = ''

    # создание подсказки для выбрасывания фишки
    def throw(self, chip, pos, helping):
        if 'reddd' in chip.objectName():
            helping.move(100, 35)
        else:
            helping.move(1300, 787)
        helping.show()
        helping.clicked.connect(lambda: self.yes_throw(pos))

    # само выбрасывание
    def yes_throw(self, pos):
        print('CHIP IS THROWED')
        self.cells[pos][0].deleteLater()
        del self.cells[pos][0]
        self.clearer()

    def make_move(self, move):
        if move is None:
            print("Invalid move. Skipping.")
            return
        self.mover(move[0], move[1], self.cells[move[0]][0])
        print("Chip moved")


# окно выбора цвета кубиков

class ChooseDiceColor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lbl = None
        self.white = None
        self.black = None
        self.both = None
        self.ok = None
        self.back_menu = None
        self.setupUI()

    def setupUI(self):
        self.setObjectName("choosing_dice_color")
        set_args(self, 315, 250)
        self.lbl = QLabel(self)

        if game_sys_lang == 'Eng':

            # надпись выбрать цвет кубиков
            self.lbl.setText("<b>Choose dice color</b>")
            self.lbl.move(70, 5)

            # кнопка выбрать белые кубики
            self.white = QtWidgets.QRadioButton("White", self)

            # кнопка выбрать чёрные кубики
            self.black = QtWidgets.QRadioButton("Black", self)

            # кнопка выбрать оба цвета для кубиков(1 белый, 1 черный)
            self.both = QtWidgets.QRadioButton("1 Black and 1 White", self)

            # кнопка возврата в меню
            self.back_menu = QtWidgets.QPushButton("Back to menu", self)

        else:

            # надпись выбрать цвет кубиков
            self.lbl.setText("<b>Выберите цвет кубиков</b>")
            self.lbl.move(40, 5)

            # кнопка выбрать белые кубики
            self.white = QtWidgets.QRadioButton("Белые", self)

            # кнопка выбрать чёрные кубики
            self.black = QtWidgets.QRadioButton("Чёрные", self)

            # кнопка выбрать оба цвета для кубиков(1 белый, 1 черный)
            self.both = QtWidgets.QRadioButton("1 Белый и 1 Чёрный", self)

            # кнопка возврата в меню
            self.back_menu = QtWidgets.QPushButton("Вернуться в меню", self)

        self.lbl.setStyleSheet("font-size: 18px;")

        # настройка кнопки выбора белого цвета
        self.white.setStyleSheet("font-size: 18px;")
        self.white.setGeometry(QtCore.QRect(15, 45, 120, 45))
        self.white.clicked.connect(chose_color_white)

        # настройка кнопки выбора чёрного цвета
        self.black.setStyleSheet("font-size: 18px;")
        self.black.setGeometry(QtCore.QRect(15, 90, 120, 45))
        self.black.clicked.connect(chose_color_black)

        # настройка кнопки выбора обоих цветов
        self.both.setStyleSheet("font-size: 18px;")
        self.both.setGeometry(QtCore.QRect(15, 135, 280, 45))
        self.both.clicked.connect(chose_color_both)

        # настройка кнопки возврата в меню
        self.back_menu.setStyleSheet("font-size: 18px;")
        self.back_menu.setGeometry(QtCore.QRect(130, 190, 160, 45))
        self.back_menu.clicked.connect(self.back_to_main_menu)

        # настройка кнопки ОК
        self.ok = QtWidgets.QPushButton("ОК", self)
        self.ok.setStyleSheet("font-size: 18px;")
        self.ok.setGeometry(QtCore.QRect(15, 190, 100, 45))
        self.ok.clicked.connect(self.oked)

    # функция возврата в меню
    def back_to_main_menu(self):
        global wnd_menu
        wnd_menu.show()
        self.close()

    # функция продолжения игры
    def oked(self):
        global dice_color, wnd_of_playing
        if dice_color != '':
            wnd_of_playing = Game()
            wnd_of_playing.show()
            self.close()
        else:
            error_of_dice_color(self)


# окно выбора режима

class ChooseGameMode(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lbl = None
        self.game_mod_1vs1 = None
        self.game_mod_versus_bot = None
        self.play = None
        self.game_mod = None
        self.ret = None
        self.setupUI()

    def setupUI(self):
        self.setObjectName("choosing_game_mod")
        set_args(self, 290, 150)
        self.lbl = QLabel(self)

        if game_sys_lang == 'Eng':

            # надпись выбрать режим игры
            self.lbl.setText("<b>Choose your enemy</b>")
            self.lbl.move(60, 5)

            # кнопка Играть 1 на 1
            self.game_mod_1vs1 = QtWidgets.QRadioButton("Person", self)

            # кнопка Играть с ботом
            self.game_mod_versus_bot = QtWidgets.QRadioButton("Computer", self)

            # кнопка Играть
            self.play = QtWidgets.QPushButton("Play", self)

            # кнопка возврата в меню
            self.ret = QtWidgets.QPushButton("Back", self)

        else:

            # надпись выбрать режим игры
            self.lbl.setText("<b>Выберите вашего соперника</b>")
            self.lbl.move(8, 5)

            # кнопка Играть 1 на 1
            self.game_mod_1vs1 = QtWidgets.QRadioButton("Человек", self)

            # кнопка Играть с ботом
            self.game_mod_versus_bot = QtWidgets.QRadioButton("Компьютер", self)

            # кнопка Играть
            self.play = QtWidgets.QPushButton("Играть", self)

            # кнопка возврата в меню
            self.ret = QtWidgets.QPushButton("Назад", self)

        self.lbl.setStyleSheet("font-size: 18px;")

        self.game_mod_1vs1.setStyleSheet("font-size: 18px;")
        self.game_mod_1vs1.setGeometry(QtCore.QRect(30, 40, 100, 45))
        self.game_mod_1vs1.setObjectName("game_mod_1vs1")
        self.game_mod_1vs1.clicked.connect(one_vs_one)

        self.game_mod_versus_bot.setStyleSheet("font-size: 18px;")
        self.game_mod_versus_bot.setGeometry(QtCore.QRect(150, 40, 130, 45))
        self.game_mod_versus_bot.setObjectName("game_mod_you_vs_bot")
        self.game_mod_versus_bot.clicked.connect(vsBot)

        self.play.setStyleSheet("font-size: 18px;")
        self.play.setGeometry(QtCore.QRect(25, 90, 100, 45))
        self.play.setObjectName("game_mod_you_vs_bot")
        self.play.clicked.connect(self.playing)

        self.ret.setStyleSheet("font-size: 18px;")
        self.ret.setGeometry(QtCore.QRect(155, 90, 100, 45))
        self.ret.setObjectName("return to main menu")

        self.ret.clicked.connect(self.back)

    # функция закрытия окна и открытия меню

    def back(self):
        self.close()
        wnd_menu.show()

    # функция проверки на выбранность режима игры

    def playing(self):
        if not game_mod is None:
            global wnd_of_choosing_dice_color
            wnd_of_choosing_dice_color = ChooseDiceColor()
            wnd_of_choosing_dice_color.show()
            self.close()
        else:
            error_of_game_mod(self)


# окно выхода из игры

class Exit(QtWidgets.QWidget):
    def __init__(self, par):
        super().__init__()
        self.lbl = None
        self.setupUi()
        self.yes = None
        self.no = None
        self.par = par

    def setupUi(self):
        self.setObjectName("exiting_window")
        set_args(self, 250, 100)
        self.lbl = QLabel(self)

        if game_sys_lang == "Рус":
            # надпись "Вы точно хотите выйти?"
            self.lbl.setText('<b>Вы точно хотите выйти?</b>')
            self.lbl.move(40, 5)

            # кнопка "Да :("
            self.yes = QtWidgets.QPushButton("Да", self)

            # кнопка "Нет :)"
            self.no = QtWidgets.QPushButton("Нет", self)

        else:

            # надпись "Вы точно хотите выйти?"
            self.lbl.setText("<b>Are you sure you want to leave?</b>")
            self.lbl.move(15, 5)

            # кнопка "Да :("
            self.yes = QtWidgets.QPushButton("Yes", self)

            # кнопка "Нет :)"
            self.no = QtWidgets.QPushButton("No", self)

        self.lbl.setStyleSheet("font-size: 14px;")

        self.yes.setGeometry(QtCore.QRect(30, 40, 75, 45))
        self.yes.setStyleSheet("font-size: 18px;")
        self.yes.setObjectName("yes_exit_button")
        self.yes.clicked.connect(self.exite)

        self.no.setGeometry(QtCore.QRect(146, 40, 75, 45))
        self.no.setStyleSheet("font-size: 18px;")
        self.no.setObjectName("no_exit_button")
        self.no.clicked.connect(self.back)

    # функция закрытия окна и возвращения в предцдущее окно, из которого хотели выйти

    def back(self):
        if self.par == 'menu':
            wnd_menu.show()
        self.close()

    # функция выхода из программы

    def exite(self):
        global wnd_of_playing
        if self.par == 'menu':
            sys.exit()
        elif self.par == 'game':
            global game_mod
            self.close()
            wnd_of_playing.close()
            game_mod = None
            wnd_menu.show()


# правила Длинных нард

class Rules(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.verticalLayout = None
        self.verticalLayout_2 = None
        self.scrollAreaWidgetContents = None
        self.scrollArea = None
        self.lbl = None
        self.list_widget = None
        self.but_back = None
        self.setupUI()

    def setupUI(self):
        global text_rules
        set_args(self, 800, 600)

        # язык кнопки + язык правил игры

        if game_sys_lang == 'Рус':
            file = codecs.open('RULES_ru.txt', 'r', 'utf_8')
            text_rules = file.read()
            file.close()
            self.but_back = QtWidgets.QPushButton('Назад', self)
        else:
            file = codecs.open('RULES_eng.txt', 'r', 'utf_8')
            text_rules = file.read()
            file.close()
            self.but_back = QtWidgets.QPushButton('Back', self)

        # виджет с правилами

        self.lbl = QLabel(self)
        self.lbl.setText(text_rules)
        self.lbl.setStyleSheet("font-size: 16px;")

        # кнопка возврата в главное меню

        self.but_back.setGeometry(QtCore.QRect(5, 505, 790, 40))
        self.but_back.setStyleSheet(
            """
            "background-color: rgb(240, 240, 255)"
            """
        )
        self.but_back.clicked.connect(self.back)

        # скроллбар + скролл колесом мыши

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setStyleSheet(
            """
            QScrollBar{ background-color: rgb(240, 240, 255) } 
            """
        )
        scroll_area.setObjectName("scrollArea")
        scroll_area.setGeometry(QtCore.QRect(0, 0, 800, 400))
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        content_widget = QtWidgets.QWidget()
        scroll_area.setWidget(content_widget)

        lay = QVBoxLayout(content_widget)
        lay.addWidget(self.lbl)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        layout.addWidget(self.but_back)

    # функция возврата в главное меню

    def back(self):
        self.close()
        wnd_menu.show()


# менюшка


class Menu(QtWidgets.QWidget):
    def __init__(self):
        global game_sys_lang
        super().__init__()
        self.wnd_of_exit = None
        self.change_lang = None
        self.wnd_of_rules = None
        self.exit_button = None
        self.rules_button = None
        self.wnd_choose_game_mode = None
        self.playing_button = None
        self.lbl1 = None
        self.lbl2 = None

        self.setupUi()

    def setupUi(self):
        set_args(self, 500, 550)
        self.setObjectName("menu")
        self.lbl1 = QLabel(self)
        self.lbl2 = QLabel(self)

        if game_sys_lang == 'Eng':

            # надпись названия игры
            self.lbl1.setText('<b>Long backgammon</b>')

            # надпись автор
            self.lbl2.setText('<b>Author: Makarov Artem(dram00nn_nn)</b>')

            # кнопка смены языка(изначальный язык игры - английский)
            self.change_lang = QtWidgets.QPushButton('Eng', self)

            # кнопка exit
            self.exit_button = QtWidgets.QPushButton("Exit", self)

            # кнопка правила игры
            self.rules_button = QtWidgets.QPushButton("Rules", self)

            # кнопка играть
            self.playing_button = QtWidgets.QPushButton("Play", self)

        else:

            # надпись названия игры
            self.lbl1.setText('<b>Длинные нарды</b>')

            # надпись автор
            self.lbl2.setText('<b>Автор: Макаров Артём(dram00nn_nn)</b>')

            # кнопка смены языка(изначальный язык игры - английский)
            self.change_lang = QtWidgets.QPushButton('Рус', self)

            # кнопка exit
            self.exit_button = QtWidgets.QPushButton("Выход", self)

            # кнопка правила игры
            self.rules_button = QtWidgets.QPushButton("Правила", self)

            # кнопка играть
            self.playing_button = QtWidgets.QPushButton("Играть", self)

        self.lbl1.setGeometry(75, 5, 500, 90)
        self.lbl1.setStyleSheet("font-size: 40px;")

        self.lbl2.setGeometry(120, 520, 400, 25)

        self.change_lang.setGeometry(QtCore.QRect(100, 470, 300, 50))
        self.change_lang.setObjectName("change_language")
        self.change_lang.setStyleSheet("font-size: 20px;")
        self.change_lang.clicked.connect(self.lang)

        self.exit_button.setGeometry(QtCore.QRect(100, 350, 300, 100))
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setStyleSheet("font-size: 20px;")
        self.exit_button.clicked.connect(self.exiting)

        self.rules_button.setGeometry(QtCore.QRect(100, 225, 300, 100))
        self.rules_button.setObjectName("rules_button")
        self.rules_button.setStyleSheet("font-size: 20px;")
        self.rules_button.clicked.connect(open_rules)

        self.playing_button.setGeometry(QtCore.QRect(100, 100, 300, 100))
        self.playing_button.setObjectName("playing_button")
        self.playing_button.setStyleSheet("font-size: 20px;")
        self.playing_button.clicked.connect(self.play_game)

    # отображение окошка exit

    def exiting(self):
        self.wnd_of_exit = Exit('menu')
        wnd_menu.hide()
        self.wnd_of_exit.show()

    # измение языка игры

    def lang(self):
        if game_sys_lang == 'Eng':
            switch_lang("Рус")
        else:
            switch_lang("Eng")

        updater(self)

    # начало игры

    def play_game(self):
        wnd_menu.hide()
        self.wnd_choose_game_mode = ChooseGameMode()
        self.wnd_choose_game_mode.show()


# Загрузка модели при запуске
load_model()

if __name__ == '__main__':
    game_sys_lang = 'Eng'
    app = QtWidgets.QApplication(sys.argv)
    wnd_menu = Menu()
    wnd_menu.show()
    sys.exit(app.exec())
