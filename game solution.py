#1600x900
import tkinter as tk
from PIL import Image, ImageTk
import random

# Create game window
window = tk.Tk()
window.title("Galactic Guardian")


# Load images
player_image = ImageTk.PhotoImage(Image.open("images/pship.png"))
enemy_image = ImageTk.PhotoImage(Image.open("images/aliens.png"))

#controls
key_bindings = {'left': 'a', 'right': 'd'}


# start screen
start_frame = tk.Frame(window)
start_frame.pack()

#start the game
def start_game():
    start_frame.pack_forget()

    #leaderboard
def show_leaderboard():
    pass

    # start button
start_button = tk.Button(start_frame, text="Start", command=start_game)
start_button.pack()

# leaderboard button
leaderboard_button = tk.Button(start_frame, text="Leaderboard", command=show_leaderboard)
leaderboard_button.pack()


# Creates a tab for the game
canvas = tk.Canvas(window, width=1600, height=900, bg='black')
canvas.pack()


window.mainloop() # starts game

