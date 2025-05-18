import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import numpy as np
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Grafica3D:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.funcion = None
        self.rango_x = None
        self.rango_y = None
        self.after_ids = []  # Lista para almacenar los IDs de los eventos after

    def limpiar_workspace(self):
        # Cancelar todos los eventos after pendientes
        for after_id in self.after_ids:
            self.workspace_frame.after_cancel(after_id)
        self.after_ids = []
        
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        self.scrollable_frame = None
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        # Título
        ctk.CTkLabel(self.workspace_frame, text="Graficas 3D", **estilo_label_titulos).pack(pady=20)
        
        # ------ Contenedor principal ------ #
        self.frame_funcion = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_funcion.pack(pady=10, padx=20, fill="x")
        self.frame_funcion.columnconfigure(0, weight=1)
        self.frame_funcion.columnconfigure(1, weight=1)
        
        # --- Sección de la función (Columna 0) --- #
        self.frame_f = ctk.CTkFrame(self.frame_funcion, fg_color=("white", "gray10"))
        self.frame_f.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_funcion_title = ctk.CTkLabel(self.frame_f, text="z = f(x, y):", **estilo_label)
        self.label_funcion_title.pack(pady=5)
        
        self.entry_funcion = ctk.CTkEntry(self.frame_f, width=200, textvariable=self.funcion)
        self.entry_funcion.pack(pady=5, padx=10)
        self.entry_funcion.insert(0, "sin(x) + cos(x)")
        
        # --- Boton de vaciar funcion --- #
        self.vaciar_funcion_button = ctk.CTkButton(self.frame_f, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_funcion)
        self.vaciar_funcion_button.pack(pady=10)

        # --- Sección del rango (Columna 0) --- #
        self.frame_rango = ctk.CTkFrame(self.frame_funcion, fg_color=("white", "gray10"))
        self.frame_rango.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_rango_title = ctk.CTkLabel(self.frame_rango, text="Rango de x:", **estilo_label)
        self.label_rango_title.pack(pady=5)
        
        self.entry_rango_x = ctk.CTkEntry(self.frame_rango, width=200, textvariable=self.rango_x)
        self.entry_rango_x.pack(pady=5, padx=10)
        self.entry_rango_x.insert(0, "-10, 10")
        
        self.label_rango_title = ctk.CTkLabel(self.frame_rango, text="Rango de y:", **estilo_label)
        self.label_rango_title.pack(pady=5)
        
        self.entry_rango_y = ctk.CTkEntry(self.frame_rango, width=200, textvariable=self.rango_y)
        self.entry_rango_y.pack(pady=5, padx=10)
        self.entry_rango_y.insert(0, "-10, 10")
        
        # --- Boton de vaciar rango --- #
        self.vaciar_rango_button = ctk.CTkButton(self.frame_rango, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_rango)
        self.vaciar_rango_button.pack(pady=10)

        # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_operaciones.pack(pady=10, padx=20, fill="x")
        
        # --- Botones --- #
        self.graficar_button = ctk.CTkButton(self.frame_operaciones, text="Graficar", command=self.graficar_funcion)
        self.graficar_button.pack(padx=5, pady=5)   
        
        # ------ Fila 3: Resultado ------ #
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.label_resultado_title = ctk.CTkLabel(self.frame_resultado, text="Resultado:", **estilo_label)
        self.label_resultado_title.pack(pady=5)
        
        # Frame para el resultado 
        self.frame_resultado_grid = ctk.CTkFrame(self.frame_resultado, width=400, fg_color=("white", "gray10")) 
        self.frame_resultado_grid.pack(pady=10)


    def vaciar_funcion(self):
        self.funcion = None
        self.entry_funcion.delete(0, ctk.END)
        
    def vaciar_rango(self):
        self.rango_x = None
        self.rango_y = None
        self.entry_rango_x.delete(0, ctk.END)
        self.entry_rango_y.delete(0, ctk.END)

    def _leer_entradas_funcion_3d(self):
        try:
            funcion_str = self.entry_funcion.get().strip()
            rango_x_str = self.entry_rango_x.get().strip()
            rango_y_str = self.entry_rango_y.get().strip()
            if not funcion_str or not rango_x_str or not rango_y_str:
                raise ValueError("Debe ingresar una función y ambos rangos.")
            if 'np.' in funcion_str:
                raise ValueError("No escribas 'np.' en la función. Solo usa sin(x), cos(x), etc. sin prefijo np.")
            # Procesar rango x
            if ',' in rango_x_str:
                numeros_x = [float(x.strip()) for x in rango_x_str.split(',')]
                if len(numeros_x) != 2:
                    raise ValueError("El rango de x debe ser dos números separados por coma.")
                rango_x = numeros_x
            else:
                rango_x = eval(rango_x_str)
                if not isinstance(rango_x, (list, tuple)) or len(rango_x) != 2:
                    raise ValueError("El rango de x debe ser dos números separados por coma o lista/tupla.")
            # Procesar rango y
            if ',' in rango_y_str:
                numeros_y = [float(y.strip()) for y in rango_y_str.split(',')]
                if len(numeros_y) != 2:
                    raise ValueError("El rango de y debe ser dos números separados por coma.")
                rango_y = numeros_y
            else:
                rango_y = eval(rango_y_str)
                if not isinstance(rango_y, (list, tuple)) or len(rango_y) != 2:
                    raise ValueError("El rango de y debe ser dos números separados por coma o lista/tupla.")
            return funcion_str, rango_x, rango_y
        except Exception as e:
            messagebox.showerror("Error", f"Error en las entradas: {e}")
            return None

    def graficar_funcion(self):
        entradas = self._leer_entradas_funcion_3d()
        if entradas is None:
            return
        funcion_str, rango_x, rango_y = entradas
        print(f"Funcion Z: {funcion_str}")
        print(f"Rango X: {rango_x}")
        print(f"Rango Y: {rango_y}")
        try:
            x_min, x_max = rango_x
            y_min, y_max = rango_y
            n_puntos = 100
            x = np.linspace(x_min, x_max, n_puntos)
            y = np.linspace(y_min, y_max, n_puntos)
            X, Y = np.meshgrid(x, y)
            namespace = {
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'exp': np.exp,
                'log': np.log,
                'sqrt': np.sqrt,
                'arcsin': np.arcsin,
                'arccos': np.arccos,
                'arctan': np.arctan,
                'abs': np.abs,
                'x': X,
                'y': Y
            }
            Z = eval(funcion_str, namespace)
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel("eje x")
            ax.set_ylabel("eje y")
            ax.set_zlabel("eje z")
            ax.set_title(f"f(x, y) = {funcion_str.replace('np.', '').replace('exp', 'e^')}")
            ax.grid(True)
            # Limpiar el frame de resultado anterior
            for widget in self.frame_resultado_grid.winfo_children():
                widget.destroy()
            # Crear un canvas para la figura
            canvas = FigureCanvasTkAgg(fig, master=self.frame_resultado_grid)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Rango o número de puntos inválido. Asegúrese de ingresar números.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar en 3D: {e}")


