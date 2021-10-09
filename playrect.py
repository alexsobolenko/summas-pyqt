from PyQt5.QtWidgets import QWidget, QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtCore import QRectF, pyqtSignal, Qt
from PyQt5.QtGui import QBrush, QPen, QFont, QPainter, QColor


class PlayRect(QGraphicsObject):
    clicked = pyqtSignal()
    pressed = False, False
    onOff, ok = True, True
    value, target = -1, -1
    row, col = -1, -1
    posx, posy = -1, -1
    size, h = -1, -1
    block = False


    def __init__(self, parent, row, col, size, h):
        QGraphicsObject.__init__(self)
        self.pressed = False
        self.h, self.size = h, size
        self.row, self.col = row, col
        self.posy = row*(size + h) + 5*h + 2*size
        self.posx = col*(size + h) + 2*h + size

        self.dc = QColor(240, 128, 128)
        self.brushOn = QColor(154, 255, 50)
        self.penOn = QColor(0, 50, 0)
        self.brushOff = QColor(25, 25, 112)
        self.penOff = QColor(224, 255, 255)
        self.brushBlockOn = QColor(255, 205, 0)
        self.penBlockOn = QColor(139, 0, 0)
        self.brushBlockOff = QColor(100, 100, 0)
        self.penBlockOff = QColor(255, 99, 71)


    def boundingRect(self):
        return QRectF(self.posx, self.posy, self.size, self.size)


    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        brush = QBrush(self.dc)
        pen = QPen(self.dc)
        pen.setWidth(2)
        font = QFont('Century Gothic', int(self.size/2.1))
        x = 0

        if self.onOff:
            brush.setColor(self.brushOn)
            pen.setColor(self.penOn)
        else:
            brush.setColor(self.brushOff)
            pen.setColor(self.penOff)

        if self.block:
            if self.onOff:
                brush.setColor(self.brushBlockOn)
                pen.setColor(self.penBlockOn)
            else:
                brush.setColor(self.brushBlockOff)
                pen.setColor(self.penBlockOff)

        painter.setBrush(brush)
        painter.setFont(font)
        painter.setPen(pen)
        painter.fillRect(rect, brush)
        painter.drawRoundedRect(rect, 3.0, 3.0)
        painter.drawText(rect, Qt.AlignCenter, str(self.value))


    def mousePressEvent(self, event):
        self.pressed = True
        self.update()


    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.update()
        if event.button() == 1 and self.block == False:
            self.onOff = not(self.onOff)
            self.clicked.emit()


    def getCoord(self):
        return self.row, self.col


    def setValue(self, val, x = 2):
        if x <= 2:
            self.target = val
        if x >= 2:
            self.value = val
        self.ok = (self.value == self.target)
        self.update()
