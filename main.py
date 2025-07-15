import subprocess

VIDEO_PATH = "/home/pi/Videos/loop.mp4"  # Change to your actual video file path

# Loop the video using omxplayer
subprocess.call([
    "omxplayer", "--loop", "--no-osd", "--aspect-mode", "fill", VIDEO_PATH
])
