from tkinter import *
import asyncio
from modules.config import *
from modules.volume import *
from modules.media_control import *

framesDirectory = "./frames/"
iconosDirectory = "./icon/"
configDirectory = "./config.json"
config = cargarConfig(configDirectory)

if config["NightModeAuto"]:
    mode = "NightMode"
else:
    mode = "LightMode"


class Player:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x280")
        self.master.title("Project Player")
        self.master.overrideredirect(1)
        self.master.attributes("-alpha", config["transparency"])
        self.master.attributes("-topmost", True)
        self.master.attributes("-transparent", "grey")
        self.master.iconbitmap(iconosDirectory + "logo.ico")


        # Frames
        self.frame_photo = PhotoImage(file=framesDirectory + config[mode]["frame"])
        self.frame_label = Label(self.master, border=0, bg="grey", image=self.frame_photo)
        self.frame_label.pack(fill=BOTH, expand=True)
        self.frame_label.bind("<B1-Motion>", lambda e: self.move_window(e))
        self.frame_label.bind("<Map>", lambda e: self.frame_mapped(e))

        # Barra de ventana
        self.exit_button = PhotoImage(file=iconosDirectory + "Exit.png")
        self.exit_label = Label(self.master, image=self.exit_button,border=0 , bg="#1E1E1E")
        self.exit_label.place(x=550, y=6)
        self.exit_label.bind("<Button>", lambda e: self.exit_app())

        self.minimize_button = PhotoImage(file=iconosDirectory + "Minimize.png")
        self.minimize_label = Label(self.master, image=self.minimize_button,border=0 , bg="#1E1E1E")
        self.minimize_label.place(x=520, y=6)
        self.minimize_label.bind("<Button>", lambda e: self.minimize_app(e))

        #Contenido
        self.NightMode_button = PhotoImage(file=iconosDirectory + config[mode]["buttonMode"])
        self.NightMode_label = Label(self.master, image=self.NightMode_button,border=0, bg=config[mode]["bg"])
        self.NightMode_label.place(x=550, y=40)
        self.NightMode_label.bind("<Button>", lambda e: self.NightMode_toggle(e))
        self.is_Adjusting_Volume = False
        self.Volume_bar = Scale(self.master, from_=100, to=0, orient=VERTICAL,bg=config[mode]["bg"], fg=config[mode]["bg"], troughcolor=config[mode]["troughcolor"], highlightthickness=0, bd=0, sliderlength=30, sliderrelief="flat", width=10, length=150,  activebackground=config[mode]["fg"])
        self.Volume_text = Label(self.master, bg=config[mode]["bg"], fg=config[mode]["fg"])
        self.Volume_bar.place(x=5, y=80)
        self.Volume_text.place(x=18, y=230)
        self.Volume_bar.bind("<ButtonPress>", lambda e: self.start_Volume())
        self.Volume_bar.bind("<B1-Motion>", lambda e: self.adjust_Volume())
        self.Volume_bar.bind("<ButtonRelease>", lambda e: self.stop_Volume())

        self.Backward_button = PhotoImage(file=iconosDirectory + config[mode]["buttonBackward"])
        self.Backward_label = Label(self.master, image=self.Backward_button,border=0, bg=config[mode]["bg"])
        self.Backward_label.place(x=250, y=200)

        self.player_button = PhotoImage(file=iconosDirectory + config[mode]["buttonPause"])
        self.player_label = Label(self.master, image=self.player_button,border=0, bg=config[mode]["bg"])
        self.player_label.place(x=300, y=205)
        self.player_label.bind("<Button>", lambda e: self.play_pause(e))

        self.forward_button = PhotoImage(file=iconosDirectory + config[mode]["buttonForward"])
        self.forward_label = Label(self.master, image=self.forward_button,border=0, bg=config[mode]["bg"])
        self.forward_label.place(x=335, y=200)


        
        self.update_Volume()

        


    def exit_app(self):
        self.master.quit()

    def move_window(self, e):
        self.master.geometry(f'+{e.x_root}+{e.y_root}')

    def frame_mapped(self, e):
        self.is_Adjusting_Volume = False
        self.master.update_idletasks()
        self.master.overrideredirect(1)
        self.master.state("normal")
        self.master.after(10, self.update_Volume)
        
    def minimize_app(self, e):
        self.is_Adjusting_Volume = True
        self.master.update_idletasks()
        self.master.overrideredirect(0)
        self.master.iconify()
        

    def start_Volume(self):
        self.is_Adjusting_Volume = True

    def stop_Volume(self):
        self.is_Adjusting_Volume = False
        self.adjust_Volume()
        self.master.after(10, self.update_Volume)

    def update_Volume(self):
        if not self.is_Adjusting_Volume:
            current_Volume = get_volume()
            self.Volume_bar.set(current_Volume)
            self.Volume_text.config(text=f"{current_Volume}%")
            self.master.after(125, self.update_Volume)
    
    def adjust_Volume(self):
        value = self.Volume_bar.get()
        volumePercent = str(value) + "%"
        self.Volume_text.config(text=volumePercent)
        set_volume(value)

    def play_pause(self, e):
        #get_media()
        pass

    def NightMode_toggle(self, e):
        config["NightModeAuto"] = not config["NightModeAuto"]
        modifConfig(configDirectory, config)
        self.update_Elements()
        self.master.update_idletasks()

    def update_Elements(self):
        global mode
        if config["NightModeAuto"]:
            mode = "NightMode"
        else:
            mode = "LightMode"
        self.frame_photo = PhotoImage(file=framesDirectory + config[mode]["frame"])
        self.frame_label.configure(image=self.frame_photo)
        self.NightMode_button = PhotoImage(file=iconosDirectory + config[mode]["buttonMode"])
        self.NightMode_label.configure(image=self.NightMode_button, bg=config[mode]["bg"])
        self.Volume_bar.configure(bg=config[mode]["bg"], fg=config[mode]["bg"], troughcolor=config[mode]["troughcolor"], activebackground=config[mode]["fg"])
        self.Volume_text.configure(bg=config[mode]["bg"], fg=config[mode]["fg"])
        self.Backward_button = PhotoImage(file=iconosDirectory + config[mode]["buttonBackward"])
        self.Backward_label.configure(image=self.Backward_button, bg=config[mode]["bg"])
        self.player_button = PhotoImage(file=iconosDirectory + config[mode]["buttonPlay"])
        self.player_label.configure(image=self.player_button, bg=config[mode]["bg"])
        
        #pause button here

        self.forward_button = PhotoImage(file=iconosDirectory + config[mode]["buttonForward"])
        self.forward_label.configure(image=self.forward_button, bg=config[mode]["bg"])
