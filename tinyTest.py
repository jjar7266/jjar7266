from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
img = Image.open("scissors_icon.ico")
photo = ImageTk.PhotoImage(img)
label = tk.Label(root, image=photo)
label.image = photo
label.pack()
root.mainloop()