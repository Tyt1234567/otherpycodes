from PIDW_include_boundary import PIDW
import numpy as np
import random

class Particles:
    def __init__(self):
        self.e_min = 0.01
        self.e_max = 100
        self.angle_min = 0
        self.angle_max = 2 * np.pi
        self.N_min = 5
        self.N_max = 25
        self.p_min = 1
        self.p_max = 3
        self.w = 0.5  # 惯性权重
        self.c1 = 1  # 认知学习因子
        self.c2 = 1.5  # 社会学习因子
        self.count = 0  # 存储迭代次数
        self.velocities = []  # 存储每个点上一次的移动速度
        for _ in range(100):
            velocity = np.random.uniform(-1, 1, 4)  # 初始移动速度
            self.velocities.append(velocity)

        self.best_D = 100000  # 设置初始方差
        self.particles = self.particles()

    def particles(self):
        particles = []
        for i in range(100):
            particles.append([])
            e = random.uniform(self.e_min, self.e_max)
            angle = random.uniform(self.angle_min, self.angle_max)
            N = random.randint(self.N_min, self.N_max)
            p = random.uniform(self.p_min, self.p_max)
            pidw = PIDW(e, angle, N, p)
            D = pidw.calculate_D()
            particles[i].append((e, angle, N, p, D))
        return particles

    # 寻找单个粒子最优
    def find_single_best(self, i):
        single_datas = self.particles[i]
        sorted_single_data = sorted(single_datas, key=lambda x: x[4])
        return sorted_single_data[0]

    # 寻找当前全局最优
    def find_global_best(self, i):
        global_datas = []
        for j in range(100):
            global_datas.append(self.particles[j][i])
        sorted_global_data = sorted(global_datas, key=lambda x: x[4])
        return sorted_global_data[0]

    # 移动粒子
    def movement(self):
        global_best_position = self.find_global_best(self.count)
        # 方差小于0.5时停止迭代
        while global_best_position[4] >= 0.5:
            new_locations = []
            for j in range(100):
                if self.count == 0:
                    inertia = np.zeros(4)
                    single_movement = np.zeros(4)
                else:
                    inertia = np.array(self.particles[j][self.count][:4]) - np.array(self.particles[j][self.count - 1][:4])
                    single_best = self.find_single_best(j)
                    single_movement = np.array(single_best[:4]) - np.array(self.particles[j][self.count][:4])

                global_movement = np.array(global_best_position[:4]) - np.array(self.particles[j][self.count][:4])

                new_velocity = []
                for k in range(4):
                    new_velocity.append(
                        self.w * self.velocities[j][k] * inertia[k] +
                        self.c1 * self.velocities[j][k] * single_movement[k] +
                        self.c2 * self.velocities[j][k] * global_movement[k]
                    )
                new_velocity = tuple(new_velocity)
                self.velocities[j] = new_velocity

                # 更新新位置，并确保第三个参数 N 是整数，第四个参数 p 保留三位小数
                new_location = list(np.array(self.particles[j][self.count][:4]) + np.array(new_velocity))

                # 保证新位置在指定范围内
                new_location[0] = np.clip(new_location[0], self.e_min, self.e_max)  # 限制 e 在范围内
                new_location[1] = np.clip(new_location[1], self.angle_min, self.angle_max)  # 限制 angle 在范围内
                new_location[2] = int(round(np.clip(new_location[2], self.N_min, self.N_max)))  # 限制 N 在范围内，并取整
                new_location[3] = round(np.clip(new_location[3], self.p_min, self.p_max), 3)  # 限制 p 在范围内，并保留三位小数

                new_locations.append(new_location)

            whether_iterate = False
            for new_location in new_locations:
                pidw = PIDW(new_location[0], new_location[1], new_location[2], new_location[3])
                D = pidw.calculate_D()
                new_location.append(D)
                if D < self.best_D:
                    self.best_D = D
                    whether_iterate = True
                    pidw.save_results(f'迭代第{self.count}次')
                    print(f'迭代第{self.count}次，e{new_location[0]},angle{new_location[1]},方差{D}')

            if whether_iterate:
                for index, new_location in enumerate(new_locations):
                    self.particles[index].append(new_location)

                self.count += 1
                global_best_position = self.find_global_best(self.count)

# 初始化并运行粒子群算法
swarm = Particles()
swarm.movement()
