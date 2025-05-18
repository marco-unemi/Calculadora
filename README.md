# TotalMath

Aplicación avanzada de matemáticas con interfaz gráfica moderna, desarrollada en Python. Permite resolver y visualizar problemas de álgebra, cálculo, ecuaciones diferenciales, sistemas lineales, modelos epidemiológicos y más.

## Características

- Interfaz gráfica intuitiva y moderna (CustomTkinter)
- Operaciones con matrices, polinomios, vectores
- Gráficas 2D y 3D
- Derivación e integración simbólica y numérica
- Ecuaciones diferenciales (analíticas y numéricas)
- Sistemas de ecuaciones lineales y sistemas diferenciales
- Simulación de modelos epidemiológicos (SIR)
- Generación de números aleatorios y método de Monte Carlo
- Visualización de resultados y tablas
- Instalación fácil: ejecutable `.exe` para Windows

## Estructura del Proyecto

```
Calculadora/
│
├── assets/           # Recursos gráficos (iconos, imágenes)
├── core/             # Lógica principal y módulos matemáticos
├── styles/           # Archivos de estilos para la interfaz
├── venv/             # Entorno virtual de Python (opcional)
├── dist/             # Carpeta de distribución (contiene app.exe)
├── app.py            # Archivo principal de la aplicación
├── requirements.txt  # Dependencias del proyecto
├── utils.py          # Funciones utilitarias
└── .gitignore
```

## Instalación

### Opción 1: Ejecutable para Windows

1. Descarga el archivo `app.exe` desde la carpeta `dist/` o desde la [página de releases](#).
2. Haz doble clic en `app.exe` para ejecutar la aplicación.  
   **No necesitas instalar Python ni dependencias.**

### Opción 2: Ejecutar desde código fuente (Python 3.10+)

1. **Clona el repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   cd Calculadora
   ```

2. **(Opcional) Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

## Módulos y Funcionalidades

- **Matrices, Polinomios, Vectores:** Operaciones básicas y avanzadas, visualización.
- **Gráficas 2D/3D:** Visualización de funciones y datos.
- **Derivación e Integración:** Métodos simbólicos y numéricos.
- **Ecuaciones Diferenciales:** Solución analítica y numérica de EDOs.
- **Sistemas de Ecuaciones:** Resolución de sistemas lineales.
- **Sistemas Diferenciales:** Solución y visualización de sistemas de EDOs lineales.
- **Modelo SIR:** Simulación y análisis de epidemias.
- **Números Aleatorios y Monte Carlo:** Herramientas de simulación y estadística.
- **Acerca de:** Información sobre la aplicación y créditos.

## Dependencias principales

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [sympy](https://www.sympy.org/)
- [scipy](https://scipy.org/)
- [pandas](https://pandas.pydata.org/)
- [Pillow](https://python-pillow.org/)

## Notas

- El ejecutable `.exe` fue generado con [PyInstaller](https://pyinstaller.org/).
- Si tienes problemas con la visualización o dependencias, asegúrate de tener los drivers de video y fuentes actualizados en tu sistema.

