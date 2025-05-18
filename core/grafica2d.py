import customtkinter as ctk
import numpy as np
from styles.styles import estilo_label_titulos, estilo_label
from tkinter import messagebox
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import math


class Grafica2D:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.funcion = None
        self.rango = None
        self.after_ids = []  # Lista para almacenar los IDs de los eventos after
        
    def limpiar_workspace(self):
        # Cancelar todos los eventos after pendientes
        for after_id in self.after_ids:
            self.workspace_frame.after_cancel(after_id)
        self.after_ids = []
        
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        # Título
        ctk.CTkLabel(self.workspace_frame, text="Graficas 2D", **estilo_label_titulos).pack(pady=20)
        
        # ------ Contenedor principal ------ #
        self.frame_funcion = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_funcion.pack(pady=10, padx=20, fill="x")
        self.frame_funcion.columnconfigure(0, weight=1)
        self.frame_funcion.columnconfigure(1, weight=1)
        
        # --- Sección de la función (Columna 0) --- #
        self.frame_f = ctk.CTkFrame(self.frame_funcion, fg_color=("white", "gray10"))
        self.frame_f.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_funcion_title = ctk.CTkLabel(self.frame_f, text="y = f(x):", **estilo_label)
        self.label_funcion_title.pack(pady=5)
        
        self.entry_funcion = ctk.CTkEntry(self.frame_f, width=200, textvariable=self.funcion)
        self.entry_funcion.pack(pady=5, padx=10)
        self.entry_funcion.insert(0, "cos(x)")
        
        # --- Boton de vaciar funcion --- #
        self.vaciar_funcion_button = ctk.CTkButton(self.frame_f, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_funcion)
        self.vaciar_funcion_button.pack(pady=10)
        
        # --- Sección del rango (Columna 0) --- #
        self.frame_rango = ctk.CTkFrame(self.frame_funcion, fg_color=("white", "gray10"))
        self.frame_rango.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_rango_title = ctk.CTkLabel(self.frame_rango, text="Rango de x:", **estilo_label)
        self.label_rango_title.pack(pady=5)
        
        self.entry_rango = ctk.CTkEntry(self.frame_rango, width=200, textvariable=self.rango)
        self.entry_rango.pack(pady=5, padx=10)
        self.entry_rango.insert(0, "-10, 10")
        
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
        self.rango = None
        self.entry_rango.delete(0, ctk.END)

    def _leer_entradas_funcion_2d(self):
        """Lee y valida la función y el rango para graficar. Devuelve (funcion_str, rango_list) o None si hay error."""
        try:
            funcion_str = self.entry_funcion.get().strip()
            rango_str = self.entry_rango.get().strip()
            if not funcion_str or not rango_str:
                raise ValueError("Debe ingresar una función y un rango.")
            if 'np.' in funcion_str:
                raise ValueError("No escribas 'np.' en la función. Solo usa sin(x), cos(x), etc. sin prefijo np.")
            # Procesar rango
            if ',' in rango_str:
                numeros = [float(x.strip()) for x in rango_str.split(',')]
                if len(numeros) != 2:
                    raise ValueError("El rango debe ser dos números separados por coma.")
                rango = numeros
            else:
                rango = eval(rango_str)
                if not isinstance(rango, (list, tuple)) or len(rango) != 2:
                    raise ValueError("El rango debe ser dos números separados por coma o lista/tupla.")
            return funcion_str, rango
        except Exception as e:
            messagebox.showerror("Error", f"Error en las entradas: {e}")
            return None

    def graficar_funcion(self):
        entradas = self._leer_entradas_funcion_2d()
        if entradas is None:
            return
        funcion_str, rango = entradas
        print(f"Funcion: {funcion_str}")
        print(f"Rango: {rango}")
        try:
            x = np.linspace(rango[0], rango[1], 100)
            namespace = {
                'np': np,
                'math': math,
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
                'x': x
            }
            y = eval(funcion_str, namespace)
            # Crear la figura y graficar
            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set_xlabel("eje x")
            ax.set_ylabel("eje y")
            ax.set_title(f"f(x) = {funcion_str.replace('np.', '').replace('exp', 'e^')}")
            ax.grid(True)
            # Limpiar el frame de resultado anterior
            for widget in self.frame_resultado_grid.winfo_children():
                widget.destroy()
            # Crear el canvas y mostrar la gráfica
            canvas = FigureCanvasTkAgg(fig, master=self.frame_resultado_grid)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar la funcion: {str(e)}")
            return
        
        
        
