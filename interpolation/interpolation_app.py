import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from show_raw_data import show_raw_data
from del_outliers import del_outliers
from PIDW_interpolation import show_results
import numpy as np
from clip import ShapefileCutterApp
from save_to_html import save_interpolation_as_html
from PIL import Image, ImageTk
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import io

class Interpolation_App:
    def __init__(self, root):
        self.root = root
        self.root.title("河流地形插值软件")
        self.root.geometry("1000x800")

        self.add_data_button = tk.Button(self.root, text="选择CSV文件", command=self.select_csv_file)
        self.add_data_button.place(x=50, y=50, width=100, height=30)

        self.raw_data = None
        self.boundary_data = None
        self.longitudes = None
        self.latitudes = None
        self.elevations = None
        self.sonars = None


        self.file_path_label = tk.Label(self.root, text="", font=("Arial", 10), fg="blue")
        self.file_path_label.place(x=200, y=50, width=700, height=30)  # 右侧显示路径

        lon_label = tk.Label(self.root, text="纬度列号（填数字）", font=("Arial", 10))
        lon_label.place(x=50, y=100, width=150, height=30)
        self.lon_col_button = tk.Entry(self.root)
        self.lon_col_button.place(x=250, y=100, width=50, height=30)

        lat_label = tk.Label(self.root, text="经度列号（填数字）", font=("Arial", 10))
        lat_label.place(x=50, y=150, width=150, height=30)
        self.lat_col_button = tk.Entry(self.root)
        self.lat_col_button.place(x=250, y=150, width=50, height=30)

        ele_label = tk.Label(self.root, text="河底高程列号（填数字）", font=("Arial", 10))
        ele_label.place(x=50, y=200, width=150, height=30)
        self.ele_col_button = tk.Entry(self.root)
        self.ele_col_button.place(x=250, y=200, width=50, height=30)

        sonar_label = tk.Label(self.root, text="声呐高程列号（填数字，没有不填）", font=("Arial", 10))
        sonar_label.place(x=50, y=250, width=200, height=30)
        self.sonar_col_button = tk.Entry(self.root)
        self.sonar_col_button.place(x=250, y=250, width=50, height=30)

        self.upload_button = tk.Button(self.root, text='上传', font=("Arial", 10), command=self.process_csv_data)
        self.upload_button.place(x=350, y=175, width=50, height=30)

        self.upload_status_label = tk.Label(self.root, text="", font=("Arial", 10), fg="green")
        self.upload_status_label.place(x=450, y=175, width=200, height=30)  # 右侧显示上传成功消息

        self.show_raw_data_button = tk.Button(self.root, text='显示原始数据', command=self.show_raw_data)
        self.show_raw_data_button.place(x=50, y=300, width=100, height=30)

        self.polygon_name = tk.Entry(self.root)
        self.polygon_name.place(x=50, y=350, width=100, height=30)
        self.polygon_name.insert(0, '在此输入边界名称')

        self.draw_polygon_button = tk.Button(self.root, text='绘制插值边界', command=self.draw_polygon)
        self.draw_polygon_button.place(x=200, y=350, width=100, height=30)

        self.upload_shp_file_button = tk.Button(self.root, text='选择边界shp文件', command=self.upload_shp_file)
        self.upload_shp_file_button.place(x=350, y=350, width=100, height=30)

        self.show_interpolation_button = tk.Button(self.root, text='显示插值结果', command=self.show_interpolation_result)
        self.show_interpolation_button.place(x=50, y=400, width=100, height=30)

        self.save_button = tk.Button(self.root, text='保存为html动图', command=self.save_to_html)
        self.save_button.place(x=50, y=450, width=100, height=30)

    def select_csv_file(self):
        file_path = filedialog.askopenfilename(
            title="选择CSV文件",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                # 读取CSV文件内容
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    df = pd.read_csv(rf"{file_path}", encoding='ISO-8859-1')
                    self.raw_data = df.values.tolist()
                    # 返回CSV内容，可以在这里进行进一步处理
                    self.file_path_label.config(text=file_path)
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件: {e}")
                return None

    def process_csv_data(self):
        try:
            lon_col = int(self.lon_col_button.get()) - 1
            lat_col = int(self.lat_col_button.get()) - 1
            ele_col = int(self.ele_col_button.get()) - 1
            longitudes = []
            latitudes = []
            elevations = []
            sonars = None

            for data in self.raw_data:
                latitudes.append(data[lat_col])
                longitudes.append(data[lon_col])
                elevations.append(data[ele_col])

            if self.sonar_col_button.get().strip() != '':
                sonar_col = int(self.sonar_col_button.get()) - 1
                #删除异常值
                self.raw_data = del_outliers(self.raw_data,ele_col, sonar_col)
                sonars = []
                for data in self.raw_data:
                    sonars.append(data[sonar_col])

            self.longitudes = longitudes
            self.latitudes = latitudes
            self.elevations = elevations
            self.sonars = sonars

            # 更新上传状态显示
            self.upload_status_label.config(text="上传成功")

        except Exception as e:
            messagebox.showerror('错误', f'请检查文件及列号: {e}')
            self.upload_status_label.config(text="上传失败")

    def show_raw_data(self):
        if self.longitudes and self.latitudes and self.elevations:
            show_raw_data(self.longitudes, self.latitudes, self.elevations)
        else:
            messagebox.showwarning("警告", "请先上传并处理CSV文件")

    def draw_polygon(self):
        if self.polygon_name.get().strip() != '在此输入边界名称':
            coordinates=[]
            for i in range(len(self.longitudes)):
                coordinates.append((self.longitudes[i],self.latitudes[i]))

            root2 =  tk.Toplevel(self.root)
            ShapefileCutterApp(root2,coordinates,self.polygon_name.get())

    def upload_shp_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            filetypes=[("Shapefiles", "*.shp")],
            title="选择 Shapefile 文件"
        )

        if file_path:
            # 读取 Shapefile 文件
            try:
                gdf = gpd.read_file(file_path)
                polygon = gdf.geometry.union_all()
                self.boundary_data = polygon
                # 你可以在这里处理 Shapefile 文件，例如显示在地图上
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件: {e}")

    def show_interpolation_result(self):
        show_results(self.longitudes,self.latitudes, self.elevations,0.711*np.pi,10,12,2,self.boundary_data)

    def save_to_html(self):
        save_interpolation_as_html(self.longitudes,self.latitudes, self.elevations,0.711*np.pi,10,12,2,self.boundary_data,'1.html')



# 创建Tkinter窗口
root = tk.Tk()
app = Interpolation_App(root)
root.mainloop()