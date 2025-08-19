import tkinter as tk
from datetime import datetime
import imageio
from PIL import ImageTk, Image
from zoneinfo import ZoneInfo 
import random
import os
import state

class PokemonApp:
    def __init__(self, pokemon_frame):
        self.pokemon_frame = pokemon_frame

        self.WIDTH = pokemon_frame.winfo_screenwidth()
        self.HEIGHT = pokemon_frame.winfo_screenheight()
        # Get actual screen size

        self.canvas = tk.Canvas(
            pokemon_frame,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        background_image = Image.open("/home/evans/IdleTV/battleBackground.jpg")
        background_image = background_image.resize((self.WIDTH, self.HEIGHT+50), Image.Resampling.LANCZOS)
        tk_background_image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image(0, 0, image=tk_background_image, anchor="nw")
        self.canvas.background_image = tk_background_image

        healthbar1_image = Image.open("/home/evans/IdleTV/icons/healthbar1.png")
        healthbar1_image = healthbar1_image.resize((330, 100), Image.Resampling.LANCZOS)
        tk_healthbar1_image = ImageTk.PhotoImage(healthbar1_image)
        self.canvas.create_image(-30, 15, image=tk_healthbar1_image, anchor="nw")
        self.canvas.healthbar1_image = tk_healthbar1_image

        healthbar2_image = Image.open("/home/evans/IdleTV/icons/healthbar2.png")
        healthbar2_image = healthbar2_image.resize((330, 100), Image.Resampling.LANCZOS)
        tk_healthbar2_image = ImageTk.PhotoImage(healthbar2_image)
        self.canvas.create_image(350, 300, image=tk_healthbar2_image, anchor="nw")
        self.canvas.healthbar2_image = tk_healthbar2_image

 # === Load GIF 1 ===
        state.gif1_selection = random.choice(os.listdir("/home/evans/IdleTV/front_pokemon"))
        gif1_frames = imageio.mimread(f"/home/evans/IdleTV/front_pokemon/{state.gif1_selection}")
        gif1_resized = [
            ImageTk.PhotoImage(Image.fromarray(frame).resize((270,220), Image.Resampling.LANCZOS))
            for frame in gif1_frames
        ]
        gif1_id = self.canvas.create_image(230, 280, image=gif1_resized[0], anchor="center")

        # === Load GIF 2 ===
        state.gif2_selection = random.choice(os.listdir("/home/evans/IdleTV/back_pokemon"))
        gif2_frames = imageio.mimread(f"/home/evans/IdleTV/back_pokemon/{state.gif2_selection}")
        gif2_resized = [
            ImageTk.PhotoImage(Image.fromarray(frame).resize((150,20), Image.Resampling.LANCZOS))
            for frame in gif2_frames
        ]
        gif2_id = self.canvas.create_image(530, 120, image=gif2_resized[0], anchor="center")


        # Store all gifs in a list
        self.gifs = [
            {"frames": gif1_resized, "id": gif1_id, "index": 0},
            {"frames": gif2_resized, "id": gif2_id, "index": 0}
        ]

        gif1_name = os.path.splitext(state.gif1_selection)[0]
        gif2_name = os.path.splitext(state.gif2_selection)[0]
        self.name1_id = self.canvas.create_text(420, 305, text=gif2_name, font=("Pokemon B/W", 25), fill="white", anchor="nw")
        self.name2_id = self.canvas.create_text(30, 15,  text=gif1_name, font=("Pokemon B/W", 25), fill="white", anchor="nw")

        # Start animation loop
        self.animate_all()

    def animate_all(self):
        for gif in self.gifs:
            gif["index"] = (gif["index"] + 1) % len(gif["frames"])
            frame = gif["frames"][gif["index"]]
            self.canvas.itemconfig(gif["id"], image=frame)
        self.pokemon_frame.after(90, self.animate_all)


    def reload_gifs(self):
        # Load GIF 1
        state.gif1_selection = random.choice(os.listdir("/home/evans/IdleTV/front_pokemon"))
        gif1_frames = imageio.mimread(f"/home/evans/IdleTV/front_pokemon/{state.gif1_selection}")
        gif1_frames = gif1_frames[1:]
        gif1_resized = [
            ImageTk.PhotoImage(Image.fromarray(frame).resize((int(Image.fromarray(frame).width * 5), int(Image.fromarray(frame).height * 5)),Image.Resampling.LANCZOS))
            for frame in gif1_frames
        ]
        self.gifs[0]["frames"] = gif1_resized
        self.gifs[0]["index"] = 0
        self.canvas.itemconfig(self.gifs[0]["id"], image=gif1_resized[0])
        self.canvas.itemconfig(self.name1_id, text=os.path.splitext(state.gif1_selection)[0])

        # Load GIF 2
        state.gif2_selection = random.choice(os.listdir("/home/evans/IdleTV/back_pokemon"))
    
        gif2_frames = imageio.mimread(f"/home/evans/IdleTV/back_pokemon/{state.gif2_selection}")
        gif2_frames = gif2_frames[1:]
        gif2_resized = [
            ImageTk.PhotoImage(Image.fromarray(frame).resize((int(Image.fromarray(frame).width * 2.5), int(Image.fromarray(frame).height * 2.5)),Image.Resampling.LANCZOS))
            for frame in gif2_frames
        ]
        self.gifs[1]["frames"] = gif2_resized
        self.gifs[1]["index"] = 0
        self.canvas.itemconfig(self.gifs[1]["id"], image=gif2_resized[0])
        self.canvas.itemconfig(self.name2_id, text=os.path.splitext(state.gif2_selection)[0])






        # Open and resize the image
       # img = Image.open("/home/evans/IdleTV/videobackground/chopper.png")
        #img = img.resize((655, 250))

        # Convert to a Tkinter-compatible image
        #self.img = ImageTk.PhotoImage(img)

        # Set the image on the label
        #self.image_label = tk.Label(calendar_frame, borderwidth=0, highlightthickness=0)
        #self.image_label.config(image=self.img)
        #self.image_label.place(x=0, y=160)
