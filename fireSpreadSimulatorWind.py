import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
grid_size = 50             # Tamaño de la cuadrícula
diffusion_rate = 0.5       # Tasa de difusión del fuego
iterations = 100            # Número de iteraciones
wind_direction = (0.2, 0.5)    # Dirección del viento
wind_influence = 0.05      # Influencia del viento en la difusión

# Estados de la celda
EMPTY = 0                  # Verde (sin quemar)
BURNING = 1                # En llamas
BURNED = 2                 # Quemado

# Inicialización de la cuadrícula y vegetación
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    vegetation = np.random.rand(size, size)  # Densidad de vegetación (0-1)
    start_x, start_y = np.random.randint(0, size), np.random.randint(0, size)
    grid[start_x, start_y] = BURNING
    return grid, vegetation

# Actualización del estado de la cuadrícula basado en difusión
def update_grid_diffusion(grid, diffusion_rate, wind_direction, wind_influence):
    new_grid = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] == BURNING:
                new_grid[i, j] = BURNED  # La celda se quema
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if grid[ni, nj] == EMPTY:
                        # Calcular probabilidad de difusión ajustada por viento
                        diffusion_prob = diffusion_rate
                        if (dx, dy) == wind_direction:
                            diffusion_prob += wind_influence
                        # Propagar el fuego basado en la tasa de difusión
                        if np.random.rand() < diffusion_prob:
                            new_grid[ni, nj] = BURNING
    return new_grid

# Función para visualizar la cuadrícula
def plot_grid(grid):
    colors = ['green', 'red', 'black']
    cmap = plt.matplotlib.colors.ListedColormap(colors)
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    plt.axis('off')

# Configuración de la animación
fig, ax = plt.subplots()
grid, vegetation = initialize_grid(grid_size)

def animate(frame):
    global grid
    ax.clear()
    ax.set_title(f"Iteración {frame+1}")
    plot_grid(grid)
    grid = update_grid_diffusion(grid, diffusion_rate, wind_direction, wind_influence)

ani = animation.FuncAnimation(fig, animate, frames=iterations, repeat=False)
plt.show()
