import asyncio
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.media_control import *
from modules.config import *

framesDirectory = "./frames/"
iconosDirectory = "./icon/"
configDirectory = "./config.json"

config = cargarConfig(configDirectory)

if config["NightModeAuto"]:
    mode = "NightMode"
else:
    mode = "LightMode"

class Player(QMainWindow):
    def __init__(self):
        super().__init__()
        #Configuracion de la ventana
        self.setGeometry(0, 0, 600, 280)
        self.setWindowTitle("Project Player")        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(config["transparency"])
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(iconosDirectory + "logo.ico"))
        self.oldPos = self.pos()

        #Frames
        self.frame_photo = QPixmap(framesDirectory + config[mode]["frame"])
        self.frame_label = QLabel(self)
        self.frame_label.setPixmap(self.frame_photo)
        self.frame_label.setScaledContents(True)
        self.frame_label.setGeometry(0, 0, 600, 280)

        #Barra de ventana
        self.exit_button = QPixmap(iconosDirectory + "Exit.png")
        self.exit_label = QLabel(self)
        self.exit_label.setPixmap(self.exit_button)
        self.exit_label.setGeometry(550, -4, 40, 40)
        self.exit_label.mousePressEvent = self.close_window

        self.minimize_button = QPixmap(iconosDirectory + "Minimize.png")
        self.minimize_label = QLabel(self)
        self.minimize_label.setPixmap(self.minimize_button)
        self.minimize_label.setGeometry(520, -4, 40, 40)
        self.minimize_label.mousePressEvent = self.minimize_window
    
    def close_window(self, event):
        self.close()
    
    def minimize_window(self, event):
        self.showMinimized()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()