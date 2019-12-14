from PyQt5.QtWidgets import QWidget, QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtCore import QRectF, pyqtSignal, Qt
from PyQt5.QtGui import QBrush, QPen, QFont, QPainter, QColor

class LabelRect(QGraphicsObject):
	clicked 			= pyqtSignal()
	pressed 			= False, False
	onOff, ok			= True, True
	value, target		= -1, -1
	row, col			= -1, -1
	posx, posy 			= -1, -1
	size, h				= -1, -1
	block				= False
	blockForTip			= False

	def __init__(self, parent, row, col, size, h):
		QGraphicsObject.__init__(self)
		self.pressed 				= False
		self.h, self.size			= h, size
		self.row, self.col 			= row, col
		self.posy 					= row*(size + h) + 5*h + 2*size
		self.posx 					= col*(size + h) + 2*h + size

		self.dc 		= QColor(240, 128, 128)
		self.brushNo 	= QColor(218, 165, 32)
		self.penNo 		= QColor(50, 50, 0)
		self.brushOk 	= QColor(30, 144, 255)
		self.penOk 		= QColor(0, 0, 50)
		self.brushBlock = QColor(139, 0, 0)
		self.penBlock 	= QColor(255, 165, 0)

	def boundingRect(self):
		return QRectF(self.posx, self.posy, self.size, self.size)

	def paint(self, painter, option, widget):
		rect 		= self.boundingRect()
		brush 		= QBrush(self.dc)
		pen 		= QPen(self.dc, 2)
		font 		= QFont('Century Gothic', int(self.size/2.1))
		ok1color 	= {True: Qt.black, False: Qt.red}
		if self.ok:
			brush.setColor(self.brushOk)
			pen.setColor(self.penOk)
		else:
			brush.setColor(self.brushNo)
			pen.setColor(self.penNo)
		if self.block:
			brush.setColor(self.brushBlock)
			pen.setColor(self.penBlock)
		painter.setBrush(brush)
		painter.setFont(font)
		painter.setPen(pen)
		painter.fillRect(rect, brush)
		painter.drawRoundedRect(rect, 3.0, 3.0)
		painter.drawText(rect, Qt.AlignCenter, str(self.target))

	def mousePressEvent(self, event):  
		self.pressed = True
		self.update()

	def mouseReleaseEvent(self, event):  
		self.pressed = False
		self.update()
		if event.button() == 1 and not(self.blockForTip):
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