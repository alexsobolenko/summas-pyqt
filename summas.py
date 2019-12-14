#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "alexsobolenko"

import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsView, QGraphicsScene, QGraphicsObject, QVBoxLayout, qApp
from PyQt5.QtCore 	 import QRectF, pyqtSignal, Qt, QBasicTimer
from PyQt5.QtGui 	 import QBrush, QPen, QFont
from win32api        import GetSystemMetrics

from playrect  		 import PlayRect
from labelrect 		 import LabelRect
from btnrect   		 import BtnRect

class Summas(QWidget):
	def __init__(self):
		super().__init__()
		
		self.size = 50
		self.capacity = 5
		self.h = 5
		self.dif = 1
		self.difText = {1:'1-9', 2:'2-4', 3:'1-19'}
		self.difKol = {1: [1, 9], 2: [2, 4], 3: [1, 19]}
		self.needToSave = False
		self.layout = QVBoxLayout()
		self.layout.setSpacing(0)
		self.view = QGraphicsView()
		self.scene = QGraphicsScene()
		self.timer = QBasicTimer()
		self.rcCoord = [None, None, None]
		self.sceneSet = QGraphicsScene()

		lblNet = BtnRect(self, 'net', self.h*2 + self.size, self.h, self.size*2, self.size, self.h, 2)
		self.sceneSet.addItem(lblNet)
		self.valNet = BtnRect(self, str(self.capacity), self.h*2 + self.size, self.h*2 + self.size, self.size*2, self.size, self.h, 3)
		self.sceneSet.addItem(self.valNet)

		decNet = BtnRect(self, '<', self.h, self.h*2 + self.size, self.size, self.size, self.h, 1)
		decNet.clicked.connect(lambda: self.changeNet())
		self.sceneSet.addItem(decNet)
		incNet = BtnRect(self, '>', self.h*3 + self.size*3, self.h*2 + self.size, self.size, self.size, self.h*2, 1)
		incNet.clicked.connect(lambda: self.changeNet())
		self.sceneSet.addItem(incNet)

		lblType = BtnRect(self, 'type', self.h*2 + self.size, self.h*3 + self.size*2, self.size*2, self.size, self.h, 2)
		self.sceneSet.addItem(lblType)
		self.valType = BtnRect(self, str(self.difText[self.dif]), self.h*2 + self.size, self.h*4 + self.size*3, self.size*2, self.size, self.h, 3)
		self.sceneSet.addItem(self.valType)

		decType = BtnRect(self, '<', self.h, self.h*4 + self.size*3, self.size, self.size, self.h, 1)
		decType.clicked.connect(lambda: self.changeType())
		self.sceneSet.addItem(decType)
		incType = BtnRect(self, '>', self.h*3 + self.size*3, self.h*4 + self.size*3, self.size, self.size, self.h*2, 1)
		incType.clicked.connect(lambda: self.changeType())
		self.sceneSet.addItem(incType)

		btnBack = BtnRect(self, 'menu', self.h*2 + self.size, self.h*6 + self.size*5, self.size*2, self.size, self.h, 1)
		btnBack.clicked.connect(self.confirmChanges)
		self.sceneSet.addItem(btnBack)

		self.newGame()

		self.scene.setSceneRect(0, 0, (self.capacity + 3)*self.h + (self.capacity + 2)*self.size, (self.capacity + 6)*self.h + (self.capacity + 3)*self.size)
		self.view.setFixedSize((self.capacity + 3)*self.h + (self.capacity + 2.5)*self.size, (self.capacity + 6)*self.h + (self.capacity + 3.5)*self.size)
		self.view.move((GetSystemMetrics(0) - self.view.size().width())/2, (GetSystemMetrics(1) - self.view.size().height())/2)
		self.view.setWindowFlags(Qt.CustomizeWindowHint)
		self.view.show()

	def newGame(self):
		self.rect = []

		self.scene.clear()

		btnWidth = ((self.capacity - 2)*self.h + (self.capacity + 2)*self.size)/4

		btnNewGame = BtnRect(self, 'new\ngame', self.h, self.h, btnWidth, self.size, self.h)
		btnNewGame.clicked.connect(self.newGame)
		self.scene.addItem(btnNewGame)

		btnRestart = BtnRect(self, 'restart', self.h*2 + btnWidth, self.h, btnWidth, self.size, self.h)
		btnRestart.clicked.connect(self.restartGame)
		self.scene.addItem(btnRestart)

		btnTools = BtnRect(self, 'settings', self.h*3 + btnWidth*2, self.h, btnWidth, self.size, self.h)
		btnTools.clicked.connect(lambda: self.view.setScene(self.sceneSet))
		self.scene.addItem(btnTools)

		btnExit = BtnRect(self, 'exit', self.h*4 + btnWidth*3, self.h, btnWidth, self.size, self.h)
		btnExit.clicked.connect(qApp.quit)
		self.scene.addItem(btnExit)


		for i in range(self.capacity):
			for j in range(self.capacity):
				r = PlayRect(self, i, j, self.size, self.h)
				r.setValue(random.randint(self.difKol[self.dif][0], self.difKol[self.dif][1]), 2)
				r.clicked.connect(self.check)
				self.scene.addItem(r)
				self.rect.append(r)

		i = 0
		kol = [int(self.capacity*self.capacity*0.36 - 1), int(self.capacity*self.capacity*0.36 + 1)]
		k = random.randint(kol[0], kol[1])
		while i < k:
			j = random.randint(1, self.capacity*self.capacity) - 1
			if self.rect[j].target != 0:
				self.rect[j].target = 0
				i += 1

		self.rowRect1 = []
		self.rowRect2 = []
		for i in range(self.capacity):
			sumValue = 0
			sumTarget = 0
			for j in range(self.capacity):
				sumValue  += self.rect[self.capacity*i + j].value
				sumTarget += self.rect[self.capacity*i + j].target
			rr1 = LabelRect(self, i, -1, self.size, self.h)
			rr1.setValue(sumTarget, 1)
			rr1.setValue(sumValue, 3)
			self.scene.addItem(rr1)
			self.rowRect1.append(rr1)
			rr2 = LabelRect(self, i, self.capacity, self.size, self.h)
			rr2.setValue(sumTarget, 1)
			rr2.setValue(sumValue, 3)
			self.scene.addItem(rr2)
			self.rowRect2.append(rr2)
			rr1.clicked.connect(self.checkRC)
			rr2.clicked.connect(self.checkRC)

		self.colRect1 = []
		self.colRect2 = []
		for i in range(self.capacity):
			sumValue = 0
			sumTarget = 0
			for j in range(self.capacity):
				sumValue  += self.rect[self.capacity*j + i].value
				sumTarget += self.rect[self.capacity*j + i].target
			cr1 = LabelRect(self, -1, i, self.size, self.h)
			cr1.setValue(sumTarget, 1)
			cr1.setValue(sumValue, 3)
			self.scene.addItem(cr1)
			self.colRect1.append(cr1)
			cr2 = LabelRect(self, self.capacity, i, self.size, self.h)
			cr2.setValue(sumTarget, 1)
			cr2.setValue(sumValue, 3)
			self.scene.addItem(cr2)
			self.colRect2.append(cr2)
			cr1.clicked.connect(self.checkRC)
			cr2.clicked.connect(self.checkRC)

		self.view.setScene(self.scene)

	def check(self):
		if self.sender().block == False:
			row, col = self.sender().getCoord()

			val = 0
			for i in range(self.capacity):
				if self.rect[row*self.capacity + i].onOff:
					val += self.rect[row*self.capacity + i].value
			self.rowRect1[row].setValue(val, 3)
			self.rowRect2[row].setValue(val, 3)

			val = 0
			for i in range(self.capacity):
				if self.rect[col + self.capacity*i].onOff:
					val += self.rect[col + self.capacity*i].value
			self.colRect1[col].setValue(val, 3)
			self.colRect2[col].setValue(val, 3)

			x = 0
			for i in range(self.capacity):
				if self.rowRect1[i].ok:
					x += 1
				if self.colRect1[i].ok:
					x += 1
			if x == 2*self.capacity:
				for i in range(self.capacity*self.capacity):
					self.rect[i].setValue(0, 2)
					self.rect[i].onOff = True
				for i in range(self.capacity):
					self.colRect1[i].setValue(0, 1)
					self.colRect2[i].setValue(0, 1)
					self.rowRect1[i].setValue(0, 1)
					self.rowRect2[i].setValue(0, 1)
				for row in range(self.capacity):
					val = 0
					for i in range(self.capacity):
						if self.rect[row*self.capacity + i].onOff:
							val += self.rect[row*self.capacity + i].value
					self.rowRect1[row].setValue(val, 3)
					self.rowRect2[row].setValue(val, 3)
				for col in range(self.capacity):
					val = 0
					for i in range(self.capacity):
						if self.rect[col + self.capacity*i].onOff:
							val += self.rect[col + self.capacity*i].value
					self.colRect1[col].setValue(val, 3)
					self.colRect2[col].setValue(val, 3)

	def checkRC(self):
		rect = self.sender()
		row, col = rect.getCoord()
		if rect.ok:
			rect.block = not(rect.block)
			if row == -1 or row == self.capacity:
				for i in range(self.capacity):
					self.rect[col + self.capacity*i].block = rect.block
					self.rect[col + self.capacity*i].update()
					self.colRect1[col].block = rect.block
					self.colRect1[col].update()
					self.colRect2[col].block = rect.block
					self.colRect2[col].update()
			if col == -1 or col == self.capacity:
				for i in range(self.capacity):
					self.rect[row*self.capacity + i].block = rect.block
					self.rect[row*self.capacity + i].update()
					self.rowRect1[row].block = rect.block
					self.rowRect1[row].update()
					self.rowRect2[row].block = rect.block
					self.rowRect2[row].update()
		else:
			if self.rcCoord[0] == None:
				self.rcCoord = [row, col, rect.target]
				self.timer.start(1500, self)
				rect.setValue(rect.value, 2)
				rect.blockForTip = True

	def timerEvent(self, e):
		self.timer.stop()
		row, col = self.rcCoord[0], self.rcCoord[1]
		if row == -1 or row == self.capacity:
			self.colRect1[col].setValue(self.rcCoord[2], 1)
			self.colRect2[col].setValue(self.rcCoord[2], 1)
			self.colRect1[col].blockForTip = False
			self.colRect2[col].blockForTip = False
		if col == -1 or col == self.capacity:
			self.rowRect1[row].setValue(self.rcCoord[2], 1)
			self.rowRect2[row].setValue(self.rcCoord[2], 1)
			self.rowRect1[row].blockForTip = False
			self.rowRect2[row].blockForTip = False
		self.rcCoord = [None, None, None]


	def restartGame(self):
		for i in range(self.capacity*self.capacity):
			self.rect[i].onOff = True
			self.rect[i].block = False
			self.rect[i].update()
		for row in range(self.capacity):
			val = 0
			for i in range(self.capacity):
				if self.rect[row*self.capacity + i].onOff:
					val += self.rect[row*self.capacity + i].value
			self.rowRect1[row].block = False
			self.rowRect2[row].block = False
			self.rowRect1[row].setValue(val, 3)
			self.rowRect2[row].setValue(val, 3)
		for col in range(self.capacity):
			val = 0
			for i in range(self.capacity):
				if self.rect[col + self.capacity*i].onOff:
					val += self.rect[col + self.capacity*i].value
			self.colRect1[col].block = False
			self.colRect2[col].block = False
			self.colRect1[col].setValue(val, 3)
			self.colRect2[col].setValue(val, 3)

	def changeNet(self):
		minNet = 5
		maxNet = 8
		btn = self.sender()
		oldNet = self.capacity
		if btn.h == self.h:
			self.capacity -= 1
			if self.capacity < minNet:
				self.capacity = maxNet
		else:
			self.capacity += 1
			if self.capacity > maxNet:
				self.capacity = minNet
		self.valNet.setText(self.capacity)
		self.needToSave = (self.needToSave or (self.capacity != oldNet))

	def changeType(self):
		minType = 1
		maxType = 3
		btn = self.sender()
		oldType = self.dif
		if btn.h == self.h:
			self.dif -= 1
			if self.dif < minType:
				self.dif = maxType
		else:
			self.dif += 1
			if self.dif > maxType:
				self.dif = minType
		self.valType.setText(self.difText[self.dif])
		self.needToSave = (self.needToSave or (self.dif != oldType))

	def confirmChanges(self):
		if self.needToSave:
			self.needToSave = False
			self.view.setScene(self.scene)
			self.newGame()
			self.scene.setSceneRect(0, 0, (self.capacity + 3)*self.h + (self.capacity + 2)*self.size, (self.capacity + 4)*self.h + (self.capacity + 3)*self.size)
			self.view.setFixedSize((self.capacity + 3)*self.h + (self.capacity + 2.5)*self.size, (self.capacity + 4)*self.h + (self.capacity + 3.5)*self.size)
			self.view.move((GetSystemMetrics(0) - self.view.size().width())/2, (GetSystemMetrics(1) - self.view.size().height())/2)
		else:
			self.view.setScene(self.scene)
	


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Summas()
    sys.exit(app.exec_())