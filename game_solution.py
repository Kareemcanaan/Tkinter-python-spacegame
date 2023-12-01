#1920 x 1080
#boss image src=http://www.clker.com/clipart-612497.html
#enemy missile src= https://opengameart.org/content/pixel-space-invaders
#player missile src= https://opengameart.org/content/pixel-space-invaders
#aliens src= https://opengameart.org/content/pixel-space-invaders
#pship src= https://opengameart.org/content/pixel-space-invaders
import tkinter as tk
import tkinter.filedialog as tkf
import random
import time as Time
from PIL import Image, ImageTk


def time() -> int:
    """Returns the current time in milliseconds"""
    return int(Time.time() *1000)

class EnemyMissile():
    """Enemy missile class"""
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = ImageTk.PhotoImage(Image.open("images/enemy_missile.png"))
        self.me = self.canvas.create_image(x, y, image=self.image)

class PlayerMissile(): #player missle class
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = ImageTk.PhotoImage(Image.open("images/player_missile.png"))
        self.me = self.canvas.create_image(x, y, image=self.image)

class Enemy():
    """Enemy class"""
    def __init__(self, root, canvas, x, y, level):
        self.root = root
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(Image.open("images/aliens.png"))
        self.me = self.canvas.create_image(x, y, image=self.image)
        self.x = x
        self.y = y
        self.level = level

        x_jump = 20
        y_jump = 10 + self.level * 2

        self.sequence = [[x_jump, 0], [x_jump, 0], [x_jump, 0], [x_jump, 0],
                          [0, y_jump], [-x_jump, 0], [-x_jump, 0], [-x_jump, 0],
                            [-x_jump, 0], [0, y_jump]]
        self.count = 0

    def move(self):
        """Move function"""
        if self.count > 9:
            self.count = 0
        self.canvas.move(self.me, *self.sequence[self.count])
        self.x += self.sequence[self.count][0]
        self.y += self.sequence[self.count][1]
        self.count += 1

    def shoot(self, count):
        """Shoot function"""
        if random.randint(1, 1+(round(0.5*count))) == 1:
            return True

class MainApplication(tk.Frame):
    """Main application class"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.run=False


        self.canvas = tk.Canvas(parent, width=1600, height=1000, bg='black')
        self.canvas.pack(side="left")
        self.active = False
        self.enemies = []
        self.enemy_ordnance = []
        self.player_ordnance = []
        self.x = 800
        self.y = 900
        self.fired = False
        self.keys = set()
        self.level = 1
        self.paused = False
        self.left_key_changing = False
        self.right_key_changing = False
        self.fire_key_changing = False
        self.boss_image = None
        self.pause_text = None

        self.player_image = None
        self.player = None
        self.boss = False

        self.keylog = ["" for _ in range(8)]

        self.current = {}
        self.functions = {}
        self.root.bind("<KeyPress>", self.keydown, add="+")
        self.root.bind("<KeyRelease>", self.keyup, add="+")

        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.score = tk.Label(self.frame, text="Score: 0", font=("Arial", 20))
        self.score.pack(side=tk.TOP)
        self.level_label = tk.Label(self.frame, text=f"Level: {self.level}", font=("Arial", 20))
        self.level_label.pack(side=tk.TOP)

        self.left_key = "a"
        self.right_key = "d"
        self.fire_key = "space"

        self.controls_frame = tk.Frame(self.frame)
        self.controls_frame.pack(side=tk.TOP, pady = (50, 50))
        self.control_button_left = tk.Button(self.controls_frame, text=f"Left: {self.left_key}",
                                             font=("Arial", 20) , command=self.left_key_change)
        self.control_button_left.pack(side=tk.LEFT, expand=True)
        self.control_button_right = tk.Button(self.controls_frame, text=f"Right: {self.right_key}",
                                              font=("Arial", 20),  command=self.right_key_change)
        self.control_button_right.pack(side=tk.RIGHT, expand=True)

        self.control_button_fire = tk.Button(self.frame, text=f"Fire: {self.fire_key}",
                                             font=("Arial", 20),  command=self.fire_key_change)
        self.control_button_fire.pack(side=tk.TOP)


        self.start_button = tk.Button(self.frame, text="Start", font=("Arial", 20),
                                      command=self.start)
        self.start_button.pack(side=tk.TOP, pady=(100, 100))

        self.data_frame = tk.Frame(self.frame)
        self.data_frame.pack(side=tk.TOP)
        self.save_button = tk.Button(self.data_frame, text="Save", font=("Arial", 20), command=self.save)
        self.save_button.pack(side=tk.LEFT)
        self.load_button = tk.Button(self.data_frame, text="Load", font=("Arial", 20), command=self.load)
        self.load_button.pack(side=tk.RIGHT)

        self.leaderboard_data = []
        self.leaderboard = tk.Label(self.frame, text="Leaderboard", font=("Arial", 20))
        self.leaderboard.pack(side=tk.TOP, pady=(50, 0))
        self.leaderboard_list = tk.Listbox(self.frame, font=("Arial", 20))
        self.leaderboard_list.pack(side=tk.TOP)


        self.bindings = {}
        self.set_controls()

        self.run_bindings = {}
        self.delay_bindings = {}

        self.leaderboard_window = None
        self.game_over_state = False

        self.key_loop()
        self.load_leaderboard()

    def disable_buttons(self):
        self.control_button_left["state"] = "disabled"
        self.control_button_right["state"] = "disabled"
        self.control_button_fire["state"] = "disabled"
        self.save_button["state"] = "disabled"
        self.load_button["state"] = "disabled"
        self.start_button["state"] = "disabled"
    
    def enable_buttons(self):
        self.control_button_left["state"] = "normal"
        self.control_button_right["state"] = "normal"
        self.control_button_fire["state"] = "normal"
        self.save_button["state"] = "normal"
        self.load_button["state"] = "normal"
        self.start_button["state"] = "normal"

    def set_controls(self):
        self.bindings = {
                    self.left_key: {"function": self.left, "repeat": 10, "delay": 0},
                    self.right_key: {"function": self.right, "repeat": 10, "delay": 0},
                    "Escape": {"function": self.pause, "repeat": 0, "delay": 0},
                    self.fire_key: {"function": self.fire, "repeat": 0, "delay": 500},
                    "b": {"function": self.boss_key, "repeat": 0, "delay": 0}
                }
        
    def boss_key(self):
        if not self.boss:
            self.pause()
            print("Boss")
            self.boss_image_src = ImageTk.PhotoImage(Image.open("images/boss.png"))
            self.boss_image = self.canvas.create_image(800, 500, image=self.boss_image_src)
            self.boss = True
            print("ok")
        else:
            self.canvas.delete(self.boss_image)
            self.boss = False
            self.pause()
      
    def left_key_change(self):
        self.disable_buttons()
        self.left_key_changing = True
    
    def right_key_change(self):
        self.disable_buttons()
        self.right_key_changing = True

    def fire_key_change(self):
        self.disable_buttons()
        self.fire_key_changing = True

    def start(self):
        if self.game_over_state:
            self.restart()
            return
        if self.paused:
            self.pause()
            return
        self.active = True
        self.disable_buttons()
        self.player_image = ImageTk.PhotoImage(Image.open("images/pship.png"))
        self.player = self.canvas.create_image(800, 900, image=self.player_image)
        for i in range(80, 1580, 150):
            for j in range(80, 440, 120):
                self.enemies.append(Enemy(self.root, self.canvas, i, j, self.level))
        if not self.run:
            self.root.after(100, self.enemies_logic)
            self.root.after(100, self.enemy_ordnance_logic)
            self.root.after(100, self.player_ordnance_logic)
            self.root.after(100, self.collision_detection)
            self.root.after(100, self.missile_collision)

    def load_leaderboard(self):
        self.leaderboard_list.delete(0, tk.END)
        try:
            with open("leaderboard.txt", "r", encoding="utf8") as f:
                f.seek(0)
                data = f.read()
        except FileNotFoundError:
            return
        data = data.split("\n")
        for item in data:
            if data != "":
                self.leaderboard_list.insert(tk.END, item)
        self.leaderboard_data = [x.split(" ") for x in data if x != ""]
    
    def save_leaderboard(self):
        with open("leaderboard.txt", "w+", encoding="utf8") as f:
            f.seek(0)
            for item in self.leaderboard_data:
                f.write(f"{item[0]} {item[1]}\n")
    
    def add_to_leaderboard(self, name, score):
        self.leaderboard_data.append([name, score])
        self.leaderboard_data = sorted(self.leaderboard_data, key=lambda x: int(x[1]), reverse=True)
        self.leaderboard_data = self.leaderboard_data[:10]
        self.save_leaderboard()
        self.load_leaderboard()
        
    def game_over(self):
        self.disable_buttons()
        self.game_over_state = True
        self.active = False
        self.paused = False
        self.enable_buttons()
        self.canvas.delete(self.player)
        self.canvas.delete(self.boss_image)
        self.boss = False
        self.canvas.delete("all")
        self.saving = True
        self.canvas.create_text(800, 450, text="GAME OVER", font=("Arial", 50), fill="white")
        if len(self.leaderboard_data) == 0:
            self.leaderboard_dialogue()
        elif len(self.leaderboard_data) < 10:
            self.leaderboard_dialogue()
        elif int(self.score["text"].split(" ")[1]) > int(self.leaderboard_data[-1][1]):
            self.leaderboard_dialogue()
        
    def leaderboard_dialogue(self):
        self.leaderboard_window = tk.Toplevel(self.root)
        self.leaderboard_window.geometry("300x200")
        self.leaderboard_window.title("Leaderboard")
        self.leaderboard_window.resizable(False, False)
        self.leaderboard_window.bind("<Return>", self.leaderboard_enter)
        self.leaderboard_window.bind("<Escape>", self.leaderboard_escape)
        self.leaderboard_entry = tk.Entry(self.leaderboard_window, font=("Arial", 20))
        self.leaderboard_entry.pack(side=tk.TOP)
        self.leaderboard_entry.focus_set()
        self.leaderboard_button = tk.Button(self.leaderboard_window, text="Enter", font=("Arial", 20), command=self.leaderboard_enter)
        self.leaderboard_button.pack(side=tk.TOP)
        self.leaderboard_button_cancel = tk.Button(self.leaderboard_window, text="Cancel", font=("Arial", 20), command=self.leaderboard_escape)
        self.leaderboard_button_cancel.pack(side=tk.TOP)


    def leaderboard_enter(self, event=None):
        self.add_to_leaderboard(self.leaderboard_entry.get(), self.score["text"].split(" ")[1])
        self.leaderboard_window.destroy()
        self.enable_buttons()
    
    def leaderboard_escape(self, event=None):
        self.leaderboard_window.destroy()
        self.enable_buttons()



    def increment_score(self):
        amount = 100 + self.level * 50
        self.score["text"] = "Score: " + str(int(self.score["text"].split(" ")[1]) + amount)

    def pause(self): #pause function
        if not self.game_over_state:
            if self.active:
                self.active = False
                self.paused = True
                self.enable_buttons()
                self.pause_text = self.canvas.create_text(800, 450, text="PAUSED", font=("Arial", 50), fill="white")
            else:
                self.active = True
                self.paused = False
                self.disable_buttons()
                self.canvas.delete(self.pause_text)

    def save(self):
        filename = tkf.asksaveasfile(initialfile = 'save.dat', defaultextension=".dat",filetypes=[("Data files","*.dat")])
        if filename is None:
            return
        data = f"""score:{self.score["text"].split(" ")[1]}
level:{self.level}
"""
        with open(filename.name, "w+", encoding="utf8") as f:
            f.write(data)

    def load(self):
        filename = tkf.askopenfile(initialfile = 'save.dat', defaultextension=".dat",filetypes=[("Data files","*.dat")])
        if filename is None:
            return
        with open(filename.name, "r", encoding="utf8") as f:
            data = f.read()
        data = data.split("\n")
        score = data[0].split(":")[1]
        level = data[1].split(":")[1]
        self.restart(level, score)

    def restart(self, level=1, score=0):
        self.game_over_state = False
        self.canvas.delete("all")
        self.active = False
        self.paused = False
        self.enable_buttons()
        self.score["text"] = f"Score: {score}"
        self.level = int(level)
        self.level_label["text"] = f"Level: {self.level}"
        self.enemies = []
        self.enemy_ordnance = []
        self.player_ordnance = []
        self.x = 800
        self.y = 900
        self.fired = False
        self.keys = set()
        self.boss = False
        self.start()

    def enemies_logic(self): #enemy logic
        if self.active:
            for enemy in self.enemies:
                enemy.move()
                if enemy.y > 800:
                    self.game_over()
                    break
                if enemy.shoot(len(self.enemies)):
                    self.enemy_ordnance.append(EnemyMissile(self.root, self.canvas, enemy.x, enemy.y+24))
        self.root.after(1000, self.enemies_logic)
    
    def enemy_ordnance_logic(self): #enemy ordnance logic
        if self.active:
            for missile in self.enemy_ordnance:
                amount = 15 + round(self.level * 0.5)
                self.canvas.move(missile.me, 0, amount)
                missile.y += amount
                if missile.y > 950:
                    self.canvas.delete(missile.me)
                    self.enemy_ordnance.remove(missile)
            for missile in self.player_ordnance:
                self.canvas.move(missile.me, 0, -10)
                missile.y += -10
                if missile.y < -100:
                    self.canvas.delete(missile.me)
                    self.player_ordnance.remove(missile)
        self.root.after(50, self.enemy_ordnance_logic)
    
    def player_ordnance_logic(self): #player ordnance logic
        if self.active:
            for missile in self.player_ordnance:
                self.canvas.move(missile.me, 0, -5)
                missile.y += -5
        self.root.after(20, self.player_ordnance_logic)
    
    def collision_detection(self):  #collision detection
        if self.active:
            enemies = [e.me for e in self.enemies]
            ordnance = [o.me for o in self.enemy_ordnance]
            data = self.canvas.find_overlapping(self.x-24, self.y-24, self.x+24, self.y+24)[1:]
            if data:
                for item in data:
                    if item in ordnance or item in enemies:
                        self.game_over()
                        break
        self.root.after(25, self.collision_detection)
    
    def missile_collision(self): #missile collision
        for missile in self.player_ordnance:
            data = self.canvas.find_overlapping(missile.x-6, missile.y-13, missile.x+6, missile.y+13)

            enemies = [e.me for e in self.enemies]
            ordnance = [o.me for o in self.enemy_ordnance]
            data = list(data)
            if self.player in data:
                data.remove(self.player)
            for item in data:
                if item in ordnance:
                    self.canvas.delete(missile.me)
                    try:
                        self.player_ordnance.remove(missile)
                    except ValueError:
                        pass
                    self.enemy_ordnance = [x for x in self.enemy_ordnance if x.me != item]
                    self.canvas.delete(item)
                elif item in enemies:
                    self.canvas.delete(missile.me)
                    try:
                        self.player_ordnance.remove(missile)
                    except ValueError:
                        pass
                    self.enemies = [x for x in self.enemies if x.me != item]
                    self.canvas.delete(item)
                    self.increment_score()
            if len(self.enemies) == 0:
                self.next_level()
        self.root.after(35, self.missile_collision)

    def next_level(self): #next level function
        self.level += 1
        self.level_label["text"] = f"Level: {self.level}"
        for i in range(80, 1580, 150):
            for j in range(80, 440, 120):
                self.enemies.append(Enemy(self.root, self.canvas, i, j, self.level))

    def left(self): #left function
        if self.active and self.x > 74:
            self.canvas.move(self.player, -10, 0)
            self.x -= 10

    def right(self): #right function
        if self.active and self.x < 1550:
            self.canvas.move(self.player, 10, 0)
            self.x += 10

    def fire(self): #fire function
        if self.active:
            self.player_ordnance.append(PlayerMissile(self.root, self.canvas, self.x, self.y+24))

    def key_loop(self): #key loop, runs every 10 ms
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

    def keydown(self, event=None): #defines keydown and keyup and binds them
        self.keys.add(event.keysym)
        self.keylog =  self.keylog[1:] + [event.keysym]
        if self.keylog == ["w", "w", "s", "s", "a", "d", "a", "d"]:
            print("Cheat Activated")
            self.bindings["space"] = {"function": self.fire, "repeat": 10, "delay": 0}
        if self.left_key_changing:
            self.left_key = event.keysym
            self.control_button_left["text"] = f"Left: {self.left_key}"
            self.left_key_changing = False
            self.set_controls()
            self.enable_buttons()
        elif self.right_key_changing:
            self.right_key = event.keysym
            self.control_button_right["text"] = f"Right: {self.right_key}"
            self.right_key_changing = False
            self.set_controls()
            self.enable_buttons()
        elif self.fire_key_changing:
            self.fire_key = event.keysym
            self.control_button_fire["text"] = f"Fire: {self.fire_key}"
            self.fire_key_changing = False
            self.set_controls()
            self.enable_buttons()

    def keyup(self, event=None):
        try:
            self.keys.remove(event.keysym)
            if event.keysym in self.run_bindings:
                del self.run_bindings[event.keysym]
        except KeyError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1900x1000")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
