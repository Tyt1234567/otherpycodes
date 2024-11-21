from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt

def haversine(lon1, lat1, lon2, lat2):
    # 将经纬度从度数转换为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # 计算差值
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    # Haversine 公式
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # 地球半径（单位：公里）
    r = 6371.0
    # 计算距离
    distance = r * c
    return distance

def prim(n,seats):
    dist = [float('inf')] * n
    visited = [False] * n
    dist[0] = 0
    previous_index = [-1] * n #用于储存连接点的上一个点
    while False in visited:
        min_dist = float('inf')
        min_index = -1
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                min_index = i
        visited[min_index] = True
        if previous_index[min_index] != -1:
            point1 = seats[previous_index[min_index]]
            point2 = seats[min_index]
            plt.plot([point1[1], point2[1]], [point1[0], point2[0]], 'r-')
        for j in range(n):
            if not visited[j]:
                cost = haversine(seats[min_index][0],seats[min_index][1],seats[j][0],seats[j][1])
                if cost < dist[j]:
                    dist[j] = cost
                    previous_index[j] = min_index
    return dist

def read_txt_to_2d_list(file_path, target_fields):
    data_2d_list = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')

        # 找到目标字段的索引
        indices = [headers.index(field) for field in target_fields]

        for line in lines[1:]:
            values = line.strip().split(',')
            selected_row = [float(values[index]) for index in indices]
            data_2d_list.append(selected_row)

    return data_2d_list


# 指定文件路径和目标字段
file_path = r'D:\pyprojects\others\遥感\seats.txt'
target_fields = ['Latitude', 'Longitude']

# 读取数据
seats = read_txt_to_2d_list(file_path, target_fields)
# 提取经度和纬度
longitudes = [point[0] for point in seats]
latitudes = [point[1] for point in seats]
# 创建图表
plt.figure(figsize=(10, 6))
plt.scatter(latitudes, longitudes, c='blue', marker='o')
seat_dis=prim(len(seats),seats)
print(sum(seat_dis)/(len(seat_dis)-1))
# 添加标题和标签
plt.title('seats_distribution')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('equal')
plt.ticklabel_format(style='plain',useOffset=False)
# 显示图表
plt.grid(True)
plt.savefig('seat_distribution.jpg')
plt.show()