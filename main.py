import subprocess,os, random,time, sys

# Replace "yourvideo.mp4" with your actual video file path
playedRequestedVideo = False

def countdown_timer(seconds, playedRequestedVideo):
    if len(sys.argv) > 1  and not playedRequestedVideo:
        video_selection =sys.argv[1]
        playedRequestedVideo = True
    else:
        video_selection = random.choice(os.listdir("videogameintros/"))
    process = subprocess.Popen([
    "cvlc",
    "--fullscreen",
    "--no-video-deco",
    "--no-embedded-video",
    "--video-on-top",
    "--width=640",
    "--height=360",
    "--loop",
    "--aspect-ratio=4:3",     # matches RCA output aspect ratio
     "--aout=alsa",
    "--autoscale",            # allow scaling
    "--no-video-title-show",
    f"videogameintros/{video_selection}"
    ])
    while seconds > 0:
        time.sleep(1)  # Pause execution for 1 second
        seconds -= 1
    print("Time's up!")
    process.terminate()

subprocess.call(["sudo", "pkill", "-f", "vlc"])
while(True):
    countdown_timer(3600, playedRequestedVideo) 
