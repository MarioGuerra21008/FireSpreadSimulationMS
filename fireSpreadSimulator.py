import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
grid_size = 50          # Tamaño de la cuadrícula
beta = 0.65             # Tasa de infección (propagación del fuego)
gamma = 0.3             # Tasa de recuperación (tiempo de quemado)
iterations = 100        # Número de iteraciones

# Estados de la celda
EMPTY = 0               # Verde (sin quemar) (Susceptible)
BURNING = 1             # En llamas (Infected)
BURNED = 2              # Quemado (Recovered)

# Crear directorio para las capturas si no existe
output_dir = "captures/withoutWind"
os.makedirs(output_dir, exist_ok=True)

# Inicialización de la cuadrícula
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    start_x, start_y = np.random.randint(0, size), np.random.randint(0, size)
    grid[start_x, start_y] = BURNING
    return grid

# Actualización del estado de la cuadrícula
def update_grid(grid, beta, gamma):
    new_grid = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] == BURNING:
                # Probabilidad de recuperación (celda se vuelve quemada)
                if np.random.rand() < gamma:
                    new_grid[i, j] = BURNED
                else:
                    # Propagación del fuego a celdas vecinas
                    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if grid[x, y] == EMPTY and np.random.rand() < beta:
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

# Almacenar los conteos en cada iteración
empty_counts = []
burning_counts = []
burned_counts = []

def animate(frame):
    global grid
    ax.clear()
    ax.set_title(f"Iteración {frame+1}")
    plot_grid(grid)
    
    # Guardar captura cada 10 iteraciones
    if (frame + 1) % 10 == 0:
        capture_path = os.path.join(output_dir, f"frame_{frame+1}.png")
        plt.savefig(capture_path, bbox_inches='tight')
        print(f"Captura guardada en: {capture_path}")
    
    # Contar los estados actuales
    empty_counts.append(np.sum(grid == EMPTY))
    burning_counts.append(np.sum(grid == BURNING))
    burned_counts.append(np.sum(grid == BURNED))
    
    # Actualizar la cuadrícula
    grid = update_grid(grid, beta, gamma)

# Ejecutar la animación
ani = animation.FuncAnimation(fig, animate, frames=iterations, repeat=False)
plt.show()

# Graficar la cantidad de celdas en cada estado a lo largo del tiempo
plt.figure()
plt.plot(empty_counts, label="Empty (Verde)")
plt.plot(burning_counts, label="Burning (En llamas)")
plt.plot(burned_counts, label="Burned (Quemado)")
plt.xlabel("Iteración")
plt.ylabel("Cantidad de celdas")
plt.title("Evolución de los estados del fuego en la simulación")
plt.legend()
plt.show()
