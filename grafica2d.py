import customtkinter as ctk  # Importa la biblioteca customtkinter para crear la interfaz gráfica moderna.
from tkinter import messagebox  # Importa messagebox para mostrar ventanas de mensajes (ej., errores).
from utils import estilo_label, estilo_boton, crear_scrollable_frame  # Importa estilos y funciones de utilidad desde un módulo local 'utils'.
import numpy as np  # Importa la biblioteca numpy para realizar operaciones numéricas eficientemente, especialmente con arrays.
import time  # Importa el módulo time para funciones relacionadas con el tiempo (se usa para una pausa breve al vaciar).
import matplotlib.pyplot as plt  # Importa matplotlib.pyplot para crear gráficos.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importa FigureCanvasTkAgg para integrar gráficos de matplotlib en Tkinter/customtkinter.


class GraficaEcuaciones2D:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame  # Guarda el frame principal donde se mostrará el contenido de esta sección.
        self.scrollable_frame = None  # Inicializa el frame con scroll a None, se creará dinámicamente.
        self.ecuacion_var = ctk.StringVar()  # Variable de control para almacenar la ecuación ingresada por el usuario.
        self.x_min_var = ctk.StringVar()  # Variable de control para almacenar el límite mínimo del eje x.
        self.x_max_var = ctk.StringVar()  # Variable de control para almacenar el límite máximo del eje x.
        self.frame_grafico = None  # Inicializa el frame donde se mostrará la gráfica a None.

    def limpiar_workspace(self):
        # Limpia el contenido previo
        for widget in self.workspace_frame.winfo_children():  # Itera sobre todos los widgets dentro del workspace frame.
            widget.destroy()  # Destruye cada widget, eliminando el contenido anterior.
        self.scrollable_frame = None  # Resetea la variable del frame con scroll.
        self.frame_grafico = None  # Resetea la variable del frame de la gráfica.


    def mostrar_contenido(self):
        # Limpia el área antes de agregar contenido nuevo
        self.limpiar_workspace()  # Llama al método para eliminar cualquier contenido anterior en el workspace.

        # Crear el frame con scroll usando la función de utils
        self.scrollable_frame = crear_scrollable_frame(self.workspace_frame)  # Utiliza una función de utilidad para crear un frame que permite el scroll si el contenido es demasiado grande.

        # Título principal
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Gráfica de ecuaciones en 2D", **estilo_label(font_size=16))  # Crea una etiqueta con el título principal, aplicando un estilo específico.
        title_label.pack(pady=20)  # Empaqueta la etiqueta en el frame con un padding vertical de 20 píxeles.


        frame_entrada = ctk.CTkFrame(self.scrollable_frame)  # Crea un frame para contener los elementos de entrada (función y rango de x).
        frame_entrada.pack(pady=10, padx=20, fill="x")  # Empaqueta el frame con padding vertical y horizontal, y se expande horizontalmente.

        label_funcion = ctk.CTkLabel(frame_entrada, text="Función y = f(x):", **estilo_label())  # Etiqueta para el campo de entrada de la función.
        label_funcion.pack(padx=5, pady=(5, 0))  # Empaqueta la etiqueta con padding horizontal y vertical superior.
        entry_funcion = ctk.CTkEntry(frame_entrada, width=400, textvariable=self.ecuacion_var)  # Campo de entrada donde el usuario escribe la función, asociado a la variable ecuacion_var.
        entry_funcion.pack(padx=5, pady=(0, 5))  # Empaqueta el campo de entrada con padding horizontal y vertical inferior.

        frame_rango_x = ctk.CTkFrame(frame_entrada)  # Frame para contener los campos de entrada del rango del eje x.
        frame_rango_x.pack(padx=0, pady=10)  # Empaqueta el frame con padding vertical.
        frame_rango_x.columnconfigure(0, weight=1)  # Configura el peso de la columna 0 para el grid layout dentro de este frame.
        frame_rango_x.columnconfigure(1, weight=1)  # Configura el peso de la columna 1 para el grid layout dentro de este frame.

        label_x_min = ctk.CTkLabel(frame_rango_x, text="x mínimo:", **estilo_label())  # Etiqueta para el campo de entrada del valor mínimo de x.
        label_x_min.grid(row=0, column=0, padx=(0, 5), sticky="w")  # Coloca la etiqueta en la celda (0, 0) del grid, con padding a la derecha y alineación oeste.
        entry_x_min = ctk.CTkEntry(frame_rango_x, width=100, textvariable=self.x_min_var)  # Campo de entrada para el valor mínimo de x, asociado a la variable x_min_var.
        entry_x_min.grid(row=0, column=1, padx=(0, 10), sticky="ew")  # Coloca el campo de entrada en la celda (0, 1) del grid, con padding a la derecha y se expande horizontalmente.

        label_x_max = ctk.CTkLabel(frame_rango_x, text="x máximo:", **estilo_label())  # Etiqueta para el campo de entrada del valor máximo de x.
        label_x_max.grid(row=0, column=2, padx=(10, 5), sticky="w")  # Coloca la etiqueta en la celda (0, 2) del grid, con padding a la izquierda y alineación oeste.
        entry_x_max = ctk.CTkEntry(frame_rango_x, width=100, textvariable=self.x_max_var)  # Campo de entrada para el valor máximo de x, asociado a la variable x_max_var.
        entry_x_max.grid(row=0, column=3, padx=(0, 5), sticky="ew")  # Coloca el campo de entrada en la celda (0, 3) del grid, con padding a la derecha y se expande horizontalmente.

        frame_buttons = ctk.CTkFrame(frame_entrada)  # Frame para contener los botones de "Vaciar" y "Graficar".
        frame_buttons.pack(padx=0, pady=(10, 15))  # Empaqueta el frame con padding vertical.
        frame_buttons.columnconfigure(0, weight=1)  # Configura el peso de la columna 0 para el grid layout dentro de este frame.
        frame_buttons.columnconfigure(1, weight=1)  # Configura el peso de la columna 1 para el grid layout dentro de este frame.

        vaciar_button = ctk.CTkButton(frame_buttons, text="Vaciar", command=self.vaciar, **estilo_boton(fg_color="#df0000", hover_color='#b81414'))  # Botón para limpiar los campos de entrada, con un estilo específico.
        vaciar_button.grid(row=0, column=0, padx=(0, 5), sticky="w")  # Coloca el botón en la celda (0, 0) del grid, con padding a la derecha y alineación oeste.

        boton_graficar = ctk.CTkButton(frame_buttons, text="Graficar", command=self.graficar_funcion, **estilo_boton())  # Botón para iniciar el proceso de graficación.
        boton_graficar.grid(row=0, column=1, padx=(5, 0), sticky="ew")  # Coloca el botón en la celda (0, 1) del grid, con padding a la izquierda y se expande horizontalmente.

        # Frame donde se mostrará la gráfica
        self.frame_grafico = ctk.CTkFrame(self.scrollable_frame)  # Crea un frame para contener la gráfica resultante.
        self.frame_grafico.pack(pady=10, padx=20, fill="both", expand=True)  # Empaqueta el frame con padding y se expande en ambas direcciones.

        label_resultado_title = ctk.CTkLabel(self.frame_grafico, text="Resultado:", **estilo_label(font_size=16))  # Etiqueta para el título del área de resultados.
        label_resultado_title.pack(pady=5)  # Empaqueta la etiqueta con padding vertical.

        # Frame dentro del frame_grafico para alojar el canvas de Matplotlib
        self.grid_frame_resultado = ctk.CTkFrame(self.frame_grafico, width=400)  # Crea un frame dentro del frame de la gráfica para contener el gráfico de Matplotlib.
        self.grid_frame_resultado.pack(pady=10)  # Empaqueta el frame con padding y se expande en ambas direcciones.


    def vaciar(self):
        self.ecuacion_var.set("")  # Limpia la variable de control de la ecuación.
        self.x_min_var.set("")  # Limpia la variable de control del límite mínimo de x.
        self.x_max_var.set("")  # Limpia la variable de control del límite máximo de x.
        time.sleep(0.01)  # Pausa breve (0.01 segundos) para asegurar que las variables se actualicen en la interfaz.
        # Limpia el frame donde se muestra la gráfica
        for widget in self.grid_frame_resultado.winfo_children():  # Itera sobre los widgets dentro del frame de resultados (donde se muestra la gráfica).
            widget.destroy()  # Destruye cada widget, eliminando cualquier gráfico anterior.

    def graficar_funcion(self):
        funcion_str = self.ecuacion_var.get()  # Obtiene la ecuación ingresada por el usuario desde la variable de control.
        x_min_str = self.x_min_var.get()  # Obtiene el límite mínimo de x ingresado por el usuario.
        x_max_str = self.x_max_var.get()  # Obtiene el límite máximo de x ingresado por el usuario.

        try:
            x_min = float(x_min_str)  # Intenta convertir el valor mínimo de x a un número de punto flotante.
            x_max = float(x_max_str)  # Intenta convertir el valor máximo de x a un número de punto flotante.
            # Genera un array de puntos x para graficar
            x = np.linspace(x_min, x_max, 400)  # Crea un array de 400 puntos espaciados uniformemente entre x_min y x_max.

            def f(x):
                try:
                    # Reemplaza las funciones de sympy (si las hubiera) por las de numpy para la evaluación numérica
                    funcion_eval = funcion_str.replace('sp.', 'np.')  # Intenta reemplazar la notación de sympy por la de numpy.
                    return eval(funcion_eval)  # Evalúa la cadena de la función utilizando la variable x (¡peligroso para entradas no confiables!).
                except (NameError, TypeError, SyntaxError):
                    messagebox.showerror("Error", "Función inválida. Asegúrese de usar 'x' como variable y funciones de NumPy (np.sin, np.exp, etc.).")  # Muestra un error si la función no es válida.
                    return np.nan * x  # Devuelve un array de NaN (Not a Number) del mismo tamaño que x en caso de error.

            # Calcula los valores de y para los puntos x
            y = f(x)  # Llama a la función f con el array de valores x para obtener los valores de y.

            # Crea la figura y los ejes de Matplotlib
            fig, ax = plt.subplots()  # Crea una nueva figura y un conjunto de subtramas (en este caso, solo una).
            # Grafica la función
            ax.plot(x, y)  # Dibuja la gráfica de y contra x en los ejes.
            # Etiquetas de los ejes
            ax.set_xlabel("eje x")  # Establece la etiqueta del eje x.
            ax.set_ylabel("eje y")  # Establece la etiqueta del eje y.

            # Título del gráfico
            titulo_grafico = funcion_str.replace('np.', '')  # Crea un título para el gráfico, intentando eliminar 'np.' si está presente.
            ax.set_title(f"Gráfico de y = {titulo_grafico}")  # Establece el título del gráfico.
            # Añade una cuadrícula al gráfico
            ax.grid(True)  # Activa la cuadrícula en el gráfico.

            # Limpia cualquier gráfico anterior en el frame de resultados
            for widget in self.grid_frame_resultado.winfo_children():  # Itera sobre los widgets en el frame de resultados.
                widget.destroy()  # Destruye cada widget (cualquier gráfico anterior).

            # Crea un canvas de Tkinter para embeber la figura de Matplotlib
            canvas = FigureCanvasTkAgg(fig, master=self.grid_frame_resultado)  # Crea un objeto canvas que puede contener la figura de Matplotlib dentro de un widget de Tkinter.
            # Obtiene el widget de Tkinter del canvas
            canvas_widget = canvas.get_tk_widget()  # Obtiene el widget de Tkinter que representa el área de dibujo del gráfico.
            # Empaqueta el widget del canvas para que se muestre en el frame
            canvas_widget.pack(fill="both", expand=True)  # Empaqueta el widget del canvas para que se expanda y llene el frame de resultados.
            # Dibuja el canvas
            canvas.draw()  # Renderiza el gráfico en el canvas.

        except ValueError:
            messagebox.showerror("Error", "Rango de x inválido. Asegúrese de ingresar números para x mínimo y máximo.")  # Muestra un error si los rangos de x no son números válidos.
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar: {e}")  # Muestra un error genérico si ocurre cualquier otra excepción durante el proceso de graficación.