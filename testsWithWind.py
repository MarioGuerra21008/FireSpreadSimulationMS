import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuraciones de simulación
grid_size = 50            # Tamaño de la cuadrícula
iterations = 100          # Número de iteraciones
simulations = [
    {"diffusion_rate": 0.3, "wind_direction": (0, 1), "wind_influence": 0.05},
    {"diffusion_rate": 0.5, "wind_direction": (1, 0), "wind_influence": 0.1},
    {"diffusion_rate": 0.7, "wind_direction": (1, 1), "wind_influence": 0.15},
    {"diffusion_rate": 0.9, "wind_direction": (0.5, 0.5), "wind_influence": 0.2}
]

# Estados de la celda
EMPTY = 0                 # Verde (sin quemar)
BURNING = 1               # En llamas
BURNED = 2                # Quemado

# Directorio para guardar gráficos
output_dir = "simulation_results_wind"
os.makedirs(output_dir, exist_ok=True)

# Inicialización de la cuadrícula y vegetación
def initialize_grid(size):
    grid = np.zeros((size, size), dtype=int)
    vegetation = np.random.rand(size, size)  # Densidad de vegetación (0-1)
    start_x, start_y = np.random.randint(0, size), np.random.randint(0, size)
    grid[start_x, start_y] = BURNING
    return grid, vegetation

# Actualización del estado de la cuadrícula con difusión y viento
def update_grid_diffusion(grid, diffusion_rate, wind_direction, wind_influence):
    new_grid = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            if grid[i, j] == BURNING:
                new_grid[i, j] = BURNED  # La celda se quema
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if grid[ni, nj] == EMPTY:
                        # Ajuste de difusión por dirección e influencia del viento
                        diffusion_prob = diffusion_rate
                        if (dx, dy) == wind_direction:
                            diffusion_prob += wind_influence
                        if np.random.rand() < diffusion_prob:
                            new_grid[ni, nj] = BURNING
    return new_grid

# Función para ejecutar una simulación y calcular métricas
def run_simulation(diffusion_rate, wind_direction, wind_influence, grid_size, max_iter=iterations):
    grid, vegetation = initialize_grid(grid_size)
    empty_counts, burning_counts, burned_counts = [], [], []
    
    for i in range(max_iter):
        empty_counts.append(np.sum(grid == EMPTY))
        burning_counts.append(np.sum(grid == BURNING))
        burned_counts.append(np.sum(grid == BURNED))
        
        # Terminar si no hay celdas en llamas (extinción)
        if np.sum(grid == BURNING) == 0:
            break
        
        grid = update_grid_diffusion(grid, diffusion_rate, wind_direction, wind_influence)
    
    # Calcular velocidad de propagación y tiempo de extinción
    burned_area = np.sum(burned_counts)
    spread_rate = burned_area / i if i > 0 else 0
    extinction_time = i

    return empty_counts, burning_counts, burned_counts, spread_rate, extinction_time

# Ejecución de simulaciones con diferentes parámetros
metrics = []
for sim in simulations:
    diffusion_rate = sim["diffusion_rate"]
    wind_direction = sim["wind_direction"]
    wind_influence = sim["wind_influence"]
    
    empty, burning, burned, spread_rate, extinction_time = run_simulation(
        diffusion_rate, wind_direction, wind_influence, grid_size
    )
    
    # Guardar resultados en métricas
    metrics.append({
        "diffusion_rate": diffusion_rate,
        "wind_direction": wind_direction,
        "wind_influence": wind_influence,
        "spread_rate": spread_rate,
        "extinction_time": extinction_time
    })
    
    # Graficar evolución de los estados en el tiempo
    plt.figure(figsize=(10, 6))
    plt.plot(empty, label="Empty (Verde)")
    plt.plot(burning, label="Burning (En llamas)")
    plt.plot(burned, label="Burned (Quemado)")
    plt.xlabel("Iteración")
    plt.ylabel("Cantidad de celdas")
    plt.title(f"Evolución del fuego - Difusión: {diffusion_rate}, Viento: {wind_direction}, Influencia: {wind_influence}")
    plt.legend()
    plt.savefig(f"{output_dir}/evolution_diffusion_{diffusion_rate}_wind_{wind_direction}.png")
    plt.close()

# Gráficos comparativos de las métricas
diffusion_rates = [m["diffusion_rate"] for m in metrics]
wind_influences = [m["wind_influence"] for m in metrics]
spread_rates = [m["spread_rate"] for m in metrics]
extinction_times = [m["extinction_time"] for m in metrics]

plt.figure(figsize=(12, 6))

# Gráfico de velocidad de propagación
plt.subplot(1, 2, 1)
plt.bar(range(len(spread_rates)), spread_rates, tick_label=[f"{d}, {w}" for d, w in zip(diffusion_rates, wind_influences)])
plt.xlabel("(Difusión, Influencia del viento)")
plt.ylabel("Velocidad de propagación")
plt.title("Comparación de velocidad de propagación")

# Gráfico de tiempo de extinción
plt.subplot(1, 2, 2)
plt.bar(range(len(extinction_times)), extinction_times, tick_label=[f"{d}, {w}" for d, w in zip(diffusion_rates, wind_influences)])
plt.xlabel("(Difusión, Influencia del viento)")
plt.ylabel("Tiempo de extinción")
plt.title("Comparación de tiempo de extinción")

plt.tight_layout()
plt.savefig(f"{output_dir}/comparative_metrics.png")
plt.show()
