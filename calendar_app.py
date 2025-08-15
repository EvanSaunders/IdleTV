import tkinter as tk
import datetime

class CalendarApp:
    def __init__(self, calendar_frame):
        self.calendar_frame = calendar_frame
        self.xspeed, self.yspeed = 1, 1

        # Get actual screen size
        self.WIDTH = calendar_frame.winfo_screenwidth()
        self.HEIGHT = calendar_frame.winfo_screenheight()

        self.canvas = tk.Canvas(
            calendar_frame,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)


        self.canvas.create_text(300, 100, text="Thursday", font=("The Led Display St", 40), fill="white", tags="day_group")
        self.canvas.create_text(300, 150, text="Aug 14", font=("The Led Display St", 30), fill="white", tags="day_group")

        self.text_tag = "day_group"

        self.move_text()

    def move_text(self):
        self.canvas.move(self.text_tag, self.xspeed, self.yspeed)

        left, top, right, bottom = self.canvas.bbox(self.text_tag)
        if left <= 0 or right >= self.WIDTH:
            self.xspeed = -self.xspeed
        if top <= 0 or bottom >= self.HEIGHT:
            self.yspeed = -self.yspeed

        self.canvas.after(30, self.move_text)
