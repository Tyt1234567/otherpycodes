import tkinter as tk
from tkintermapview import TkinterMapView


class ShapefileCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shapefile Cutter")

        # 创建地图视图
        self.map_view = TkinterMapView(self.root, width=800, height=600)
        self.map_view.pack(fill="both", expand=True)

        # 设置地图为卫星图
        self.map_view.set_tile_server("https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}")

        # 绑定点击事件
        self.root.bind("<Button-1>", self.on_map_click)
        print("Event binding successful.")  # Debug: 确认事件绑定

    def on_map_click(self, event):
        lat, lon = self.map_view.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        print(f"点击坐标：纬度={lat}, 经度={lon}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShapefileCutterApp(root)
    root.mainloop()