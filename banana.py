import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

root = tk.Tk()
root.title("Banana Detector")

cap = cv2.VideoCapture(0)

label = tk.Label(root)
label.pack()

text_label = tk.Label(root, text="", font=("Arial", 20))
text_label.place(x=10, y=10)

def update_frame():
    ret, frame = cap.read()
    if not ret:
        root.after(20, update_frame)
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    yellow_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]

    if yellow_pixels > total_pixels * 0.01: 
        banana_detected = True
    else:
        banana_detected = False

    if banana_detected:
        text_label.config(text="Banana", fg="green")
    else:
        text_label.config(text="No Banana", fg="red")

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    display_frame = cv2.addWeighted(frame, 1, mask_rgb, 0.5, 0)

    img = Image.fromarray(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    label.after(20, update_frame)

update_frame()
root.mainloop()
