import os, requests, time, threading
from io import BytesIO
from PIL import ImageTk, Image
from dotenv import load_dotenv
import tkinter as tk
import state

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
    def __init__(self, spotify_frame):
        self.spotify_frame = spotify_frame
        self.access_token = refresh_access_token()
        self.token_expires_at = time.time() + 3600

        self.track_label = tk.Label(spotify_frame, text="Loading...", font=("alarm clock", 20), fg="white", bg="black")
        self.track_label.place(x=0, y=10)

        self.image_label = tk.Label(spotify_frame)
        self.image_label.pack()

        self.photo_image = None
        self.image_url = None
        self.x_pos = self.spotify_frame.winfo_width()  # scroll start

        self.schedule_spotify_update()
        self.scroll_text()

    def schedule_spotify_update(self):
        threading.Thread(target=self.update_now_playing, daemon=True).start()
        self.spotify_frame.after(5000, self.schedule_spotify_update)

    def update_now_playing(self):
        if time.time() >= self.token_expires_at - 60:
            self.access_token = refresh_access_token()
            self.token_expires_at = time.time() + 3600

        url = "https://api.spotify.com/v1/me/player/currently-playing?fields=item(name,album(images(url)))"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                is_playing = data.get("is_playing", False)
                if data and "item" in data and data["item"]:
                    if not is_playing:
                        state.channel = "calendar"
                        state.hasChanged = True
                    elif state.channel != "spotify":
                        state.channel = "spotify"
                        state.hasChanged = True

                    track_name = data["item"]["name"]
                    artist_name = data["item"]["artists"][0]["name"]
                    images = data["item"]["album"]["images"]

                    if images and self.image_url != images[0]["url"]:
                        self.image_url = images[0]["url"]
                        img_resp = requests.get(self.image_url, timeout=5)
                        img = Image.open(BytesIO(img_resp.content))
                        img = img.resize((300, 300)).convert("L")
                        photo = ImageTk.PhotoImage(img)
                        self.spotify_frame.after(0, lambda: self._update_ui(f"{track_name} - {artist_name}", photo))
                    else:
                        self.spotify_frame.after(0, lambda: self.track_label.config(text=f"{track_name} - {artist_name}"))
                else:
                    self.spotify_frame.after(0, self._clear_ui)
            else:
                self.spotify_frame.after(0, lambda: self.track_label.config(text=f"API call failed: {resp.status_code}"))
                state.channel = "calendar"
        except requests.RequestException:
            self.spotify_frame.after(0, lambda: self.track_label.config(text="Network error"))
            state.channel = "calendar"

    def _update_ui(self, track_name, photo):
        self.track_label.config(text=track_name)
        self.photo_image = photo
        self.image_label.config(image=self.photo_image)
        self.image_label.place(x=185, y=90)

    def _clear_ui(self):
        self.track_label.config(text="No track currently playing.")
        self.image_label.config(image='')
        self.photo_image = None

    def scroll_text(self):
        self.x_pos -= 2
        self.track_label.place(x=self.x_pos, y=10)
        if self.x_pos < -self.track_label.winfo_width():
            self.x_pos = self.spotify_frame.winfo_width()
        self.spotify_frame.after(30, self.scroll_text)
