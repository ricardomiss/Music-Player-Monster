import sys
import asyncio
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.media_control import *
from modules.config import *



framesDirectory = "./frames/"
histoyuDirectory = "./history/"
iconosDirectory = "./icon/"
sourceDirectory = "./icon/source/"
configDirectory = "./config.json"

config = cargarConfig(configDirectory)

playing = False
source = None


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

        #Content
        self.NightMode_button = QPixmap(iconosDirectory + config[mode]["buttonMode"])
        self.NightMode_label = QLabel(self)
        self.NightMode_label.setPixmap(self.NightMode_button)
        self.NightMode_label.setGeometry(550, 40, 40, 40)
        self.NightMode_label.mousePressEvent = self.NightMode_Toggle

        #TODO: Barra de volumen

        self.Backward_button = QPixmap(iconosDirectory + config[mode]["buttonBackward"])
        self.Backward_label = QLabel(self)
        self.Backward_label.setPixmap(self.Backward_button)
        self.Backward_label.setGeometry(310, 200, 40, 40)
        self.Backward_label.mousePressEvent = self.def_backwards

        self.Player_button = QPixmap(iconosDirectory + config[mode]["buttonPlay"])
        self.Player_label = QLabel(self)
        self.Player_label.setPixmap(self.Player_button)
        self.Player_label.setGeometry(380, 200, 40, 40)
        self.Player_label.mousePressEvent = self.player_toggle

        self.Forward_button = QPixmap(iconosDirectory + config[mode]["buttonForward"])
        self.Forward_label = QLabel(self)
        self.Forward_label.setPixmap(self.Forward_button)
        self.Forward_label.setGeometry(440, 200, 40, 40)
        self.Forward_label.mousePressEvent = self.def_forwards

        #Song Info
        
        self.Title = QLabel(self)
        self.Title.setText("No hay informacion")
        self.Title.setGeometry(240, 50, 310, 80)
        self.Title.setStyleSheet(f'color: {config[mode]["fg"]}; font-size: 25px; font-family: Arial;')
        self.Title.setWordWrap(True)
        self.Title.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.Artist = QLabel(self)
        self.Artist.setText("No hay informacion")
        self.Artist.setGeometry(245, 135, 300, 20)
        self.Artist.setStyleSheet(f'color: {config[mode]["fg"]}; font-size: 15px; font-family: Arial;')
        self.Artist.setAlignment(Qt.AlignCenter)

        self.thumbnail = QLabel(self)
        self.thumbnail.setGeometry(85, 65, 150, 150)
        self.thumbnail.setPixmap(QPixmap(iconosDirectory + "NoThumbnail.png"))
        self.thumbnail.setScaledContents(True)

        self.Source = QLabel(self)
        self.Source.setText("No info")
        self.Source.setGeometry(65, 225, 200, 20)
        self.Source.setStyleSheet(f'color: {config[mode]["fg"]}; font-size: 15px; font-family: Arial;')
        self.Source.setAlignment(Qt.AlignCenter)

        self.SourceIcon = QPixmap(sourceDirectory + "NoThumbnail.png")
        self.SourceIconLabel = QLabel(self)
        self.SourceIconLabel.setPixmap(self.SourceIcon)
        self.SourceIconLabel.setGeometry(105, 223, 25, 25)
        self.SourceIconLabel.setScaledContents(True)

        media_signals.media_changed.connect(self.info_media)
        media_signals.playback_changed.connect(self.playback_status)
    def close_window(self, event):
        config["windowX"] = self.x()
        config["windowY"] = self.y()
        modifConfig(configDirectory, config)
        self.close()
        raise Exception("closing window")
    
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

    def playback_status(self, data):
        global playing
        if data == 0 or data == 5:
            self.Player_button = QPixmap(iconosDirectory + config[mode]["buttonPlay"])
            self.Player_label.setPixmap(self.Player_button)
            playing = False
        else:
            playing = True
            self.Player_button = QPixmap(iconosDirectory + config[mode]["buttonPause"])
            self.Player_label.setPixmap(self.Player_button)


    def info_media(self, data):
        global source
        try:
            if data:
                self.Title.setText(data[0])
                self.Artist.setText(data[1])
                if data[3] == source:
                    pass
                else:
                    source = data[3]
                    source_icon = source + ".png"
                    self.Source.setText(data[3])
                    if os.path.exists(sourceDirectory + source_icon):
                        self.SourceIcon = QPixmap(sourceDirectory + source_icon)
                        self.SourceIconLabel.setPixmap(self.SourceIcon)
                    self.SourceIconLabel.setPixmap(self.SourceIcon)

                self.thumbnail.setPixmap(QPixmap(histoyuDirectory + data[6]))
        except:
            self.Title.setText("No hay informacion")
            self.Artist.setText("No hay informacion")
            self.Source.setText("No info")

    def def_backwards(self, event):
        asyncio.create_task(control_media(3))

    def player_toggle(self, event):
        asyncio.create_task(control_media(1))
        

    def def_forwards(self, event):
        asyncio.create_task(control_media(2))

    def update_elements(self):
        global mode
        if config["NightModeAuto"]:
            mode = "NightMode"
        else:
            mode = "LightMode"
        self.frame_photo = QPixmap(framesDirectory + config[mode]["frame"])
        self.frame_label.setPixmap(self.frame_photo)
        self.NightMode_button = QPixmap(iconosDirectory + config[mode]["buttonMode"])
        self.NightMode_label.setPixmap(self.NightMode_button)
        self.Backward_button = QPixmap(iconosDirectory + config[mode]["buttonBackward"])
        self.Backward_label.setPixmap(self.Backward_button)
        if playing:
            self.Player_button = QPixmap(iconosDirectory + config[mode]["buttonPause"])
            self.Player_label.setPixmap(self.Player_button)
        else:
            self.Player_button = QPixmap(iconosDirectory + config[mode]["buttonPlay"])
            self.Player_label.setPixmap(self.Player_button)
        self.Forward_button = QPixmap(iconosDirectory + config[mode]["buttonForward"])
        self.Forward_label.setPixmap(self.Forward_button)
        
        self.Title.setStyleSheet(f'color: {config[mode]["fg"]}; font-size: 25px; font-family: Arial;')
        self.Artist.setStyleSheet(f'color: {config[mode]["fg"]}; font-size: 15px; font-family: Arial;')
        self.Source.setStyleSheet(f'color: {config[mode]["fg"]}; font-size: 15px; font-family: Arial;')