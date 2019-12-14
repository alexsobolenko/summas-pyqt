from PyQt5.QtWidgets import QWidget, QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtCore import QRectF, pyqtSignal, Qt, QFile, QIODevice
from PyQt5.QtGui import QBrush, QPen, QPainter, QFont, QColor


class BtnRect(QGraphicsObject):
	clicked 			= pyqtSignal()
	pressed 			= False, False
	text				= -1
	posx, posy 			= -1, -1
	width, height, h	= -1, -1, -1
	block				= False
	btnType				= -1

	def __init__(self, parent, text, posx, posy, width, height, h, bt = 1):
		QGraphicsObject.__init__(self)
		self.pressed 				= False
		self.h 						= h
		self.width, self.height		= width, height
		self.posy, self.posx 		= posy, posx
		self.text 					= str(text)
		self.btnType 				= bt - 1

		font1 = QFont('Century Gothic', int(self.height/3.0))
		font2 = QFont('Century Gothic', int(self.height/2.3))
		font3 = QFont('Century Gothic', int(self.height/2.1))
		self.fontType = [font1, font2, font3]
		self.dc = QColor(240, 128, 128)
		bu0 = QColor(0, 0, 130)
		bp0 = QColor(50, 200, 50)
		pu0 = bp0
		pp0 = bu0
		b1 = QColor(200, 200, 255)
		p1 = QColor(20, 110, 20)
		b2 = QColor(140, 130, 240)
		p2 = QColor(0, 50, 0)
		self.brushUnpress = [bu0, b1, b2]
		self.penUnpress = [pu0, p1, p2]
		self.brushPress = [bp0, b1, b2]
		self.penPress = [pp0, p1, p2]

	def boundingRect(self):
		return QRectF(self.posx, self.posy, self.width, self.height)

	def paint(self, painter, option, widget):
		rect = self.boundingRect()
		if self.pressed:
			brush = QBrush(self.brushPress[self.btnType])
			pen = QPen(self.penPress[self.btnType])
		else:
			brush = QBrush(self.brushUnpress[self.btnType])
			pen = QPen(self.penUnpress[self.btnType])
		pen.setWidth(3)
		font = self.fontType[self.btnType]
		painter.setBrush(brush)
		painter.setFont(font)
		painter.setPen(pen)
		painter.fillRect(rect, brush)
		painter.drawRoundedRect(rect, 3.0, 3.0)
		painter.drawText(rect, Qt.AlignCenter, self.text)

	def mousePressEvent(self, event):  
		if self.btnType < 1:
			self.pressed = True
		self.update()

	def mouseReleaseEvent(self, event):  
		if self.btnType < 1:
			self.pressed = False
		self.update()
		if event.button() == 1:
			self.clicked.emit()

	def setText(self, text):
		self.text = str(text)
		self.update()