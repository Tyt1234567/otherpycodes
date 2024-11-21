import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 读取 shapefile 文件
shapefile_path = 'arcgis_element/studyarea.shp'
gdf = gpd.read_file(shapefile_path)

polygon = gdf.geometry.iloc[0]

# 提取四边形的外边界顶点坐标
coords = list(polygon.exterior.coords)
if len(coords) == 5:
    coords = coords[:-1]  # 去掉重复的首尾点

'''
print(coords)
for i,coord in enumerate(coords):
    plt.scatter(coord[0],coord[1])
    plt.text(coord[0], coord[1], str(i + 1), fontsize=12, ha='right', va='bottom')  # 添加标签
plt.show()
'''
sw_longitude = np.linspace(coords[0][0],coords[1][0],50)
sw_latitude = np.linspace(coords[0][1],coords[1][1],50)
sw_elevations = [5.6273]*len(sw_longitude)

ne_longitude = np.linspace(coords[2][0],coords[3][0],50)
ne_latitude = np.linspace(coords[2][1],coords[3][1],50)
ne_elevations = [5.6273]*len(sw_longitude)

# 创建 DataFrame
df = pd.DataFrame({
    'Longitude_SW': np.concatenate([sw_longitude, ne_longitude]),
    'Latitude_SW': np.concatenate([sw_latitude, ne_latitude]),
    'Elevation': np.concatenate([sw_elevations, ne_elevations])
})

# 保存到 CSV 文件
csv_path = 'boundary_tata.csv'
df.to_csv(csv_path, index=False)

print(f"数据已保存到 {csv_path}")