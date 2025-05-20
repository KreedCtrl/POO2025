import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk
import os

class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Redactor Grafic")


        self.pen_color = "black"
        self.bg_color = "white"
        self.tool = "pencil"

        self.setup_ui()
        self.setup_canvas()

        self.image = Image.new("RGB", (800, 600), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        self.start_x = None
        self.start_y = None
        self.points = [] 

    def setup_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tools = ["pencil", "line", "rect", "oval", "fill", "bezier"]
        for t in tools:
            b = tk.Button(toolbar, text=t.capitalize(), command=lambda tool=t: self.select_tool(tool))
            b.pack(side=tk.LEFT)

        color_btn = tk.Button(toolbar, text="Culoare", command=self.choose_color)
        color_btn.pack(side=tk.LEFT)

        bg_btn = tk.Button(toolbar, text="Fundal", command=self.choose_bg_color)
        bg_btn.pack(side=tk.LEFT)

        save_btn = tk.Button(toolbar, text="Salvează", command=self.save_image)
        save_btn.pack(side=tk.LEFT)

        open_btn = tk.Button(toolbar, text="Deschide", command=self.open_image)
        open_btn.pack(side=tk.LEFT)

        clear_btn = tk.Button(toolbar, text="Nou", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, width=800, height=600)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def select_tool(self, tool):
        self.tool = tool
        self.points.clear()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.clear_canvas()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def save_image(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.image.save(path)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.bmp")])
        if path:
            self.image = Image.open(path).convert("RGB")
            self.draw = ImageDraw.Draw(self.image)
            self.tk_img = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.tool == "fill":
            self.flood_fill(event.x, event.y)
        elif self.tool == "bezier":
            self.points.append((event.x, event.y))
            if len(self.points) == 4:
                self.draw_bezier_curve()
                self.points.clear()

    def on_drag(self, event):
        if self.tool == "pencil":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color)
            self.draw.line([self.start_x, self.start_y, event.x, event.y], fill=self.pen_color)
            self.start_x, self.start_y = event.x, event.y

    def on_release(self, event):
        if self.tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.pen_color)
            self.draw.line([self.start_x, self.start_y, event.x, event.y], fill=self.pen_color)
        elif self.tool == "rect":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color)
            self.draw.rectangle([self.start_x, self.start_y, event.x, event.y], outline=self.pen_color)
        elif self.tool == "oval":
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color)
            self.draw.ellipse([self.start_x, self.start_y, event.x, event.y], outline=self.pen_color)

    def flood_fill(self, x, y):
        target_color = self.image.getpixel((x, y))
        replacement_color = self.hex_to_rgb(self.pen_color)
        if target_color == replacement_color:
            return

        stack = [(x, y)]
        while stack:
            px, py = stack.pop()
            if 0 <= px < self.image.width and 0 <= py < self.image.height:
                if self.image.getpixel((px, py)) == target_color:
                    self.image.putpixel((px, py), replacement_color)
                    stack.extend([(px+1, py), (px-1, py), (px, py+1), (px, py-1)])

    def hex_to_rgb(self, hex_color):
        if not hex_color or not hex_color.startswith("#") or len(hex_color) != 7:
            return (0, 0, 0) 
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


    def draw_bezier_curve(self):
        p0, p1, p2, p3 = self.points
        previous = p0
        for t in range(1, 101):
            t /= 100
            x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
            self.canvas.create_line(previous[0], previous[1], x, y, fill=self.pen_color)
            self.draw.line([previous, (x, y)], fill=self.pen_color)
            previous = (x, y)


if __name__ == '__main__':
    root = tk.Tk()
    app = GraphicEditor(root)
    root.mainloop()
