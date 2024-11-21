import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.path import Path

def custom_distance(x1, y1, x2, y2, angle, e ):
    dx = x2 - x1
    dy = y2 - y1
    term1 = (np.cos(angle) ** 2 + e * (np.sin(angle)) ** 2) * (dx ** 2)
    term2 = (np.sin(angle) ** 2 + e * (np.cos(angle)) ** 2) * (dy ** 2)
    term3 = (e - 1) * 2 * np.sin(angle) * np.cos(angle) * abs(dx) * abs(dy)

    return np.sqrt(term1 + term2 + term3)

def interpolation(x, y, values, xi, yi, angle, e, N, p):
    x = np.array(x)
    y = np.array(y)
    values = np.array(values)
    xi = np.array(xi)
    yi = np.array(yi)
    interpolated_values = np.zeros_like(xi)

    for i in range(len(xi)):
        # 计算当前查询点 (xi[i], yi[i]) 到所有点的距离
        dist = custom_distance(xi[i], yi[i], x, y, angle, e) #到所有点的距离列表

        # 找到最近的 N 个点
        nearest_indices = np.argsort(dist)[:N] #距离最近点的索引
        nearest_distances = dist[nearest_indices]
        nearest_values = values[nearest_indices]

        # 防止除零错误，将零距离改为一个非常小的值
        nearest_distances = np.where(nearest_distances == 0, 1e-10, nearest_distances)

        # 计算权重并进行 IDW 插值
        weights = 1 / (nearest_distances ** p)
        interpolated_values[i] = np.sum(weights * nearest_values) / np.sum(weights)


    return interpolated_values

def create_grid(lon,lat,ele,angle,e,N,p,polygon):
    minx, miny, maxx, maxy = polygon.bounds

    xi, yi = np.meshgrid(np.linspace(minx, maxx, 100), np.linspace(miny, maxy, 100))
    zi = interpolation(lon, lat, ele, xi.flatten(), yi.flatten(),angle, e, N,p)

    zi = zi.reshape(xi.shape)
    return xi, yi, zi

def create_mask(lon, lat, polygon):
    """
    根据 polygon 创建掩膜。
    """
    mask = np.zeros(lon.shape, dtype=bool)
    path = Path(np.array(polygon.exterior.coords))
    for i in range(lon.shape[0]):
        for j in range(lon.shape[1]):
            if path.contains_point((lon[i, j], lat[i, j])):
                mask[i, j] = True
    return mask

def show_results(lon,lat,ele,angle,e,N,p,polygon):
    xi, yi, zi = create_grid(lon, lat, ele, angle, e, N, p, polygon)
    # 创建掩膜
    mask = create_mask(xi, yi, polygon)
    elevation_clipped = np.where(mask, zi, np.nan)  # 应用掩膜到插值结果
    fig = plt.figure(figsize=(7, 7))

    ax2 = fig.add_subplot(111, projection='3d')
    surf = ax2.plot_surface(xi, yi, elevation_clipped, cmap='viridis', edgecolor='none', alpha=0.7)
    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')
    ax2.set_zlabel('Elevation')
    cbar2 = plt.colorbar(surf, ax=ax2)
    cbar2.set_label('Elevation')
    zh_font = fm.FontProperties(family='SimHei')
    ax2.set_title('插值结果', fontproperties=zh_font)

    plt.show()
