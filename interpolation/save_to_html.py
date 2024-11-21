import numpy as np
import matplotlib.font_manager as fm
from matplotlib.path import Path
import plotly.graph_objs as go
import plotly.io as pio
from shapely.geometry import Polygon

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
        dist = custom_distance(xi[i], yi[i], x, y, angle, e)
        nearest_indices = np.argsort(dist)[:N]
        nearest_distances = dist[nearest_indices]
        nearest_values = values[nearest_indices]
        nearest_distances = np.where(nearest_distances == 0, 1e-10, nearest_distances)
        weights = 1 / (nearest_distances ** p)
        interpolated_values[i] = np.sum(weights * nearest_values) / np.sum(weights)

    return interpolated_values

def create_grid(lon, lat, ele, angle, e, N, p, polygon):
    minx, miny, maxx, maxy = polygon.bounds
    xi, yi = np.meshgrid(np.linspace(minx, maxx, 100), np.linspace(miny, maxy, 100))
    zi = interpolation(lon, lat, ele, xi.flatten(), yi.flatten(), angle, e, N, p)
    zi = zi.reshape(xi.shape)
    return xi, yi, zi

def create_mask(lon, lat, polygon):
    mask = np.zeros(lon.shape, dtype=bool)
    path = Path(np.array(polygon.exterior.coords))
    for i in range(lon.shape[0]):
        for j in range(lon.shape[1]):
            if path.contains_point((lon[i, j], lat[i, j])):
                mask[i, j] = True
    return mask

def save_interpolation_as_html(lon, lat, ele, angle, e, N, p, polygon, output_file):
    xi, yi, zi = create_grid(lon, lat, ele, angle, e, N, p, polygon)
    mask = create_mask(xi, yi, polygon)
    elevation_clipped = np.where(mask, zi, np.nan)
    fig = go.Figure(data=[go.Surface(z=elevation_clipped, x=xi, y=yi, colorscale='Viridis')])
    fig.update_layout(scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Elevation'),
        title='插值结果',
    )
    pio.write_html(fig, file=output_file, auto_open=True)