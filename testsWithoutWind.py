import os
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la simulación
grid_size = 50          # Tamaño de la cuadrícula inicial
iterations = 100        # Número de iteraciones
simulations = [
    {"beta": 0.3, "gamma": 0.1, "grid_size": grid_size},
    {"beta": 0.5, "gamma": 0.2, "grid_size": grid_size},
    {"beta": 0.7, "gamma": 0.4, "grid_size": grid_size},
    {"beta": 0.9, "gamma": 0.5, "grid_size": grid_size}
]
num_simulations = 50

# Estados de la celda
EMPTY = 0               # Verde (sin quemar) (Susceptible)
BURNING = 1             # En llamas (Infected)
BURNED = 2              # Quemado (Recovered)

# Directorio para guardar gráficos
output_dir = "simulation_results"
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
                if np.random.rand() < gamma:
                    new_grid[i, j] = BURNED
                else:
                    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if grid[x, y] == EMPTY and np.random.rand() < beta:
                            new_grid[x, y] = BURNING
    return new_grid

# Función para ejecutar una simulación y calcular métricas
def run_simulation(beta, gamma, grid_size, max_iter=iterations):
    grid = initialize_grid(grid_size)
    empty_counts, burning_counts, burned_counts = [], [], []
    for i in range(max_iter):
        empty_counts.append(np.sum(grid == EMPTY))
        burning_counts.append(np.sum(grid == BURNING))
        burned_counts.append(np.sum(grid == BURNED))
        
        # Terminar si no hay celdas en llamas (extinción)
        if np.sum(grid == BURNING) == 0:
            break
        
        grid = update_grid(grid, beta, gamma)

    # Calcular velocidad de propagación y tiempo de extinción
    burned_area = np.sum(burned_counts)
    spread_rate = burned_area / i if i > 0 else 0
    extinction_time = i
    
    return empty_counts, burning_counts, burned_counts, spread_rate, extinction_time

# Ejecutar simulaciones múltiples y calcular promedios
def run_simulations_with_averages(simulations, num_simulations, max_iter=iterations):
    averaged_metrics = []
    for sim in simulations:
        beta, gamma, grid_size = sim["beta"], sim["gamma"], sim["grid_size"]
        total_empty = np.zeros(max_iter)
        total_burning = np.zeros(max_iter)
        total_burned = np.zeros(max_iter)

        for _ in range(num_simulations):
            empty, burning, burned, _, _ = run_simulation(beta, gamma, grid_size, max_iter)
            
            # Ajustar los tamaños de los resultados si la simulación terminó antes de max_iter
            empty = np.pad(empty, (0, max_iter - len(empty)), 'edge')
            burning = np.pad(burning, (0, max_iter - len(burning)), 'constant', constant_values=0)
            burned = np.pad(burned, (0, max_iter - len(burned)), 'edge')

            total_empty += np.array(empty)
            total_burning += np.array(burning)
            total_burned += np.array(burned)

        avg_empty = total_empty / num_simulations
        avg_burning = total_burning / num_simulations
        avg_burned = total_burned / num_simulations

        averaged_metrics.append({
            "beta": beta,
            "gamma": gamma,
            "avg_empty": avg_empty,
            "avg_burning": avg_burning,
            "avg_burned": avg_burned
        })

    return averaged_metrics

# Ejecutar y graficar resultados
averaged_metrics = run_simulations_with_averages(simulations, num_simulations=50, max_iter=iterations)

for metrics in averaged_metrics:
    beta, gamma = metrics["beta"], metrics["gamma"]
    avg_empty, avg_burning, avg_burned = metrics["avg_empty"], metrics["avg_burning"], metrics["avg_burned"]

    plt.figure(figsize=(10, 6))
    plt.plot(avg_empty, label="Empty (Verde)")
    plt.plot(avg_burning, label="Burning (En llamas)")
    plt.plot(avg_burned, label="Burned (Quemado)")
    plt.xlabel("Iteración")
    plt.ylabel("Promedio de cantidad de celdas")
    plt.title(f"Promedio de evolución de estados - Beta: {beta}, Gamma: {gamma}")
    plt.legend()
    plt.savefig(f"{output_dir}/average_evolution_beta_{beta}_gamma_{gamma}.png")
    plt.show()

# Ejecución de todas las simulaciones con diferentes parámetros
metrics = []
for sim in simulations:
    beta, gamma, grid_size = sim["beta"], sim["gamma"], sim["grid_size"]
    empty, burning, burned, spread_rate, extinction_time = run_simulation(beta, gamma, grid_size)
    
    # Guardar resultados en métricas
    metrics.append({
        "beta": beta,
        "gamma": gamma,
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
    plt.title(f"Evolución de los estados del fuego - Beta: {beta}, Gamma: {gamma}")
    plt.legend()
    plt.savefig(f"{output_dir}/evolution_beta_{beta}_gamma_{gamma}.png")
    plt.close()

# Gráficos comparativos de las métricas
betas = [m["beta"] for m in metrics]
gammas = [m["gamma"] for m in metrics]
spread_rates = [m["spread_rate"] for m in metrics]
extinction_times = [m["extinction_time"] for m in metrics]

plt.figure(figsize=(12, 6))

# Gráfico de velocidad de propagación
plt.subplot(1, 2, 1)
plt.bar(range(len(spread_rates)), spread_rates, tick_label=[f"{b}, {g}" for b, g in zip(betas, gammas)])
plt.xlabel("(Beta, Gamma)")
plt.ylabel("Velocidad de propagación")
plt.title("Comparación de velocidad de propagación")

# Gráfico de tiempo de extinción
plt.subplot(1, 2, 2)
plt.bar(range(len(extinction_times)), extinction_times, tick_label=[f"{b}, {g}" for b, g in zip(betas, gammas)])
plt.xlabel("(Beta, Gamma)")
plt.ylabel("Tiempo de extinción")
plt.title("Comparación de tiempo de extinción")

plt.tight_layout()
plt.savefig(f"{output_dir}/comparative_metrics.png")
plt.show()
