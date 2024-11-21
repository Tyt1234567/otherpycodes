import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from shapely.geometry import Point, Polygon
from matplotlib.path import Path
from mpl_toolkits.mplot3d import Axes3D

# 读取数据
df = pd.read_csv('2023-05-15 16-00-48.csv', encoding='ISO-8859-1')
data_lst = df.values.tolist()

# 删除异常值
def del_outliers(data):
    surface_elevation = [i[3] + i[4] for i in data]
    sorted_surface_elevation_data = sorted(surface_elevation)
    Q1 = sorted_surface_elevation_data[len(data) // 4]
    Q3 = sorted_surface_elevation_data[(len(data) * 3) // 4]
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_data = [i for i in data if lower_bound <= i[3] + i[4] <= upper_bound]
    return filtered_data

def idw_interpolation(x, y, values, xi, yi, p=2):
    tree = cKDTree(np.c_[x, y])
    distances, indices = tree.query(np.c_[xi, yi], k=len(x))
    interpolated_values = np.zeros_like(xi)
    for i, (dist, idx) in enumerate(zip(distances, indices)):

        dist = np.where(dist == 0, 1e-10, dist)  # 防止除零错误,将零距离改为一个非常小的值
        weights = 1 / (dist ** p)
        interpolated_values[i] = np.sum(weights * np.array(values)[idx]) / np.sum(weights)

    return interpolated_values

def find_elevation(x_coords, y_coords, xi, yi, zi):

    x_coords, y_coords = np.array(x_coords), np.array(y_coords)
    # 将插值网格坐标也转换为 NumPy 数组
    xi_flat = xi.flatten()
    yi_flat = yi.flatten()
    # 创建KDTree用于快速查询
    tree = cKDTree(np.c_[xi_flat, yi_flat])
    # 查询最近的插值点
    distances, indices = tree.query(np.c_[x_coords, y_coords], k=1)
    # 从插值结果中提取高程
    elevations = zi.flatten()[indices.flatten()]
    return elevations

datas = del_outliers(data_lst)
longitudes = []
latitudes = []
elevations = []
for data in datas:
    latitudes.append(data[1])
    longitudes.append(data[2])
    elevations.append(data[3])

# IDW 插值
shapefile = 'arcgis_element/studyarea.shp'
gdf = gpd.read_file(shapefile)

boundary = gdf.geometry.union_all()
minx, miny, maxx, maxy = boundary.bounds

# 网格插值
xi, yi = np.meshgrid(np.linspace(minx,maxx, 100),
                     np.linspace(miny,maxy, 100))

zi = idw_interpolation(longitudes, latitudes, elevations, xi.flatten(), yi.flatten(), p=2)
zi = zi.reshape(xi.shape)


estimate_elevations = find_elevation(longitudes, latitudes, xi, yi, zi)

for i in range(len(estimate_elevations)):
    print(f'longitude:{longitudes[i]},latitude:{latitudes[i]},true_elevation:{elevations[i]},estimate_elevation:{estimate_elevations[i]}')

variance = np.var(estimate_elevations-elevations)
print(variance)

