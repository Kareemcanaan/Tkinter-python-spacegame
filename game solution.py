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


class Enemy():
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(Image.open("images/aliens.png"))
        self.me = self.canvas.create_image(x, y, image=self.image)
        self.x = x
        self.y = y

        x_jump = 25
        y_jump = 10

        self.sequence = [[x_jump, 0], [x_jump, 0], [x_jump, 0], [x_jump, 0], [0, y_jump], [-x_jump, 0], [-x_jump, 0], [-x_jump, 0], [-x_jump, 0], [0, y_jump]]
        self.count = 0

    def move(self):
        if self.count > 9:
            self.count = 0
        self.canvas.move(self.me, *self.sequence[self.count])
        self.x += self.sequence[self.count][0]
        self.y += self.sequence[self.count][1]
        self.count += 1

    def shoot(self, count):
        if random.randint(1, 1+(round(0.5*count))) == 1:
            return True