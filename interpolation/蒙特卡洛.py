import numpy as np
import random
from tqdm import tqdm
from PIDW_include_boundary import PIDW

class Montecarlo:
    def __init__(self,points):
        self.points = points #蒙特卡洛算法投点个数

        self.e_exp_min = 0
        self.e_exp_max = 2

        self.angle_min = 0
        self.angle_max = np.pi

        self.p = 2
        self.N = 12

        self.particles = self.initial_particles()




    def initial_particles(self):
        particles = []
        for i in range(self.points):
            angle = random.uniform(self.angle_min,self.angle_max)
            e_exp = random.uniform(self.e_exp_min,self.e_exp_max)
            e = 10 ** e_exp
            particles.append([e, angle, self.N, self.p])
        return particles


    def find_best(self):
        best_particle = None  # 存储最佳位置
        best_value = float('inf')
        for particle in tqdm(self.particles):
            pidw = PIDW(particle[0], particle[1], particle[2], particle[3])
            D = pidw.calculate_D()
            eig = pidw.calculate_hessian_eigenvalue()
            value = D * 150 + eig
            if value < best_value:
                best_value = value
                best_particle = particle
                print(best_particle)

        print(best_particle)
        return best_particle

mon = Montecarlo(1000)
mon.find_best()





