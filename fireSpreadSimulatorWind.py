import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
grid_size = 50            # Tamaño de la cuadrícula
base_prob_spread = 1.5    # Probabilidad base de propagación del fuego
iterations = 50           # Número de iteraciones
wind_direction = (0, 0.1)   # Dirección del viento
wind_influence = 0.05      # Influencia del viento en la probabilidad de propagación

# Estados de la celda
EMPTY = 0                 # Verde (sin quemar)
BURNING = 1               # En llamas
BURNED = 2                # Quemado

# Inicialización de la cuadrícula y vegetación
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    vegetation = np.random.rand(size, size)  # Densidad de vegetación (0-1)
    center = size // 2
    grid[center, center] = BURNING  # Inicia el fuego en el centro
    return grid, vegetation

# Calcular la probabilidad de propagación ajustada para cada celda
def calculate_spread_prob(vegetation_density, wind_direction, cell_position):
    prob = base_prob_spread * vegetation_density
    # Ajuste por viento si la celda está en la dirección del viento
    if (cell_position[0] - wind_direction[0], cell_position[1] - wind_direction[1]) == wind_direction:
        prob += wind_influence
    return min(1.0, prob)  # Limitar probabilidad a un máximo de 1

# Actualización del estado de la cuadrícula
def update_grid(grid, vegetation, wind_direction):
    new_grid = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] == BURNING:
                # Si una celda está en llamas, se vuelve quemada
                new_grid[i, j] = BURNED
                # Propagación del fuego a celdas vecinas
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if grid[ni, nj] == EMPTY:
                        # Calcular la probabilidad de propagación en base a vegetación y viento
                        spread_prob = calculate_spread_prob(vegetation[ni, nj], wind_direction, (dx, dy))
                        if np.random.rand() < spread_prob:
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
    grid = update_grid(grid, vegetation, wind_direction)

ani = animation.FuncAnimation(fig, animate, frames=iterations, repeat=False)
plt.show()
