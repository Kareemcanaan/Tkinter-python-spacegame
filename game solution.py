#1920 x 1080
import tkinter as tk
from PIL import Image, ImageTk
import random
import time as Time


def time() -> int:
    return int(Time.time() *1000)

class EnemyMissile():
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = ImageTk.PhotoImage(Image.open("images/enemy_missile.png"))
        self.me = self.canvas.create_image(x, y, image=self.image)

class PlayerMissile():
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = ImageTk.PhotoImage(Image.open("images/player_missile.png"))
        self.me = self.canvas.create_image(x, y, image=self.image)