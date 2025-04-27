import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import sympy as sp
from sympy.abc import x

class Derivacion:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.funcion = None
        self.evaluar = None
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Derivacion", **estilo_label_titulos).pack(pady=20)
        
        # ------ Fila 1: contenedor de derivadas ------ #
        self.frame_derivadas = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_derivadas.pack(pady=10, padx=20, fill="x")
        self.frame_derivadas.columnconfigure(0, weight=1)
        self.frame_derivadas.columnconfigure(1, weight=1)
        
        # ------ Sección de función (Columna 0) ------ #
        self.frame_funcion = ctk.CTkFrame(self.frame_derivadas, fg_color=("white", "gray10"))
        self.frame_funcion.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_funcion = ctk.CTkLabel(self.frame_funcion, text="Función:", **estilo_label)
        self.label_funcion.pack(pady=5)
        
        self.entry_funcion = ctk.CTkEntry(self.frame_funcion, width=200, placeholder_text="Ej: cos(x) + 2**x")
        self.entry_funcion.pack(pady=5, padx=10)
        self.entry_funcion.bind("<Return>", lambda event: self.actualizar_funcion())
        
        # --- Boton de vaciar función --- #
        self.vaciar_funcion_button = ctk.CTkButton(self.frame_funcion, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_funcion)
        self.vaciar_funcion_button.pack(pady=10)
        
        # ------ Sección de evaluar (Columna 1) ------ #
        self.frame_evaluar = ctk.CTkFrame(self.frame_derivadas, fg_color=("white", "gray10"))
        self.frame_evaluar.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_evaluar = ctk.CTkLabel(self.frame_evaluar, text="Evaluar:", **estilo_label)
        self.label_evaluar.pack(pady=5)
        
        self.entry_evaluar = ctk.CTkEntry(self.frame_evaluar, width=200, placeholder_text="Ej: 2")
        self.entry_evaluar.pack(pady=5, padx=10)
        self.entry_evaluar.bind("<Return>", lambda event: self.actualizar_evaluar())
        
        # --- Boton de vaciar evaluar --- #
        self.vaciar_evaluar_button = ctk.CTkButton(self.frame_evaluar, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_evaluar)
        self.vaciar_evaluar_button.pack(pady=10)
        
        # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_operaciones.pack(pady=10, padx=20)
        self.frame_operaciones.columnconfigure(0, weight=1)
        self.frame_operaciones.columnconfigure(1, weight=1)
        
        self.derivada_button = ctk.CTkButton(self.frame_operaciones, text="Derivada", width=100, command=self.derivada)
        self.derivada_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.evaluar_derivada_button = ctk.CTkButton(self.frame_operaciones, text="Evaluar derivada", width=100, command=self.evaluar_derivada)
        self.evaluar_derivada_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
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
        
        
    def actualizar_funcion(self):
        try:
            texto = self.entry_funcion.get()
            self.funcion = texto
            print(self.funcion)
        except Exception:
            self.funcion = None
                
                
    def actualizar_evaluar(self):
        try:
            texto = self.entry_evaluar.get()
            self.evaluar = texto
            print(self.evaluar)
        except Exception:
            self.evaluar = None
                
        
    def vaciar_funcion(self):
        self.funcion = None
        self.entry_funcion.delete(0, ctk.END)
        
    def vaciar_evaluar(self):
        self.evaluar = None
        self.entry_evaluar.delete(0, ctk.END)
        
    def derivada(self):
        try:
            if self.funcion is None:
                self.mostrar_error(self.frame_resultado_grid, "La función no puede estar vacía")
                return
            # Convertir la función a una expresión simbólica
            funcion_sympy = sp.sympify(self.funcion)
            
            # Calcular la derivada
            derivada = sp.diff(funcion_sympy, x)
            
            self.mostrar_resultado(derivada, self.frame_resultado_grid, "f'(x) =")
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular la derivada: {str(e)}")
            return
        
    def evaluar_derivada(self):
        try:
            if self.funcion is None:
                self.mostrar_error(self.frame_resultado_grid, "La función no puede estar vacía")
                return
            if self.evaluar is None:
                self.mostrar_error(self.frame_resultado_grid, "El valor a evaluar no puede estar vacío")
                return
            
            # Convertir la función a una expresión simbólica
            funcion_sympy = sp.sympify(self.funcion)
            # Calcular la derivada
            derivada = sp.diff(funcion_sympy, x)
            
            # Evaluar la derivada en el valor especificado
            resultado = round(derivada.subs(x, self.evaluar).evalf(), 2)
            
            self.mostrar_resultado(resultado, self.frame_resultado_grid, f"f'({self.evaluar}) =")
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al calcular la derivada: {str(e)}")
            return
        
        
    def mostrar_resultado(self, derivada, frame, label=None):
        # Limpiar el frame de resultados
        for widget in frame.winfo_children():
            widget.destroy()
        
        for widget in frame.winfo_children():
            widget.destroy()
            
        if derivada is not None:
            if label:
                # Mostrar etiqueta
                self.frame_resultado_label.grid_rowconfigure(0, weight=1)
                self.frame_resultado_label.grid_columnconfigure(0, weight=1)
                label_widget = ctk.CTkLabel(self.frame_resultado_label, text=label)
                label_widget.grid(row=0, column=0, sticky="nsew")
            
            # Mostrar resultado
            texto_resultado = str(derivada).replace("**", "^")
            resultado = ctk.CTkLabel(frame, text=texto_resultado, fg_color=("white", "gray10"))
            resultado.pack(padx=5, pady=5)
        else:
            # Centrar mensaje de no hay resultado
            label_vacio = ctk.CTkLabel(frame, text=label)
            label_vacio.pack(padx=5, pady=5)
            
            
    def mostrar_error(self, frame, text):
        for widget in frame.winfo_children():
            widget.destroy()
        self.label_err = ctk.CTkLabel(frame, text=text, text_color="red")
        self.label_err.pack()
        
