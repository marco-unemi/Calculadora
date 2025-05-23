import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import sympy as sp
from sympy.abc import x


class Integracion:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.funcion = None
        self.limites = None
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Integracion", **estilo_label_titulos).pack(pady=20)
        
        # ------ Fila 1: Contenedor de funciones ------ #
        self.frame_integrales = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_integrales.pack(pady=10, padx=20, fill="x")
        
        self.frame_integrales.columnconfigure(0, weight=1)
        self.frame_integrales.columnconfigure(1, weight=1)
        
        # ------ Sección de función (Columna 0) ------ #
        self.frame_funcion = ctk.CTkFrame(self.frame_integrales, fg_color=("white", "gray10"))
        self.frame_funcion.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_funcion = ctk.CTkLabel(self.frame_funcion, text="Función:", **estilo_label)
        self.label_funcion.pack(pady=5)
        
        self.entry_funcion = ctk.CTkEntry(self.frame_funcion, width=200, placeholder_text="Ej: e**x + 2*x")
        self.entry_funcion.pack(pady=5, padx=10)
        self.entry_funcion.insert(0, "e**x + 2*x")
        
        # --- Boton de vaciar función --- #
        self.vaciar_funcion_button = ctk.CTkButton(self.frame_funcion, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_funcion)
        self.vaciar_funcion_button.pack(pady=10)
        
        # ------ Sección de evaluar (Columna 1) ------ #
        self.frame_limites = ctk.CTkFrame(self.frame_integrales, fg_color=("white", "gray10"))
        self.frame_limites.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_limites = ctk.CTkLabel(self.frame_limites, text="Límites (a, b):", **estilo_label)
        self.label_limites.pack(pady=5)

        self.entry_limites = ctk.CTkEntry(self.frame_limites, width=200, placeholder_text="Ej: 0, 1")
        self.entry_limites.pack(pady=5, padx=10)
        self.entry_limites.insert(0, "0, 1")
        
        # --- Boton de vaciar limites --- #
        self.vaciar_limites_button = ctk.CTkButton(self.frame_limites, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_limites)
        self.vaciar_limites_button.pack(pady=10)
        
        # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_operaciones.pack(pady=10, padx=20)
        self.frame_operaciones.columnconfigure(0, weight=1)
        self.frame_operaciones.columnconfigure(1, weight=1)
        
        self.integrar_button = ctk.CTkButton(self.frame_operaciones, text="Calcular", width=100, command=self.integrar)
        self.integrar_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.evaluar_integracion_button = ctk.CTkButton(self.frame_operaciones, text="Evaluar Integral", width=100, command=self.evaluar_integracion)
        self.evaluar_integracion_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
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


    def vaciar_funcion(self):
        self.funcion = None
        self.entry_funcion.delete(0, ctk.END)

    def vaciar_limites(self):
        self.limites = None
        self.entry_limites.delete(0, ctk.END)

    def get_funcion(self):
        return self.entry_funcion.get()

    def get_limites(self):
        texto = self.entry_limites.get()
        try:
            numeros = [float(x.strip()) for x in texto.split(',')]
            if len(numeros) != 2:
                return None
            return numeros
        except Exception:
            return None

    def _leer_entradas_integracion(self):
        try:
            funcion_str = self.entry_funcion.get().strip()
            limites_str = self.entry_limites.get().strip()
            if not funcion_str or not limites_str:
                raise ValueError("Debe ingresar una función y los límites.")
            # Procesar límites
            if ',' in limites_str:
                numeros = [float(x.strip()) for x in limites_str.split(',')]
                if len(numeros) != 2:
                    raise ValueError("Los límites deben ser dos números separados por coma.")
                limites = numeros
            else:
                limites = eval(limites_str)
                if not isinstance(limites, (list, tuple)) or len(limites) != 2:
                    raise ValueError("Los límites deben ser dos números separados por coma o lista/tupla.")
            return funcion_str, limites
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error en las entradas: {e}")
            return None

    def integrar(self):
        try:
            entradas = self._leer_entradas_integracion()
            if entradas is None:
                return
            funcion, _ = entradas
            if not funcion:
                self.mostrar_error(self.frame_resultado_grid, "La función no puede estar vacía")
                return
            funcion_sympy = sp.sympify(funcion, locals={'e': sp.E})
            resultado = sp.integrate(funcion_sympy, x)
            resultado_str = str(resultado)
            if 'C' in resultado_str:
                pass
            else:
                resultado_str = f"{resultado_str} + C"
            print(resultado)
            self.mostrar_resultado(resultado_str, self.frame_resultado_grid, f"∫ {funcion.replace('**', '^')} =")
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al integrar: {str(e)}")
            return

    def evaluar_integracion(self):
        try:
            entradas = self._leer_entradas_integracion()
            if entradas is None:
                return
            funcion, limites = entradas
            if not funcion:
                self.mostrar_error(self.frame_resultado_grid, "La función no puede estar vacía")
                return
            if not limites:
                self.mostrar_error(self.frame_resultado_grid, "Los límites no pueden estar vacíos")
                return
            funcion_sympy = sp.sympify(funcion, locals={'e': sp.E})
            resultado = sp.integrate(funcion_sympy, (x, limites[0], limites[1]))
            a = limites[0]
            b = limites[1]
            label = f"∫[{a}, {b}] {funcion.replace('**', '^')} ="
            self.mostrar_resultado(resultado, self.frame_resultado_grid, label)
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al evaluar integración: {str(e)}")
            print(f"Error al evaluar integración: {str(e)}")
            return
            
    def integral_a_unicode(self, expr):
        # Convierte una expresión sympy o string a string con superíndices unicode para los exponentes
        super_map = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
        s = str(expr).replace("**", "^")
        # Reemplaza x^n por xⁿ
        import re
        def super_replace(match):
            base = match.group(1)
            exp = match.group(2)
            return base + exp.translate(super_map)
        s = re.sub(r"(x)\^([\-\d]+)", super_replace, s)
        return s

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
            # Mostrar resultado en Unicode bonito
            texto_resultado = self.integral_a_unicode(derivada)
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
        

