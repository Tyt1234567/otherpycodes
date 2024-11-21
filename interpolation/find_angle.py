import numpy as np
import random
from tqdm import tqdm
from PIDW_include_boundary import PIDW
import matplotlib.pyplot as plt

angle = []
ds = []
eigs = []



def find_best():
    best_angle = None
    eig_max = 0
    for i in tqdm(np.arange(0,np.pi,0.01)):
        pidw = PIDW(100, i, 20, 2)

        d = pidw.calculate_D()
        eig = pidw.calculate_hessian_eigenvalue()

        if eig > eig_max:
            best_angle = i
            eig_max = eig

        angle.append(i)
        ds.append(d*100)
        eigs.append(eig)
    return best_angle


an = find_best()
print(an)
plt.plot(angle,ds,color = 'blue')
plt.plot(angle, eigs, color = 'red')
plt.show()