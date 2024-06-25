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
        self.setGeometry(config["windowX"], config["windowY"], 600, 280)
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
        self.minimize_label.setGeometry(505, -4, 40, 40)
        self.minimize_label.mousePressEvent = self.minimize_window

        #Contenido
        self.NightMode_button = QPixmap(iconosDirectory + config[mode]["buttonMode"])
        self.NightMode_label = QLabel(self)
        self.NightMode_label.setPixmap(self.NightMode_button)
        self.NightMode_label.setGeometry(550, 40, 40, 40)
        self.NightMode_label.mousePressEvent = self.NightMode_Toggle

        #TODO: Barra de volumen

        self.Backward_button = QPixmap(iconosDirectory + config[mode]["buttonBackward"])
        self.Backward_label = QLabel(self)
        self.Backward_label.setPixmap(self.Backward_button)
        self.Backward_label.setGeometry(230, 200, 40, 40)

        self.Player_button = QPixmap(iconosDirectory + config[mode]["buttonPlay"])
        self.Player_label = QLabel(self)
        self.Player_label.setPixmap(self.Player_button)
        self.Player_label.setGeometry(300, 200, 40, 40)

        self.Forward_button = QPixmap(iconosDirectory + config[mode]["buttonForward"])
        self.Forward_label = QLabel(self)
        self.Forward_label.setPixmap(self.Forward_button)
        self.Forward_label.setGeometry(350, 200, 40, 40)

        self.Title = QLabel(self)
        self.Title.setText("Titulo")
        self.Title.setGeometry(200, 70, 200, 20)
        self.Title.setStyleSheet("color: white; font-size: 30px; font-family: Arial;")
        self.Title.setAlignment(Qt.AlignCenter)

        self.Artist = QLabel(self)
        self.Artist.setText("Artist")
        self.Artist.setGeometry(200, 100, 200, 20)
        self.Artist.setStyleSheet("color: white; font-size: 15px; font-family: Arial;")
        self.Artist.setAlignment(Qt.AlignCenter)

        self.Source = QLabel(self)
        self.Source.setText("Source")
        self.Source.setGeometry(10, 210, 200, 20)
        self.Source.setStyleSheet("color: white; font-size: 15px; font-family: Arial;")
        self.Source.setAlignment(Qt.AlignCenter)

    def close_window(self, event):
        config["windowX"] = self.x()
        config["windowY"] = self.y()
        modifConfig(configDirectory, config)
        self.close()
    
    def minimize_window(self, event):
        self.showMinimized()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def NightMode_Toggle(self, event):
        config["NightModeAuto"] = not config["NightModeAuto"]
        modifConfig(configDirectory, config)
        self.update_elements()

    def update_elements(self):
        if config["NightModeAuto"]:
            mode = "NightMode"
        else:
            mode = "LightMode"
        self.frame_photo = QPixmap(framesDirectory + config[mode]["frame"])
        self.frame_label.setPixmap(self.frame_photo)
        self.NightMode_button = QPixmap(iconosDirectory + config[mode]["buttonMode"])
        self.NightMode_label.setPixmap(self.NightMode_button)