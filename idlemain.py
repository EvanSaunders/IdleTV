import os
import requests
import time
from io import BytesIO
from dotenv import load_dotenv
import tkinter as tk
from PIL import ImageTk, Image
import cv2

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

def refresh_access_token():
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    auth_header = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(url, data=payload, auth=auth_header)
    response.raise_for_status()
    return response.json()["access_token"]

class SpotifyNowPlayingApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("360x270")
        self.access_token = refresh_access_token()
        self.token_expires_at = time.time() + 3600  # 1 hour from now

        self.track_label = tk.Label(root, text="Loading...", font=("Arial", 14))
        self.track_label.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.photo_image = None  # to keep a reference

        self.update_now_playing()

    def update_now_playing(self):
        # Refresh token if close to expiry
        if time.time() >= self.token_expires_at - 60:
            self.access_token = refresh_access_token()
            self.token_expires_at = time.time() + 3600

        url = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            if data and "item" in data and data["item"]:
                track_name = data["item"]["name"]
                images = data["item"]["album"]["images"]
                if images:
                    image_url = images[0]["url"]  # typically largest image
                    # Download image
                    img_resp = requests.get(image_url)
                    img_data = img_resp.content
                    img = Image.open(BytesIO(img_data))
                    img = img.resize((300, 300))  # resize to fit window
                    img = img.convert("L")

                    self.photo_image = ImageTk.PhotoImage(img)
                    self.image_label.config(image=self.photo_image)
                    self.image_label.place(x=200, y=70)

                self.track_label.config(text=f"{track_name}")
            else:
                self.track_label.config(text="No track currently playing.")
                self.image_label.config(image='')
                self.photo_image = None
        else:
            self.track_label.config(text=f"API call failed: {resp.status_code}")
            self.image_label.config(image='')
            self.photo_image = None

        # Schedule next update in 5 seconds
        self.root.after(10000, self.update_now_playing)
        

def play_video():
    ret, frame = cap.read()
    if ret:
        # Convert BGR to RGB
        #frame = cv2.resize(frame, (360, 720))  
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)
    lbl.after(30, play_video)  # about 33fps


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg="black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Assuming your video original resolution is 1920x1080 (adjust if different)
    video_original_width = 1920
    video_original_height = 1080
    video_aspect_ratio = video_original_width / video_original_height

    # Calculate max video size to fit screen with aspect ratio preserved
    if screen_width / screen_height > video_aspect_ratio:
        video_height = screen_height
        video_width = int(screen_height * video_aspect_ratio)
    else:
        video_width = screen_width
        video_height = int(screen_width / video_aspect_ratio)

    # Center position
    x_pos = (screen_width - video_width) // 2
    y_pos = (screen_height - video_height) // 2

    # Video label fills the calculated video size and placed centered
    lbl = tk.Label(root, bg="black")
    lbl.place(x=x_pos, y=y_pos, width=video_width, height=video_height)
    lbl.lower()  # send video label to back

    cap = cv2.VideoCapture('videobackground/lines.mp4')

    # Spotify UI on top
    app = SpotifyNowPlayingApp(root)

    # Optional: Bind Escape key to exit fullscreen and close app
    def exit_app(event=None):
        root.attributes('-fullscreen', False)
        root.destroy()

    root.bind("<Escape>", exit_app)

    play_video()
    root.mainloop()