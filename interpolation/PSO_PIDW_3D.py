from PIDW_include_boundary import PIDW
import numpy as np
import random
from math import log
import logging
from tqdm import tqdm


logging.basicConfig(filename= 'pso.log',
                    level=logging.INFO,  # 设置最低的日志级别为 INFO
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    )

class Particles:
    def __init__(self):
        self.e_min_exp = 0  # 对应 e_exp 的最小值
        self.e_max_exp = 2  # 对应 e_exp 的最大值

        self.N_min = 5
        self.N_max = 25
        self.p_min = 1
        self.p_max = 3
        self.w = 0.3  # 惯性权重
        self.c1 = 0.6  # 认知学习因子
        self.c2 = 0.8  # 社会学习因子
        self.count = 0  # 存储总迭代次数
        self.velocities = []  # 存储每个点上一次的移动速度
        for _ in range(100):
            velocity = np.random.uniform(-1, 1, 4)  # 初始移动速度
            self.velocities.append(velocity)

        self.best_evaluation = float('inf')  # 设置初始最优值
        self.best_loc = None #存储最佳例子位置
        self.particles, self.max_variance, self.max_eigenvalue = self.particles()

    def find_max_eigenvalue_variance(self,particles):
        variances = []
        eigenvalues = []
        for i in range(len(particles)):
            variances.append(particles[i][0][4])
            eigenvalues.append(particles[i][0][5])

        return max(variances), max(eigenvalues)

    def particles(self):
        particles = []
        for i in tqdm(range(100)):
            particles.append([])

            # 生成 e_exp 值，然后通过指数映射得到 e
            e_exp = random.uniform(self.e_min_exp, self.e_max_exp)

            N = random.randint(self.N_min, self.N_max)
            p = random.uniform(self.p_min, self.p_max)
            angle = 0.711 * np.pi

            # 只在计算 D 时用 e
            e = 10 ** e_exp
            pidw = PIDW(e, angle, N, p)
            D = pidw.calculate_D()
            eigenvalue = pidw.calculate_hessian_eigenvalue()
            particles[i].append((e_exp, angle, N, p, D, eigenvalue))

        max_variance, max_eigenvalue = self.find_max_eigenvalue_variance(particles)
        for i in range(100):
            e_exp = particles[i][0][0]
            angle = particles[i][0][1]
            N = particles[i][0][2]
            p = particles[i][0][3]
            D = particles[i][0][4]
            eigenvalue = particles[i][0][5]

            evaluation = 5 * log(D)/log(max_variance) + log(eigenvalue)/log(max_eigenvalue)
            particles[i][0] = (e_exp, angle, N, p, D, eigenvalue, evaluation)
        return particles,max_variance,max_eigenvalue

    def calculate_value(self,variance, eigenvalue):
        if variance <= self.max_variance and eigenvalue <= self.max_eigenvalue:
            value = 5* log(variance)/log(self.max_variance) + log(eigenvalue)/log(self.max_eigenvalue)
        else:
            value = float('inf')
        return value

    # 寻找单个粒子最优
    def find_single_best(self, i):
        single_datas = self.particles[i]
        sorted_single_data = sorted(single_datas, key=lambda x: x[6])
        return sorted_single_data[0]

    # 寻找当前全局最优
    def find_global_best(self, i):
        global_datas = []
        for j in range(100):
            global_datas.append(self.particles[j][i])
        sorted_global_data = sorted(global_datas, key=lambda x: x[6])
        return sorted_global_data[0]

    # 移动粒子
    def movement(self):
        self.best_loc = self.find_global_best(self.count)
        #进行100次迭代
        while self.count < 100:
            new_locations = []
            for j in range(100):
                if self.count == 0:
                    inertia = np.zeros(4)
                    single_movement = np.zeros(4)
                else:
                    inertia = np.array(self.particles[j][self.count][:4]) - np.array(self.particles[j][self.count - 1][:4])
                    single_best = self.find_single_best(j)
                    single_movement = np.array(single_best[:4]) - np.array(self.particles[j][self.count][:4])

                global_movement = np.array(self.best_loc[:4]) - np.array(self.particles[j][self.count][:4])

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

                # 保证 e_exp 的新位置在 [0, 2] 范围内，并通过指数映射计算 e
                new_location[0] = np.clip(new_location[0], self.e_min_exp, self.e_max_exp)  # 限制 e_exp 在范围内
                new_location[1] = 0.711 * np.pi
                new_location[2] = int(round(np.clip(new_location[2], self.N_min, self.N_max)))  # 限制 N 在范围内，并取整
                new_location[3] = round(np.clip(new_location[3], self.p_min, self.p_max), 3)  # 限制 p 在范围内，并保留三位小数

                new_locations.append(new_location)

            whether_better = False
            for new_location in new_locations:
                # 计算方差时将 e_exp 转换为 e
                e = 10 ** new_location[0]
                pidw = PIDW(e, new_location[1], new_location[2], new_location[3])
                D = pidw.calculate_D()
                eigenvalue = pidw.calculate_hessian_eigenvalue()
                evaluation = self.calculate_value(D, eigenvalue)

                new_location.append(D)
                new_location.append(eigenvalue)
                new_location.append(evaluation)

                if evaluation < self.best_evaluation:
                    self.best_evaluation = evaluation
                    whether_better = True

            # 保存更新粒子的位置
            for index, new_location in enumerate(new_locations):
                self.particles[index].append(new_location)


            if whether_better:
                self.best_loc = self.find_global_best(self.count)

            print(self.particles)
            #找到当前更新的最优解并保存
            current_best = self.find_single_best(-1)
            pidw = PIDW(current_best[0], current_best[1], current_best[2], current_best[3])
            pidw.save_results(f'迭代第{self.count + 1}次')
            print(f'iterate{self.count + 1}, e_exp {current_best[0]}, N:{current_best[2]}, p{current_best[3]} D {current_best[4]}, eig{current_best[5]}, eva{current_best[6]}')
            logging.info(f'iterate{self.count + 1}，e_exp {current_best[0]}, N:{current_best[2]}, p{current_best[3]} D {current_best[4]}, eig{current_best[5]}, eva{current_best[6]}')

            self.count+=1



# 初始化并运行粒子群算法
swarm = Particles()
swarm.movement()
