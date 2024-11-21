import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import geopandas as gpd
from shapely.geometry import Point

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


datas = del_outliers(data_lst)
longitudes = []
latitudes = []
elevations = []
for data in datas:
    latitudes.append(data[1])
    longitudes.append(data[2])
    elevations.append(data[3])


# IDW 插值
def idw_interpolation(x, y, values, xi, yi, p=2):
    tree = cKDTree(np.c_[x, y])
    distances, indices = tree.query(np.c_[xi, yi], k=len(x))
    interpolated_values = np.zeros_like(xi)
    for i, (dist, idx) in enumerate(zip(distances, indices)):

        dist = np.where(dist == 0, 1e-10, dist)  #防止除零错误,将零距离改为一个非常小的值
        weights = 1 / (dist ** p)
        interpolated_values[i] = np.sum(weights * np.array(values)[idx]) / np.sum(weights)

    return interpolated_values

shapefile = 'arcgis_element/studyarea.shp'
gdf = gpd.read_file(shapefile)

boundary = gdf.geometry.union_all()
minx, miny, maxx, maxy = boundary.bounds


# 网格插值
xi, yi = np.meshgrid(np.linspace(minx,maxx, 100),
                     np.linspace(miny,maxy, 100))

zi = idw_interpolation(longitudes, latitudes, elevations, xi.flatten(), yi.flatten(), p=2)
zi = zi.reshape(xi.shape)


#删除多余区域



fig = plt.figure(figsize=(14, 7))
# 原始数据 3D 散点图
ax1 = fig.add_subplot(121, projection='3d')
sc = ax1.scatter(longitudes, latitudes, elevations, c=elevations, cmap='viridis', s=50, alpha=0.7, edgecolors='w')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.set_zlabel('Elevation')
cbar = plt.colorbar(sc, ax=ax1)
cbar.set_label('Elevation')
ax1.set_title('Original Data')

# 插值结果 3D 表面图
ax2 = fig.add_subplot(122, projection='3d')
surf = ax2.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none', alpha=0.7)
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
ax2.set_zlabel('Elevation')
cbar2 = plt.colorbar(surf, ax=ax2)
cbar2.set_label('Elevation')
ax2.set_title('IDW Interpolation')

plt.show()