import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
import math
import re

class EcuacionDiferencial:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.current_figure_canvas = None

        # Referencias a widgets
        self.entry_fxy = None
        self.entry_x0 = None
        self.entry_y0 = None
        self.entry_x_final = None
        self.entry_h_step = None
        
        self.resultado_textbox = None
        self.label_resultado_title = None
        self.placeholder_label = None
        

    def _build_ui(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.workspace_frame, text="Ecuaciones Diferenciales", **estilo_label_titulos).pack(pady=20)

        self.frame_inputs_edo = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_inputs_edo.pack(pady=10, padx=10, fill="x", anchor="n")
        
        self.frame_inputs_edo.columnconfigure(0, weight=0) 
        self.frame_inputs_edo.columnconfigure(1, weight=1) 
        self.frame_inputs_edo.columnconfigure(2, weight=0) 
        self.frame_inputs_edo.columnconfigure(3, weight=1) 

        label_fxy = ctk.CTkLabel(self.frame_inputs_edo, text="dy/dx = f(x,y):", **estilo_label)
        label_fxy.grid(row=0, column=0, padx=(10,5), pady=10, sticky="w")
        self.entry_fxy = ctk.CTkEntry(self.frame_inputs_edo)
        self.entry_fxy.grid(row=0, column=1, columnspan=2, padx=5, pady=10, sticky="ew")
        self.entry_fxy.insert(0, "x/y")  

        label_x0 = ctk.CTkLabel(self.frame_inputs_edo, text="Condición Inicial x₀:", **estilo_label)
        label_x0.grid(row=1, column=0, padx=(10,5), pady=10, sticky="w")
        self.entry_x0 = ctk.CTkEntry(self.frame_inputs_edo, width=120, placeholder_text="Ej: 0")
        self.entry_x0.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        self.entry_x0.insert(0, "1")

        label_y0 = ctk.CTkLabel(self.frame_inputs_edo, text="y(x₀):", **estilo_label)
        label_y0.grid(row=1, column=2, padx=(10,5), pady=10, sticky="w")
        self.entry_y0 = ctk.CTkEntry(self.frame_inputs_edo, width=120, placeholder_text="Ej: 1")
        self.entry_y0.grid(row=1, column=3, padx=5, pady=10, sticky="w")
        self.entry_y0.insert(0, "2")

        label_x_final = ctk.CTkLabel(self.frame_inputs_edo, text="Resolver hasta x_final:", **estilo_label)
        label_x_final.grid(row=2, column=0, padx=(10,5), pady=10, sticky="w")
        self.entry_x_final = ctk.CTkEntry(self.frame_inputs_edo, width=120, placeholder_text="Ej: 10")
        self.entry_x_final.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        self.entry_x_final.insert(0, "5")
        
        # Entrada para el tamaño del paso (h)
        label_h_step = ctk.CTkLabel(self.frame_inputs_edo, text="Tamaño del Paso (h):", **estilo_label)
        label_h_step.grid(row=2, column=2, padx=(10,5), pady=10, sticky="w")
        self.entry_h_step = ctk.CTkEntry(self.frame_inputs_edo, width=120, placeholder_text="Ej: 0.1") 
        self.entry_h_step.grid(row=2, column=3, padx=5, pady=10, sticky="w")
        self.entry_h_step.insert(0, "0.5")
        
        # Botón para vaciar los campos de entrada
        self.vaciar_campos_button = ctk.CTkButton(self.frame_inputs_edo, text="Vaciar Campos de Entrada", 
                                                 command=self.vaciar_todos_los_campos_de_entrada,
                                                 fg_color="#df0000", hover_color="#b81414")
        self.vaciar_campos_button.grid(row=3, column=0, columnspan=4, pady=10, padx=10)

        # Frame para los botones de métodos
        self.frame_botones_metodo = ctk.CTkFrame(self.workspace_frame, fg_color="transparent")
        self.frame_botones_metodo.pack(pady=10, padx=10, fill="x", anchor="n")
        self.frame_botones_metodo.columnconfigure(0, weight=1)
        self.frame_botones_metodo.columnconfigure(1, weight=1)

        # Frame para el método analítico
        self.frame_analitico = ctk.CTkFrame(self.frame_botones_metodo, fg_color=("white", "gray10"))
        self.frame_analitico.grid(row=0, column=0, padx=(0,5), pady=5, sticky="nsew")
        
        ctk.CTkLabel(self.frame_analitico, text="Método Analítico", **estilo_label).pack(pady=(10,5))
        self.analitico_button = ctk.CTkButton(self.frame_analitico, text="Resolver Analíticamente", command=self.llamar_resolver_analitico)
        self.analitico_button.pack(pady=5, padx=10)

        # Frame para el método numérico
        self.frame_numerico = ctk.CTkFrame(self.frame_botones_metodo, fg_color=("white", "gray10"))
        self.frame_numerico.grid(row=0, column=1, padx=(5,0), pady=5, sticky="nsew")

        ctk.CTkLabel(self.frame_numerico, text="Método Numérico", **estilo_label).pack(pady=(10,5))
        
        # Frame para los botones de métodos numéricos
        frame_botones_num_internos = ctk.CTkFrame(self.frame_numerico, fg_color="transparent")
        frame_botones_num_internos.pack(pady=5, padx=10)
        frame_botones_num_internos.columnconfigure(0, weight=1)
        frame_botones_num_internos.columnconfigure(1, weight=1)

        # Botones para los métodos numéricos
        self.euler_button = ctk.CTkButton(frame_botones_num_internos, text="Euler", command=self.llamar_resolver_euler)
        self.euler_button.grid(row=0, column=0, padx=(0,5), sticky="ew")
        
        self.runge_kutta_button = ctk.CTkButton(frame_botones_num_internos, text="Runge-Kutta (RK4)", command=self.llamar_resolver_runge_kutta)
        self.runge_kutta_button.grid(row=0, column=1, padx=(5,0), sticky="ew")


        # Frame para el resultado
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=10, padx=10, fill="both", expand=True)
        self.frame_resultado.columnconfigure(0, weight=1)  # Columna de texto
        self.frame_resultado.columnconfigure(1, weight=1)  # Columna de gráfica
        self.frame_resultado.rowconfigure(0, weight=0)     # Etiqueta "Resultado:"
        self.frame_resultado.rowconfigure(1, weight=1)     # Contenido
        self.frame_resultado.rowconfigure(2, weight=1)     # Contenido

        # Etiqueta para el resultado
        etiqueta_resultado = ctk.CTkLabel(self.frame_resultado, text="Resultados:", **estilo_label)
        etiqueta_resultado.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=10)

    
        
        scrollable_frame = ctk.CTkScrollableFrame(self.frame_resultado, corner_radius=0, fg_color=("white", "gray10"), width=400, height=400)
        scrollable_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

        self.table_frame = ctk.CTkFrame(scrollable_frame, fg_color=("white", "gray10"))
        self.table_frame.pack(fill="both", expand=True)

        # Espacio para gráfica (columna derecha) con tamaño fijo
        self.graph_canvas = ctk.CTkFrame(self.frame_resultado, fg_color=("white", "gray10"), width=600, height=400)
        self.graph_canvas.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Etiqueta temporal mientras no hay gráfica
        self.placeholder_label = ctk.CTkLabel(
            self.graph_canvas, 
            text="La gráfica aparecerá aquí...", 
            text_color=("#000000", "#FFFFFF"),
            width=600,
            height=500
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
        
    
    def vaciar_todos_los_campos_de_entrada(self):
        if self.entry_fxy: self.entry_fxy.delete(0, "end")
        if self.entry_x0: self.entry_x0.delete(0, "end")
        if self.entry_y0: self.entry_y0.delete(0, "end")
        if self.entry_x_final: self.entry_x_final.delete(0, "end")
        if self.entry_h_step: self.entry_h_step.delete(0, "end") # Modificado
        
        if self.resultado_textbox:
            self.resultado_textbox.configure(state="normal")
            self.resultado_textbox.delete("1.0", "end")
            self.resultado_textbox.configure(state="disabled")
        print("Campos de entrada EDO vaciados.")

    def _preparar_display_resultado(self):
        if self.resultado_textbox:
            self.resultado_textbox.configure(state="normal")
            self.resultado_textbox.delete("1.0", "end")

        if self.graph_canvas:
            # Limpia el contenido actual (como texto o imágenes)
            for widget in self.graph_canvas.winfo_children():
                widget.destroy()
            # Puedes agregar un placeholder si quieres:
            self.placeholder_label = ctk.CTkLabel(self.graph_canvas, text="Cargando gráfica...", text_color=("#444", "#ccc"))
            self.placeholder_label.pack(expand=True)

    def _finalizar_display_resultado(self):
        if self.resultado_textbox:
            self.resultado_textbox.configure(state="disabled")

        # Si quieres quitar el placeholder al finalizar, puedes hacer esto:
        if hasattr(self, 'placeholder_label') and self.placeholder_label.winfo_exists():
            self.placeholder_label.destroy()

    def _leer_entradas_numericas_comunes(self):
        try:
            f_str = self.entry_fxy.get()
            x0_str = self.entry_x0.get()
            y0_str = self.entry_y0.get()
            x_final_str = self.entry_x_final.get()
            h_str = self.entry_h_step.get() # Modificado para leer h

            if not all([f_str, x0_str, y0_str, x_final_str, h_str]):
                raise ValueError("Todos los campos de entrada son obligatorios.")

            x0 = float(x0_str)
            y0 = float(y0_str)
            x_final = float(x_final_str)
            h_val = float(h_str) # Leer h como float

            if h_val <= 1e-9: # h debe ser positivo y no demasiado cercano a cero
                raise ValueError("El tamaño del paso (h) debe ser un número positivo significativo.")
            
            if x_final < x0: # Para h positivo, x_final debe ser >= x0
                 raise ValueError("x_final debe ser mayor o igual que x₀ si h es positivo.")


            return f_str, x0, y0, x_final, h_val # Devuelve h_val
        except ValueError as e:
            self._preparar_display_resultado()
            # Para que el mensaje de error también aparezca centrado
            error_msg = f"Error en los datos de entrada:{e}\nPor favor, verifica los valores ingresados."
            self.resultado_textbox.insert("center", error_msg) # Intentar insertar con justificación
            self._finalizar_display_resultado()
            return None 

    def _mostrar_puntos(self, puntos):
        """Muestra los puntos en una tabla usando CTkLabel"""
        # Limpiar tabla existente
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
        # Crear encabezados
        headers = ["i", "xᵢ", "yᵢ"]
        for j, header in enumerate(headers):
            cell = ctk.CTkLabel(
                master=self.table_frame,
                text=header,
                fg_color=("gray80", "gray30"),
                corner_radius=0,
                font=("Arial", 12, "bold"),
                padx=5,
                pady=5
            )
            cell.grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
            self.table_frame.grid_columnconfigure(j, weight=1)

        # Insertar datos
        for i, (x_val, y_val) in enumerate(puntos):
            row_data = [str(i), f"{x_val:.4f}", f"{y_val:.4f}"]
            for j, cell_data in enumerate(row_data):
                cell = ctk.CTkLabel(
                    master=self.table_frame,
                    text=cell_data,
                    fg_color=("gray90", "gray20"),
                    corner_radius=0,
                    font=("Arial", 12),
                    padx=5,
                    pady=5
                )
                cell.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=1)
            self.table_frame.grid_rowconfigure(i+1, weight=1)

    def graficar_soluciones(self, lista_soluciones_data):
        """
        Grafica una o múltiples soluciones.
        lista_soluciones_data: lista de diccionarios, cada uno con:
                                {'puntos': [(x,y),...], 'nombre': 'Metodo Euler', 'estilo': 'bo-'}
                                o para analítica:
                                {'expr': sympy_expr, 'x_sym': self.x_sym, 'y_func': self.y_func_sym, 
                                 'x_start': x0, 'x_end': x_final, 'y_cond': y0,
                                 'nombre': 'Analítica', 'estilo': 'r-'}
        """

        fig, ax = plt.subplots(figsize=(8, 4)) # Ajusta figsize según el espacio
        
        for data in lista_soluciones_data:
            if 'puntos' in data: # Solución numérica
                x_vals = [p[0] for p in data['puntos']]
                y_vals = [p[1] for p in data['puntos']]
                ax.plot(x_vals, y_vals, data.get('estilo', 'o-'), label=data['nombre'], markersize=4)
            elif 'expr' in data: # Solución analítica
                try:
                    sol_expr_rhs = data['expr'].rhs # Tomamos el lado derecho de Eq(y(x), ...)
                    # Crear función numérica a partir de la expresión Sympy
                    # Si hay constantes de integración C1, C2 etc. deben estar resueltas.
                    # Si dsolve no pudo resolver las constantes con ics, fallará aquí o antes.
                    y_lamdify = sp.lambdify(data['x_sym'], sol_expr_rhs, modules=['numpy'])
                    
                    x_plot = np.linspace(data['x_start'], data['x_end'], 200)
                    y_plot = y_lamdify(x_plot)
                    ax.plot(x_plot, y_plot, data.get('estilo', '-'), label=data['nombre'])
                except Exception as e:
                    self.resultado_textbox.configure(state="normal")
                    self.resultado_textbox.insert("end", f"\nError al graficar solución analítica para '{data['nombre']}': {e}\nNo se pudo convertir la expresión a una función graficable. Asegúrate que la solución no contenga constantes sin resolver (C1, C2...).")
                    self.resultado_textbox.configure(state="disabled")
                    print(f"Error lambdify/plot analítico: {e}") # Log para desarrollador


        ax.set_xlabel("x")
        ax.set_ylabel("y(x)")
        ax.grid(True)
        ax.legend()
        fig.tight_layout() 
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        canvas.draw()

    def resolver_metodo_numerico(self, metodo_nombre, solver_func):
        self._preparar_display_resultado()
        inputs = self._leer_entradas_numericas_comunes()
        if inputs is None: return
        
        f_str, x0, y0, x_final, h = inputs
        if h is None: # h es obligatorio para métodos numéricos
            print("Error: El tamaño del paso (h) es obligatorio para métodos numéricos.")
            self._finalizar_display_resultado()
            return

        try:
            puntos_solucion, warning_msg = solver_func(f_str, x0, y0, x_final, h)
            if not puntos_solucion: # Si por alguna razón no hay puntos
                 raise ValueError("El método numérico no devolvió puntos de solución.")

            self._mostrar_puntos(puntos_solucion)
            
            sol_data = [{
                'puntos': puntos_solucion, 
                'nombre': metodo_nombre, 
                'estilo': 'bo-' if 'Euler' in metodo_nombre else 'go-'
            }]
            self.graficar_soluciones(sol_data)

        except (ValueError, ZeroDivisionError) as e:
            print(f"\nError durante el cálculo ({metodo_nombre}):\n{e}\nCálculo detenido.")
        except Exception as e:
            print(f"\nError inesperado ({metodo_nombre}):\n{e}\nCálculo detenido.")
        finally:
            self._finalizar_display_resultado()

    def llamar_resolver_euler(self):
        self.resolver_metodo_numerico("Euler", self.solve_euler)

    def llamar_resolver_runge_kutta(self):
        self.resolver_metodo_numerico("Runge-Kutta RK4", self.solve_runge_kutta)

    def llamar_resolver_analitico(self):
        self._preparar_display_resultado()
        inputs = self._leer_entradas_numericas_comunes()
        if inputs is None:
            return
        
        f_str, x0, y0, x_final, h = inputs
        f_str = 'dy/dx=' + f_str
        duration = x_final - x0

        try:
            tiempos, valores, solucion = self.resolver_ecuacion_diferencial(
                ecuacion_str=f_str,
                x0=x0,
                y0=y0,
                t_total=duration,
                h=h,
                func_name='y',
                indep_var='x'
            )

            if tiempos is None or valores is None:
                raise ValueError("No se pudo resolver la ecuación analíticamente.")

            puntos_para_mostrar = list(zip(tiempos, valores))
            self._mostrar_puntos(puntos_para_mostrar)

            # Definir símbolos para la gráfica
            x = sp.Symbol('x')
            y = sp.Function('y')(x)

            sol_data = [{
                'expr': solucion,
                'x_sym': x,
                'x_start': x0,
                'x_end': x_final,
                'nombre': 'Analítica',
                'estilo': 'r-'
            }]
            self.graficar_soluciones(sol_data)

        except Exception as e:
            print(f"\nError: {str(e)}")
        finally:
            self._finalizar_display_resultado()   
            
    # --- INICIO: Métodos utilitarios fusionados ---
    @staticmethod
    def evaluate_fxy_numerical(f_str, x_val, y_val):
        allowed_names = {
            "math": math, "x": x_val, "y": y_val,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
            "exp": math.exp, "log": math.log, "log10": math.log10, "sqrt": math.sqrt,
            "pow": math.pow, "fabs": math.fabs,
            "pi": math.pi, "e": math.e,
        }
        try:
            return eval(f_str, {"__builtins__": {}}, allowed_names)
        except ZeroDivisionError:
            raise ZeroDivisionError(f"División por cero al evaluar f(x,y)='{f_str}' con x={x_val:.4f}, y={y_val:.4f}")
        except Exception as e:
            raise ValueError(f"Error al evaluar f(x,y)='{f_str}' con x={x_val:.4f}, y={y_val:.4f}\n{type(e).__name__}: {e}")

    @staticmethod
    def _paso_euler(f_str, x_actual, y_actual, h):
        f_evaluada = EcuacionDiferencial.evaluate_fxy_numerical(f_str, x_actual, y_actual)
        return y_actual + h * f_evaluada

    @staticmethod
    def _paso_runge_kutta_4(f_str, x_actual, y_actual, h):
        k1 = EcuacionDiferencial.evaluate_fxy_numerical(f_str, x_actual, y_actual)
        k2 = EcuacionDiferencial.evaluate_fxy_numerical(f_str, x_actual + h/2, y_actual + (h/2)*k1)
        k3 = EcuacionDiferencial.evaluate_fxy_numerical(f_str, x_actual + h/2, y_actual + (h/2)*k2)
        k4 = EcuacionDiferencial.evaluate_fxy_numerical(f_str, x_actual + h, y_actual + h*k3)
        return y_actual + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

    @staticmethod
    def solve_numerical_method(f_str, x0, y0, x_final, h, step_function):
        puntos_solucion = []
        x_actual = x0
        y_actual = y0
        iter_count = 0
        max_iter = 100000
        epsilon = 1e-9
        warning_message = ""
        while x_actual < x_final + epsilon and iter_count <= max_iter:
            puntos_solucion.append((x_actual, y_actual))
            if abs(x_actual - x_final) < epsilon:
                break
            y_actual = step_function(f_str, x_actual, y_actual, h)
            x_actual_prev = x_actual
            x_actual += h
            if x_actual > x_final and abs(x_actual - (x_actual_prev + h)) < epsilon:
                x_actual = x_final
            iter_count += 1
        if iter_count > max_iter:
            warning_message = "\nAdvertencia: Se alcanzó el número máximo de iteraciones."
        return puntos_solucion, warning_message

    @staticmethod
    def solve_euler(f_str, x0, y0, x_final, h):
        return EcuacionDiferencial.solve_numerical_method(
            f_str, x0, y0, x_final, h, lambda fs, xa, ya, hi: EcuacionDiferencial._paso_euler(fs, xa, ya, hi)
        )

    @staticmethod
    def solve_runge_kutta(f_str, x0, y0, x_final, h):
        return EcuacionDiferencial.solve_numerical_method(
            f_str, x0, y0, x_final, h, lambda fs, xa, ya, hi: EcuacionDiferencial._paso_runge_kutta_4(fs, xa, ya, hi)
        )

    @staticmethod
    def normalizar_raices(expr_str, func_name, indep_var):
        patrones = [
            (fr'sqrt\\s*\\(\\s*{func_name}\\s*\\)', f'Pow({func_name}({indep_var}), Rational(1, 2))'),
            (fr'raiz\\s*\\(\\s*{func_name}\\s*\\)', f'Pow({func_name}({indep_var}), Rational(1, 2))'),
            (r'sqrt\\s*\\(([^)]+)\\)', r'Pow(\1, Rational(1, 2))'),
            (r'raiz\\s*\\(([^)]+)\\)', r'Pow(\1, Rational(1, 2))')
        ]
        for patron, reemplazo in patrones:
            expr_str = re.sub(patron, reemplazo, expr_str, flags=re.IGNORECASE)
        expr_str = re.sub(
            r'(\w+|\([^)]+\))\\s*[\^*]{1,2}\\s*\((\d+)/(\d+)\)',
            lambda m: f'Pow({m.group(1)}{"(" + indep_var + ")" if m.group(1) == func_name else ""}, Rational({m.group(2)}, {m.group(3)}))',
            expr_str
        )
        return expr_str

    @staticmethod
    def preparar_ecuacion(ecuacion_str, func_name, indep_var):
        ecuacion_str = ecuacion_str.replace(' ', '')
        ecuacion_str = re.sub(
            fr'd2{func_name}/d{indep_var}2',
            f'Derivative({func_name}({indep_var}), {indep_var}, {indep_var})',
            ecuacion_str
        )
        ecuacion_str = re.sub(
            fr'd{func_name}/d{indep_var}',
            f'Derivative({func_name}({indep_var}), {indep_var})',
            ecuacion_str
        )
        ecuacion_str = EcuacionDiferencial.normalizar_raices(ecuacion_str, func_name, indep_var)
        ecuacion_str = re.sub(fr'\b{func_name}\b(?!\()', f'{func_name}({indep_var})', ecuacion_str)
        return ecuacion_str

    @staticmethod
    def obtener_condiciones_iniciales(condiciones, x, y, x0):
        ics = {}
        y0 = None
        for ci_str, valor in condiciones.items():
            if 'd' + y.name in ci_str:
                ics[y.diff(x).subs(x, x0)] = valor
            elif y.name in ci_str:
                ics[y.subs(x, x0)] = valor
                y0 = valor
        return ics, y0

    @staticmethod
    def evaluar_solucion(sol_candidata, x0, h, y0, x):
        test_points = [x0, x0 + h, x0 + 2*h]
        for test_x in test_points:
            try:
                test_val = sol_candidata.rhs.subs(x, test_x)
                if isinstance(test_val, sp.Pow):
                    test_y = complex(test_val.evalf())
                    if abs(test_y.imag) > 1e-10:
                        return False
                    test_y = test_y.real
                else:
                    test_y = float(test_val.evalf())
                if not np.isfinite(test_y):
                    return False
                if test_x == x0 and y0 is not None:
                    if (y0 > 0 and test_y < 0) or (y0 < 0 and test_y > 0):
                        return False
            except:
                return False
        return True

    @staticmethod
    def resolver_ecuacion_diferencial(ecuacion_str, x0, y0, t_total, h, func_name, indep_var):
        try:
            x = sp.Symbol(indep_var)
            y_func = sp.Function(func_name)
            y = y_func(x)
            ecuacion_str = EcuacionDiferencial.preparar_ecuacion(ecuacion_str, func_name, indep_var)
            print(f"Ecuación procesada: {ecuacion_str}")
            local_dict = {
                'Derivative': sp.Derivative,
                'Pow': sp.Pow,
                'Rational': sp.Rational,
                'sqrt': sp.sqrt,
                func_name: y_func,
                indep_var: x
            }
            if '=' in ecuacion_str:
                lhs, rhs = ecuacion_str.split('=', 1)
                lhs_expr = sp.parse_expr(lhs, local_dict=local_dict)
                rhs_expr = sp.parse_expr(rhs, local_dict=local_dict)
                expr = sp.Eq(lhs_expr, rhs_expr)
            else:
                expr = sp.parse_expr(ecuacion_str, local_dict=local_dict)
            solucion = sp.dsolve(expr, y, ics={y.subs(x, x0): y0})
            tiempos = np.arange(x0, x0 + t_total + h, h)
            f = sp.lambdify(x, solucion.rhs, 'numpy')
            valores = f(tiempos)
            return tiempos, valores, solucion
        except Exception as e:
            print(f"Error en resolver_ecuacion_diferencial: {str(e)}")
            return None, None, None
    # --- FIN: Métodos utilitarios fusionados ---
            
        