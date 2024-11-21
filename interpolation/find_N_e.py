import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from PIDW_include_boundary import PIDW

N_min = 5
N_max = 25

e_min_exp = 0
e_max_exp = 2

angle = 0.711 * np.pi
p = 2

Ns = np.arange(N_min, N_max + 1)
es = np.arange(e_min_exp, e_max_exp, 0.1)
Ns_grid, es_grid = np.meshgrid(Ns, 10**es)

# Initialize grids as float arrays
Ds_grid = np.zeros_like(Ns_grid, dtype=float)
eigs_grid = np.zeros_like(Ns_grid, dtype=float)

for i, N in enumerate(Ns):
    for j, e_exp in enumerate(np.arange(e_min_exp, e_max_exp, 0.1)):
        pidw = PIDW(10 ** e_exp, angle, N, 2)
        Ds_grid[j, i] = pidw.calculate_D() * 100
        eigs_grid[j, i] = pidw.calculate_hessian_eigenvalue()

# Create surface plot for D
surface1 = go.Surface(
    x=Ns_grid,
    y=es_grid,
    z=Ds_grid,
    colorscale='Blues',
    opacity=0.8,
    name='D'
)

# Create surface plot for eigs
surface2 = go.Surface(
    x=Ns_grid,
    y=es_grid,
    z=eigs_grid,
    colorscale='Reds',
    opacity=0.8,
    name='Eigenvalue'
)

# Combine the surfaces
data = [surface1, surface2]

layout = go.Layout(
    title='3D Surface Plot of D and Hessian Eigenvalue',
    scene=dict(
        xaxis_title='N',
        yaxis_title='e',
        zaxis_title='Z value',
    ),
)

fig = go.Figure(data=data, layout=layout)

# Save the figure as an HTML file
plot(fig, filename='ND_plot.html')