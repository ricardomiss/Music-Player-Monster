import tkinter as tk
from tkinter import *
from modules.player import Player

def main():
    root = tk.Tk()
    Player(root)
    root.mainloop()

if __name__ == "__main__":
    main()