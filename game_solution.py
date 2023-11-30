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
        

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        self.canvas = tk.Canvas(parent, width=1600, height=900, bg='black')
        self.canvas.pack(side="left")
        self.active = False
        self.enemies = []
        self.enemyOrdnance = []
        self.playerOrdnance = []
        self.x = 800
        self.y = 800
        self.fired = False
        self.keys = set()
        self.rects = []



        self.current = {}
        self.functions = {}
        self.root.bind("<KeyPress>", self.keydown, add="+")
        self.root.bind("<KeyRelease>", self.keyup, add="+")

        self.bindings = {            
            "a": {"function": self.left, "repeat": 10, "delay": 0},
            "d": {"function": self.right, "repeat": 10, "delay": 0},
            "esc": {"function": self.pause, "repeat": 0, "delay": 0},
            "space": {"function": self.fire, "repeat": 0, "delay": 500},
        }

        self.run_bindings = {}
        self.delay_bindings = {}


        self.key_loop()
      #  self.root.after(100, self.clear_rects)
        self.start()

    def clear_rects(self):
        for rect in self.rects:
            self.canvas.delete(rect)
        self.rects = []
        self.root.after(100, self.clear_rects)

    def start(self):
        self.active = True
        self.player_image = ImageTk.PhotoImage(Image.open("images/pship.png"))
        self.player = self.canvas.create_image(800, 800, image=self.player_image)
        for i in range(80, 1580, 150):
            for j in range(80, 440, 120):
                self.enemies.append(Enemy(self.root, self.canvas, i, j))
        self.root.after(100, self.enemies_logic)
        self.root.after(100, self.enemy_ordnance_logic)
        self.root.after(100, self.player_ordnance_logic)
        self.root.after(100, self.collision_detection)
        self.root.after(100, self.missile_collision)

        
    def pause(self):
        pass


    def enemies_logic(self):
        if self.active:
            for enemy in self.enemies:
                enemy.move()
                if enemy.shoot(len(self.enemies)):
                    self.enemyOrdnance.append(EnemyMissile(self.root, self.canvas, enemy.x, enemy.y+24))
        self.root.after(1000, self.enemies_logic)
    
    def enemy_ordnance_logic(self):
        if self.active:
            for missile in self.enemyOrdnance:
                self.canvas.move(missile.me, 0, 15)
                missile.x += 10
                if missile.y > 900:
                    self.canvas.delete(missile.me)
                    self.enemyOrdnance.remove(missile)
            for missile in self.playerOrdnance:
                self.canvas.move(missile.me, 0, -10)
                missile.y += -20
                if missile.y < 0:
                    self.canvas.delete(missile.me)
                    self.playerOrdnance.remove(missile)
        self.root.after(50, self.enemy_ordnance_logic)
    
    def player_ordnance_logic(self):
        if self.active:
            for missile in self.playerOrdnance:
                self.canvas.move(missile.me, 0, -5)
                missile.y += -5
        self.root.after(20, self.player_ordnance_logic)
    
    def collision_detection(self):
        if self.active:
            enemies = [e.me for e in self.enemies]
            ordnance = [o.me for o in self.enemyOrdnance]
            data = self.canvas.find_overlapping(self.x, self.y, self.x+48, self.y+48)[1:]
         #   self.rects.append(self.canvas.create_rectangle(self.x-24, self.y-24, self.x+24, self.y+24, outline="white"))
            if data:
                for item in data:
                    if item in ordnance or item in enemies:
                        self.active = False
                        self.canvas.create_text(800, 450, text="GAME OVER", font=("Arial", 50), fill="white")
                        break
        self.root.after(25, self.collision_detection)
    
    def missile_collision(self):
        for missile in self.playerOrdnance:
            data = self.canvas.find_overlapping(missile.x-6, missile.y-13, missile.x+6, missile.y+13)
          #  self.rects.append(self.canvas.create_rectangle(missile.x-6, missile.y-13, missile.x+6, missile.y+13, outline="white"))

            enemies = [e.me for e in self.enemies]
            ordnance = [o.me for o in self.enemyOrdnance]
            data = list(data)
            if self.player in data:
                data.remove(self.player)
            for item in data:
                if item in ordnance:
                    self.canvas.delete(missile.me)
                    self.playerOrdnance.remove(missile)
                    self.enemyOrdnance = [x for x in self.enemyOrdnance if x.me != item]
                    self.canvas.delete(item)
                elif item in enemies:
                    self.canvas.delete(missile.me)
                    self.playerOrdnance.remove(missile)
                    self.enemies = [x for x in self.enemies if x.me != item]
                    self.canvas.delete(item)
        self.root.after(35, self.missile_collision)


    def left(self):
        if self.active and self.x > 74:
            self.canvas.move(self.player, -10, 0)
            self.x -= 10

    def right(self):
        if self.active and self.x < 1550:
            self.canvas.move(self.player, 10, 0)
            self.x += 10

    def fire(self):
        if self.active:
            self.playerOrdnance.append(PlayerMissile(self.root, self.canvas, self.x, self.y+24))

    def key_loop(self):
        now = time()
        for key in self.keys:
            if key in self.bindings:
                if key not in self.run_bindings:
                    self.run_bindings[key] = now
                if key not in self.delay_bindings:
                    self.delay_bindings[key] = now
                if self.bindings[key]["delay"] == 0 and self.bindings[key]["repeat"] == 0:
                    if self.run_bindings[key] == now:
                        self.bindings[key]["function"]()
                elif self.bindings[key]["delay"] == 0 and self.bindings[key]["repeat"] != 0:
                    if now - self.run_bindings[key] >= self.bindings[key]["repeat"]:
                        self.bindings[key]["function"]()
                        self.run_bindings[key] = now
                elif self.bindings[key]["delay"] != 0 and self.bindings[key]["repeat"] == 0:
                    if now - self.delay_bindings[key] >= self.bindings[key]["delay"] and self.run_bindings[key] == now:
                        self.bindings[key]["function"]()
                        self.delay_bindings[key] = now
                else:
                    if now - self.delay_bindings[key] >= self.bindings[key]["delay"]:
                        self.bindings[key]["function"]()
                        self.delay_bindings[key] = now

                    
        
        
        self.root.after(10, self.key_loop)

    def keydown(self, event=None):
        self.keys.add(event.keysym)
            
    def keyup(self, event=None):
        self.keys.remove(event.keysym)
        if event.keysym in self.run_bindings:
            del self.run_bindings[event.keysym]



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x900")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    