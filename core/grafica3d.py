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
        
        self.entry_funcion = ctk.CTkEntry(self.frame_f, width=200, placeholder_text="Ej: np.cos(x) + np.sin(y)", textvariable=self.funcion)
        self.entry_funcion.pack(pady=5, padx=10)
        self.entry_funcion.bind("<Return>", lambda event: self.actualizar_funcion())
        
        # --- Boton de vaciar funcion --- #
        self.vaciar_funcion_button = ctk.CTkButton(self.frame_f, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_funcion)
        self.vaciar_funcion_button.pack(pady=10)

        # --- Sección del rango (Columna 0) --- #
        self.frame_rango = ctk.CTkFrame(self.frame_funcion, fg_color=("white", "gray10"))
        self.frame_rango.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_rango_title = ctk.CTkLabel(self.frame_rango, text="Rango de x:", **estilo_label)
        self.label_rango_title.pack(pady=5)
        
        self.entry_rango_x = ctk.CTkEntry(self.frame_rango, width=200, placeholder_text="Ej: -10, 10", textvariable=self.rango_x)
        self.entry_rango_x.pack(pady=5, padx=10)
        self.entry_rango_x.bind("<Return>", lambda event: self.actualizar_rango())
        
        self.label_rango_title = ctk.CTkLabel(self.frame_rango, text="Rango de y:", **estilo_label)
        self.label_rango_title.pack(pady=5)
        
        self.entry_rango_y = ctk.CTkEntry(self.frame_rango, width=200, placeholder_text="Ej: -10, 10", textvariable=self.rango_y)
        self.entry_rango_y.pack(pady=5, padx=10)
        self.entry_rango_y.bind("<Return>", lambda event: self.actualizar_rango())
        
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

    def actualizar_funcion(self):
        try:
            texto = self.entry_funcion.get()
            # Verificar que la función es válida evaluándola en un punto
            x = 0
            y = 0   
            namespace = {'np': np, 'x': x, 'y': y}
            eval(texto, namespace)
            self.funcion = texto
        except Exception:
            self.funcion = None
            
    def actualizar_rango(self):
        try:
            texto_x = self.entry_rango_x.get()
            texto_y = self.entry_rango_y.get()
            
            # Si el usuario ingresó dos números separados por coma
            if ',' in texto_x:
                numeros = [float(x.strip()) for x in texto_x.split(',')]
                if len(numeros) != 2:
                    raise ValueError("Debe ingresar dos números separados por coma")
                self.rango_x = numeros
            else:
                # Si el usuario ingresó en formato lista/tupla
                self.rango_x = eval(texto_x)
                if not isinstance(self.rango_x, (list, tuple)) or len(self.rango_x) != 2:
                    raise ValueError("El rango debe ser dos números separados por coma")
            
            # Procesar el rango de y    
            if ',' in texto_y:
                numeros = [float(x.strip()) for x in texto_y.split(',')]
                if len(numeros) != 2:
                    raise ValueError("Debe ingresar dos números separados por coma")
                self.rango_y = numeros
            else:
                # Si el usuario ingresó en formato lista/tupla
                self.rango_y = eval(texto_y)
                if not isinstance(self.rango_y, (list, tuple)) or len(self.rango_y) != 2:
                    raise ValueError("El rango debe ser dos números separados por coma")
        except Exception:
            self.rango_x = None
            self.rango_y = None

    def vaciar_funcion(self):
        self.funcion = None
        self.entry_funcion.delete(0, ctk.END)
        
    def vaciar_rango(self):
        self.rango_x = None
        self.rango_y = None
        self.entry_rango_x.delete(0, ctk.END)
        self.entry_rango_y.delete(0, ctk.END)

    def graficar_funcion(self):
        print(f"Funcion Z: {self.funcion}")
        print(f"Rango X: {self.rango_x}")
        print(f"Rango Y: {self.rango_y}")
        
        if self.funcion is None:
            messagebox.showerror("Error", "Debe ingresar una funcion")
            return
        
        try:
            
            x_min, x_max = self.rango_x
            y_min, y_max = self.rango_y
            n_puntos = 100
            
            x = np.linspace(x_min, x_max, n_puntos)
            y = np.linspace(y_min, y_max, n_puntos)
            
            X, Y = np.meshgrid(x, y)
            
            def f(x, y):
                try:
                    funcion_eval = self.funcion.replace('sp.', 'np.')
                    return eval(funcion_eval)
                except (NameError, TypeError, SyntaxError):
                    messagebox.showerror("Error", "Función inválida. Asegúrese de usar 'x', 'y' y funciones de NumPy.")
                    return np.nan * X
            
            Z = f(X, Y)
            
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel("eje x")
            ax.set_ylabel("eje y")
            ax.set_zlabel("eje z")
            ax.set_title(f"f(x, y) = {self.funcion.replace('np.', '').replace('exp', 'e^')}")
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


