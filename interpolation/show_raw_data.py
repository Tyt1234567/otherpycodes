import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

df = pd.read_csv('2023-05-15 16-00-48.csv',encoding='ISO-8859-1')
data_lst = df.values.tolist()

def show_raw_data(lon, lat, ele):
    longitudes = lon
    latitudes = lat
    elevations = ele


    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(longitudes, latitudes, elevations, c=elevations, cmap='viridis', s=50, alpha=0.7, edgecolors='w')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Elevation')

    # 设置经纬度轴刻度格式为普通浮点数格式
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # 添加颜色条
    cbar = plt.colorbar(sc)
    cbar.set_label('Elevation')

    # 设置图标题
    ax.set_title('primitive_data')
    # 显示图形
    plt.show()

