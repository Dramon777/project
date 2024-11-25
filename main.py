import codecs
import sys
from random import randint

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QDesktopWidget, QLabel

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


# функция выбора режима игры 1 на 1

def one_vs_one():
    global game_mod
    game_mod = '1vs1'


# функция выбора режима игры игрока против бота

def vsBot():
    global game_mod
    game_mod = 'bot'


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
        self.setStyleSheet("background-color: #f8f8d9;")
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


# окно игры

class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.bg_lbl = None
        self.bg_pixmap = None
        self.button_back = None
        self.lbl_dice1 = None
        self.pixmap_dice1 = None
        self.lbl_dice2 = None
        self.pixmap_dice2 = None
        self.button_throw_dice = None
        self.wnd_of_exit = None
        self.first_dice = 0
        self.second_dice = 0
        self.txt_lbl = None
        self.setupUI()

    def setupUI(self):
        set_args(self, 1700, 873)
        self.setStyleSheet("background-color: #f8dbaf;")

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

    # функция выхода в меню

    def back(self):
        self.wnd_of_exit = Exit('game')
        self.wnd_of_exit.show()

    # функция броска кубиков

    def throwed(self):

        # бросок кубиков + защита от спама кнопки

        self.first_dice = randint(1, 6)
        self.second_dice = randint(1, 6)
        self.button_throw_dice.setEnabled(False)
        print(self.first_dice, self.second_dice)

        # отображение кубиков на панели справа

        global dice_color
        self.lbl_dice1 = QLabel(self)
        self.lbl_dice2 = QLabel(self)
        self.txt_lbl = QLabel(self)
        if dice_color != 'both':
            self.pixmap_dice1 = QPixmap(dices_colors[dice_color][self.first_dice])
            self.pixmap_dice2 = QPixmap(dices_colors[dice_color][self.second_dice])
        else:
            self.pixmap_dice1 = QPixmap(dices_colors['white'][self.first_dice])
            self.pixmap_dice2 = QPixmap(dices_colors['black'][self.second_dice])
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
        set_args(self, 290, 220)
        self.setStyleSheet("background-color: #f8f8d9;")
        self.lbl = QLabel(self)

        if my_sys_lang == 'Eng':

            # надпись выбрать цвет кубиков
            self.lbl.setText("<b>Choose dice color</b>")
            self.lbl.move(70, 5)

            # кнопка выбрать белые кубики
            self.white = QtWidgets.QPushButton("White", self)

            # кнопка выбрать чёрные кубики
            self.black = QtWidgets.QPushButton("Black", self)

            # кнопка выбрать оба цвета для кубиков(1 белый, 1 черный)
            self.both = QtWidgets.QPushButton("1 Black and 1 White", self)

            # кнопка возврата в меню
            self.back_menu = QtWidgets.QPushButton("Back to menu", self)

        else:

            # надпись выбрать цвет кубиков
            self.lbl.setText("<b>Выберите цвет кубиков</b>")
            self.lbl.move(40, 5)

            # кнопка выбрать белые кубики
            self.white = QtWidgets.QPushButton("Белые", self)

            # кнопка выбрать чёрные кубики
            self.black = QtWidgets.QPushButton("Чёрные", self)

            # кнопка выбрать оба цвета для кубиков(1 белый, 1 черный)
            self.both = QtWidgets.QPushButton("1 Белый и 1 Чёрный", self)

            # кнопка возврата в меню
            self.back_menu = QtWidgets.QPushButton("Вернуться в меню", self)

        self.lbl.setStyleSheet("font-size: 18px;")

        # настройка кнопки выбора белого цвета
        self.white.setStyleSheet("font-size: 18px;")
        self.white.setGeometry(QtCore.QRect(5, 45, 120, 45))
        self.white.clicked.connect(chose_color_white)

        # настройка кнопки выбора чёрного цвета
        self.black.setStyleSheet("font-size: 18px;")
        self.black.setGeometry(QtCore.QRect(165, 45, 120, 45))
        self.black.clicked.connect(chose_color_black)

        # настройка кнопки выбора обоих цветов
        self.both.setStyleSheet("font-size: 18px;")
        self.both.setGeometry(QtCore.QRect(5, 100, 280, 45))
        self.both.clicked.connect(chose_color_both)

        # настройка кнопки возврата в меню
        self.back_menu.setStyleSheet("font-size: 18px;")
        self.back_menu.setGeometry(QtCore.QRect(120, 165, 160, 45))
        self.back_menu.clicked.connect(self.back_to_main_menu)

        # настройка кнопки ОК
        self.ok = QtWidgets.QPushButton("ОК", self)
        self.ok.setStyleSheet("font-size: 18px;")
        self.ok.setGeometry(QtCore.QRect(5, 165, 100, 45))
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
        set_args(self, 290, 200)
        self.setStyleSheet("background-color: #f8f8d9;")
        self.lbl = QLabel(self)

        if my_sys_lang == 'Eng':

            # надпись выбрать режим игры
            self.lbl.setText("<b>Choose your enemy</b>")
            self.lbl.move(60, 5)

            # кнопка Играть 1 на 1
            self.game_mod_1vs1 = QtWidgets.QPushButton("Person", self)

            # кнопка Играть с ботом
            self.game_mod_versus_bot = QtWidgets.QPushButton("Computer", self)

            # кнопка Играть
            self.play = QtWidgets.QPushButton("Play", self)

            # кнопка возврата в меню
            self.ret = QtWidgets.QPushButton("Back", self)


        else:

            # надпись выбрать режим игры
            self.lbl.setText("<b>Выберите вашего соперника</b>")
            self.lbl.move(8, 5)

            # кнопка Играть 1 на 1
            self.game_mod_1vs1 = QtWidgets.QPushButton("Человек", self)

            # кнопка Играть с ботом
            self.game_mod_versus_bot = QtWidgets.QPushButton("Компьютер", self)

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
        self.play.setGeometry(QtCore.QRect(95, 90, 100, 45))
        self.play.setObjectName("game_mod_you_vs_bot")
        self.play.clicked.connect(self.playing)

        self.ret.setStyleSheet("font-size: 18px;")
        self.ret.setGeometry(QtCore.QRect(95, 150, 100, 45))
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

    # функция закрытия окна и открытия меню

    def back(self):
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
        self.setStyleSheet("background-color: #FFEFC1;")

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
        self.but_back.setStyleSheet("background-color: #FFEAAC;"
                                    "font-size: 18px;")
        self.but_back.clicked.connect(self.back)

        # скроллбар + скролл колесом мыши

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setStyleSheet("background-color: #FFEAAC;")
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
        self.setObjectName("menu")
        set_args(self, 500, 550)
        self.setStyleSheet("background-color: #f8f8d9;")
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

