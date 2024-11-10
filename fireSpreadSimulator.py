import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
grid_size = 50          # Tamaño de la cuadrícula
prob_spread = 0.65       # Probabilidad de propagación del fuego
iterations = 50         # Número de iteraciones

# Estados de la celda
EMPTY = 0               # Verde (sin quemar)
BURNING = 1             # En llamas
BURNED = 2              # Quemado

# Inicialización de la cuadrícula
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    start_x, start_y = np.random.randint(0, size), np.random.randint(0, size)
    grid[start_x, start_y] = BURNING
    return grid

# Actualización del estado de la cuadrícula
def update_grid(grid, prob_spread):
    new_grid = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] == BURNING:
                # Si una celda está en llamas, se vuelve quemada
                new_grid[i, j] = BURNED
                # Propagación del fuego a celdas vecinas
                for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if grid[x, y] == EMPTY and np.random.rand() < prob_spread:
                        new_grid[x, y] = BURNING
    return new_grid

# Función para visualizar la cuadrícula
def plot_grid(grid):
    colors = ['green', 'red', 'black']
    cmap = plt.matplotlib.colors.ListedColormap(colors)
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    plt.axis('off')

# Configuración de la animación
fig, ax = plt.subplots()
grid = initialize_grid(grid_size)

def animate(frame):
    global grid
    ax.clear()
    ax.set_title(f"Iteración {frame+1}")
    plot_grid(grid)
    grid = update_grid(grid, prob_spread)

ani = animation.FuncAnimation(fig, animate, frames=iterations, repeat=False)
plt.show()
