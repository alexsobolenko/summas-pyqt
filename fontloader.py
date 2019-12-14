from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtGui import QFont, QFontDatabase

class FontLoader(QFont):
	def __init__(self, parent, addr, size):
		QFont.__init__(self)

		file = QFile(addr + '.ttf')
		file.open(QIODevice.ReadOnly)
		font_data = file.readAll()
		db_font = QFontDatabase()
		font_id = db_font.addApplicationFontFromData(font_data)
		font_fam = db_font.applicationFontFamilies(font_id)[0]
		self.setFamily(font_fam)
		self.setPointSize(size)
		self.setCapitalization(QFont.SmallCaps)