import tkinter as tk

class BusScheduleApp:
    def __init__(self, root):
        self.root = root
        self.bus_label = tk.Label(root, text="C  2 - BUCKEYE", font=("The Led Display St", 40), fg="white", bg="black")
        self.bus_label.place(x=0, y=10)
