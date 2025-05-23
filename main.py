import asyncio
import codecs
import sys
from random import randint
import os
from os import system
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QDesktopWidget, QLabel, QPushButton

game_sys_lang = 'Eng'
game_mod = None
wnd_menu = None
wnd_error = None
wnd_of_rules = None
text_rules = None
wnd_of_playing = None
wnd_of_choosing_dice_color = None
wnd_win = None
wnd_of_difficulty = None
diff = None
dice_color = ''

# Цветовая схема
COLORS = {
    'background': QColor(240, 240, 245),
    'button': QColor(70, 130, 180),  # SteelBlue
    'button_hover': QColor(65, 105, 225),  # RoyalBlue
    'button_pressed': QColor(30, 144, 255),  # DodgerBlue
    'text': QColor(50, 50, 50),
    'text_light': QColor(255, 255, 255),
    'error': QColor(220, 80, 80),
    'success': QColor(85, 170, 85),
    'panel': QColor(230, 230, 235)
}

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


# Добавляем функцию для корректного пути к ресурсам
def resource_path(relative_path):
    """Возвращает корректный путь для ресурсов после сборки в exe"""
    if hasattr(sys, '_MEIPASS'):
        # Если запущено из .exe, используем временную папку _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Иначе используем обычный путь
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

    # Установка цветовой палитры
    palette = QPalette()
    palette.setColor(QPalette.Window, COLORS['background'])
    palette.setColor(QPalette.WindowText, COLORS['text'])
    palette.setColor(QPalette.Button, COLORS['button'])
    palette.setColor(QPalette.ButtonText, COLORS['text_light'])
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    self.setPalette(palette)

    # Базовый стиль для кнопок
    self.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button'].name()};
            color: {COLORS['text_light'].name()};
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 18px;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['button_hover'].name()};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['button_pressed'].name()};
        }}
        QLabel {{
            color: {COLORS['text'].name()};
            font-size: 18px;
        }}
        QRadioButton {{
            color: {COLORS['text'].name()};
            font-size: 18px;
            spacing: 8px;
        }}
    """)
# функция отображения окна ошибка в связи с невыбранностью режима игры

def error_of_game_mod(self1):
    global wnd_error
    if game_sys_lang == 'Eng':
        wnd_error = Error('<b>Wrong game mod</b>')
    else:
        wnd_error = Error('<b>Ошибка игрового режима</b>')
    self1.hide()
    wnd_error.show()

# функция отображения окна ошибка в связи с невыбранностью сложноти бота
def error_of_difficulty(self1):
    global wnd_error
    if game_sys_lang == 'Eng':
        wnd_error = Error('<b>Wrong bot difficulty</b>')
    else:
        wnd_error = Error('<b>Ошибка сложности игры</b>')
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
        set_args(self, 400, 150)
        self.setObjectName("error")

        # Установка стиля для окна ошибки
        self.setStyleSheet(f"""
             QLabel {{
                 font-size: 18px;
                 color: {COLORS['error'].name()};
             }}
         """)

        # Сообщение об ошибке
        self.lbl = QLabel(f'{self.wrong}!', self)
        self.lbl.setGeometry(50, 30, 300, 40)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопка OK
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(150, 80, 100, 40)
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
        set_args(self, 400, 200)

        # Установка стиля для окна победы
        self.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {COLORS['text'].name()};
            }}
        """)

        # Сообщение о победе
        winner_text = f"<b>{'White' if self.winner == 'white' else 'Red'} won!!!</b>" if game_sys_lang == 'Eng' else f"<b>{'Белые' if self.winner == 'white' else 'Красные'} одержали победу!!!</b>"
        self.txt_lbl = QLabel(winner_text, self)
        self.txt_lbl.setGeometry(50, 40, 300, 50)
        self.txt_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопка возврата в меню
        btn_text = 'Back to menu' if game_sys_lang == 'Eng' else 'Вернуться в меню'
        self.back_menu = QPushButton(btn_text, self)
        self.back_menu.setGeometry(100, 110, 200, 50)
        self.back_menu.clicked.connect(self.back)

    def back(self):
        global game_mod
        game_mod = None
        wnd_menu.show()
        self.close()
        wnd_of_playing.close()

# окно выбора сложности при игре против бота
class SetDifficulty(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.easy_diff = None
        self.medium_diff = None
        self.hard_diff = None
        self.lbl = None
        self.back_menu = None
        self.ok = None

        self.setupUI()
    def setupUI(self):

        set_args(self, 350, 250)
        self.setObjectName("choosing_difficulty")

        # Заголовок
        title = '<b>Choose difficulty:</b>' if game_sys_lang == 'Eng' else '<b>Выберите сложность:</b>'
        self.lbl = QLabel(title, self)
        self.lbl.setGeometry(70, 10, 210, 30)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Радиокнопки выбора сложности
        self.easy_diff = QtWidgets.QRadioButton('Easy' if game_sys_lang == 'Eng' else 'Легкая', self)
        self.medium_diff = QtWidgets.QRadioButton('Medium' if game_sys_lang == 'Eng' else 'Средняя', self)
        self.hard_diff = QtWidgets.QRadioButton('Hard' if game_sys_lang == 'Eng' else 'Сложная', self)

        self.easy_diff.setGeometry(30, 50, 120, 40)
        self.medium_diff.setGeometry(30, 100, 120, 40)
        self.hard_diff.setGeometry(30, 150, 120, 40)

        # Кнопки управления
        self.ok = QPushButton('OK', self)
        self.ok.setGeometry(30, 200, 100, 40)
        self.ok.clicked.connect(self.oked)

        btn_text = 'Back to menu' if game_sys_lang == 'Eng' else 'Вернуться в меню'
        self.back_menu = QPushButton(btn_text, self)
        self.back_menu.setGeometry(150, 200, 170, 40)
        self.back_menu.clicked.connect(self.back_to_main_menu)

        # Подключение событий
        self.easy_diff.clicked.connect(self.set_easy)
        self.medium_diff.clicked.connect(self.set_medium)
        self.hard_diff.clicked.connect(self.set_hard)


    # функция перехода в игру
    def oked(self):
        global diff, wnd_of_playing
        if diff is not None:
            wnd_of_playing = Game()
            wnd_of_playing.show()
            self.close()
        else:
            error_of_difficulty(self)

    # функция возврата в меню
    def back_to_main_menu(self):
        global wnd_menu
        wnd_menu.show()
        self.close()

    # присваивание глобальнрому режиму сложности легкий уровень
    def set_easy(self):
        global diff
        diff = 3
        print("EasyMod")

    # присваивание глобальнрому режиму сложности средний уровень
    def set_medium(self):
        global diff
        diff = 5
        print("MediumMod")

    # присваивание глобальнрому режиму сложности сложный уровень
    def set_hard(self):
        global diff
        diff = 7
        print("HardMod")



class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.bot_thinking = None
        global diff

        self.bot_color = None
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
        self.but_play = None
        self.was = False

        self.success = False
        self.depth = diff
        self.throw_list_r = []
        self.throw_list_w = []
        self.setupUI()

    def setupUI(self):
        set_args(self, 1700, 873)

        # Дополнительные стили для игрового окна
        self.setStyleSheet(f"""
            QLabel#moving_player {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text'].name()};
                background-color: {COLORS['panel'].name()};
                border-radius: 5px;
                padding: 5px;
            }}
        """)

        # Игровое поле
        self.bg_lbl = QLabel(self)
        self.bg_pixmap = QPixmap(resource_path("Game_desk.png"))
        self.bg_lbl.setPixmap(self.bg_pixmap)
        self.bg_lbl.move(0, 0)

        # Панель управления
        control_panel = QtWidgets.QWidget(self)
        control_panel.setGeometry(1440, 0, 260, 873)
        control_panel.setStyleSheet(f"background-color: {COLORS['panel'].name()};")

        # Текущий игрок
        self.moving_player = QLabel(control_panel)
        self.moving_player.setObjectName("moving_player")
        self.moving_player.setGeometry(1, 600, 260, 30)
        self.moving_player.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопки управления
        if game_sys_lang == 'Рус':
            self.button_throw_dice = QtWidgets.QPushButton("Бросить кубики", control_panel)
            self.button_back = QtWidgets.QPushButton("Выход", control_panel)
            self.but_play = QtWidgets.QPushButton("Начать игру", control_panel)
        else:
            self.button_throw_dice = QtWidgets.QPushButton("Throw Dice", control_panel)
            self.button_back = QtWidgets.QPushButton("Exit", control_panel)
            self.but_play = QtWidgets.QPushButton("Start Game", control_panel)

        # Позиционирование и стилизация кнопок
        buttons = [
            (self.but_play, 1, 654, 258, 73),
            (self.button_throw_dice, 1, 727, 258, 73),
            (self.button_back, 1, 800, 258, 73)
        ]

        for btn, x, y, w, h in buttons:
            btn.setGeometry(x, y, w, h)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['button'].name()};
                    color: {COLORS['text_light'].name()};
                    font-size: 18px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['button_hover'].name()};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['button_pressed'].name()};
                }}
            """)

        # Подключение событий
        self.button_back.clicked.connect(self.back)
        self.button_throw_dice.clicked.connect(self.throwed)
        self.but_play.clicked.connect(self.play)

        # Инициализация игровых элементов
        self.but_size = QPixmap(resource_path('red_chip.png')).size()
        self.cells = []
        self.helper = [[], []]

        # Создание фишек
        for i in range(1, 16):
            # Красные фишки
            chip1 = self.create_chip('r', i)
            chip1.move(195, 787 - (52 * i) + 52)

            # Белые фишки
            chip2 = self.create_chip('w', i)
            chip2.move(1200, (52 * i) - 17)

            chip1.clicked.connect(lambda checked, chip=chip1: self.travel(chip))
            chip2.clicked.connect(lambda checked, chip=chip2: self.travel(chip))

            self.helper[0].insert(0, chip1)
            self.helper[1].insert(0, chip2)

        # Настройка игрового поля
        self.cells.append(self.helper[0])
        self.cells = self.cells + [[], [], [], [], [], [], [], [], [], [], []]
        self.cells.append(self.helper[1])
        self.cells = self.cells + [[], [], [], [], [], [], [], [], [], [], []]
        self.helper.clear()

    def play(self):
        self.but_play.hide()
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
        QtWidgets.QApplication.processEvents()

        while True:
            # Проверяем, не закончилась ли игра
            if self.is_game_end(self.player_color_now):
                global wnd_win
                wnd_win = GameEnd(self.player_color_now)
                wnd_win.show()

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
        # если кубики использованы, то ходить мы не можем
        if self.first_dice == -1000 == self.second_dice:
            print('Dices are empty')
            return False

        for i in self.cells:
            # если текущее поле пустое - не смотрим
            if len(i) == 0:
                continue

            # если текущее рассматриваемое поле вражеское - не смотрим
            if self.player_color_now not in i[0].objectName():
                continue

            pos = self.on_desk(i[0])

            # если выбрасываем фишки текущего цвета
            if self.player_color_now in i[0].objectName() and (self.fl_r and self.player_color_now == 'reddd') or (
                    self.fl_w and self.player_color_now == 'white'):
                pos = 6 - (pos % 6)
                if self.first_dice == pos:
                    return True
                elif self.first_dice < pos:
                    print('<')
                    continue
                else:
                    print('>')
                    if self.nothing_before(pos, i[0]):
                        return True

            # ХОДИМ
            # если первый кубик не пустой
            if self.first_dice != -1000:
                # если целевая позиция пуста - ход есть
                if len(self.cells[(pos + self.first_dice) % 24]) == 0:
                    return True

                # если на целевой позиции наша фишка - ход есть
                if self.player_color_now in self.cells[(pos + self.first_dice) % 24][0].objectName() or '-1' in self.cells[(pos + self.first_dice) % 24][0].objectName() or '-2' in self.cells[(pos + self.first_dice) % 24][0].objectName():
                    return True

            # если второй кубик не пустой
            if self.second_dice != -1000:

                # если целевая позиция пуста - ход есть
                if len(self.cells[(pos + self.second_dice) % 24]) == 0:
                    return True

                # если на целевой позиции наша фишка - ход есть
                if self.player_color_now in self.cells[(pos + self.second_dice) % 24][0].objectName() or '-1' in self.cells[(pos + self.second_dice) % 24][0].objectName() or '-2' in self.cells[(pos + self.second_dice) % 24][0].objectName():
                    return True
        print('LOX')
        return False

    # меняем цвета ходящего игрока
    def change_player(self):
        self.player_color_now = 'white' if 'reddd' == self.player_color_now else 'reddd'
        print(f'Color has changed to {self.player_color_now}')

        # Уведомляем текущего игрока о необходимости бросить кубики
        self.moving_player.setText(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'}, бросьте кубики!")

    # игра против бота

    def play_vs_bot(self):
        """
        Режим игры против бота.
        """
        self.player_color_now = 'reddd'  # Игрок всегда красный
        self.bot_color = 'white'

        if game_sys_lang == 'Рус':
            self.moving_player.setText(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'}, бросьте кубики!")
        else:
            self.moving_player.setText(f"{'Red' if self.player_color_now == 'reddd' else 'White'}, throw the dice!")

        while True:
            if self.is_game_end(self.player_color_now):
                global wnd_win
                wnd_win = GameEnd(self.player_color_now)
                wnd_win.show()

            for i in range(len(self.cells)):
                for j in range(len(self.cells[i])):
                    if '-1' in self.cells[i][j].objectName() or '-2' in self.cells[i][j].objectName():
                       continue
                    direction = -52 if i % 24 < 12 else 52
                    self.cells[i][j].move(triangles[i][0], triangles[i][1] + direction * j)
                    self.cells[i][j].show()
            if self.player_color_now == 'reddd':
                # Ожидание броска кубиков
                QtWidgets.QApplication.processEvents()  # Позволяем интерфейсу обновляться
                while self.button_throw_dice.isEnabled():
                    QtWidgets.QApplication.processEvents()
                # После броска кубиков начинаем ход
                self.button_throw_dice.setEnabled(False)
                if game_sys_lang == 'Рус':
                    self.moving_player.setText(f"Игрок, ходите!")
                else:
                    self.moving_player.setText(f"Player, make move!")
                # Проверяем, есть ли доступные ходы
                available_moves = self.check_available_moves()
                if not available_moves or self.first_dice == -1000 == self.second_dice:
                    print(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'} не могут сделать ход.")
                    self.change_player()
                    self.first_dice = self.second_dice = -1000
                    continue
            else:
                print(7)
                if game_sys_lang == 'Рус':
                    self.moving_player.setText(f"Бот сделал ход!")
                else:
                    self.moving_player.setText(f"Bot made move!")
                print(8)
                #бот бросает кубики
                self.throwed()
                print(9)
                # Проверяем, есть ли доступные ходы
                available_moves = self.check_available_moves()
                if not available_moves:
                    print(10)
                    print(f"{'Красные' if self.player_color_now == 'reddd' else 'Белые'} не могут сделать ход.")
                    self.change_player()
                    self.first_dice = self.second_dice = -1000
                    continue
                print(11)
                if self.first_dice != -1000 and self.second_dice != -1000:
                    print(12)
                    self.bot_make_move()
                print(13, self.first_dice, self.second_dice)

    # вспомогательная функция хода
    def bot_make_move(self):
        """
        Ход бота с использованием дерева принятия решений.
        """
        print(14)
        self.bot_thinking = True
        print(15)
        # Получаем лучший ход от дерева принятия решений
        best_move = self.get_best_move()
        print(16)
        if best_move:
            self.execute_bot_move(best_move)
        best_move = self.get_best_move()
        print(16)
        if best_move:
            self.execute_bot_move(best_move)
        print(17)
        self.bot_thinking = False
        self.change_player()
        self.throwed()
        for i in self.cells:
            if len(i):
                i[0].show()
        self.clearer()
        print(18)

    # реализация хода бота
    def execute_bot_move(self, move):
        """
        Выполняет ход бота.
        """
        print(19)
        src, dst = move # текущая позиция фишки, целевая позиция фишки
        self.cells[src][0].click()
        self.cells[src][0].click()
        asyncio.sleep(1)
        print(self.cells[dst][0].objectName(), src, dst, self.first_dice, self.second_dice)
        print([(x[0].objectName() if x else '-') for x in self.cells])
        self.cells[dst][0].click()
        self.clearer()
        print(21)

    # функции для реализации модели дерево принятия решений
    def evaluate_board(self):
        """
        Оценка текущего состояния доски.
        Чем выше значение, тем лучше для бота.
        """
        score = 0
        for i, cell in enumerate(self.cells):
            if cell and 'white' in cell[0].objectName():  # Фишки бота (белые)
                score += len(cell) * (24 - i)  # Чем ближе к выходу, тем лучше
        return score

    def minimax(self, depth, alpha, beta, maximizing_player):
        """
        Алгоритм Minimax с альфа-бета отсечением.
        """

        if depth == 0 or self.is_game_end('white') or self.is_game_end('reddd'):
            return self.evaluate_board()

        if maximizing_player:  # Ход бота (максимизация)
            max_eval = -float('inf')
            for move in self.get_all_possible_moves('white'):
                # Симулируем ход
                self.make_move(move[0], move[1])
                evall = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(move[0], move[1])  # Отменяем ход
                max_eval = max(max_eval, evall)
                alpha = max(alpha, evall)
                if beta <= alpha:
                    break  # Альфа-бета отсечение
            return max_eval
        else:  # Ход игрока (минимизация)
            min_eval = float('inf')
            for move in self.get_all_possible_moves('reddd'):
                # Симулируем ход
                self.make_move(move[0], move[1])
                evall = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(move[0], move[1])  # Отменяем ход
                min_eval = min(min_eval, evall)
                beta = min(beta, evall)
                if beta <= alpha:
                    break  # Альфа-бета отсечение
            return min_eval

    def get_best_move(self):
        """
        Возвращает лучший ход для бота на основе Minimax.
        """
        best_move = None
        max_eval = -float('inf')
        for move in self.get_all_possible_moves('white'):
            # Симулируем ход
            self.make_move(move[0], move[1])
            eval = self.minimax(self.depth - 1, -float('inf'), float('inf'), False)
            self.undo_move(move[0], move[1])  # Отменяем ход
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def get_all_possible_moves(self, color):
        """
        Возвращает все возможные ходы для текущего игрока.
        """

        print(23, [(x[0].objectName() if x else '----') for x in self.cells])
        moves = []
        for src in range(23):
            if not self.cells[src]: continue
            if color not in self.cells[src][0].objectName(): continue
            for dice in [self.first_dice, self.second_dice]:
                if dice == -1000: continue
                dst = (src + dice) % 24
                if self.is_move_valid(src, dice):
                    moves.append((src, dst))
        print(31, moves, self.first_dice, self.second_dice)
        return moves

    # проверка на то, выиграл ли игрок с цветом <color>
    def is_game_end(self, color):
        for i in self.cells:
            if len(i) == 0:
                continue
            if color in i[0].objectName():
                return False
        return True

    def make_move(self, f, s):
        print(10001, f, s)
        self.mover(f % 24, min(abs(f - s), 24 - abs(f - s)), self.cells[s % 24][0] if self.cells[s % 24] else None, True)
        self.clearer()

    def undo_move(self, f, s):
        print(10002, f, s)
        # возникает ошибка в undo_move с движение фишки обратно!!!!!!!!!!!!!
        self.mover(s % 24, -min(abs(f - s), 24 - abs(f - s)), self.cells[f % 24][0] if self.cells[f % 24] else None, True)
        self.clearer()

    def is_move_valid(self, pos, dice):
        print(100)
        but1 = self.cells[pos][0]
        target_pos = (pos + dice) % 24
        if 'white' in but1.objectName() and target_pos % 24 > 11 and -1 < pos < 12:
            return False

        player_color, enemy_color = 'white', 'reddd'

        if self.cells[target_pos % 24]:
            if player_color in self.cells[target_pos % 24][0].objectName():
                return True
            else:
                return False # вражеская фишка на позиции
        else:
            return True
    # функция выхода в меню
    def back(self):
        self.wnd_of_exit = Exit('game')
        self.wnd_of_exit.show()

    # функция броска кубиков
    def throwed(self):
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

        self.pixmap_dice1 = QPixmap(resource_path(dices_colors[dice_color if dice_color != 'both' else 'white'][self.first_dice]))

        # настройка второго кубика

        self.pixmap_dice2 = QPixmap(resource_path(dices_colors[dice_color if dice_color != 'both' else 'black'][self.second_dice]))

        if self.first_dice == self.second_dice:
            self.lbl_dice3 = QLabel(self)
            self.lbl_dice4 = QLabel(self)

            self.pixmap_dice3 = QPixmap(resource_path(dices_colors[dice_color if dice_color != 'both' else 'white'][self.first_dice]))
            self.pixmap_dice3 = self.pixmap_dice3.scaled(110, 110, QtCore.Qt.KeepAspectRatio)
            self.lbl_dice3.setPixmap(self.pixmap_dice3)
            self.lbl_dice3.move(1450, 155)

            self.pixmap_dice4 = QPixmap(resource_path(dices_colors[dice_color if dice_color != 'both' else 'black'][self.second_dice]))
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
            pix = QPixmap(resource_path('red_chip.png' if c == 'r' else ('white_chip.png' if c == 'w' else 'green_chip.png')))
            but.setIcon(QIcon(pix))
            but.setIconSize(self.but_size)
        but.setFixedSize(self.but_size)
        but.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }" if c != "none" else "QPushButton { background-color: red; }")
        but.setObjectName(f'chip_{"white" if c == "w" else ("reddd" if c == "r" else "field")}_{str(num)}')
        return but

    # вспомогательная объединяющая функция для движения
    def travel(self, but1, is_vs_bot=False):
        # Проверка, что фишка принадлежит текущему игроку
        player_color = 'reddd' if 'reddd' in but1.objectName() else 'white'
        if player_color != self.player_color_now:
            return

        # Проверка на последнюю нажатую кнопку
        if (self.num_of_last_pushed_but and self.num_of_last_pushed_but[-2:] == but1.objectName()[-2:] and
            self.num_of_last_pushed_but[:5] in but1.objectName()) or self.first_dice == 0:
            print('\n')
            return

        pos1 = self.on_desk(but1)

        # Удаление предыдущих подсказок, если они есть
        if self.num_of_last_pushed_but and not is_vs_bot:
            self.clearer()

        cnt = 0
        for i in range(6, 12) if 'white' in but1.objectName() else range(18, 24):
            cnt += len(self.cells[i])

        if self.first_dice != -1000:
            # Создание подсказки для первого кубика
            self.can_move_but1 = self.create_chip('g', -1)
            self.move_chip(but1, pos1, self.first_dice, self.can_move_but1, is_vs_bot)

            # Создание подсказки для выбрасывания от первого кубика
            self.can_throw_but1 = self.create_chip('g', -2)
            self.move_chip(but1, pos1, self.first_dice, self.can_throw_but1, is_vs_bot)

        if self.second_dice != -1000:
            # Создание подсказки для второго кубика
            self.can_move_but2 = self.create_chip('g', -1)
            self.move_chip(but1, pos1, self.second_dice, self.can_move_but2, is_vs_bot)

            # Создание подсказки для выбрасывания от второго кубика
            self.can_throw_but2 = self.create_chip('g', -2)
            self.move_chip(but1, pos1, self.second_dice, self.can_throw_but2, is_vs_bot)

    # двигаем фишку-подсказку
    def move_chip(self, but1, pos1, dice, move_button, is_vs_bot=False):
        # если кубик выброшен до этого
        if dice == -1000:
            return
        target_pos = pos1 + dice
        # Проверка выхода за пределы игрового поля, при недостижении состояния выбрасывания
        if '-1' in move_button.objectName():
            if (('white' in but1.objectName() and target_pos % 24 > 11 and -1 < pos1 < 12) or
                    ('reddd' in but1.objectName() and target_pos > 23)):
                move_button = None
                return

            self.num_of_last_pushed_but = but1.objectName()[5:10] + but1.objectName()[-2:]

            player_color, enemy_color = ('reddd', 'white') if 'reddd' in but1.objectName() else ('white', 'reddd')

            if self.cells[target_pos % 24]:
                if player_color in self.cells[target_pos % 24][0].objectName():
                    direction = -52 if target_pos % 24 < 12 else 52
                    move_button.move(triangles[target_pos % 24][0], triangles[target_pos % 24][1] + direction * len(self.cells[target_pos]))
                else:
                    move_button = None
                    return  # вражеская фишка на позиции
            else:
                x, y = triangles[target_pos % 24][0], triangles[target_pos % 24][1]
                move_button.move(x, y + (-52 if target_pos % 24 < 12 else 52) * (len(self.cells[target_pos % 24]) - (1 if len(self.cells[target_pos % 24]) else 0)))
                self.cells[target_pos % 24] = [move_button] + self.cells[target_pos % 24]
            if not is_vs_bot:
                move_button.show()
                move_button.clicked.connect(lambda: self.mover(pos1, dice, move_button))

        elif self.can_throw_but1 is not None:
            cnt = sum(len(self.cells[i]) for i in (range(6, 12) if 'white' in but1.objectName() else range(18, 24)))
            print(cnt)

            if not self.fl_r and 'reddd' in but1.objectName() and target_pos > 23 and cnt == 15:
                self.fl_r = True

            if not self.fl_w and 'white' in but1.objectName() and target_pos > 11 and cnt == 15:
                self.fl_w = True

            if (self.fl_r and 'reddd' in but1.objectName()) or (self.fl_w and 'white' in but1.objectName()):
                self.helper.clear()
                self.num_of_last_pushed_but = but1.objectName()[5:10] + but1.objectName()[-2:]

                pos = 6 - (pos1 % 6)
                if dice == pos:
                    print('==')
                    self.throw(but1, pos1, move_button)
                    print(move_button.x(), move_button.y())
                elif dice < pos:
                    print('<')
                    move_button = None
                    return
                else:
                    print('>')
                    if self.nothing_before(pos1, but1):
                        self.throw(but1, pos1, move_button)
                        print(move_button.x(), move_button.y())
                    else:
                        move_button = None
                        return
        else:
            move_button = None
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

    # ОН НЕ ВОЗВРАЩАЕТ НА МЕСТО НЕКОТОРЫЕ ВЗЯТЫЕ ФИШКИ ИЛИ ОНИ НЕ ПОКАЗЫВАЮТСЯ ПО КАКОЙ-ТО ПРИЧИНЕ
    # откуда, куда, место на доске куда пойдет
    # двигаем игровую фишку
    def mover(self, pos, dice, to_pos=None, aboba=False):
        if aboba:
            print('101--------------------')
            print([(x[0].objectName() if x else 'None') for x in self.cells])
            print('102--------------------')
            print(101, [len(x) for x in self.cells])
            target_pos = (pos + dice) % 24
            print(f"Таргет поз: {target_pos}, Поз сейчас: {pos}, Кубик: {dice}")
            m = self.cells[pos][0]
            self.cells[pos] = self.cells[pos][1:] if self.cells[pos] else []
            print(102)
            if self.cells[target_pos % 24]:
                self.cells[target_pos % 24].pop(0) if ('-1' in self.cells[target_pos % 24][0].objectName() or '-2' in self.cells[target_pos % 24][0].objectName()) else print()
                print(103)
                self.cells[target_pos % 24] = [m] + self.cells[target_pos % 24]
                print(104)
            else:
                self.cells[target_pos % 24] = [m]
            if to_pos is not None:
                x, y = to_pos.x(), to_pos.y()
                self.cells[target_pos % 24][0].move(x, y)
            elif len(self.cells[target_pos % 24]) > 1:
                x, y = triangles[target_pos % 24][0], triangles[target_pos % 24][1]
                self.cells[target_pos % 24][0].move(x, y)
                direction = -52 if target_pos % 24 < 12 else 52
                self.cells[target_pos % 24][0].move(self.cells[target_pos % 24][0].x(), self.cells[target_pos % 24][0].y() + direction)
            elif len(self.cells[target_pos % 24]) == 1:
                x, y = triangles[target_pos % 24][0], triangles[target_pos % 24][1]
                self.cells[target_pos % 24][0].move(x, y)
            print('The chip moved to position')
            self.clearer()
            print('Helps are cleared')
            print('\n')
        else:
            print(self.first_dice, self.second_dice, self.first_dice + pos, self.second_dice + pos)
            target_pos = pos + dice
            m = self.cells[pos][0]
            del self.cells[pos][0]
            self.cells[target_pos % 24] = [m] + self.cells[target_pos % 24]
            x, y = to_pos.x(), to_pos.y()
            self.cells[target_pos % 24][0].move(x, y)
            self.cells[target_pos % 24][0].show()
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
        if len(self.throw_list_r):
            self.throw_list_r.clear()
        if len(self.throw_list_w):
            self.throw_list_w.clear()
        for i in self.cells:
            if not i:
                continue
            if '-1' in i[0].objectName() or '-2' in i[0].objectName():
                i.pop(0)
        self.num_of_last_pushed_but = ''

    # создание подсказки для выбрасывания фишки
    def throw(self, chip, pos, helping):
        if 'reddd' in chip.objectName():
            helping.move(100, 35)
            self.throw_list_r.append(helping)
        else:
            helping.move(1300, 787)
            self.throw_list_w.append(helping)
        helping.show()
        helping.clicked.connect(lambda: self.yes_throw(pos))

    # само выбрасывание
    def yes_throw(self, pos):
        print('CHIP IS THROWED')
        self.cells[pos][0].deleteLater()
        del self.cells[pos][0]
        self.clearer()


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
        set_args(self, 350, 250)
        self.setObjectName("choosing_dice_color")

        # Заголовок
        title = '<b>Choose dice color</b>' if game_sys_lang == 'Eng' else '<b>Выберите цвет кубиков</b>'
        self.lbl = QLabel(title, self)
        self.lbl.setGeometry(40, 10, 270, 30)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Радиокнопки выбора цвета
        self.white = QtWidgets.QRadioButton("White" if game_sys_lang == 'Eng' else "Белые", self)
        self.black = QtWidgets.QRadioButton("Black" if game_sys_lang == 'Eng' else "Чёрные", self)
        self.both = QtWidgets.QRadioButton("1 Black and 1 White" if game_sys_lang == 'Eng' else "1 Белый и 1 Чёрный",
                                           self)

        self.white.setGeometry(30, 50, 120, 40)
        self.black.setGeometry(30, 100, 120, 40)
        self.both.setGeometry(30, 150, 290, 40)

        # Кнопки управления
        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setGeometry(30, 200, 100, 40)
        self.ok.clicked.connect(self.oked)

        btn_text = "Back to menu" if game_sys_lang == 'Eng' else "Вернуться в меню"
        self.back_menu = QtWidgets.QPushButton(btn_text, self)
        self.back_menu.setGeometry(150, 200, 170, 40)
        self.back_menu.clicked.connect(self.back_to_main_menu)

        # Подключение событий
        self.white.clicked.connect(chose_color_white)
        self.black.clicked.connect(chose_color_black)
        self.both.clicked.connect(chose_color_both)

    # функция возврата в меню
    def back_to_main_menu(self):
        global wnd_menu
        wnd_menu.show()
        self.close()

    # функция перехода к выбору сложности
    def oked(self):
        global dice_color
        if dice_color != '':
            if game_mod == 'bot':
                global wnd_of_difficulty
                wnd_of_difficulty = SetDifficulty()
                wnd_of_difficulty.show()
            else:
                global wnd_of_playing
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
        set_args(self, 290, 150)
        self.setObjectName("choosing_game_mod")

        # Заголовок
        title = '<b>Choose your opponent</b>' if game_sys_lang == 'Eng' else '<b>Выберите соперника</b>'
        self.lbl = QLabel(title, self)
        self.lbl.setGeometry(10, 5, 300, 30)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Радиокнопки выбора режима
        self.game_mod_1vs1 = QtWidgets.QRadioButton("Person" if game_sys_lang == 'Eng' else "Человек", self)
        self.game_mod_versus_bot = QtWidgets.QRadioButton("Computer" if game_sys_lang == 'Eng' else "Компьютер", self)

        self.game_mod_1vs1.setGeometry(30, 40, 100, 45)
        self.game_mod_versus_bot.setGeometry(150, 40, 130, 45)

        # Кнопки управления
        btn_text = "Play" if game_sys_lang == 'Eng' else "Играть"
        self.play = QtWidgets.QPushButton(btn_text, self)
        self.play.setGeometry(25, 90, 100, 45)
        self.play.clicked.connect(self.playing)

        btn_text = "Back" if game_sys_lang == 'Eng' else "Назад"
        self.ret = QtWidgets.QPushButton(btn_text, self)
        self.ret.setGeometry(155, 90, 100, 45)
        self.ret.clicked.connect(self.back)

        # Подключение событий
        self.game_mod_1vs1.clicked.connect(one_vs_one)
        self.game_mod_versus_bot.clicked.connect(vsBot)

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

        self.lbl.setStyleSheet("font-size: 12px;")

        self.yes.setGeometry(QtCore.QRect(15, 40, 75, 45))
        self.yes.setStyleSheet("font-size: 18px;")
        self.yes.setObjectName("yes_exit_button")
        self.yes.clicked.connect(self.exite)

        self.no.setGeometry(QtCore.QRect(131, 40, 75, 45))
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

        # Загрузка правил
        if game_sys_lang == 'Рус':
            with codecs.open('RULES_ru.txt', 'r', 'utf_8') as file:
                text_rules = file.read()
        else:
            with codecs.open('RULES_eng.txt', 'r', 'utf_8') as file:
                text_rules = file.read()

        # Текст правил
        self.lbl = QLabel(text_rules, self)
        self.lbl.setGeometry(10, 10, 780, 500)
        self.lbl.setWordWrap(True)

        # Кнопка возврата
        btn_text = 'Back' if game_sys_lang == 'Eng' else 'Назад'
        self.but_back = QtWidgets.QPushButton(btn_text, self)
        self.but_back.setGeometry(300, 520, 200, 50)
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

        # Заголовок
        title = '<b>Long Backgammon</b>' if game_sys_lang == 'Eng' else '<b>Длинные нарды</b>'
        self.lbl1 = QLabel(title, self)
        self.lbl1.setGeometry(50, 20, 400, 80)
        self.lbl1.setStyleSheet("font-size: 36px; color: #4a6fa5;")
        self.lbl1.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопки меню
        buttons = [
            ('Play' if game_sys_lang == 'Eng' else 'Играть', 100, 120, 300, 80, self.play_game),
            ('Rules' if game_sys_lang == 'Eng' else 'Правила', 100, 220, 300, 80, open_rules),
            ('Exit' if game_sys_lang == 'Eng' else 'Выход', 100, 320, 300, 80, self.exiting),
            ('Eng' if game_sys_lang == 'Eng' else 'Рус', 100, 420, 300, 80, self.lang)
        ]

        for text, x, y, w, h, handler in buttons:
            btn = QtWidgets.QPushButton(text, self)
            btn.setGeometry(x, y, w, h)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['button'].name()};
                    color: {COLORS['text_light'].name()};
                    font-size: 20px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['button_hover'].name()};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['button_pressed'].name()};
                }}
            """)
            btn.clicked.connect(handler)

        # Информация об авторе
        author = '<b>Author: Makarov Artem (dram00nn_nn)</b>' if game_sys_lang == 'Eng' else '<b>Автор: Макаров Артём (dram00nn_nn)</b>'
        self.lbl2 = QLabel(author, self)
        self.lbl2.setGeometry(50, 520, 400, 25)
        self.lbl2.setStyleSheet("font-size: 14px; color: #666;")
        self.lbl2.setAlignment(QtCore.Qt.AlignCenter)
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

if __name__ == '__main__':
    system("pip3 install -r requirments.txt")
    game_sys_lang = 'Eng'
    app = QtWidgets.QApplication(sys.argv)
    # Установка глобального стиля
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {COLORS['background'].name()};
            color: {COLORS['text'].name()};
            font-family: 'Segoe UI';
        }}
    """)
    wnd_menu = Menu()
    wnd_menu.show()

    sys.exit(app.exec())