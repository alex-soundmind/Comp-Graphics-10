import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №10")

        self.create_widgets()

    def create_widgets(self):
        self.open_button = tk.Button(self.root, text="Открыть изображение", command=self.open_image)
        self.open_button.pack(pady=10)

        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if file_path:
            img = Image.open(file_path)

            # Первое изображение - оригинальное
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.image_frame, image=img_tk)
            label.image = img_tk
            label.grid(row=0, column=0, padx=5, pady=5)

            # Второе изображение - поворот на 15 градусов с интерполяцией по ближайшему соседу
            rotated_img = self.rotate_nearest_neighbor(img, 15)
            rotated_img_tk = ImageTk.PhotoImage(rotated_img)
            label = tk.Label(self.image_frame, image=rotated_img_tk)
            label.image = rotated_img_tk
            label.grid(row=0, column=1, padx=5, pady=5)

            # Третье изображение - масштабирование в 1,5 раза с билинейной интерполяцией
            scaled_img = self.bilinear_interpolation(img, 1.5)
            scaled_img_tk = ImageTk.PhotoImage(scaled_img)
            label = tk.Label(self.image_frame, image=scaled_img_tk)
            label.image = scaled_img_tk
            label.grid(row=0, column=2, padx=5, pady=5)

            # Четвертое изображение - скос на 10 градусов с бикубической интерполяцией
            skewed_img = self.bicubic_interpolation(img, 10)
            skewed_img_tk = ImageTk.PhotoImage(skewed_img)
            label = tk.Label(self.image_frame, image=skewed_img_tk)
            label.image = skewed_img_tk
            label.grid(row=0, column=3, padx=5, pady=5)

    def rotate_nearest_neighbor(self, image, angle):
        angle = -angle
        width, height = image.size
        angle_rad = np.radians(angle)
        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)

        new_width = int(abs(width * cos_theta) + abs(height * sin_theta))
        new_height = int(abs(width * sin_theta) + abs(height * cos_theta))

        rotated_img = Image.new('RGB', (new_width, new_height))

        cx = width // 2
        cy = height // 2
        ncx = new_width // 2
        ncy = new_height // 2

        for x in range(new_width):
            for y in range(new_height):
                xx = int((x - ncx) * cos_theta + (y - ncy) * sin_theta + cx)
                yy = int(-(x - ncx) * sin_theta + (y - ncy) * cos_theta + cy)

                if 0 <= xx < width and 0 <= yy < height:
                    rotated_img.putpixel((x, y), image.getpixel((xx, yy)))

        return rotated_img

    def bilinear_interpolation(self, image, scale_factor):
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        def interpolate(x, y):
            l = int(np.floor(x))
            k = int(np.floor(y))
            a = x - l
            b = y - k
            f_ll = image.getpixel((l, k)) if 0 <= l < width and 0 <= k < height else (0, 0, 0)
            f_l1 = image.getpixel((l + 1, k)) if 0 <= l + 1 < width and 0 <= k < height else (0, 0, 0)
            f_1k = image.getpixel((l, k + 1)) if 0 <= l < width and 0 <= k + 1 < height else (0, 0, 0)
            f_11 = image.getpixel((l + 1, k + 1)) if 0 <= l + 1 < width and 0 <= k + 1 < height else (0, 0, 0)
            return (
                int((1 - a) * (1 - b) * f_ll[0] + a * (1 - b) * f_l1[0] + (1 - a) * b * f_1k[0] + a * b * f_11[0]),
                int((1 - a) * (1 - b) * f_ll[1] + a * (1 - b) * f_l1[1] + (1 - a) * b * f_1k[1] + a * b * f_11[1]),
                int((1 - a) * (1 - b) * f_ll[2] + a * (1 - b) * f_l1[2] + (1 - a) * b * f_1k[2] + a * b * f_11[2])
            )

        scaled_img = Image.new('RGB', (new_width, new_height))

        for x in range(new_width):
            for y in range(new_height):
                px, py = x / scale_factor, y / scale_factor
                scaled_img.putpixel((x, y), interpolate(px, py))

        return scaled_img

    def bicubic_interpolation(self, image, angle):
        width, height = image.size
        angle_rad = np.radians(angle)
        skew_matrix = (1, np.tan(angle_rad), 0, 0, 1, 0)
        skewed_img = image.transform((width, height), Image.AFFINE, skew_matrix, resample=Image.BICUBIC)
        return skewed_img

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
