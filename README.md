# Calculadora

Una aplicación de calculadora avanzada desarrollada en Python, con una interfaz gráfica moderna y soporte para operaciones matemáticas básicas y avanzadas.

## Características

- Interfaz gráfica intuitiva y moderna (usando [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter))
- Soporte para operaciones matemáticas básicas y científicas
- Gráficas y visualización de funciones (usando `matplotlib`)
- Cálculos simbólicos y algebraicos (usando `sympy`)
- Diseño modular y fácil de mantener

## Estructura del Proyecto

```
Calculadora/
│
├── assets/           # Recursos gráficos (iconos, imágenes)
├── core/             # Lógica principal de la calculadora
├── styles/           # Archivos de estilos para la interfaz
├── UI/               # Componentes de la interfaz de usuario
├── venv/             # Entorno virtual de Python
├── app.py            # Archivo principal de la aplicación
├── main.py           # Punto de entrada alternativo
├── requirements.txt  # Dependencias del proyecto
├── utils.py          # Funciones utilitarias
└── .gitignore
```

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   cd Calculadora
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual:**
   - En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación con:

```bash
python main.py
```

## Dependencias principales

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [sympy](https://www.sympy.org/)

