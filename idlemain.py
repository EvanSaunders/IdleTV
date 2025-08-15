import tkinter as tk
import random
import os
import state, cv2
from spotify_app import SpotifyNowPlayingApp
from bus_app import BusScheduleApp
from calendar_app import CalendarApp
from video_player import play_video

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.config(cursor="none")
    root.configure(bg="black")

    spotify_frame = tk.Frame(root, bg='black')
    bus_frame = tk.Frame(root, bg='black')
    calendar_frame = tk.Frame(root, bg='black')
    spotify_frame.place(x=0, y=0, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    bus_frame.place(x=0, y=0, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    calendar_frame.place(x=0, y=0, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    spotify_app = SpotifyNowPlayingApp(spotify_frame)
    bus_app = BusScheduleApp(bus_frame)
    calendar_app = CalendarApp(calendar_frame)

    # Initialize video
    video_selection = random.choice(os.listdir("/home/evans/IdleTV/videobackground"))
    state.cap = cv2.VideoCapture(f"/home/evans/IdleTV/videobackground/{video_selection}")
    state.lbl = tk.Label(spotify_frame, bg="black")
    state.lbl.place(x=0, y=40)
    state.lbl.lower()

    def check_channel():
        if state.hasChanged:
            if state.channel == "spotify":
                spotify_frame.tkraise()
                video_selection = random.choice(os.listdir("/home/evans/IdleTV/videobackground"))
                state.cap.open(f"/home/evans/IdleTV/videobackground/{video_selection}")
                state.hasChanged = False
            elif state.channel == "bus":
                bus_frame.tkraise()
            elif state.channel == "calendar":
                calendar_frame.tkraise()
        root.after(5000, check_channel)

    check_channel()

    root.bind("<Escape>", lambda e: (root.attributes('-fullscreen', False), root.destroy()))
    play_video()
    root.mainloop()
