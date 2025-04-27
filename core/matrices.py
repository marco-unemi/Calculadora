import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from styles.styles import estilo_label_titulos, estilo_label
from decimal import Decimal, ROUND_HALF_UP


class Matriz:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.matriz_a = None
        self.matriz_b = None
        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.frame_resultado = None 
        self.filas_a = ctk.StringVar(value="2")
        self.columnas_a = ctk.StringVar(value="2")
        self.filas_b = ctk.StringVar(value="2")
        self.columnas_b = ctk.StringVar(value="2")
        
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
        self.matriz_a_entries = [] 
        self.matriz_b_entries = []
        self.frame_resultado = None 
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Matrices", **estilo_label_titulos).pack(pady=20)
        
        # ------ Fila 1: contenedor de matrices A y B ------ #
        self.frame_matrices = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_matrices.pack(pady=10, padx=20, fill="x") 
        self.frame_matrices.columnconfigure(0, weight=1) 
        self.frame_matrices.columnconfigure(1, weight=1) 
        
        # --- Sección de Matriz A (Columna 0) --- #
        self.frame_matriz_a = ctk.CTkFrame(self.frame_matrices, fg_color=("white", "gray10")) 
        self.frame_matriz_a.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 
        
        self.label_matriz_a_title = ctk.CTkLabel(self.frame_matriz_a, text="Matriz A", **estilo_label) 
        self.label_matriz_a_title.pack(pady=5) 
        
        self.frame_dimension_a = ctk.CTkFrame(self.frame_matriz_a, fg_color=("white", "gray10")) 
        self.frame_dimension_a.pack(pady=5) 
        
        self.label_filas_a = ctk.CTkLabel(self.frame_dimension_a, text="Filas:") 
        self.label_filas_a.pack(side="left", padx=5) 
        self.entry_filas_a = ctk.CTkEntry(self.frame_dimension_a, width=50, textvariable=self.filas_a) 
        self.entry_filas_a.pack(side="left", padx=5)
        self.label_columnas_a = ctk.CTkLabel(self.frame_dimension_a, text="Columnas:") 
        self.label_columnas_a.pack(side="left", padx=5) 
        self.entry_columnas_a = ctk.CTkEntry(self.frame_dimension_a, width=50, textvariable=self.columnas_a)
        self.entry_columnas_a.pack(side="left", padx=5)
        self.boton_crear_a = ctk.CTkButton(self.frame_dimension_a, text="Crear", command=self.generar_matriz_a, fg_color="green", hover_color='#1d5f32', width=10) 
        self.boton_crear_a.pack(side="left", padx=10)
        
        # --- Frame para mostrar la matriz --- #
        self.grid_frame_a = ctk.CTkFrame(self.frame_matriz_a, fg_color=("gray93", "gray12"))
        self.grid_frame_a.pack(pady=5)
        
        # --- Boton de vaciar --- #
        self.frame_botones_a = ctk.CTkFrame(self.frame_matriz_a, fg_color=("white", "gray10")) 
        self.frame_botones_a.pack(pady=10) 
        self.vaciar_a_button = ctk.CTkButton(self.frame_botones_a, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_matriz_a) 
        self.vaciar_a_button.pack(side="left", padx=5) 
        
        # --- Sección de Matriz B (Columna 1) --- #
        self.frame_matriz_b = ctk.CTkFrame(self.frame_matrices, fg_color=("white", "gray10")) 
        self.frame_matriz_b.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") 
        
        self.label_matriz_b_title = ctk.CTkLabel(self.frame_matriz_b, text="Matriz B", **estilo_label) 
        self.label_matriz_b_title.pack(pady=5) 
        
        self.frame_dimension_b = ctk.CTkFrame(self.frame_matriz_b, fg_color=("white", "gray10")) 
        self.frame_dimension_b.pack(pady=5) 
        
        self.label_filas_b = ctk.CTkLabel(self.frame_dimension_b, text="Filas:") 
        self.label_filas_b.pack(side="left", padx=5) 
        self.entry_filas_b = ctk.CTkEntry(self.frame_dimension_b, width=50, textvariable=self.filas_b) 
        self.entry_filas_b.pack(side="left", padx=5)
        self.label_columnas_b = ctk.CTkLabel(self.frame_dimension_b, text="Columnas:") 
        self.label_columnas_b.pack(side="left", padx=5) 
        self.entry_columnas_b = ctk.CTkEntry(self.frame_dimension_b, width=50, textvariable=self.columnas_b)
        self.entry_columnas_b.pack(side="left", padx=5)
        boton_crear_b = ctk.CTkButton(self.frame_dimension_b, text="Crear", command=self.generar_matriz_b, fg_color="green", hover_color='#1d5f32', width=10) 
        boton_crear_b.pack(side="left", padx=10)
        
        # --- Frame para mostrar la matriz --- #
        self.grid_frame_b = ctk.CTkFrame(self.frame_matriz_b, fg_color=("gray93", "gray12"))
        self.grid_frame_b.pack(pady=5)
        
        # --- Boton de vaciar --- #
        self.frame_botones_b = ctk.CTkFrame(self.frame_matriz_b, fg_color=("white", "gray10")) 
        self.frame_botones_b.pack(pady=10) 
        self.vaciar_b_button = ctk.CTkButton(self.frame_botones_b, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_matriz_b) 
        self.vaciar_b_button.pack(side="left", padx=5) 
        
        # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10")) 
        self.frame_operaciones.pack(pady=10, padx=20, fill="x") 
        self.frame_operaciones.columnconfigure(0, weight=1) 
        self.frame_operaciones.columnconfigure(1, weight=1) 
        self.frame_operaciones.columnconfigure(2, weight=1) 
        self.frame_operaciones.columnconfigure(3, weight=1) 
        
        # --- Botones --- #
        self.sumar_button = ctk.CTkButton(self.frame_operaciones, text="Sumar", command=self.sumar)
        self.sumar_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew") 
        self.restar_button = ctk.CTkButton(self.frame_operaciones, text="Restar", command=self.restar) 
        self.restar_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew") 
        self.multiplicar_button = ctk.CTkButton(self.frame_operaciones, text="Multiplicar", command=self.multiplicar) 
        self.multiplicar_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.determinante_a_button = ctk.CTkButton(self.frame_operaciones, text="Determinante (A)", command=self.determinante_a)
        self.determinante_a_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew") 
        self.determinante_b_button = ctk.CTkButton(self.frame_operaciones, text="Determinante (B)", command=self.determinante_b)
        self.determinante_b_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew") 
        self.inversa_a_button = ctk.CTkButton(self.frame_operaciones, text="Inversa (A)", command=self.inversa_a) 
        self.inversa_a_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew") 
        self.inversa_b_button = ctk.CTkButton(self.frame_operaciones, text="Inversa (B)", command=self.inversa_b) 
        self.inversa_b_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew") 
        self.transpuesta_a_button = ctk.CTkButton(self.frame_operaciones, text="Transpuesta (A)", command=self.transpuesta_a)
        self.transpuesta_a_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.transpuesta_b_button = ctk.CTkButton(self.frame_operaciones, text="Transpuesta (B)", command=self.transpuesta_b)
        self.transpuesta_b_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # ------ Fila 3: Resultado ------ #
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=20, padx=20, fill="both", expand=True) 

        self.label_resultado_title = ctk.CTkLabel(self.frame_resultado, text="Resultado:", **estilo_label) 
        self.label_resultado_title.pack(pady=5) 

        # Frame contenedor para resultado y etiqueta
        self.frame_contenedor = ctk.CTkFrame(self.frame_resultado, fg_color=("white", "gray10"))
        self.frame_contenedor.pack(pady=10, padx=20, expand=True)
        
        # Configurar el grid del contenedor
        self.frame_contenedor.grid_columnconfigure(0, weight=1)  # Columna de etiqueta
        self.frame_contenedor.grid_columnconfigure(1, weight=1)  # Columna de matriz

        # Frame para la etiqueta (izquierda)
        self.frame_resultado_label = ctk.CTkFrame(self.frame_contenedor, fg_color=("white", "gray10"))
        self.frame_resultado_label.grid(row=0, column=0, padx=(20,5), pady=10, sticky="nsew")

        # Frame para el resultado (derecha)
        self.frame_resultado_grid = ctk.CTkFrame(self.frame_contenedor, fg_color=("white", "gray10"))
        self.frame_resultado_grid.grid(row=0, column=1, padx=(5,20), pady=10, sticky="nsew")

    # ------ Funciones para generar matrices ------ #
    def generar_matriz_a(self):
        for entry in self.matriz_a_entries:
            entry.destroy()
        self.matriz_a_entries = []
        
        try:
            filas = int(self.filas_a.get())
            columnas = int(self.columnas_a.get())
            self.matriz_a = np.zeros((filas, columnas))
            for i in range(filas):
                for j in range(columnas):
                    entry = ctk.CTkEntry(self.grid_frame_a, width=50, justify="center")
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    entry.bind("<KeyRelease>", lambda event, r=i, c=j: self.actualizar_matriz_a(r, c, event))
                    self.matriz_a_entries.append(entry)
        except ValueError:
            messagebox.showerror("Error", "Ingrese números enteros válidos para las dimensiones de la Matriz A")
            self.matriz_a = None 

    def actualizar_matriz_a(self, fila, columna, event):
        if self.matriz_a is not None: 
            try:
                value = float(event.widget.get()) 
                self.matriz_a[fila, columna] = value 
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido en la Matriz A")
                event.widget.delete(0, ctk.END) 
                self.matriz_a[fila, columna] = 0 

    def generar_matriz_b(self):
        for entry in self.matriz_b_entries:
            entry.destroy()
        self.matriz_b_entries = []
        try:
            filas = int(self.filas_b.get())
            columnas = int(self.columnas_b.get())
            self.matriz_b = np.zeros((filas, columnas))
            for i in range(filas):
                for j in range(columnas):
                    entry = ctk.CTkEntry(self.grid_frame_b, width=50, justify="center")
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    # Vincular al evento <KeyRelease> para actualización en tiempo real
                    entry.bind("<KeyRelease>", lambda event, r=i, c=j: self.actualizar_matriz_b(r, c, event))
                    self.matriz_b_entries.append(entry)
        except ValueError:
            messagebox.showerror("Error:", "Ingrese números enteros válidos para las dimensiones de la Matriz B")
            self.matriz_b = None

    def actualizar_matriz_b(self, fila, columna, event):
        if self.matriz_b is not None:
            try:
                value = float(event.widget.get())
                self.matriz_b[fila, columna] = value
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido en la Matriz B")
                event.widget.delete(0, ctk.END)
                self.matriz_b[fila, columna] = 0

    def vaciar_matriz_a(self):
        self.matriz_a = None
        for entry in self.matriz_a_entries:
            entry.delete(0, ctk.END)
        print('Matriz A vaciada...')
        # Opcional: Restablecer la matriz NumPy a un array vacío con las dimensiones actuales
        try:
            filas = int(self.filas_a.get())
            columnas = int(self.columnas_a.get())
            self.matriz_a = np.zeros((filas, columnas))
        except ValueError:
            # Si las dimensiones no son válidas, se mantendrá en None
            pass
    
    def vaciar_matriz_b(self):
        self.matriz_b = None
        for entry in self.matriz_b_entries:
            entry.delete(0, ctk.END)
        print('Matriz B vaciada...')
        # Opcional: Restablecer la matriz NumPy a un array vacío con las dimensiones actuales
        try:
            filas = int(self.filas_b.get())
            columnas = int(self.columnas_b.get())
            self.matriz_b = np.zeros((filas, columnas))
        except ValueError:
            # Si las dimensiones no son válidas, se mantendrá en None
            pass
        
        
    # ------ Operaciones ------ #
    def sumar(self):
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero")
            return
        if self.matriz_a.shape != self.matriz_b.shape:
            messagebox.showerror("Error", "Las matrices deben tener el mismo tamaño, la misma cantidad de columnas y de filas.")
            return
        try:
            resultado = self.matriz_a + self.matriz_b 
            print(resultado)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A + B =')
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones de las matrices deben ser iguales para la suma")
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al sumar matrices: {e}")
        
    def restar(self):
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero")
            return
        if self.matriz_a.shape != self.matriz_b.shape:
            messagebox.showerror("Error", "Las matrices deben tener el mismo tamaño, la misma cantidad de columnas y de filas.")
            return
        try:
            resultado = self.matriz_a - self.matriz_b
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A - B =')
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones de las matrices deben ser iguales para la resta")
            return
        except Exception as e:
            self.mostrar_resultado(None, self.frame_resultado_grid)
            messagebox.showerror("Error", f"Error al restar matrices: {e}")
            return
        
    def multiplicar(self):
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero")
            return
        try:
            resultado = np.dot(self.matriz_a, self.matriz_b)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A × B =')
        except ValueError:
            messagebox.showerror("Error", "El número de columnas de la Matriz A debe ser igual al número de filas de la Matriz B para la multiplicación")
            return
        except Exception as e:
            self.mostrar_resultado(None, self.frame_resultado_grid)
            messagebox.showerror("Error", f"Error al multiplicar matrices: {e}")
            return
        
    def determinante_a(self):
        if self.matriz_a is None:
            messagebox.showerror("Error", "Cargue la matriz (A) primero.")
            return
        try:
            resultado = np.linalg.det(self.matriz_a)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'det(A) =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_label, f"Error al calcular el determinante de A: {e}")
        
    def determinante_b(self):
        if self.matriz_b is None:
            messagebox.showerror("Error", "Cargue la matriz (B) primero.")
            return
        try:
            resultado = np.linalg.det(self.matriz_b)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'det(B) =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_label, f"Error al calcular el determinante de B: {e}")
        
    def inversa_a(self):
        if self.matriz_a is None:
            messagebox.showerror("Error", "Cargue la matriz (A) primero.")
            return
        try:
            det = np.linalg.det(self.matriz_a) 
            if det == 0:
                messagebox.showerror("Error", "La Matriz A no es invertible (su determinante es cero).")
                return
            resultado = np.linalg.inv(self.matriz_a) 
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A⁻¹ =')

        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular la inversa de A: {e}")
        
    def inversa_b(self):
        if self.matriz_b is None:
            messagebox.showerror("Error", "Cargue la matriz (B) primero.")
            return
        try:
            det = np.linalg.det(self.matriz_b) 
            if det == 0:
                messagebox.showerror("Error", "La Matriz B no es invertible (su determinante es cero).")
                return
            resultado = np.linalg.inv(self.matriz_b) 
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'B⁻¹ =')

        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular la inversa de B: {e}")

    def transpuesta_a(self):
        if self.matriz_a is None:
            messagebox.showerror("Error", "Cargue la matriz (A) primero.")
            return
        try:
            resultado = np.transpose(self.matriz_a)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'Aᵀ =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular la transpuesta de A: {e}")
            
    def transpuesta_b(self):
        if self.matriz_b is None:
            messagebox.showerror("Error", "Cargue la matriz (B) primero.")
            return
        try:
            resultado = np.transpose(self.matriz_b)
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'Bᵀ =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular la transpuesta de B: {e}")

    # ------ Funciones para mostrar errores y resultados ------ #
    def mostrar_error(self, frame, text):
        for widget in frame.winfo_children():
            widget.destroy()   
            
        self.label_err = ctk.CTkLabel(frame, text=text, text_color="red")
        self.label_err.pack()

    def mostrar_resultado(self, matriz, frame, label=None):
        # Limpiar frames
        for widget in self.frame_resultado_grid.winfo_children():
            widget.destroy()
            
        for widget in self.frame_resultado_label.winfo_children():
            widget.destroy()

        if matriz is not None:
            # Si es un escalar (determinante)
            if isinstance(matriz, (int, float, np.float64, np.float32)):
                if label:
                    # Mostrar etiqueta
                    self.frame_resultado_label.grid_rowconfigure(0, weight=1)
                    self.frame_resultado_label.grid_columnconfigure(0, weight=1)
                    label_widget = ctk.CTkLabel(self.frame_resultado_label, text=label)
                    label_widget.grid(row=0, column=0, sticky="nsew")

                # Configurar grid para el resultado escalar
                self.frame_resultado_grid.grid_rowconfigure(0, weight=1)
                self.frame_resultado_grid.grid_columnconfigure(0, weight=1)
                
                # Formatear el número
                valor = Decimal(str(matriz)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                if valor == valor.to_integral():
                    result = int(valor)
                else:
                    result = float(valor)
                
                resultado = ctk.CTkLabel(self.frame_resultado_grid, width=40, justify="center", 
                                      text=str(result), fg_color=("white", "gray10"))
                resultado.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            
            # Si es una matriz
            else:
                filas, columnas = matriz.shape 
                if label:
                    # Mostrar etiqueta
                    self.frame_resultado_label.grid_rowconfigure(0, weight=1)
                    self.frame_resultado_label.grid_columnconfigure(0, weight=1)
                    label_widget = ctk.CTkLabel(self.frame_resultado_label, text=label)
                    label_widget.grid(row=0, column=0, sticky="nsew")

                # Configurar grid para la matriz
                for i in range(filas):
                    self.frame_resultado_grid.grid_rowconfigure(i, weight=1)
                for j in range(columnas):
                    self.frame_resultado_grid.grid_columnconfigure(j, weight=1)

                # Mostrar matriz
                for i in range(filas):
                    for j in range(columnas):
                        valor = Decimal(str(matriz[i, j])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                        if valor == valor.to_integral():
                            result = int(valor)
                        else:
                            result = float(valor)

                        resultado = ctk.CTkLabel(self.frame_resultado_grid, width=40, justify="center", 
                                              text=str(result), fg_color=("white", "gray10")) 
                        resultado.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        else:
            # Centrar mensaje de no hay resultado
            self.frame_resultado_grid.grid_rowconfigure(0, weight=1)
            self.frame_resultado_grid.grid_columnconfigure(0, weight=1)
            label_vacio = ctk.CTkLabel(self.frame_resultado_grid, text="No hay resultado para mostrar.")
            label_vacio.grid(row=0, column=0, sticky="nsew")
            
            