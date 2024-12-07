import codecs
import sys
import this
from random import randint

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QDesktopWidget, QLabel, QRadioButton

my_sys_lang = 'Eng'
game_mod = None
wnd_menu = None
wnd_error = None
wnd_of_rules = None
text_rules = None
wnd_of_playing = None
wnd_of_choosing_dice_color = None
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
    1: [195, 787],
    2: [285, 787],
    3: [372, 787],
    4: [460, 787],
    5: [547, 787],
    6: [635, 787],
    7: [765, 787],
    8: [855, 787],
    9: [940, 787],
    10: [1028, 787],
    11: [1115, 787],
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
    22: [280, 35]
}


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
    global my_sys_lang
    my_sys_lang = language


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
    if my_sys_lang == 'Eng':
        wnd_error = Error('<b>Wrong game mod</b>')
    else:
        wnd_error = Error('<b>Ошибка игрового режима</b>')
    self1.hide()
    wnd_error.show()


# функция отображения окна ошибка в связи с невыбранностью цвета кубиков
def error_of_dice_color(self1):
    global wnd_error
    if my_sys_lang == 'Eng':
        wnd_error = Error('<b>Wrong dice color</b>')
    else:
        wnd_error = Error('<b>Ошибка цвета кубиков</b>')
    self1.hide()
    wnd_error.show()


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

        if my_sys_lang == 'Eng':
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


# v = [[chip1, chip3, chip6], [], ]
# n = []

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
        self.txt_lbl = None
        self.red_chips = None
        self.white_chips = None
        self.is_same = False
        self.cells = None
        self.helper = None
        self.but_size = None

        self.can_move_but = None
        self.setupUI()

    def setupUI(self):
        set_args(self, 1700, 873)
        # игровое поле

        self.bg_lbl = QLabel(self)
        self.bg_pixmap = QPixmap("Game_desk.png")
        self.bg_lbl.setPixmap(self.bg_pixmap)
        self.bg_lbl.move(0, 0)

        if my_sys_lang == 'Рус':
            # кнопка броска кубиков
            self.button_throw_dice = QtWidgets.QPushButton("Кинуть кубики", self)

            # кнопка выхода из игры в главное меню
            self.button_back = QtWidgets.QPushButton("Выход", self)

        else:
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

        # пробное создание красных фишек

        for i in range(1, 16):
            # создание и отображение красных фишек
            chip1 = self.create_chip('r', i)
            chip1.move(195, 787 - (52 * i) + 52)
            chip1.clicked.connect(lambda: self.travel(chip1))

            # создание и отображение белых фишек
            chip2 = self.create_chip('w', i)
            chip2.move(1200, (52 * i) - 17)
            chip2.clicked.connect(lambda: self.travel(chip2))

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

    # функция выхода в меню

    def back(self):
        self.wnd_of_exit = Exit('game')
        self.wnd_of_exit.show()

    # функция броска кубиков

    def throwed(self):
        if not self.lbl_dice1 is None:
            self.lbl_dice1.clear()
        if not self.lbl_dice2 is None:
            self.lbl_dice2.clear()
        if not self.lbl_dice3 is None:
            self.lbl_dice3.clear()
        if not self.lbl_dice4 is None:
            self.lbl_dice4.clear()
        if not self.txt_lbl is None:
            self.txt_lbl.clear()

        # бросок кубиков + защита от спама кнопки

        self.first_dice = randint(1, 6)
        self.second_dice = randint(1, 6)
        # self.button_throw_dice.setEnabled(False)
        print(self.first_dice, self.second_dice)

        # отображение кубиков на панели справа

        global dice_color
        self.lbl_dice1 = QLabel(self)
        self.lbl_dice2 = QLabel(self)
        self.txt_lbl = QLabel(self)

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
        # настройка и отображение суммы значений выпавших кубиков
        if my_sys_lang == 'Eng':
            self.txt_lbl.setText(f'Sum = {self.first_dice + self.second_dice}')
        else:
            self.txt_lbl.setText(f'Сумма = {self.first_dice + self.second_dice}')
        self.txt_lbl.move(1445, 455)
        self.txt_lbl.setStyleSheet("font-size: 20px;")
        self.txt_lbl.show()

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

    def travel(self, but):
        print(self.cells)
        if self.first_dice == 0:
            return
        print(1)
        for i in self.cells:
            if len(i) > 0:
                print(i[0].objectName()[-2:], end=' ')
                if i[0].objectName()[-2:] == '-1':
                    self.can_move_but.deleteLater()
                    self.cells[self.cells.index(i)] = self.cells[self.cells.index(i)][1:]

            else:
                print(0, end=' ')
        print(2)
        pos1 = self.on_desk(but) + 1
        print(pos1, pos1 + self.first_dice)
        self.can_move_but = self.create_chip('g', -1)
        global triangles
        # разбиение на 2 случая, в зависимости от цвета фишки
        if but.objectName()[5:10] == 'reddd':
            # защита от зацикливания
            if pos1 + self.first_dice < 25:
                # условие на пустоту в треугольнике
                if len(self.cells[pos1 + self.first_dice]) > 0:
                    print(but.objectName()[5:10], self.cells[pos1 + self.first_dice][0].objectName())
                    # проверка на то, не стоит ли вражеская фишка на позиции, куда можно пойти
                    if but.objectName()[5:10] in self.cells[pos1 + self.first_dice][0].objectName():
                        # разбиение на случаи в зависимости от половины, в которую идём И ТАМ УЖЕ ЕСТЬ НАША ФИШКА
                        if pos1 + self.first_dice < 11:
                            self.can_move_but.move(self.cells[pos1 + self.first_dice].x(),
                                              self.cells[pos1 + self.first_dice].y() + 52)
                        else:
                            self.can_move_but.move(self.cells[pos1 + self.first_dice].x(),
                                              self.cells[pos1 + self.first_dice].y() - 52)
                else:
                    # т к в треугольник мы можем пойти и он пустой
                    x, y = triangles[pos1 + self.first_dice][0], triangles[pos1 + self.first_dice][1]
                    self.can_move_but.move(x, y)

            self.cells[pos1 + self.first_dice - 1] = [self.can_move_but] + self.cells[pos1 + self.first_dice - 1]
        else:
            # защита от зацикливания
            if (0 < pos1 < 12 and (pos1 + self.first_dice < 13)) or pos1 > 12:
                # условие на пустоту в треугольнике
                if len(self.cells[(pos1 + self.first_dice) % 24]) > 0:
                    print(but.objectName()[5:10], self.cells[(pos1 + self.first_dice) % 25][0].objectName())
                    # проверка на то, не стоит ли вражеская фишка на позиции, куда можно пойти
                    if but.objectName()[5:10] in self.cells[(pos1 + self.first_dice) % 25][0].objectName():
                        # разбиение на случаи в зависимости от половины, в которую идём И ТАМ УЖЕ ЕСТЬ НАША ФИШКА
                        if 12 < pos1 + self.first_dice < 25:
                            self.can_move_but.move(self.cells[pos1 + self.first_dice].x(),
                                              self.cells[pos1 + self.first_dice].y() + 52)
                        else:
                            self.can_move_but.move(self.cells[pos1 + self.first_dice].x(),
                                              self.cells[pos1 + self.first_dice].y() - 52)
                else:
                    # т к в треугольник мы можем пойти и он пустой
                    x, y = triangles[pos1 + self.first_dice - 1][0], triangles[pos1 + self.first_dice - 1][1]
                    self.can_move_but.move(x, y)
            self.cells[pos1 + self.first_dice - 1] = [self.can_move_but] + self.cells[pos1 + self.first_dice - 1]
        self.can_move_but.show()
        self.can_move_but.clicked.connect(lambda: self.mover(pos1, self.first_dice))

    # ПЕРВЫЙ СТОЛБЕЦ - СПИСОК. НАДО ПОФИКСИТЬ
    def mover(self, pos, dice):
        m = self.cells[pos - 1][0][0]
        self.cells[pos - 1][0] = self.cells[pos - 1][1:]
        self.cells[pos + dice - 1] = [m] + self.cells[pos + dice - 1]
        if 'reddd' in m.objectName():
            x, y = triangles[pos + dice][0], triangles[pos + dice][1]
        else:
            x, y = triangles[pos + dice - 1][0], triangles[pos + dice - 1][1]
        self.cells[pos + dice - 1][0].move(x, y)
        self.can_move_but.deleteLater()

    # функция проверки наличия фишки на доске, которая возвращает -1 при отсутствии фишки и позицию фишки, если она находится не доске
    def on_desk(self, but):
        for i in self.cells:
            if but in i:
                return self.cells.index(i)


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

        if my_sys_lang == 'Eng':

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

        if my_sys_lang == 'Eng':

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
        self.game_mod_versus_bot.setGeometry(QtCore.QRect(160, 40, 100, 45))
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

        if my_sys_lang == "Рус":
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

        if my_sys_lang == 'Рус':
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
        global my_sys_lang
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

        if my_sys_lang == 'Eng':

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

        self.lbl2.setGeometry(275, 520, 400, 25)

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
        if my_sys_lang == 'Eng':
            switch_lang("Рус")
        else:
            switch_lang("Eng")

        updater(self)

    # начало игры

    def play_game(self):
        wnd_menu.hide()
        self.wnd_choose_game_mode = ChooseGameMode()
        self.wnd_choose_game_mode.show()


if __name__ == '__main__':
    my_sys_lang = 'Eng'
    app = QtWidgets.QApplication(sys.argv)
    wnd_menu = Menu()
    wnd_menu.show()
    sys.exit(app.exec())
