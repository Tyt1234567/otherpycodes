import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('2023-05-15 16-00-48.csv',encoding='ISO-8859-1')
data_lst = df.values.tolist()

def del_outliers(data,ele_col,sonar_col):
    surface_elevation = [i[ele_col]+i[sonar_col] for i in data]
    sorted_surface_elevation_data = sorted(surface_elevation)
    Q1 = sorted_surface_elevation_data[len(data)//4]
    Q3 = sorted_surface_elevation_data[(len(data)*3)//4]
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    for i in data:
        if i[ele_col]+i[sonar_col] < lower_bound or i[ele_col]+i[sonar_col] >upper_bound:
            data.remove(i)
    return data
'''
datas = del_outliers(data_lst,3,4)
longitudes = []
latitudes = []
elevations = []
sonar = []
for data in datas:
    latitudes.append(data[1])
    longitudes.append(data[2])
    elevations.append(data[3])
    sonar.append(data[4])

print((sum(elevations)+sum(sonar))/len(elevations))

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(longitudes, latitudes, elevations, c=elevations, cmap='viridis', s=50, alpha=0.7, edgecolors='w')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation')

# 添加颜色条
cbar = plt.colorbar(sc)
cbar.set_label('Elevation')

# 设置图标题
ax.set_title('river_elevation_model')
plt.title('after deleting anomalies')
# 显示图形
plt.show()
'''