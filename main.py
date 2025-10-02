import cv2
import os
from tkinter import Tk, filedialog, simpledialog
from crop_tool import CropTool

def pick_image():
    Tk().withdraw()
    path = filedialog.askopenfilename(title="Select Image")
    if not path:
        print("⚠️ No image selected.")
        return None
    img = cv2.imread(path)
    if img is None:
        print("❌ Failed to load image.")
        return None
    return img

def get_resize_dims():
    choice = simpledialog.askstring("Resize?", "Resize image? (y/n):")
    if not choice or choice.lower() != "y":
        return None, None
    w = simpledialog.askinteger("Width", "Enter new width:")
    h = simpledialog.askinteger("Height", "Enter new height:")
    return w, h

def get_save_info():
    folder = filedialog.askdirectory(title="Choose Save Folder")
    if not folder:
        folder = os.path.join(os.getcwd(), "temp_crop")
        print(f"⚠️ No folder selected. Using fallback: {folder}")
    name = simpledialog.askstring("Base Name", "Enter base filename:")
    if not name:
        name = "crop"
        print("⚠️ No filename entered. Using default name: 'crop'")
    return folder, name

def main():
    img = pick_image()
    if img is None:
        return

    w, h = get_resize_dims()
    if w and h:
        img = cv2.resize(img, (w, h))
        print(f"📐 Resized to {w}×{h}")

    folder, base_name = get_save_info()
    tool = CropTool(img, folder, base_name)

    mode = simpledialog.askstring("Mode", "Choose mode: grid / auto / draw")
    if not mode:
        print("⚠️ No mode selected.")
        return

    mode = mode.lower()
    if mode == "grid":
        rows = simpledialog.askinteger("Rows", "Enter number of rows:")
        cols = simpledialog.askinteger("Columns", "Enter number of columns:")
        if rows and cols:
            tool.crop_grid(rows, cols)
        else:
            print("⚠️ Invalid grid size.")
    elif mode == "auto":
        tool.crop_auto()
    elif mode == "draw":
        tool.crop_draw()
    else:
        print("⚠️ Invalid mode. Choose 'grid', 'auto', or 'draw'.")

if __name__ == "__main__":
    main()