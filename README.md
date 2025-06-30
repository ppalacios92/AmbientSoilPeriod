# AmbientSoilPeriod

**AmbientSoilPeriod** es una biblioteca científica en Python diseñada para estimar el **periodo predominante** de señales de vibración ambiental, con énfasis en aplicaciones geotécnicas y sísmicas. Utiliza un enfoque orientado a objetos, integrando técnicas como **STA/LTA**, selección automática de ventanas, **análisis espectral por FFT**, **suavizado Konno & Ohmachi**, y visualización de resultados.

El análisis está inicialmente diseñado para una única componente, y se extenderá a señales tridimensionales para la aplicación del método de **Nakamura** en caracterización de suelos.

---

## 📁 Estructura del Proyecto

```bash
AmbientSoilPeriod/
├── notebooks/                # Jupyter Notebooks de uso y validación
├── outputs/                  # Resultados generados (gráficos, datos)
├── signals/                  # Señales sísmicas a analizar (.txt)
│   └── Suelo01_01.txt
├── src/
│   └── ambientperiod/        # Paquete principal
│       ├── analysis/         # FFT, suavizado, detección de periodos
│       ├── builder/          # Clases principales de construcción
│       ├── preprocessing/    # STA/LTA, filtros, selección de ventanas
│       └── tools/            # Funciones de graficado
├── README.md
