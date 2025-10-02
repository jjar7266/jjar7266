import cv2
import os

class CropTool:
    def __init__(self, image, folder, base_name):
        self.image = image
        self.folder = folder
        self.base_name = base_name
        self.count = 1
        os.makedirs(folder, exist_ok=True)

    def resize(self, width, height):
        if width > 0 and height > 0:
            self.image = cv2.resize(self.image, (width, height))
            print(f"📐 Resized to {width}×{height}")
        else:
            print("⚠️ Invalid dimensions. Skipping resize.")

    def save_crop(self, crop):
        filename = os.path.join(self.folder, f"{self.base_name}_{self.count:02}.png")
        success = cv2.imwrite(filename, crop)
        if success:
            print(f"✅ Saved: {filename}")
            self.count += 1
        else:
            print(f"❌ Failed to save: {filename}")

    def crop_grid(self, rows, cols):
        h, w, _ = self.image.shape
        cell_h, cell_w = h // rows, w // cols
        for r in range(rows):
            for c in range(cols):
                x, y = c * cell_w, r * cell_h
                crop = self.image[y:y+cell_h, x:x+cell_w]
                if crop.size > 0:
                    self.save_crop(crop)
        print(f"🎉 Grid crop complete. Saved {self.count - 1} images.")

    def crop_auto(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = sorted([cv2.boundingRect(c) for c in contours], key=lambda b: (b[1], b[0]))
        for x, y, w, h in boxes:
            crop = self.image[y:y+h, x:x+w]
            if crop.size > 0:
                self.save_crop(crop)
        print(f"🎉 Auto-detect complete. Saved {self.count - 1} images.")

    def crop_draw(self):
        clone = self.image.copy()
        img = clone.copy()
        drawing = False
        ix, iy = -1, -1
        rect = None

        def draw(event, x, y, flags, param):
            nonlocal ix, iy, drawing, rect
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix, iy = x, y
            elif event == cv2.EVENT_MOUSEMOVE and drawing:
                img[:] = clone.copy()
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                rect = (min(ix, x), min(iy, y), abs(x - ix), abs(y - iy))
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
                cv2.putText(img, "Press Enter to save", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.namedWindow("Draw Crop Area")
        cv2.setMouseCallback("Draw Crop Area", draw)

        print("🖱️ Draw rectangles. Release mouse, then press Enter to save. Esc or Q to quit.")

        while True:
            cv2.imshow("Draw Crop Area", img)
            key = cv2.waitKey(1) & 0xFF

            if key == 13 and rect:  # Enter
                x, y, w, h = rect
                crop = clone[y:y+h, x:x+w]
                if crop.size > 0:
                    self.save_crop(crop)
                else:
                    print("⚠️ Selected area is empty. Skipping save.")
                rect = None
                img = clone.copy()

            elif key == 27 or key == ord('q'):
                break

        cv2.destroyAllWindows()
        print(f"🎉 Draw mode complete. Saved {self.count - 1} images.")