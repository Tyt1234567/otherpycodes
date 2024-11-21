import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from scipy.spatial import cKDTree
import random
from pyproj import Transformer

class PIDW:
    def __init__(self,ellipic_e,ellipic_angle,N,p):
        self.ellipic_e = ellipic_e
        self.ellipic_angle = ellipic_angle
        self.N = N
        self.p = p
        self.longitudes,self.latitudes,self.elevations = self.read_data()

        #随机挑选90％为训练集
        indexs = [i for i in range(len(self.longitudes))]
        random.shuffle(indexs)
        test_index = indexs[len(indexs)//10*8:]
        train_index = indexs[:len(indexs)//10*8]
        self.test_lon = [self.longitudes[i] for i in test_index]
        self.test_lat = [self.latitudes[i] for i in test_index]
        self.test_ele = [self.elevations[i] for i in test_index]

        self.train_lon = [self.longitudes[i] for i in train_index]
        self.train_lat = [self.latitudes[i] for i in train_index]
        self.train_ele = [self.elevations[i] for i in train_index]
        self.xi,self.yi,self.zi,self.polygon = self.create_grid()




    def del_outliers(self,data):
        surface_elevation = [i[3] + i[4] for i in data]
        sorted_surface_elevation_data = sorted(surface_elevation)
        Q1 = sorted_surface_elevation_data[len(data) // 4]
        Q3 = sorted_surface_elevation_data[(len(data) * 3) // 4]
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        filtered_data = [i for i in data if lower_bound <= i[3] + i[4] <= upper_bound]
        return filtered_data

    def read_data(self):
        # 读取数据
        df = pd.read_csv('2023-05-15 16-00-48.csv', encoding='ISO-8859-1')
        data_lst = df.values.tolist()
        datas = self.del_outliers(data_lst)

        df_boundary = pd.read_csv('boundry_data.csv', encoding='ISO-8859-1')
        boundary_data_lst = df_boundary.values.tolist()

        longitudes = []
        latitudes = []
        elevations = []
        for data in datas:
            latitudes.append(data[1])
            longitudes.append(data[2])
            elevations.append(data[3])

        for data in boundary_data_lst:
            latitudes.append(data[1])
            longitudes.append(data[0])
            elevations.append(data[2])

        return latitudes,longitudes,elevations

    def custom_distance(self, x1, y1, x2, y2):

        dx = x2 - x1
        dy = y2 - y1
        term1 = (np.cos(self.ellipic_angle) ** 2 + self.ellipic_e * (np.sin(self.ellipic_angle)) ** 2) * (dx ** 2)
        term2 = (np.sin(self.ellipic_angle) ** 2 + self.ellipic_e * (np.cos(self.ellipic_angle)) ** 2) * (dy ** 2)
        term3 = (self.ellipic_e - 1) * 2 * np.sin(self.ellipic_angle) * np.cos(self.ellipic_angle) * abs(dx) * abs(dy)

        return np.sqrt(term1 + term2 + term3)


    def interpolation(self,x, y, values, xi, yi):
        x = np.array(x)
        y = np.array(y)
        values = np.array(values)
        xi = np.array(xi)
        yi = np.array(yi)

        interpolated_values = np.zeros_like(xi)

        for i in range(len(xi)):
            # 计算当前查询点 (xi[i], yi[i]) 到所有点的距离
            dist = self.custom_distance(xi[i], yi[i], x, y) #到所有点的距离列表

            # 找到最近的 N 个点
            nearest_indices = np.argsort(dist)[:self.N] #距离最近点的索引
            nearest_distances = dist[nearest_indices]
            nearest_values = values[nearest_indices]

            # 防止除零错误，将零距离改为一个非常小的值
            nearest_distances = np.where(nearest_distances == 0, 1e-10, nearest_distances)

            # 计算权重并进行 IDW 插值
            weights = 1 / (nearest_distances ** self.p)
            interpolated_values[i] = np.sum(weights * nearest_values) / np.sum(weights)


        return interpolated_values


    def create_grid(self):
        shapefile = 'arcgis_element/studyarea.shp'
        gdf = gpd.read_file(shapefile)
        polygon = gdf.geometry.union_all()
        minx, miny, maxx, maxy = polygon.bounds


        # 网格插值
        xi, yi = np.meshgrid(np.linspace(minx, maxx, 100), np.linspace(miny, maxy, 100))
        zi = self.interpolation(self.train_lon, self.train_lat, self.train_ele, yi.flatten(), xi.flatten())


        zi = zi.reshape(xi.shape)
        return xi,yi,zi,polygon

    # 创建掩膜函数
    def create_mask(self,lon, lat, polygon):
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

    def find_elevation(self,x_coords, y_coords):

        x_coords, y_coords = np.array(x_coords), np.array(y_coords)
        # 将插值网格坐标也转换为 NumPy 数组
        xi_flat = self.xi.flatten()
        yi_flat = self.yi.flatten()
        # 创建KDTree用于快速查询
        tree = cKDTree(np.c_[xi_flat, yi_flat])
        # 查询最近的插值点
        distances, indices = tree.query(np.c_[x_coords, y_coords], k=1)
        # 从插值结果中提取高程
        elevations = self.zi.flatten()[indices.flatten()]
        return elevations

    def calculate_D(self):
        estimate_elevations = self.find_elevation(self.test_lat,self.test_lon)
        variance = np.var(estimate_elevations - self.test_ele)
        return variance

    def calculate_hessian_eigenvalue(self):
        #将xi，yi转为米为单位，与zi统一
        # 创建一个 Transformer 对象
        transformer = Transformer.from_crs("epsg:4326", "epsg:32651", always_xy=True)  # 根据需要调整坐标系
        # 将 numpy 数组直接传入以进行批量转换
        xi, yi = transformer.transform(self.xi, self.yi)

        # 计算梯度
        dz_dx, dz_dy = np.gradient(self.zi, xi[0, :], yi[:, 0])

        # 计算二阶偏导数
        d2z_dx2, _ = np.gradient(dz_dx, xi[0, :], yi[:, 0])
        _, d2z_dy2 = np.gradient(dz_dy, xi[0, :], yi[:, 0])
        d2z_dxdy, _ = np.gradient(dz_dy, xi[0, :], yi[:, 0])

        # 初始化 Hessian 矩阵
        H = np.zeros((xi.shape[0], xi.shape[1], 2, 2))

        for i in range(xi.shape[0]):
            for j in range(xi.shape[1]):
                H[i, j] = np.array([
                    [d2z_dx2[i, j], d2z_dxdy[i, j]],
                    [d2z_dxdy[i, j], d2z_dy2[i, j]]
                ])

        total_eigenvalue = 0
        #计算hessian矩阵特征值
        for matrix in H:
            eigenvalues, eigenvectors = np.linalg.eig(matrix)
            for i in eigenvalues:
                for eigenvalue in i:
                    total_eigenvalue += abs(eigenvalue)
        average_eigenvalue = total_eigenvalue/len(H)
        return average_eigenvalue


    def show_results(self):

        # 创建掩膜
        mask = self.create_mask(self.xi, self.yi, self.polygon)
        elevation_clipped = np.where(mask, self.zi, np.nan)  # 应用掩膜到插值结果

        # 可视化结果
        fig = plt.figure(figsize=(7, 7))

        # 插值结果 3D 表面图
        ax2 = fig.add_subplot(111, projection='3d')
        surf = ax2.plot_surface(self.xi, self.yi, elevation_clipped, cmap='viridis', edgecolor='none', alpha=0.7)
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Latitude')
        ax2.set_zlabel('Elevation')
        cbar2 = plt.colorbar(surf, ax=ax2)
        cbar2.set_label('Elevation')
        d = self.calculate_D()
        average_hessian_eigenvalue = self.calculate_hessian_eigenvalue()
        ax2.set_title(f'e:{round(self.ellipic_e,3)}, angle:{round(self.ellipic_angle,3)}, N:{self.N}, p:{round(self.p,3)}, variance:{round(d,3)}, eigenvalue:{round(average_hessian_eigenvalue,3)}')

        plt.show()

    def save_results(self,name):

        # 创建掩膜
        mask = self.create_mask(self.xi, self.yi, self.polygon)
        elevation_clipped = np.where(mask, self.zi, np.nan)  # 应用掩膜到插值结果

        # 可视化结果
        fig = plt.figure(figsize=(7, 7))

        # 插值结果 3D 表面图
        ax2 = fig.add_subplot(111, projection='3d')
        surf = ax2.plot_surface(self.xi, self.yi, elevation_clipped, cmap='viridis', edgecolor='none', alpha=0.7)
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Latitude')
        ax2.set_zlabel('Elevation')
        cbar2 = plt.colorbar(surf, ax=ax2)
        cbar2.set_label('Elevation')
        d = self.calculate_D()
        eigenvalue = self.calculate_hessian_eigenvalue()
        ax2.set_title(f'e:{round(self.ellipic_e,3)}, angle:{round(self.ellipic_angle,3)}, N:{self.N}, p:{self.p}, variance:{round(d,3)}, eigenvalue:{round(eigenvalue,3)}')

        plt.savefig(f"new_results/{name}.png")

if __name__ == '__main__':
    pidw = PIDW(100, 0.2*np.pi, 15, 2)
    pidw.show_results()