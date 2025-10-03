import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import cv2
from crop_tool import CropTool
from PIL import Image, ImageTk

class CropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.set_window_size(500, 400)

        self.image = None
        self.folder = ""
        self.base_name = "crop"

        # File picker
        tk.Button(root, text="Select Image", command=self.load_image).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(root, text="Select Save Folder", command=self.pick_folder).grid(row=0, column=1, padx=5, pady=5)

        # Base name
        tk.Label(root, text="Base Filename:").grid(row=1, column=0, sticky="e")
        self.name_entry = tk.Entry(root)
        self.name_entry.insert(0, "crop")
        self.name_entry.grid(row=1, column=1)

        # Resize sliders
        tk.Label(root, text="Resize Width:").grid(row=2, column=0, sticky="e")
        self.width_slider = tk.Scale(root, from_=0, to=2000, orient="horizontal")
        self.width_slider.grid(row=2, column=1)

        tk.Label(root, text="Resize Height:").grid(row=3, column=0, sticky="e")
        self.height_slider = tk.Scale(root, from_=0, to=2000, orient="horizontal")
        self.height_slider.grid(row=3, column=1)

        # Mode dropdown
        tk.Label(root, text="Crop Mode:").grid(row=4, column=0, sticky="e")
        self.mode_var = tk.StringVar()
        self.mode_dropdown = ttk.Combobox(root, textvariable=self.mode_var, values=["grid", "auto", "draw"])
        self.mode_dropdown.grid(row=4, column=1)
        self.mode_dropdown.current(0)

        # Crop button
        tk.Button(root, text="Crop", command=self.run_crop).grid(row=5, column=0, columnspan=2, pady=10)

        # Status label
        self.status = tk.Label(root, text="", fg="blue", anchor="w")
        self.status.grid(row=7, column=0, columnspan=2, sticky="w", padx=5)
        self.status.config(wraplength=480)

        # Stretch columns

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Reset button
        tk.Button(root, text="Reset", command=self.reset_fields).grid(row=6, column=0, columnspan=2, pady=5)
                        
    def set_window_size(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(True, True)

    def load_image(self):
        path = filedialog.askopenfilename(title="Select Image")
        if path:
            self.image = cv2.imread(path)
            self.status.config(text=f"Loaded: {path}")

    def pick_folder(self):
        self.folder = filedialog.askdirectory(title="Select Save Folder")
        self.status.config(text=f"Save to: {self.folder}")

    def run_crop(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        if not self.folder:
            messagebox.showerror("Error", "No save folder selected.")
            return

        width = self.width_slider.get()
        height = self.height_slider.get()
        if width > 0 and height > 0:
            self.image = cv2.resize(self.image, (width, height))

        self.base_name = self.name_entry.get() or "crop"
        tool = CropTool(self.image, self.folder, self.base_name)
        mode = self.mode_var.get()

        if mode == "grid":
            rows = 2
            cols = 2
            tool.crop_grid(rows, cols)
        elif mode == "auto":
            tool.crop_auto()
        elif mode == "draw":
            tool.crop_draw()

        self.status.config(text=f"✅ Cropping complete. Saved {tool.count - 1} images.")
        self.reset_fields()

    def reset_fields(self):
        self.image = None
        self.folder = ""
        self.base_name = "crop"
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, "crop")
        self.width_slider.set(0)
        self.height_slider.set(0)
        self.mode_dropdown.current(0)
        self.status.config(text="🔄 Cropping complete. You can start a new session or close the app.")


def show_splash(on_close):
    splash_root = tk.Tk()
    splash_root.withdraw()

    splash = tk.Toplevel(splash_root)
    splash.overrideredirect(True)
    splash.geometry("300x200+500+300")
    splash.configure(bg="white")

    try:
        img = Image.open("scissors_icon.ico")
        img = img.resize((64, 64))
        photo = ImageTk.PhotoImage(img)
        icon_label = tk.Label(splash, image=photo, bg="white")
        icon_label.image = photo
        icon_label.pack(pady=10)
    except Exception:
        icon_label = tk.Label(splash, text="✂️", font=("Helvetica", 32), bg="white")
        icon_label.pack(pady=10)

    text_label = tk.Label(splash, text="AutoCrop is loading…", font=("Helvetica", 14), bg="white")
    text_label.pack()

    splash.after(2000, lambda: (splash.destroy(), splash_root.destroy(), on_close()))
    splash.mainloop()

def launch_gui():
    root = tk.Tk()
    app = CropApp(root)
    root.mainloop()

if __name__ == "__main__":
    show_splash(launch_gui)

