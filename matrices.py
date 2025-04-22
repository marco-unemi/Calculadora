import customtkinter as ctk
from tkinter import messagebox
from utils import estilo_label, estilo_boton, crear_scrollable_frame
import numpy as np

class OperacionesMatrices:
    def __init__(self, workspace_frame):
        # Constructor de la clase OperacionesMatrices.
        # Inicializa la interfaz y las variables necesarias para las operaciones con matrices.
        self.workspace_frame = workspace_frame # Frame principal donde se mostrará el contenido de esta sección.
        self.matriz_a = None             # Almacenará la primera matriz (Matriz A) como un array de NumPy. Inicialmente está vacía.
        self.matriz_b = None             # Almacenará la segunda matriz (Matriz B) como un array de NumPy. Inicialmente está vacía.
        self.resultado_label = None      # Etiqueta para mostrar mensajes o el resultado de las operaciones (aunque luego se usa un frame).
        self.filas_a_var = ctk.StringVar(value="2")   # Variable de cadena para almacenar el número de filas de la Matriz A. Valor inicial "2".
        self.columnas_a_var = ctk.StringVar(value="2")# Variable de cadena para almacenar el número de columnas de la Matriz A. Valor inicial "2".
        self.filas_b_var = ctk.StringVar(value="2")   # Variable de cadena para almacenar el número de filas de la Matriz B. Valor inicial "2".
        self.columnas_b_var = ctk.StringVar(value="2")# Variable de cadena para almacenar el número de columnas de la Matriz B. Valor inicial "2".
        self.matriz_a_entries = []       # Lista para almacenar los widgets de entrada (ctk.CTkEntry) de los elementos de la Matriz A.
        self.matriz_b_entries = []       # Lista para almacenar los widgets de entrada de los elementos de la Matriz B.
        self.scrollable_frame = None     # Frame con scroll para contener toda la interfaz de operaciones con matrices si el contenido es muy grande.
        self.grid_frame_resultado = None # Frame con estructura de grid para mostrar el resultado de las operaciones matriciales.

    def limpiar_workspace(self):
        # Limpia el contenido previo dentro del workspace_frame.
        for widget in self.workspace_frame.winfo_children():
            widget.destroy() # Elimina cada widget hijo del workspace_frame.
        self.matriz_a_entries = [] # Reinicia la lista de entradas de la Matriz A.
        self.matriz_b_entries = [] # Reinicia la lista de entradas de la Matriz B.
        self.scrollable_frame = None # Elimina la referencia al frame con scroll.
        self.grid_frame_resultado = None # Elimina la referencia al frame de resultados.

    def mostrar_contenido(self):
        # Limpia el área antes de agregar contenido nuevo.
        self.limpiar_workspace()

        # Crear el frame con scroll usando la función de utils.
        self.scrollable_frame = crear_scrollable_frame(self.workspace_frame)

        # Título principal.
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Operaciones con Matrices y Vectores", **estilo_label(font_size=16))
        title_label.pack(pady=20)

        # --- Fila 1: Matrices A y B ---
        frame_matrices = ctk.CTkFrame(self.scrollable_frame) # Frame para contener las secciones de Matriz A y Matriz B.
        frame_matrices.pack(pady=10, padx=20, fill="x") # Empaquetar el frame con relleno vertical y horizontal, y se expande horizontalmente.
        frame_matrices.columnconfigure(0, weight=1) # Configurar la primera columna para que se expanda si la ventana se redimensiona.
        frame_matrices.columnconfigure(1, weight=1) # Configurar la segunda columna para que se expanda si la ventana se redimensiona.

        # Sección de Matriz A (Columna 0)
        frame_matriz_a = ctk.CTkFrame(frame_matrices) # Frame para la interfaz de la Matriz A.
        frame_matriz_a.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") # Colocar en la primera fila, primera columna del frame_matrices, con relleno y se expande en todas direcciones.

        label_matriz_a_title = ctk.CTkLabel(frame_matriz_a, text="Matriz A", **estilo_label()) # Etiqueta con el título "Matriz A".
        label_matriz_a_title.pack(pady=5) # Empaquetar con relleno vertical.

        frame_dimension_a = ctk.CTkFrame(frame_matriz_a) # Frame para contener las entradas de las dimensiones de la Matriz A.
        frame_dimension_a.pack(pady=5) # Empaquetar con relleno vertical.
        label_filas_a = ctk.CTkLabel(frame_dimension_a, text="Filas:", **estilo_label()) # Etiqueta "Filas:".
        label_filas_a.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        entry_filas_a = ctk.CTkEntry(frame_dimension_a, width=50, textvariable=self.filas_a_var) # Campo de entrada para el número de filas de A.
        entry_filas_a.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        label_columnas_a = ctk.CTkLabel(frame_dimension_a, text="Columnas:", **estilo_label()) # Etiqueta "Columnas:".
        label_columnas_a.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        entry_columnas_a = ctk.CTkEntry(frame_dimension_a, width=50, textvariable=self.columnas_a_var) # Campo de entrada para el número de columnas de A.
        entry_columnas_a.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        boton_crear_a = ctk.CTkButton(frame_dimension_a, text="Crear", command=self.crear_interfaz_matriz_a, **estilo_boton(fg_color="green", hover_color='#1d5f32'), width=10) # Botón para crear la interfaz de entrada de la Matriz A.
        boton_crear_a.pack(side="left", padx=10) # Empaquetar a la izquierda con relleno horizontal.

        self.grid_frame_a = ctk.CTkFrame(frame_matriz_a) # Frame con estructura de grid para los campos de entrada de los elementos de la Matriz A.
        self.grid_frame_a.pack(pady=5) # Empaquetar con relleno vertical.

        frame_botones_a = ctk.CTkFrame(frame_matriz_a) # Frame para contener los botones de acción de la Matriz A.
        frame_botones_a.pack(pady=5) # Empaquetar con relleno vertical.
        vaciar_a_button = ctk.CTkButton(frame_botones_a, text="Vaciar", command=self.vaciar_matriz_a, **estilo_boton(fg_color="#df0000", hover_color='#b81414')) # Botón para vaciar la Matriz A.
        vaciar_a_button.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.

        # Sección de Matriz B (Columna 1)
        frame_matriz_b = ctk.CTkFrame(frame_matrices) # Frame para la interfaz de la Matriz B.
        frame_matriz_b.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") # Colocar en la primera fila, segunda columna del frame_matrices, con relleno y se expande en todas direcciones.

        label_matriz_b_title = ctk.CTkLabel(frame_matriz_b, text="Matriz B", **estilo_label()) # Etiqueta con el título "Matriz B".
        label_matriz_b_title.pack(pady=5) # Empaquetar con relleno vertical.

        frame_dimension_b = ctk.CTkFrame(frame_matriz_b) # Frame para contener las entradas de las dimensiones de la Matriz B.
        frame_dimension_b.pack(pady=5) # Empaquetar con relleno vertical.
        label_filas_b = ctk.CTkLabel(frame_dimension_b, text="Filas:", **estilo_label()) # Etiqueta "Filas:".
        label_filas_b.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        entry_filas_b = ctk.CTkEntry(frame_dimension_b, width=50, textvariable=self.filas_b_var) # Campo de entrada para el número de filas de B.
        entry_filas_b.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        label_columnas_b = ctk.CTkLabel(frame_dimension_b, text="Columnas:", **estilo_label()) # Etiqueta "Columnas:".
        label_columnas_b.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        entry_columnas_b = ctk.CTkEntry(frame_dimension_b, width=50, textvariable=self.columnas_b_var) # Campo de entrada para el número de columnas de B.
        entry_columnas_b.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.
        boton_crear_b = ctk.CTkButton(frame_dimension_b, text="Crear", command=self.crear_interfaz_matriz_b, **estilo_boton(fg_color="green", hover_color='#1d5f32'), width=10) # Botón para crear la interfaz de entrada de la Matriz B.
        boton_crear_b.pack(side="left", padx=10) # Empaquetar a la izquierda con relleno horizontal.

        self.grid_frame_b = ctk.CTkFrame(frame_matriz_b) # Frame con estructura de grid para los campos de entrada de los elementos de la Matriz B.
        self.grid_frame_b.pack(pady=5) # Empaquetar con relleno vertical.

        frame_botones_b = ctk.CTkFrame(frame_matriz_b) # Frame para contener los botones de acción de la Matriz B.
        frame_botones_b.pack(pady=5) # Empaquetar con relleno vertical.
        vaciar_b_button = ctk.CTkButton(frame_botones_b, text="Vaciar", command=self.vaciar_matriz_b, **estilo_boton(fg_color="#df0000", hover_color='#b81414')) # Botón para vaciar la Matriz B.
        vaciar_b_button.pack(side="left", padx=5) # Empaquetar a la izquierda con relleno horizontal.

        # --- Fila 2: Botones de Operaciones ---
        frame_operaciones = ctk.CTkFrame(self.scrollable_frame) # Frame para contener los botones de las operaciones matriciales.
        frame_operaciones.pack(pady=10, padx=20, fill="x") # Empaquetar con relleno vertical y horizontal, y se expande horizontalmente.
        frame_operaciones.columnconfigure(0, weight=1) # Configurar la primera columna para que se expanda.
        frame_operaciones.columnconfigure(1, weight=1) # Configurar la segunda columna para que se expanda.
        frame_operaciones.columnconfigure(2, weight=1) # Configurar la tercera columna para que se expanda.

        sumar_button = ctk.CTkButton(frame_operaciones, text="Sumar", command=self.sumar_matrices, **estilo_boton()) # Botón para realizar la suma de matrices.
        sumar_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew") # Colocar en la primera fila, primera columna, con relleno y se expande horizontalmente.
        restar_button = ctk.CTkButton(frame_operaciones, text="Restar", command=self.restar_matrices, **estilo_boton()) # Botón para realizar la resta de matrices.
        restar_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # Colocar en la primera fila, segunda columna, con relleno y se expande horizontalmente.
        multiplicar_button = ctk.CTkButton(frame_operaciones, text="Multiplicar", command=self.multiplicar_matrices, **estilo_boton()) # Botón para realizar la multiplicación de matrices.
        multiplicar_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew") # Colocar en la primera fila, tercera columna, con relleno y se expande horizontalmente.
        determinante_button = ctk.CTkButton(frame_operaciones, text="Determinante (A)", command=self.calcular_determinante, **estilo_boton()) # Botón para calcular el determinante de la Matriz A.
        determinante_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew") # Colocar en la segunda fila, primera columna, con relleno y se expande horizontalmente.
        inversa_button = ctk.CTkButton(frame_operaciones, text="Inversa (A)", command=self.calcular_inversa, **estilo_boton()) # Botón para calcular la inversa de la Matriz A.
        inversa_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # Colocar en la segunda fila, segunda columna, con relleno y se expande horizontalmente.
        valores_propios_button = ctk.CTkButton(frame_operaciones, text="Valores Propios y Vectores Propios (A)", command=self.calcular_valores_propios, **estilo_boton()) # Botón para calcular los valores y vectores propios de la Matriz A.
        valores_propios_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew") # Colocar en la segunda fila, tercera columna, con relleno y se expande horizontalmente.
        solu_ecuaciones_button = ctk.CTkButton(frame_operaciones, text="Solucion de un sistema de ecuaciones", command=self.calcular_sistemas_de_ecuaciones, **estilo_boton()) # Botón para resolver un sistema de ecuaciones lineales.
        solu_ecuaciones_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew") # Colocar en la tercera fila, primera columna, con relleno y se expande horizontalmente.

        # --- Fila 3: Resultado ---
        frame_resultado = ctk.CTkFrame(self.scrollable_frame) # Frame para mostrar el resultado de las operaciones.
        frame_resultado.pack(pady=20, padx=20, fill="x") # Empaquetar con relleno vertical y horizontal, y se expande horizontalmente.

        label_resultado_title = ctk.CTkLabel(frame_resultado, text="Resultado:", **estilo_label(font_size=16)) # Etiqueta con el título "Resultado:".
        label_resultado_title.pack(pady=5) # Empaquetar con relleno vertical.

        self.grid_frame_resultado = ctk.CTkFrame(frame_resultado, width=600) # Frame con estructura de grid para mostrar la matriz o vector resultante.
        self.grid_frame_resultado.pack(pady=10) # Empaquetar con relleno vertical.

# MATRICES
    def crear_interfaz_matriz_a(self):
        # Crea la interfaz de entrada para la Matriz A basándose en las dimensiones ingresadas.
        for entry in self.matriz_a_entries:
            entry.destroy() # Elimina los widgets de entrada de la Matriz A si ya existían.
        self.matriz_a_entries = [] # Reinicia la lista para almacenar los nuevos widgets de entrada.
        try:
            filas = int(self.filas_a_var.get())     # Obtiene el número de filas ingresado y lo convierte a entero.
            columnas = int(self.columnas_a_var.get()) # Obtiene el número de columnas ingresado y lo convierte a entero.
            self.matriz_a = np.zeros((filas, columnas))  # Inicializa la matriz A como un array de NumPy de la dimensión especificada, lleno de ceros.
            for i in range(filas):
                for j in range(columnas):
                    entry = ctk.CTkEntry(self.grid_frame_a, width=50) # Crea un nuevo campo de entrada.
                    entry.grid(row=i, column=j, padx=5, pady=5)      # Coloca el campo de entrada en la grid.
                    entry.bind("<FocusOut>", lambda event, r=i, c=j: self.actualizar_matriz_a(r, c, event))
                    # Vincula el evento "FocusOut" (cuando el usuario sale del campo de entrada) a la función actualizar_matriz_a.
                    # La función lambda captura la fila (r) y la columna (c) para saber qué elemento de la matriz actualizar.
                    self.matriz_a_entries.append(entry) # Agrega el campo de entrada a la lista de entradas de la Matriz A.
        except ValueError:
            messagebox.showerror("Error", "Ingrese números enteros válidos para las dimensiones de la Matriz A")
            self.matriz_a = None # Si hay un error al convertir las dimensiones, la Matriz A se establece a None.

    def actualizar_matriz_a(self, fila, columna, event):
        # Actualiza el valor correspondiente en la Matriz A cuando un campo de entrada pierde el foco.
        if self.matriz_a is not None: # Asegura que la Matriz A haya sido inicializada.
            try:
                value = float(event.widget.get()) # Obtiene el valor del campo de entrada y lo convierte a float.
                self.matriz_a[fila, columna] = value # Actualiza el elemento correspondiente en el array de NumPy.
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido en la Matriz A")
                event.widget.delete(0, ctk.END) # Limpia el campo de entrada si el valor no es un número válido.
                self.matriz_a[fila, columna] = 0  # Establece el valor en la matriz a 0 (o algún otro valor por defecto).

    def crear_interfaz_matriz_b(self):
        # Crea la interfaz de entrada para la Matriz B, similar a crear_interfaz_matriz_a.
        for entry in self.matriz_b_entries:
            entry.destroy()
        self.matriz_b_entries = []
        try:
            filas = int(self.filas_b_var.get())
            columnas = int(self.columnas_b_var.get())
            self.matriz_b = np.zeros((filas, columnas))  # Inicializa la matriz B con ceros
            for i in range(filas):
                for j in range(columnas):
                    entry = ctk.CTkEntry(self.grid_frame_b, width=50)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    entry.bind("<FocusOut>", lambda event, r=i, c=j: self.actualizar_matriz_b(r, c, event))
                    self.matriz_b_entries.append(entry)
        except ValueError:
            messagebox.showerror("Error:", "Ingrese números enteros válidos para las dimensiones de la Matriz B")
            self.matriz_b = None

    def actualizar_matriz_b(self, fila, columna, event):
        # Actualiza el valor correspondiente en la Matriz B cuando un campo de entrada pierde el foco.
        if self.matriz_b is not None:
            try:
                value = float(event.widget.get())
                self.matriz_b[fila, columna] = value
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido en la Matriz B")
                event.widget.delete(0, ctk.END)
                self.matriz_b[fila, columna] = 0  # O algún otro valor por defecto

    def vaciar_matriz_a(self):
        # Restablece la Matriz A a None y limpia los campos de entrada.
        self.matriz_a = None
        for entry in self.matriz_a_entries:
            entry.delete(0, ctk.END)

    def vaciar_matriz_b(self):
        # Restablece la Matriz B a None y limpia los campos de entrada.
        self.matriz_b = None
        for entry in self.matriz_b_entries:
            entry.delete(0, ctk.END)


    # OPERACIONES
    def sumar_matrices(self):
        # Realiza la suma de las matrices A y B si ambas están cargadas y tienen las mismas dimensiones.
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero")
            return
        if self.matriz_a.shape != self.matriz_b.shape:
            messagebox.showerror("Error", "Las matrices deben tener el mismo tamaño, la misma cantidad de columnas y de filas.")
            return
        try:
            resultado = self.matriz_a + self.matriz_b # Realiza la suma utilizando la funcionalidad de NumPy.
            self.mostrar_resultado(resultado, self.grid_frame_resultado) # Muestra el resultado en la interfaz.
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones de las matrices deben ser iguales para la suma")
        except Exception as e:
            self.mostrar_resultado(None, self.grid_frame_resultado)
            messagebox.showerror("Error", f"Error al sumar matrices: {e}")

    def restar_matrices(self):
        # Realiza la resta de las matrices A y B si ambas están cargadas y tienen las mismas dimensiones.
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero")
            return
        if self.matriz_a.shape != self.matriz_b.shape:
            messagebox.showerror("Error", "Las matrices deben tener el mismo tamaño, la misma cantidad de columnas y de filas.")
            return
        try:
            resultado = self.matriz_a - self.matriz_b # Realiza la resta utilizando la funcionalidad de NumPy.
            self.mostrar_resultado(resultado, self.grid_frame_resultado) # Muestra el resultado en la interfaz.
        except ValueError:
            messagebox.showerror("Error", "Las dimensiones de las matrices deben ser iguales para la resta")
            return
        except Exception as e:
            self.mostrar_resultado(None, self.grid_frame_resultado)
            messagebox.showerror("Error", f"Error al restar matrices: {e}")
            return

    def multiplicar_matrices(self):
        # Realiza la multiplicación de las matrices A y B si ambas están cargadas y sus dimensiones son compatibles.
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero")
            return
        try:
            resultado = np.dot(self.matriz_a, self.matriz_b) # Realiza la multiplicación matricial utilizando la función dot de NumPy.
            self.mostrar_resultado(resultado, self.grid_frame_resultado) # Muestra el resultado en la interfaz.
        except ValueError:
            messagebox.showerror("Error", "El número de columnas de la Matriz A debe ser igual al número de filas de la Matriz B para la multiplicación")
            return
        except Exception as e:
            self.mostrar_resultado(None, self.grid_frame_resultado)
            messagebox.showerror("Error", f"Error al multiplicar matrices: {e}")
            return

    def calcular_determinante(self):
        # Calcula el determinante de la Matriz A si está cargada.
        if self.matriz_a is None:
            messagebox.showerror("Error", "Cargue la matriz (A) primero.")
            return
        try:
            for widget in self.grid_frame_resultado.winfo_children():
                widget.destroy() # Limpia el frame de resultados antes de mostrar el determinante.

            resultado = int(np.linalg.det(self.matriz_a)) # Calcula el determinante utilizando la función det de linalg en NumPy.
            # Se convierte a int para mostrar un valor entero si el determinante es entero.

            lambda_label = ctk.CTkLabel(self.grid_frame_resultado, text=f"Det: ", **estilo_label())
            lambda_label.grid(row=1, column=0, padx=(5, 0), pady=5, sticky="w")

            valor_entry = ctk.CTkEntry(self.grid_frame_resultado, width=70)
            valor_entry.insert(0, resultado)
            valor_entry.configure(state="disabled") # El campo de entrada se deshabilita para que el usuario no pueda editar el resultado.
            valor_entry.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="e")

        except Exception as e:
            self.mostrar_resultado(None, self.grid_frame_resultado)
            self.resultado_label.configure(text=f"Error al sacar el determinante: {e}", **estilo_label())
            return

    def calcular_inversa(self):
        # Calcula la inversa de la Matriz A si está cargada y es invertible (determinante no es cero).
        if self.matriz_a is None:
            messagebox.showerror("Error", "Cargue la matriz (A) primero.")
            return
        try:
            det = np.linalg.det(self.matriz_a) # Calcula el determinante para verificar si la matriz es invertible.
            if det == 0:
                messagebox.showerror("Error", "La Matriz A no es invertible (su determinante es cero).")
                return
            resultado = np.linalg.inv(self.matriz_a) # Calcula la inversa utilizando la función inv de linalg en NumPy.
            self.mostrar_resultado(resultado, self.grid_frame_resultado) # Muestra la matriz inversa en la interfaz.

        except Exception as e:
            self.mostrar_resultado(None, self.grid_frame_resultado)
            messagebox.showerror("Error", f"Error al calcular la inversa de A: {e}")
            return

    def calcular_valores_propios(self):
        # Calcula los valores y vectores propios de la Matriz A si está cargada.
        if self.matriz_a is None:
            messagebox.showerror("Error", "Cargue la matriz (A) primero.")
            return
        try:
            valores_propios, vectores_propios = np.linalg.eig(self.matriz_a) # Calcula los valores y vectores propios utilizando la función eig de linalg en NumPy.
            self.mostrar_resultado_vector(valores_propios, vectores_propios, self.grid_frame_resultado) # Muestra los resultados en la interfaz.
        except np.linalg.LinAlgError:
            self.mostrar_resultado_vector(None, self.grid_frame_resultado)
            messagebox.showerror("Error", "Error al calcular los valores propios de la Matriz A.")
            return
        except Exception as e:
            self.mostrar_resultado_vector(None, self.grid_frame_resultado)
            messagebox.showerror("Error", f"Error al calcular los valores propios de la Matriz A: {e}")
            return

    def calcular_sistemas_de_ecuaciones(self):
        # Resuelve un sistema de ecuaciones lineales Ax = b, donde A es self.matriz_a y b es self.matriz_b.
        if self.matriz_a is None or self.matriz_b is None:
            messagebox.showerror("Error", "Cargue ambas matrices primero.")
            return

        if self.matriz_b.shape[1] > 1:
            messagebox.showerror("Error", "El vector de terminos independientes no debe de tener mas de 1 columna.")
            return
        try:
            solucion = np.linalg.solve(self.matriz_a, self.matriz_b) # Resuelve el sistema utilizando la función solve de linalg en NumPy.
            self.mostrar_resultado(solucion, self.grid_frame_resultado) # Muestra la solución (vector x) en la interfaz.
        except ValueError:
            self.mostrar_resultado_vector(None, self.grid_frame_resultado)
            messagebox.showerror("Error", "Error al calcular .....") # Mensaje de error genérico, podría ser más específico.
            return
        except Exception as e:
            self.mostrar_resultado_vector(None, self.grid_frame_resultado)
            messagebox.showerror("Error", f"Error al calcular el sistema de ecuaciones: {e}")
            return
    
    # RESULTADO
    def mostrar_resultado(self, matriz, frame_grid):
        # Función para mostrar una matriz (resultado de una operación) en el frame de resultados.
        # Limpiar cualquier widget anterior en el frame de resultado
        for widget in frame_grid.winfo_children():
            widget.destroy() # Elimina todos los widgets que pudieran estar en el frame de resultados.

        if matriz is not None:
            filas, columnas = matriz.shape # Obtiene las dimensiones de la matriz resultante.
            for i in range(filas):
                for j in range(columnas):
                    valor = matriz[i, j] # Obtiene el valor del elemento en la posición (i, j).
                    if valor == int(valor):
                        result = int(valor) # Si el valor es entero, lo convierte a entero para mostrarlo sin decimales innecesarios.
                    else:
                        result = round(valor, 2) # Si no es entero, lo redondea a 2 decimales para una mejor presentación.

                    entry_resultado = ctk.CTkEntry(frame_grid, width=70) # Crea un nuevo campo de entrada para mostrar el resultado.
                    entry_resultado.insert(0, result) # Inserta el valor del resultado en el campo de entrada.
                    entry_resultado.configure(state="disabled") # Deshabilita la edición del campo de entrada para que el usuario no pueda modificar el resultado.
                    entry_resultado.grid(row=i, column=j, padx=5, pady=5) # Coloca el campo de entrada en la grid del frame de resultados.
        else:
            label_vacio = ctk.CTkLabel(frame_grid, text="No hay resultado para mostrar.")
            label_vacio.pack() # Si la matriz es None (por ejemplo, por un error en la operación), muestra un mensaje indicando que no hay resultado.

    def mostrar_resultado_vector(self, valores_propios, vectores_propios, frame_grid):
        # Función para mostrar los valores y vectores propios en el frame de resultados.
        for widget in frame_grid.winfo_children():
            widget.destroy() # Limpia cualquier widget anterior en el frame de resultados.

        row = 0

        if valores_propios is not None:
            num_valores = valores_propios.shape[0] # Obtiene el número de valores propios.
            lambda_label = ctk.CTkLabel(frame_grid, text=f"Valores propios:", **estilo_label())
            lambda_label.grid(row=row, column=1, padx=5, pady=5)

            row += 1

            for i in range(num_valores):
                valor = valores_propios[i]
                result_valor = int(valor) if valor == int(valor) else round(valor, 2) # Formatea el valor propio.

                lambda_label = ctk.CTkLabel(frame_grid, text=f"λ{i+1}: ", **estilo_label())
                lambda_label.grid(row=row, column=0, padx=(5, 0), pady=5, sticky="w")

                # Entrada para el valor propio
                valor_entry = ctk.CTkEntry(frame_grid, width=70)
                valor_entry.insert(0, result_valor)
                valor_entry.configure(state="disabled")
                valor_entry.grid(row=row, column=1, padx=(0, 5), pady=5, sticky="e")

                row += 1  # Pasar a la siguiente fila

        if vectores_propios is not None:
            num_vectores = vectores_propios.shape[1]  # Los vectores propios son las columnas
            num_componentes = vectores_propios.shape[0] # Número de componentes por vector

            lambda_label = ctk.CTkLabel(frame_grid, text=f"Vectores propios:", **estilo_label())
            lambda_label.grid(row=row, column=1, padx=5, pady=5)

            row += 1

            for i in range(num_vectores):
                # Etiqueta para el vector propio
                vector_label = ctk.CTkLabel(frame_grid, text=f"V{i+1}: ", **estilo_label())
                vector_label.grid(row=row, column=0, padx=(5, 0), pady=5, sticky="w")

                # Mostrar los componentes del vector propio en columnas adyacentes
                for j in range(num_componentes):
                    valor_componente = vectores_propios[j, i] # Acceder por fila (componente) y luego columna (vector)
                    result_componente = int(valor_componente) if valor_componente == int(valor_componente) else round(valor_componente, 2)

                    componente_entry = ctk.CTkEntry(frame_grid, width=70)
                    componente_entry.insert(0, result_componente)
                    componente_entry.configure(state="disabled")
                    componente_entry.grid(row=row, column=j + 1, padx=(0, 5), pady=5, sticky="e")

                row += 1

        if valores_propios is None and vectores_propios is None:
            label_vacio = ctk.CTkLabel(frame_grid, text="No hay resultado para mostrar.")
            label_vacio.pack()