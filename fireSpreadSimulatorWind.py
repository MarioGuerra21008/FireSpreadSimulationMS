import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
grid_size = 50             # Tamaño de la cuadrícula
diffusion_rate = 0.5       # Tasa de difusión del fuego
iterations = 100            # Número de iteraciones
wind_direction = (0.2, 0.5)    # Dirección del viento
wind_influence = 0.05      # Influencia del viento en la difusión

# Crear directorio para las capturas si no existe
output_dir = "captures/withWind"
os.makedirs(output_dir, exist_ok=True)

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

# Almacenar los conteos en cada iteración
empty_counts = []
burning_counts = []
burned_counts = []

def animate(frame):
    global grid
    ax.clear()
    ax.set_title(f"Iteración {frame+1}")
    plot_grid(grid)
    
    if (frame + 1) % 10 == 0:
        capture_path = os.path.join(output_dir, f"frame_{frame+1}.png")
        plt.savefig(capture_path, bbox_inches='tight')
        print(f"Captura guardada en: {capture_path}")
    
    # Contar los estados actuales
    empty_counts.append(np.sum(grid == EMPTY))
    burning_counts.append(np.sum(grid == BURNING))
    burned_counts.append(np.sum(grid == BURNED))
    
    grid = update_grid_diffusion(grid, diffusion_rate, wind_direction, wind_influence)

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
