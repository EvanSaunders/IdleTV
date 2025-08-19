from PIL import Image, ImageTk
import cv2
import state

def play_video():
    ret, frame = state.cap.read()
    if not ret:
        state.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = state.cap.read()

    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)
        img = Image.fromarray(gray_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        state.lbl.imgtk = imgtk
        state.lbl.configure(image=imgtk)

    state.lbl.after(40, play_video)
