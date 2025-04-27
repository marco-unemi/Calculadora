import customtkinter as ctk
import numpy as np
from styles.styles import estilo_label_titulos, estilo_label
from tkinter import messagebox


class Vector:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.vector1 = None
        self.vector2 = None
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        self.vector1 = None
        self.vector2 = None
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Vectores", **estilo_label_titulos).pack(pady=20)
        
        # ------ Fila 1: contenedor de vectores A y B ------ #
        self.frame_vectores = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_vectores.pack(pady=10, padx=20, fill="x")
        self.frame_vectores.columnconfigure(0, weight=1)
        self.frame_vectores.columnconfigure(1, weight=1)
        
        # --- Sección de Vector A (Columna 0) --- #
        self.frame_vector1 = ctk.CTkFrame(self.frame_vectores, fg_color=("white", "gray10"))
        self.frame_vector1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_vector1_title = ctk.CTkLabel(self.frame_vector1, text="Vector 1", **estilo_label)
        self.label_vector1_title.pack(pady=5)
        
        self.entry_vector1 = ctk.CTkEntry(self.frame_vector1, width=200, placeholder_text="Ej: 1, 2, 3")
        self.entry_vector1.pack(pady=5, padx=10)
        self.entry_vector1.bind("<KeyRelease>", lambda event: self.actualizar_vector1())
        
        # --- Boton de vaciar vector 1 --- #
        self.vaciar_a_button = ctk.CTkButton(self.frame_vector1, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_vector1)
        self.vaciar_a_button.pack(pady=10)
        
        # --- Sección de Vector B (Columna 1) --- #
        self.frame_vector2 = ctk.CTkFrame(self.frame_vectores, fg_color=("white", "gray10"))
        self.frame_vector2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_vector2_title = ctk.CTkLabel(self.frame_vector2, text="Vector 2", **estilo_label)
        self.label_vector2_title.pack(pady=5)
        
        self.entry_vector2 = ctk.CTkEntry(self.frame_vector2, width=200, placeholder_text="Ej: 1, 2, 3")
        self.entry_vector2.pack(pady=5, padx=10)
        self.entry_vector2.bind("<KeyRelease>", lambda event: self.actualizar_vector2())
        
        # --- Boton de vaciar vector 2 --- #
        self.vaciar_b_button = ctk.CTkButton(self.frame_vector2, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_vector2)
        self.vaciar_b_button.pack(pady=5)
        
        # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_operaciones.pack(pady=10, padx=20, fill="x")
        self.frame_operaciones.columnconfigure(0, weight=1)
        self.frame_operaciones.columnconfigure(1, weight=1)
        self.frame_operaciones.columnconfigure(2, weight=1)
        self.frame_operaciones.columnconfigure(3, weight=1)
        
        # --- Botones --- #
        self.sumar_button = ctk.CTkButton(self.frame_operaciones, text="Sumar", command=self.suma_vectores)
        self.sumar_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.restar_button = ctk.CTkButton(self.frame_operaciones, text="Restar", command=self.resta_vectores)
        self.restar_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.producto_escalar_button = ctk.CTkButton(self.frame_operaciones, text="Producto Escalar", command=self.producto_escalar)
        self.producto_escalar_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.producto_vectorial_button = ctk.CTkButton(self.frame_operaciones, text="Producto Vectorial", command=self.producto_vectorial)
        self.producto_vectorial_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        self.magnitud_button = ctk.CTkButton(self.frame_operaciones, text="Magnitud", command=self.magnitud_vector)
        self.magnitud_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.vector_unitario_button = ctk.CTkButton(self.frame_operaciones, text="Vector Unitario", command=self.vector_unitario)
        self.vector_unitario_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.angulo_button = ctk.CTkButton(self.frame_operaciones, text="Ángulo entre Vectores", command=self.angulo_vectores)
        self.angulo_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        self.proyeccion_button = ctk.CTkButton(self.frame_operaciones, text="Proyección", command=self.proyeccion_vector)
        self.proyeccion_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        # ------ Fila 3: Resultado ------ #
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.label_resultado_title = ctk.CTkLabel(self.frame_resultado, text="Resultado:", **estilo_label)
        self.label_resultado_title.pack(pady=5)
        
        # Frame contenedor para resultado y etiqueta
        self.frame_contenedor = ctk.CTkFrame(self.frame_resultado, fg_color=("white", "gray10"))
        self.frame_contenedor.pack(pady=10, padx=20, expand=True)
        
        # Configurar el grid del contenedor
        self.frame_contenedor.grid_columnconfigure(0, weight=1)
        self.frame_contenedor.grid_columnconfigure(1, weight=1)
        
        # Frame para la etiqueta (izquierda)
        self.frame_resultado_label = ctk.CTkFrame(self.frame_contenedor, fg_color=("white", "gray10"))
        self.frame_resultado_label.grid(row=0, column=0, padx=(20,5), pady=10, sticky="nsew")
        
        # Frame para el resultado (derecha)
        self.frame_resultado_grid = ctk.CTkFrame(self.frame_contenedor, fg_color=("white", "gray10"))
        self.frame_resultado_grid.grid(row=0, column=1, padx=(5,20), pady=10, sticky="nsew")
        
    def actualizar_vector1(self):
        try:
            texto = self.entry_vector1.get()
            self.vector1 = self.parse_vector(texto)
            print(f"Vector 1: {self.vector1}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el Vector 1: {str(e)}")
            self.vector1 = None

    def actualizar_vector2(self):
        try:
            texto = self.entry_vector2.get()
            self.vector2 = self.parse_vector(texto)
            print(f"Vector 2: {self.vector2}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el Vector 2: {str(e)}")
            self.vector2 = None

    def vaciar_vector1(self):
        self.vector1 = None
        self.entry_vector1.delete(0, ctk.END)

    def vaciar_vector2(self):
        self.vector2 = None
        self.entry_vector2.delete(0, ctk.END)
        
    def parse_vector(self, vector_str):
        try:
            return np.array([float(x.strip()) for x in vector_str.split(',')])
        except:
            return None
            
    def mostrar_resultado(self, resultado, frame, label=None):
        # Limpiar frames
        for widget in self.frame_resultado_grid.winfo_children():
            widget.destroy()
        for widget in self.frame_resultado_label.winfo_children():
            widget.destroy()

        if resultado is not None:
            if label:
                # Mostrar etiqueta
                self.frame_resultado_label.grid_rowconfigure(0, weight=1)
                self.frame_resultado_label.grid_columnconfigure(0, weight=1)
                label_widget = ctk.CTkLabel(self.frame_resultado_label, text=label)
                label_widget.grid(row=0, column=0, sticky="nsew")

            # Mostrar resultado
            self.frame_resultado_grid.grid_rowconfigure(0, weight=1)
            self.frame_resultado_grid.grid_columnconfigure(0, weight=1)
            resultado_widget = ctk.CTkLabel(self.frame_resultado_grid, text=str(resultado))
            resultado_widget.grid(row=0, column=0, sticky="nsew")
        
    def mostrar_error(self, frame, text):
        for widget in frame.winfo_children():
            widget.destroy()
        self.label_err = ctk.CTkLabel(frame, text=text, text_color="red")
        self.label_err.pack(pady=5)
        
    def suma_vectores(self):
        if self.vector1 is None or self.vector2 is None:
            messagebox.showerror("Error", "Ingrese ambos vectores primero")
            return
        try:
            if len(self.vector1) != len(self.vector2):
                messagebox.showerror("Error", "Los vectores deben tener la misma dimensión")
                return
            resultado = self.vector1 + self.vector2
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A + B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al sumar vectores: {e}")
        
    def resta_vectores(self):
        if self.vector1 is None or self.vector2 is None:
            messagebox.showerror("Error", "Ingrese ambos vectores primero")
            return
        try:
            if len(self.vector1) != len(self.vector2):
                messagebox.showerror("Error", "Los vectores deben tener la misma dimensión")
                return
            resultado = self.vector1 - self.vector2
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A - B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al restar vectores: {e}")
        
    def producto_escalar(self):
        if self.vector1 is None or self.vector2 is None:
            messagebox.showerror("Error", "Ingrese ambos vectores primero")
            return
        try:
            if len(self.vector1) != len(self.vector2):
                messagebox.showerror("Error", "Los vectores deben tener la misma dimensión")
                return
            resultado = np.dot(self.vector1, self.vector2)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A · B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular producto escalar: {e}")
        
    def producto_vectorial(self):
        if self.vector1 is None or self.vector2 is None:
            messagebox.showerror("Error", "Ingrese ambos vectores primero")
            return
        try:
            if len(self.vector1) != 3 or len(self.vector2) != 3:
                messagebox.showerror("Error", "El producto vectorial solo está definido para vectores 3D")
                return
            resultado = np.cross(self.vector1, self.vector2)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A × B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular producto vectorial: {e}")
        
    def magnitud_vector(self):
        if self.vector1 is None:
            messagebox.showerror("Error", "Ingrese el vector primero")
            return
        try:
            resultado = np.linalg.norm(self.vector1)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, '|A| =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular magnitud: {e}")
        
    def vector_unitario(self):
        if self.vector1 is None:
            messagebox.showerror("Error", "Ingrese el vector primero")
            return
        try:
            magnitud = np.linalg.norm(self.vector1)
            if magnitud == 0:
                messagebox.showerror("Error", "No se puede calcular el vector unitario de un vector nulo")
                return
            resultado = self.vector1 / magnitud
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'Vector unitario de A =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular vector unitario: {e}")
        
    def angulo_vectores(self):
        if self.vector1 is None or self.vector2 is None:
            messagebox.showerror("Error", "Ingrese ambos vectores primero")
            return
        try:
            if len(self.vector1) != len(self.vector2):
                messagebox.showerror("Error", "Los vectores deben tener la misma dimensión")
                return
            cos_angle = np.dot(self.vector1, self.vector2) / (np.linalg.norm(self.vector1) * np.linalg.norm(self.vector2))
            angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
            resultado = np.degrees(angle)
            self.mostrar_resultado(f"{resultado:.2f}°", self.frame_resultado_grid, 'Ángulo entre A y B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular ángulo: {e}")
        
    def proyeccion_vector(self):
        if self.vector1 is None or self.vector2 is None:
            messagebox.showerror("Error", "Ingrese ambos vectores primero")
            return
        try:
            if len(self.vector1) != len(self.vector2):
                messagebox.showerror("Error", "Los vectores deben tener la misma dimensión")
                return
            v2_norm = np.linalg.norm(self.vector2)
            if v2_norm == 0:
                messagebox.showerror("Error", "No se puede proyectar sobre un vector nulo")
                return
            resultado = (np.dot(self.vector1, self.vector2) / (v2_norm ** 2)) * self.vector2
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'Proyección de A sobre B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular proyección: {e}")