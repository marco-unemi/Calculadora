import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import numpy as np
from core.ecuaciones_lineales import resolver_sistema_de_ecuaciones



class UISistemaEcuaciones:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.dimension = 3  # Por defecto 3x3
        self.entries = []   # Para guardar referencias a los inputs
        

    def _build_ui(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.workspace_frame, text="Sistemas de Ecuaciones Lineales", **estilo_label_titulos).pack(pady=20)
        
        self.frame_sistema = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_sistema.pack(pady=10, padx=20, fill="x")
        self.frame_sistema.grid_rowconfigure(0, weight=1)
        self.frame_sistema.grid_columnconfigure(0, weight=1)
        
        self.frame_sistema_ecuaciones = ctk.CTkFrame(self.frame_sistema, fg_color=("white", "gray10"))
        self.frame_sistema_ecuaciones.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.frame_dimension = ctk.CTkFrame(self.frame_sistema_ecuaciones, fg_color=("white", "gray10")) 
        self.frame_dimension.pack(pady=5)
        
        ctk.CTkLabel(self.frame_dimension, text="Dimensiones:").pack(side="left", padx=5)
        
        self.boton_aumentar = ctk.CTkButton(self.frame_dimension, text="Aumentar", command=self.aumentar_dimension, fg_color="green", hover_color='#1d5f32', width=10) 
        self.boton_aumentar.pack(side="left", padx=10)
        
        self.boton_disminuir = ctk.CTkButton(self.frame_dimension, text="Disminuir", command=self.disminuir_dimension, fg_color="green", hover_color='#1d5f32', width=10) 
        self.boton_disminuir.pack(side="left", padx=10)
        
        # --- Frame para mostrar el sistema de ecuaciones --- #
        self.grid_frame_sistema = ctk.CTkFrame(self.frame_sistema_ecuaciones, fg_color=("gray93", "gray12"))
        self.grid_frame_sistema.pack(pady=40)
        self.renderizar_celdas()
        
        # --- Boton de vaciar --- #
        self.frame_botones = ctk.CTkFrame(self.frame_sistema_ecuaciones, fg_color=("white", "gray10")) 
        self.frame_botones.pack(pady=10) 
        self.vaciar_a_button = ctk.CTkButton(self.frame_botones, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_todos_los_campos_de_entrada) 
        self.vaciar_a_button.pack(padx=5) 
        
         # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10")) 
        self.frame_operaciones.pack(pady=10, padx=20, fill="x")
        
        self.resolver_button = ctk.CTkButton(self.frame_operaciones, text="Resolver", command=self.resolver_sistema)
        self.resolver_button.pack(padx=5)
        
        # ------ Fila 3: Resultado ------ #
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.label_resultado_title = ctk.CTkLabel(self.frame_resultado, text="Resultado:", **estilo_label) 
        self.label_resultado_title.pack(pady=5)

         # Frame contenedor para resultado y etiqueta
        self.frame_contenedor = ctk.CTkFrame(self.frame_resultado, fg_color=("white", "gray10"))
        self.frame_contenedor.pack(pady=10, padx=20, expand=True, fill="x")
        
        
    def vaciar_todos_los_campos_de_entrada(self):
        for i in range(self.dimension):
            for j in range(self.dimension + 1):
                self.entries[i][j].delete(0, "end")

    def _leer_entradas(self):
        try:
            n = self.dimension
            A = np.zeros((n, n))
            b = np.zeros(n)
            
            # Leer los datos de los entries
            for i in range(n):
                for j in range(n):
                    val = self.entries[i][j].get()
                    if val.strip() == '':
                        raise ValueError(f"Falta un coeficiente en la fila {i+1}, columna {j+1}")
                    A[i, j] = float(val)
                val_b = self.entries[i][n].get()
                if val_b.strip() == '':
                    raise ValueError(f"Falta el término independiente en la fila {i+1}")
                b[i] = float(val_b)
                
            return A, b

        except ValueError as e:
            self._preparar_display_resultado()
            # Para que el mensaje de error también aparezca centrado
            error_msg = f"Error en los datos de entrada:{e}\nPor favor, verifica los valores ingresados."
            print(error_msg) 
            return None 

    def aumentar_dimension(self):
        if self.dimension < 4:  # Limita el tamaño máximo si quieres
            self.dimension += 1
            self.renderizar_celdas()

    def disminuir_dimension(self):
        if self.dimension > 2:  # Limita el tamaño mínimo si quieres
            self.dimension -= 1
            self.renderizar_celdas()

    def resolver_sistema(self):
        try:
            A, b = self._leer_entradas()
            
            resultado = resolver_sistema_de_ecuaciones(A, b)
            
            self.mostrar_resultado(resultado)
            
        except np.linalg.LinAlgError:
            self.mostrar_resultado("El sistema no tiene solución única (puede ser incompatible o tener infinitas soluciones).")

    def mostrar_resultado(self, texto):
        # Limpia el frame_contenedor y muestra el resultado
        for widget in self.frame_contenedor.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self.frame_contenedor, text=texto, justify="center")
        label.pack(padx=10, pady=10)

    def renderizar_celdas(self):
        # Limpia el frame antes de dibujar
        for widget in self.grid_frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []

        n = self.dimension
        # Mapea los dígitos a sus subíndices Unicode
        subindices = {
            "0": "\u2080",
            "1": "\u2081",
            "2": "\u2082",
            "3": "\u2083",
            "4": "\u2084",
            "5": "\u2085",
            "6": "\u2086",
            "7": "\u2087",
            "8": "\u2088",
            "9": "\u2089"
        }

        def get_subindice(num):
            return ''.join(subindices[d] for d in str(num))

        for i in range(n):
            fila_entries = []
            for j in range(n):
                entry = ctk.CTkEntry(self.grid_frame_sistema, width=60)
                # Valores por defecto
                if n == 3:
                    default_matrix = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
                    entry.insert(0, str(default_matrix[i][j]))
                elif n == 2:
                    default_matrix = [[1, 2], [3, 4]]
                    entry.insert(0, str(default_matrix[i][j]))
                entry.grid(row=i, column=2*j, padx=2, pady=2)
                fila_entries.append(entry)
                # Etiqueta de incógnita
                sub = get_subindice(j+1)
                label = ctk.CTkLabel(self.grid_frame_sistema, text=f"X{sub} + ", width=20)
                label.grid(row=i, column=2*j+1)
                if j < n-1:
                    plus = ctk.CTkLabel(self.grid_frame_sistema, text="+")
                    plus.grid(row=i, column=2*j+2) 
            # Igual y resultado
            igual = ctk.CTkLabel(self.grid_frame_sistema, text="=")
            igual.grid(row=i, column=2*n)
            entry_result = ctk.CTkEntry(self.grid_frame_sistema, width=60)
            # Valores por defecto para vector b
            if n == 3:
                default_b = [1, 0, 1]
                entry_result.insert(0, str(default_b[i]))
            elif n == 2:
                default_b = [5, 6]
                entry_result.insert(0, str(default_b[i]))
            entry_result.grid(row=i, column=2*n+1, padx=2, pady=2)
            fila_entries.append(entry_result)
            self.entries.append(fila_entries)
