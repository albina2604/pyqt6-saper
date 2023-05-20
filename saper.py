import random
import time

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

LEVELS = (
    (8, 10),
    (16, 40),
    (24, 99),
)

IMG_BOMB = QImage('./images/bomb.png')
IMG_CLOCK = QImage('./images/clock.png')


class Cell(QWidget):

    def __init__(self, x, y):
        super().__init__()
        self.setFixedSize(20, 20)

        self.x = x
        self.y = y

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = event.rect()
        outer, inner = Qt.GlobalColor.gray, Qt.GlobalColor.lightGray
        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_mine:
                p.drawPixmap(r, QPixmap(IMG_BOMB))

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.mines_around = 0
        self.is_revealed = False
        self.is_flagged = False
        self.is_end = False
        self.update()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.level = 0
        self.board_size, self.mines_count = LEVELS[self.level]

        self.setWindowTitle('Сапер')
        self.setFixedSize(self.sizeHint())
        self.initUI()
        self.init_grid()
        self.reset()
        self.show()

    def initUI(self):
        central_widget = QWidget()
        toolbar = QHBoxLayout()

        self.mines = QLabel(str(self.mines_count))
        self.mines.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clock = QLabel('000')
        self.clock.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.mines.font()
        font.setPointSize(24)
        font.setWeight(75)
        self.mines.setFont(font)
        self.clock.setFont(font)

        self.button = QPushButton()
        self.button.setFixedSize(32, 32)
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon('./images/smiley.png'))
        self.button.setFlat(True)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        l.setAlignment(Qt.AlignmentFlag.AlignRight |
                       Qt.AlignmentFlag.AlignVCenter)
        toolbar.addWidget(l)

        toolbar.addWidget(self.mines)
        toolbar.addWidget(self.button)
        toolbar.addWidget(self.clock)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        l.setAlignment(Qt.AlignmentFlag.AlignLeft |
                       Qt.AlignmentFlag.AlignVCenter)
        toolbar.addWidget(l)

        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        main_layout.addLayout(self.grid)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def init_grid(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                cell = Cell(x, y)
                self.grid.addWidget(cell, x, y)

    def reset(self):
        self.mines_count = LEVELS[self.level][1]
        self.mines.setText(f'{self.mines_count:03d}')
        self.clock.setText('000')

        for _, _, cell in self.get_all_cells():
            cell.reset()

        mine_positions = self.set_mines()

    def get_all_cells(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                yield (x, y, self.grid.itemAtPosition(x, y).widget())

    def set_mines(self):
        positions = []
        while len(positions) < self.mines_count:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x, y) not in positions:
                self.grid.itemAtPosition(x, y).widget().is_mine = True
                positions.append((x, y))
            return positions


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
