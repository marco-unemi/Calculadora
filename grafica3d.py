import customtkinter as ctk
from tkinter import messagebox
from utils import estilo_label, estilo_boton, crear_scrollable_frame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # Importa la biblioteca para crear gráficos en 3D.
import time


class GraficaEcuaciones3D:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame  # Guarda el frame principal donde se mostrará el contenido.
        self.scrollable_frame = None  # Inicializa el frame con scroll a None.
        # Variables de control para la función y los rangos, con valores predeterminados.
        self.funcion_var = ctk.StringVar(value="np.sin(np.sqrt(x**2 + y**2)) / (np.sqrt(x**2 + y**2) + 1e-6)")
        self.x_min_var = ctk.StringVar(value="-5")
        self.x_max_var = ctk.StringVar(value="5")
        self.y_min_var = ctk.StringVar(value="-5")
        self.y_max_var = ctk.StringVar(value="5")
        self.n_puntos_var = ctk.StringVar(value="100")  # Variable para controlar la resolución de la gráfica.
        self.frame_grafico = None  # Inicializa el frame donde se mostrará la gráfica 3D.

    def limpiar_workspace(self):
        # Limpia el contenido previo
        for widget in self.workspace_frame.winfo_children():  # Itera sobre todos los widgets en el workspace.
            widget.destroy()  # Destruye cada widget.
        self.scrollable_frame = None  # Resetea el frame con scroll.
        self.frame_grafico = None  # Resetea el frame de la gráfica.

    def mostrar_contenido(self):
        # Limpia el área antes de agregar contenido nuevo
        self.limpiar_workspace()  # Llama al método para limpiar el workspace.

        # Crear el frame con scroll usando la función de utils
        self.scrollable_frame = crear_scrollable_frame(self.workspace_frame)  # Crea un frame con funcionalidad de scroll.

        # Título principal
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Gráfica de ecuaciones en 3D", **estilo_label(font_size=16))  # Crea la etiqueta del título.
        title_label.pack(pady=20)  # Empaqueta la etiqueta con padding vertical.

        frame_entrada = ctk.CTkFrame(self.scrollable_frame)  # Frame para los elementos de entrada.
        frame_entrada.pack(pady=10, padx=20, fill="x")  # Empaqueta el frame con padding y se expande horizontalmente.

        label_funcion = ctk.CTkLabel(frame_entrada, text="Función z = f(x, y):", **estilo_label())  # Etiqueta para el campo de la función.
        label_funcion.pack(padx=5, pady=(5, 0))  # Empaqueta la etiqueta.
        entry_funcion = ctk.CTkEntry(frame_entrada, width=400, textvariable=self.funcion_var)  # Campo de entrada para la función z = f(x, y).
        entry_funcion.pack(padx=5, pady=(0, 5))  # Empaqueta el campo de entrada.

        frame_rango_x = ctk.CTkFrame(frame_entrada)  # Frame para el rango del eje x.
        frame_rango_x.pack(padx=5, pady=10)  # Empaqueta el frame.
        frame_rango_x.columnconfigure(0, weight=1)  # Configura el peso de las columnas para el grid.
        frame_rango_x.columnconfigure(1, weight=1)  # Configura el peso de las columnas para el grid.

        label_x_min = ctk.CTkLabel(frame_rango_x, text="x mínimo:", **estilo_label())  # Etiqueta para el mínimo de x.
        label_x_min.grid(row=0, column=0, padx=(0, 5), sticky="w")  # Coloca la etiqueta en la grid.
        entry_x_min = ctk.CTkEntry(frame_rango_x, width=100, textvariable=self.x_min_var)  # Campo de entrada para el mínimo de x.
        entry_x_min.grid(row=0, column=1, padx=5, sticky="ew")  # Coloca el campo de entrada en la grid.

        label_x_max = ctk.CTkLabel(frame_rango_x, text="x máximo:", **estilo_label())  # Etiqueta para el máximo de x.
        label_x_max.grid(row=0, column=2, padx=(10, 5), sticky="w")  # Coloca la etiqueta en la grid.
        entry_x_max = ctk.CTkEntry(frame_rango_x, width=100, textvariable=self.x_max_var)  # Campo de entrada para el máximo de x.
        entry_x_max.grid(row=0, column=3, padx=5, sticky="ew")  # Coloca el campo de entrada en la grid.

        frame_rango_y = ctk.CTkFrame(frame_entrada)  # Frame para el rango del eje y.
        frame_rango_y.pack(padx=5, pady=10)  # Empaqueta el frame.
        frame_rango_y.columnconfigure(0, weight=1)  # Configura el peso de las columnas para el grid.
        frame_rango_y.columnconfigure(1, weight=1)  # Configura el peso de las columnas para el grid.

        label_y_min = ctk.CTkLabel(frame_rango_y, text="y mínimo:", **estilo_label())  # Etiqueta para el mínimo de y.
        label_y_min.grid(row=0, column=0, padx=(0, 5), sticky="w")  # Coloca la etiqueta en la grid.
        entry_y_min = ctk.CTkEntry(frame_rango_y, width=100, textvariable=self.y_min_var)  # Campo de entrada para el mínimo de y.
        entry_y_min.grid(row=0, column=1, padx=5, sticky="ew")  # Coloca el campo de entrada en la grid.

        label_y_max = ctk.CTkLabel(frame_rango_y, text="y máximo:", **estilo_label())  # Etiqueta para el máximo de y.
        label_y_max.grid(row=0, column=2, padx=(10, 5), sticky="w")  # Coloca la etiqueta en la grid.
        entry_y_max = ctk.CTkEntry(frame_rango_y, width=100, textvariable=self.y_max_var)  # Campo de entrada para el máximo de y.
        entry_y_max.grid(row=0, column=3, padx=5, sticky="ew")  # Coloca el campo de entrada en la grid.

        frame_resolucion = ctk.CTkFrame(frame_entrada)  # Frame para la resolución de la gráfica.
        frame_resolucion.pack(padx=5, pady=10)  # Empaqueta el frame.
        label_puntos = ctk.CTkLabel(frame_resolucion, text="Número de puntos:", **estilo_label())  # Etiqueta para el número de puntos.
        label_puntos.grid(row=0, column=0, padx=(0, 5), sticky="w")  # Coloca la etiqueta en la grid.
        entry_puntos = ctk.CTkEntry(frame_resolucion, width=100, textvariable=self.n_puntos_var)  # Campo de entrada para el número de puntos.
        entry_puntos.grid(row=0, column=1, padx=(5, 0), sticky="ew")  # Coloca el campo de entrada en la grid.

        frame_buttons = ctk.CTkFrame(frame_entrada)  # Frame para los botones.
        frame_buttons.pack(padx=0, pady=(10, 15))  # Empaqueta el frame.
        frame_buttons.columnconfigure(0, weight=1)  # Configura el peso de las columnas para el grid.
        frame_buttons.columnconfigure(1, weight=1)  # Configura el peso de las columnas para el grid.

        vaciar_button = ctk.CTkButton(frame_buttons, text="Vaciar", command=self.vaciar, **estilo_boton(fg_color="#df0000", hover_color='#b81414'))  # Botón para limpiar los campos.
        vaciar_button.grid(row=0, column=0, padx=(0, 5), sticky="w")  # Coloca el botón en la grid.

        boton_graficar = ctk.CTkButton(frame_buttons, text="Graficar 3D", command=self.graficar_funcion, **estilo_boton())  # Botón para generar la gráfica 3D.
        boton_graficar.grid(row=0, column=1, padx=(5, 0), sticky="ew")  # Coloca el botón en la grid.

        self.frame_grafico = ctk.CTkFrame(self.scrollable_frame)  # Frame para contener la gráfica 3D.
        self.frame_grafico.pack(pady=10, padx=20, fill="both", expand=True)  # Empaqueta el frame y lo expande.

        label_resultado_title = ctk.CTkLabel(self.frame_grafico, text="Resultado:", **estilo_label(font_size=16))  # Etiqueta para el título del resultado.
        label_resultado_title.pack(pady=5)  # Empaqueta la etiqueta.

        self.grid_frame_resultado = ctk.CTkFrame(self.frame_grafico, width=400)  # Frame para contener el canvas de Matplotlib.
        self.grid_frame_resultado.pack(pady=10)  # Empaqueta el frame.

    def vaciar(self):
        self.funcion_var.set("")  # Limpia la variable de la función.
        self.x_min_var.set("")  # Limpia la variable del mínimo de x.
        self.x_max_var.set("")  # Limpia la variable del máximo de x.
        self.y_min_var.set("")  # Limpia la variable del mínimo de y.
        self.y_max_var.set("")  # Limpia la variable del máximo de y.
        self.n_puntos_var.set("")  # Limpia la variable del número de puntos.
        time.sleep(0.01)  # Pausa breve.
        for widget in self.grid_frame_resultado.winfo_children():  # Itera sobre los widgets en el frame de resultados.
            widget.destroy()  # Destruye cada widget (gráfica anterior).

    def graficar_funcion(self):
        funcion_str = self.funcion_var.get()  # Obtiene la función del usuario.
        x_min_str = self.x_min_var.get()  # Obtiene el mínimo de x.
        x_max_str = self.x_max_var.get()  # Obtiene el máximo de x.
        y_min_str = self.y_min_var.get()  # Obtiene el mínimo de y.
        y_max_str = self.y_max_var.get()  # Obtiene el máximo de y.
        n_puntos_str = self.n_puntos_var.get()  # Obtiene el número de puntos para la resolución.

        try:
            x_min = float(x_min_str)  # Convierte el mínimo de x a float.
            x_max = float(x_max_str)  # Convierte el máximo de x a float.
            y_min = float(y_min_str)  # Convierte el mínimo de y a float.
            y_max = float(y_max_str)  # Convierte el máximo de y a float.
            n_puntos = int(n_puntos_str)  # Convierte el número de puntos a entero.

            # Crea arrays de puntos x e y utilizando linspace para el rango y la resolución especificados.
            x = np.linspace(x_min, x_max, n_puntos)
            y = np.linspace(y_min, y_max, n_puntos)
            # Crea una malla de coordenadas a partir de los arrays x e y.
            X, Y = np.meshgrid(x, y)

            def f(x, y):
                try:
                    # Reemplaza la notación de sympy por la de numpy y evalúa la función.
                    funcion_eval = funcion_str.replace('sp.', 'np.')
                    return eval(funcion_eval)
                except (NameError, TypeError, SyntaxError):
                    messagebox.showerror("Error", "Función inválida. Asegúrese de usar 'x', 'y' y funciones de NumPy.")
                    return np.nan * X  # Devuelve un array de NaN del mismo tamaño en caso de error.

            # Calcula los valores de z para cada punto (x, y) en la malla.
            Z = f(X, Y)

            # Crea una nueva figura para el gráfico.
            fig = plt.figure()
            # Añade una subtrama a la figura con proyección 3D.
            ax = fig.add_subplot(projection='3d')
            # Crea una superficie 3D con los datos X, Y, Z y un mapa de colores 'viridis'.
            ax.plot_surface(X, Y, Z, cmap='viridis')
            # Establece las etiquetas de los ejes.
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")
            # Establece el título del gráfico.
            ax.set_title(f"Gráfico 3D de z = {funcion_str}")

            # Limpia cualquier gráfico anterior en el frame de resultados.
            for widget in self.grid_frame_resultado.winfo_children():
                widget.destroy()

            # Crea un canvas de Tkinter para embeber la figura de Matplotlib.
            canvas = FigureCanvasTkAgg(fig, master=self.grid_frame_resultado)
            # Obtiene el widget de Tkinter del canvas.
            canvas_widget = canvas.get_tk_widget()
            # Empaqueta el widget del canvas para que se muestre y se expanda.
            canvas_widget.pack(fill="both", expand=True)
            # Dibuja el canvas.
            canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Rango o número de puntos inválido. Asegúrese de ingresar números.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar en 3D: {e}")