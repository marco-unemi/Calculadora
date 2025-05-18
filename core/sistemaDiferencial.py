import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import pandas as pd


class SistemaDiferencial:
    @staticmethod
    def resolver_sistema_diferencial(A_numeric, X0, t0=0, tf=5, h=0.1):
        """
        Resuelve el sistema dX/dt = A*X con condiciones iniciales X0.
        Devuelve: (tabla pandas, valores_propios, vectores_propios, funciones_lambdify)
        """
        t = sp.symbols('t', real=True)
        n = A_numeric.shape[0]
        X_syms = sp.symbols(f'x0:{n}')
        X_funcs = sp.Matrix([sp.Function(f'x{i}')(t) for i in range(n)])
        A = sp.Matrix(A_numeric)
        dXdt = X_funcs.diff(t)
        eqs = [sp.Eq(dXdt[i], (A * X_funcs)[i]) for i in range(n)]

        # Valores y vectores propios
        eigen_data = A.eigenvects()
        valores_propios = [val.evalf() for val, _, _ in eigen_data]
        vectores_propios = [v[0].evalf() for _, _, v in eigen_data]

        # Solución general
        sol = sp.dsolve(eqs)
        sol_matrix = sp.Matrix([s.rhs for s in sol])

        # Condiciones iniciales
        ics = {X_funcs[i].subs(t, t0): X0[i] for i in range(n)}
        consts = sp.solve([s.rhs.subs(t, t0) - ics[s.lhs.subs(t, t0)] for s in sol], dict=True)[0]
        sol_num = sol_matrix.subs(consts)

        # Funciones numéricas
        funcs = [sp.lambdify(t, sol_num[i], 'numpy') for i in range(n)]

        # Tabla de valores
        n_puntos = int((tf - t0) / h) + 1
        t_vals = np.linspace(t0, tf, n_puntos)
        var_names = ['x', 'y', 'z', 'w']  # Puedes extender si quieres más dimensiones
        data = {f'{var_names[i]}(t)': funcs[i](t_vals) for i in range(n)}
        data['t'] = t_vals
        tabla = pd.DataFrame(data)

        return tabla, valores_propios, vectores_propios, funcs

    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.dimension = 2
        self.entries = []
        self.entries_x0 = []
        self.frame_grafica = None
        self.table_frame = None

    def _build_ui(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.workspace_frame, text="Sistema de Ecuaciones Diferenciales Lineales", **estilo_label_titulos).pack(pady=20)

        # Frame principal de entradas
        self.frame_sistema = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_sistema.pack(pady=10, padx=20, fill="x")
        self.frame_sistema.grid_rowconfigure(0, weight=1)
        self.frame_sistema.grid_columnconfigure(0, weight=1)

        # Frame interno para matriz y condiciones
        self.frame_sistema_ecuaciones = ctk.CTkFrame(self.frame_sistema, fg_color=("white", "gray10"))
        self.frame_sistema_ecuaciones.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Frame para seleccionar dimensión (igual que en UISistemaEcuaciones)
        self.frame_dimension = ctk.CTkFrame(self.frame_sistema_ecuaciones, fg_color=("white", "gray10"))
        self.frame_dimension.pack(pady=5)
        ctk.CTkLabel(self.frame_dimension, text="Dimensiones:").pack(side="left", padx=5)
        self.boton_aumentar = ctk.CTkButton(self.frame_dimension, text="+", command=self.aumentar_dimension, fg_color="green", hover_color='#1d5f32', width=40)
        self.boton_aumentar.pack(side="left", padx=10)
        self.boton_disminuir = ctk.CTkButton(self.frame_dimension, text="-", command=self.disminuir_dimension, fg_color="green", hover_color='#1d5f32', width=40)
        self.boton_disminuir.pack(side="left", padx=10)

        # Frame para la matriz y condiciones (dos columnas)
        self.frame_entradas = ctk.CTkFrame(self.frame_sistema_ecuaciones, fg_color=("white", "gray10"))
        self.frame_entradas.pack(pady=10, padx=10, fill="both", expand=True)
        self.renderizar_celdas()

        # Botón de calcular
        self.calcular_button = ctk.CTkButton(self.frame_sistema_ecuaciones, text="Calcular", command=self.calcular)
        self.calcular_button.pack(pady=10)

        # Frame de resultados
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame_resultado.columnconfigure(0, weight=1)
        self.frame_resultado.columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_resultado, text="Resultados:", **estilo_label).grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=10)
        self.table_frame = ctk.CTkFrame(self.frame_resultado, fg_color=("white", "gray10"), width=300, height=400)
        self.table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=0)
        self.table_frame.rowconfigure(1, weight=1)
        self.frame_grafica = ctk.CTkFrame(self.frame_resultado, fg_color=("white", "gray10"), width=700, height=400)
        self.frame_grafica.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.graficar()  # Mostrar gráfica en blanco por defecto

    def renderizar_celdas(self):
        # Limpia el frame antes de dibujar
        for widget in self.frame_entradas.winfo_children():
            widget.destroy()
        self.entries = []
        n = self.dimension
        # Configura el grid para centrar
        self.frame_entradas.columnconfigure(0, weight=1)
        self.frame_entradas.columnconfigure(1, weight=1)
        self.frame_entradas.rowconfigure(0, weight=1)
        # Columna 0: Matriz A
        frame_matriz = ctk.CTkFrame(self.frame_entradas, fg_color=("white", "gray10"))
        frame_matriz.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        # Labels de ecuaciones dinámicos
        default_matrix = [[0.3, 0.1], [0.02, -0.05]]
        default_x0 = 50
        default_y0 = 10
        default_tf = 5
        default_h = 1
        for i in range(n):
            var = chr(ord('x') + i)  # x, y, z, ...
            ctk.CTkLabel(frame_matriz, text=f'd{var}/dt =', **estilo_label).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
        # Entradas de la matriz
        for i in range(n):
            fila = []
            for j in range(n):
                e = ctk.CTkEntry(frame_matriz, width=60, justify="center")
                # Valores por defecto solo para 2x2
                if n == 2:
                    e.insert(0, str(default_matrix[i][j]))
                fila.append(e)
                e.grid(row=i+1, column=j+1, padx=2, pady=2)
            self.entries.append(fila)
        # Columna 1: Condiciones iniciales y parámetros
        frame_cond = ctk.CTkFrame(self.frame_entradas, fg_color=("white", "gray10"))
        frame_cond.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.entries_x0 = []
        # x₀
        ctk.CTkLabel(frame_cond, text="x₀:", **estilo_label).grid(row=0, column=0, sticky="w", pady=2)
        self.entry_x0 = ctk.CTkEntry(frame_cond, width=60, justify="center")
        if n == 2:
            self.entry_x0.insert(0, str(default_x0))
        self.entry_x0.grid(row=0, column=1, pady=2)
        self.entries_x0.append(self.entry_x0)
        # y₀
        ctk.CTkLabel(frame_cond, text="y₀:", **estilo_label).grid(row=1, column=0, sticky="w", pady=2)
        self.entry_y0 = ctk.CTkEntry(frame_cond, width=60, justify="center")
        if n == 2:
            self.entry_y0.insert(0, str(default_y0))
        self.entry_y0.grid(row=1, column=1, pady=2)
        self.entries_x0.append(self.entry_y0)
        # Tiempo total tf
        ctk.CTkLabel(frame_cond, text="Tiempo total (tf):", **estilo_label).grid(row=2, column=0, sticky="w", pady=2)
        self.entry_tf = ctk.CTkEntry(frame_cond, width=60, justify="center")
        if n == 2:
            self.entry_tf.insert(0, str(default_tf))
        self.entry_tf.grid(row=2, column=1, pady=2)
        # Paso h
        ctk.CTkLabel(frame_cond, text="Tamaño de paso (h):", **estilo_label).grid(row=3, column=0, sticky="w", pady=2)
        self.entry_h = ctk.CTkEntry(frame_cond, width=60, justify="center")
        if n == 2:
            self.entry_h.insert(0, str(default_h))
        self.entry_h.grid(row=3, column=1, pady=2)

    def _leer_entradas(self):
        try:
            n = self.dimension
            A = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    val = self.entries[i][j].get()
                    if val.strip() == '':
                        raise ValueError(f"Falta un coeficiente en la fila {i+1}, columna {j+1}")
                    A[i, j] = float(val)
            # Condiciones iniciales y parámetros
            x0 = self.entry_x0.get()
            y0 = self.entry_y0.get()
            tf = self.entry_tf.get()
            h = self.entry_h.get()
            if x0.strip() == '' or y0.strip() == '' or tf.strip() == '' or h.strip() == '':
                raise ValueError("Faltan condiciones iniciales o parámetros")
            X0 = np.array([float(x0), float(y0)])
            tf = float(tf)
            h = float(h)
            return A, X0, tf, h
        except ValueError as e:
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.table_frame, text=f"Error en los datos de entrada: {e}", text_color="red").pack(padx=10, pady=10)
            return None, None, None, None

    def graficar(self, t_vals=None, x_vals=None, labels=None):
        # Limpia el frame de la gráfica
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(6, 4))
        if t_vals is not None and x_vals is not None:
            for i, x in enumerate(x_vals):
                label = labels[i] if labels else f"x{i+1}(t)"
                ax.plot(t_vals, x, label=label)
            ax.legend()
        ax.set_xlabel('t')
        ax.set_ylabel('Valor')
        ax.set_title('Solución del sistema')
        ax.grid(True)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        canvas.draw()

    def calcular(self):
        try:
            A, X0, tf, h = self._leer_entradas()
            if A is None or X0 is None:
                return
            tabla, valores, vectores, funcs = self.resolver_sistema_diferencial(A, X0, t0=0, tf=tf, h=h)

            # Limpiar frame
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Fila 0: valores y vectores propios
            frame_propios = ctk.CTkFrame(self.table_frame, fg_color=("white", "gray10"))
            frame_propios.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            # Mostrar valores propios como 'λ = valor' en una sola línea
            ctk.CTkLabel(frame_propios, text="Valores propios:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,0))
            valores_str = '   '.join([f'λ{i+1} = {v:.4f}' for i, v in enumerate(valores)])
            ctk.CTkLabel(frame_propios, text=valores_str, font=("Arial", 13)).pack(anchor="w", pady=(0,5))
            ctk.CTkLabel(frame_propios, text="Vectores propios (columnas):", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,0))
            for idx, v in enumerate(vectores):
                v_str = ', '.join([f"{x:.4f}" for x in np.array(v).flatten()])
                ctk.CTkLabel(frame_propios, text=f"vp{idx+1} = [{v_str}]", font=("Arial", 11)).pack(anchor="w")

            # Fila 1: tabla de resultados
            frame_tabla = ctk.CTkScrollableFrame(self.table_frame, fg_color=("white", "gray10"))
            frame_tabla.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
            # Reordena las columnas para que sea t | x(t) | y(t) | ...
            columnas = ['t']
            var_names = ['x', 'y', 'z', 'w']
            for var in var_names[:self.dimension]:
                columnas.append(f'{var}(t)')
            # Filtra solo las columnas que existen en la tabla
            columnas = [col for col in columnas if col in tabla.columns]
            tabla = tabla[columnas]
            for j, header in enumerate(columnas):
                cell = ctk.CTkLabel(frame_tabla, text=header, fg_color=("gray80", "gray30"), font=("Arial", 12, "bold"))
                cell.grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
                frame_tabla.grid_columnconfigure(j, weight=1)
            for i, row in tabla.head(10).iterrows():
                for j, val in enumerate(row):
                    cell = ctk.CTkLabel(frame_tabla, text=f"{val:.4f}", fg_color=("gray90", "gray20"), font=("Arial", 12))
                    cell.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=1)
                frame_tabla.grid_rowconfigure(i+1, weight=1)

            # Graficar con datos
            t_vals = tabla['t']
            x_vals = [tabla[f'{var_names[i]}(t)'] for i in range(self.dimension)]
            labels = [f"{var_names[i]}(t)" for i in range(self.dimension)]
            self.graficar(t_vals, x_vals, labels)
        except Exception as e:
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.table_frame, text=f"Error: {e}", text_color="red").pack(padx=10, pady=10)
            self.graficar()  # Muestra gráfica en blanco si hay error

    def aumentar_dimension(self):
        if self.dimension < 3:
            self.dimension += 1
            self.renderizar_celdas()

    def disminuir_dimension(self):
        if self.dimension > 2:
            self.dimension -= 1
            self.renderizar_celdas()
