import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label

class MonteCarlo:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
    
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
            
    def _build_ui(self):
        self.limpiar_workspace()
        ctk.CTkLabel(self.workspace_frame, text="Área entre dos curvas - Monte Carlo", **estilo_label_titulos).pack(pady=20)
        self.frame = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"), width=700, height=250)
        self.frame.pack(pady=10, padx=10)

        # Entradas para funciones, límites y número de puntos (con valores por defecto)
        ctk.CTkLabel(self.frame, text="Curva inferior f(x):", **estilo_label).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.funcion_inf_entry = ctk.CTkEntry(self.frame, width=200)
        self.funcion_inf_entry.insert(0, "x**2")
        self.funcion_inf_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame, text="Curva superior g(x):", **estilo_label).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.funcion_sup_entry = ctk.CTkEntry(self.frame, width=200)
        self.funcion_sup_entry.insert(0, "sqrt(x)")
        self.funcion_sup_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame, text="Límite inferior (a):", **estilo_label).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.limite_inferior_entry = ctk.CTkEntry(self.frame, width=100)
        self.limite_inferior_entry.insert(0, "0")
        self.limite_inferior_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self.frame, text="Límite superior (b):", **estilo_label).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.limite_superior_entry = ctk.CTkEntry(self.frame, width=100)
        self.limite_superior_entry.insert(0, "1")
        self.limite_superior_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self.frame, text="N° de puntos:", **estilo_label).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.n_puntos_entry = ctk.CTkEntry(self.frame, width=100)
        self.n_puntos_entry.insert(0, "500")
        self.n_puntos_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.calcular_btn = ctk.CTkButton(self.frame, text="Calcular", command=self.leer_entradas)
        self.calcular_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Frame para tabla y gráfica
        self.result_frame = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.result_frame.rowconfigure(0, weight=0)
        self.result_frame.rowconfigure(1, weight=1)
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.result_frame, text="Resultados:", **estilo_label).grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=10)
        
        self.resultados_frame = ctk.CTkFrame(self.result_frame, fg_color=("gray98", "gray12"))
        self.resultados_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.resultados_frame.rowconfigure(0, weight=0)
        self.resultados_frame.columnconfigure(0, weight=1)
        self.resultados_frame.columnconfigure(1, weight=1)
        
        # Frame para la tabla
        self.table_frame = ctk.CTkFrame(self.resultados_frame, fg_color=("white", "gray10"), width=500, height=400)
        self.table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=0)
        self.table_frame.rowconfigure(1, weight=1)

        # Frame para la gráfica
        self.frame_grafica = ctk.CTkFrame(self.resultados_frame, fg_color=("white", "gray10"), width=500, height=400)
        self.frame_grafica.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        

    def leer_entradas(self):
        try:
            funcion_inf_str = self.funcion_inf_entry.get()
            funcion_sup_str = self.funcion_sup_entry.get()
            a = float(self.limite_inferior_entry.get())
            b = float(self.limite_superior_entry.get())
            n = int(self.n_puntos_entry.get())
            self.calcular_area_entre_curvas(funcion_inf_str, funcion_sup_str, a, b, n)
        except ValueError:
            self.mostrar_error("Por favor, ingrese valores válidos.")

    def mostrar_error(self, mensaje):
        error_label = ctk.CTkLabel(self.result_frame, text=mensaje, text_color="red", **estilo_label)
        error_label.pack()

    def calcular_area_entre_curvas(self, funcion_inf_str, funcion_sup_str, a, b, n):
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import math

        # Limpiar resultados anteriores SOLO de los frames de resultados
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()

        # Preparar funciones seguras
        def f_inf(x):
            try:
                return eval(funcion_inf_str, {"x": x, "np": np, "math": math, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log, "sqrt": np.sqrt})
            except Exception:
                return float('nan')
        def f_sup(x):
            try:
                return eval(funcion_sup_str, {"x": x, "np": np, "math": math, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log, "sqrt": np.sqrt})
            except Exception:
                return float('nan')

        # Encontrar el rango vertical para muestreo
        x_plot = np.linspace(a, b, 200)
        y_inf = np.array([f_inf(xi) for xi in x_plot])
        y_sup = np.array([f_sup(xi) for xi in x_plot])
        y_min = min(np.min(y_inf), np.min(y_sup), 0)
        y_max = max(np.max(y_inf), np.max(y_sup), 0)

        # Generar puntos aleatorios
        x_rand = np.random.uniform(a, b, n)
        y_rand = np.random.uniform(y_min, y_max, n)
        f_inf_rand = np.array([f_inf(xi) for xi in x_rand])
        f_sup_rand = np.array([f_sup(xi) for xi in x_rand])

        # Determinar si el punto está entre las curvas
        interior = ((y_rand >= np.minimum(f_inf_rand, f_sup_rand)) & (y_rand <= np.maximum(f_inf_rand, f_sup_rand))).astype(int)
        n_interior = np.sum(interior)
        area_rect = (b - a) * (y_max - y_min)
        area_estim = area_rect * n_interior / n

        # --- Presentación de resultados en table_frame ---
        # Totales arriba
        totales_frame = ctk.CTkFrame(self.table_frame, fg_color=("white", "gray10"))
        totales_frame.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(totales_frame, text=f"Interior: {n_interior}   ;   Totales: {n}   ;   Área estimada: {area_estim:.6f}", width=120, text_color="white", **estilo_label).pack(side="left", padx=5)


        # Tabla scrolleable
        tabla_scroll = ctk.CTkScrollableFrame(self.table_frame, width=500, height=400)
        tabla_scroll.pack(fill="both", expand=True)
        headers = ["X", "f_inf(x)", "f_sup(x)", "aleatorios", "interior"]
        for j, h in enumerate(headers):
            ctk.CTkLabel(tabla_scroll, text=h, width=100, anchor="center", fg_color=("gray80", "gray30"), font=("Arial", 12, "bold")).grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
        for i in range(n):
            ctk.CTkLabel(tabla_scroll, text=f"{x_rand[i]:.6f}", width=100).grid(row=i+1, column=0)
            ctk.CTkLabel(tabla_scroll, text=f"{f_inf_rand[i]:.6f}", width=100).grid(row=i+1, column=1)
            ctk.CTkLabel(tabla_scroll, text=f"{f_sup_rand[i]:.6f}", width=100).grid(row=i+1, column=2)
            ctk.CTkLabel(tabla_scroll, text=f"{y_rand[i]:.6f}", width=100).grid(row=i+1, column=3)
            ctk.CTkLabel(tabla_scroll, text=f"{interior[i]}", width=100).grid(row=i+1, column=4)

        # --- Presentación de la gráfica en frame_grafica ---
        fig, ax = plt.subplots(figsize=(6,3), dpi=100)
        ax.plot(x_plot, y_inf, label="Curva inferior f(x)", color="blue")
        ax.plot(x_plot, y_sup, label="Curva superior g(x)", color="orange")
        # Puntos Monte Carlo: interiores en rojo, exteriores en verde
        ax.scatter(x_rand[interior==1], y_rand[interior==1], color="red", s=10, alpha=0.6, label="Puntos interiores")
        ax.scatter(x_rand[interior==0], y_rand[interior==0], color="green", s=10, alpha=0.6, label="Puntos exteriores")
        ax.set_title("Área entre dos curvas - Monte Carlo")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
