import numpy as np
import matplotlib.pyplot as plt

def plot_common_windows(builders):
    """
    Plot signals and highlight the common selected windows for each component (X, Y, Z).
    Calculates and assigns common window IDs internally to each builder.

    Parameters
    ----------
    builders : list of tuple
        Each tuple must be (builder_X, builder_Y, builder_Z) with:
        - builder.signal
        - builder.windows_time
        - builder.win_ids
        - builder.config["Fs"]
    """
    for builder_X, builder_Y, builder_Z in builders:
        fs = builder_X.config["Fs"]

        # Tiempo para cada señal
        t_X = np.arange(len(builder_X.signal)) / fs
        t_Y = np.arange(len(builder_Y.signal)) / fs
        t_Z = np.arange(len(builder_Z.signal)) / fs

        # Obtener win_ids y calcular intersección común
        ids_X = np.array(builder_X.win_ids)
        ids_Y = np.array(builder_Y.win_ids)
        ids_Z = np.array(builder_Z.win_ids)

        common_ids = np.intersect1d(ids_X, ids_Y)
        common_ids = np.intersect1d(common_ids, ids_Z)

        # Asignar internamente
        builder_X.common_win_ids = common_ids
        builder_Y.common_win_ids = common_ids
        builder_Z.common_win_ids = common_ids

        # Buscar columnas reales asociadas a esos IDs
        col_X = [np.where(ids_X == i)[0][0] for i in common_ids]
        col_Y = [np.where(ids_Y == i)[0][0] for i in common_ids]
        col_Z = [np.where(ids_Z == i)[0][0] for i in common_ids]

        # Colores únicos por ventana
        colors = plt.cm.hsv(np.linspace(0, 1, len(common_ids)))

        # === Componente X ===
        plt.figure(figsize=(10, 2.5))
        plt.plot(t_X, builder_X.signal, color='black')
        for i, col in enumerate(col_X):
            x0 = builder_X.windows_time[0, col]
            x1 = builder_X.windows_time[-1, col]
            plt.axvspan(x0, x1, color=colors[i], alpha=0.3)
        plt.title("X Component - Common Windows", fontweight='bold')
        plt.ylabel("X", fontweight='bold')
        plt.xlabel("Time [s]", fontweight='bold')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # === Componente Y ===
        plt.figure(figsize=(10, 2.5))
        plt.plot(t_Y, builder_Y.signal, color='black')
        for i, col in enumerate(col_Y):
            x0 = builder_Y.windows_time[0, col]
            x1 = builder_Y.windows_time[-1, col]
            plt.axvspan(x0, x1, color=colors[i], alpha=0.3)
        plt.title("Y Component - Common Windows", fontweight='bold')
        plt.ylabel("Y", fontweight='bold')
        plt.xlabel("Time [s]", fontweight='bold')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # === Componente Z ===
        plt.figure(figsize=(10, 2.5))
        plt.plot(t_Z, builder_Z.signal, color='black')
        for i, col in enumerate(col_Z):
            x0 = builder_Z.windows_time[0, col]
            x1 = builder_Z.windows_time[-1, col]
            plt.axvspan(x0, x1, color=colors[i], alpha=0.3)
        plt.title("Z Component - Common Windows", fontweight='bold')
        plt.ylabel("Z", fontweight='bold')
        plt.xlabel("Time [s]", fontweight='bold')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
