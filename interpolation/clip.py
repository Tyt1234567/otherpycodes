import tkinter as tk
from tkintermapview import TkinterMapView
import geopandas as gpd
from shapely.geometry import Polygon


class ShapefileCutterApp:
    def __init__(self,root,points,name):
        self.root = root
        self.points = points
        self.name = name
        self.root.title("Shapefile Cutter")
        self.path_line = None

        # 创建 TkinterMapView 组件
        self.map_view = TkinterMapView(self.root, width=800, height=600, corner_radius=0)
        self.map_view.pack(fill="both", expand=True)

        # 设置地图中心点和缩放级别
        self.map_view.set_position(self.points[0][1], self.points[0][0])  # 你可以根据需要调整中心点
        self.map_view.set_zoom(10)  # 你可以根据需要调整缩放级别

        # 设置卫星影像服务的 tile 服务器 URL
        self.map_view.set_tile_server(
            "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}")

        # 显示提供的坐标点
        self.display_points(self.points)

        # 列表来存储用户点击的点
        self.points = []

        # 绑定鼠标点击事件
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<Double-1>", self.on_double_click)

        # 按钮来完成点选
        self.finish_button = tk.Button(self.root, text="完成选择", command=self.finish_selection)
        self.finish_button.pack()

    def display_points(self, points):
        for idx, (lon, lat) in enumerate(points):
            self.map_view.set_marker(lat, lon)

    def on_click(self, event):
        lat, lon = self.map_view.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        self.points.append((lat, lon))

        # 显示点击点
        self.map_view.set_marker(lat, lon, text=f"点 {len(self.points)}")

        # 如果有两个以上点，绘制多边形
        # 如果已有多个点，连成多边形
        if len(self.points) > 2:
            if self.path_line:
                self.map_view.delete(self.path_line)

                # 绘制新的路径
            self.path_line = self.map_view.set_path(self.points, width=1)

    def on_double_click(self, event):
        lat, lon = self.map_view.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        self.points.append((lat, lon))

        # 显示点击点
        self.map_view.set_marker(lat, lon, text=f"点 {len(self.points)}")
        if len(self.points) > 2:
            # 双击时，将第一个点和最后一个点连接，形成封闭多边形
            self.points.append(self.points[0])

            # 删除旧的路径
            if self.path_line:
                self.map_view.delete(self.path_line)
            # 绘制封闭的多边形路径
            self.path_line = self.map_view.set_path(self.points, width=1)
    def finish_selection(self):
        # 将点击的点转换为多边形
        polygon = Polygon(self.points)

        # 保存多边形为 .shp 文件
        gdf = gpd.GeoDataFrame({'geometry': [polygon]}, crs="EPSG:4326")
        gdf.to_file(f"shp_files/{self.name}.shp")


if __name__ == "__main__":

    app = ShapefileCutterApp([(120.0750046,33.4890505),(120.0750044, 33.4890505), (120.0750041, 33.4890505), (120.0750038, 33.4890505)],'try')

