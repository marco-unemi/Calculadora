import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import poisson


class DistribucionPoisson:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
    
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
            
    def _build_ui(self):
        self.limpiar_workspace()
        ctk.CTkLabel(self.workspace_frame, text="Distribución de Poisson", **estilo_label_titulos).pack(pady=20)

        # Frame de entradas
        self.frame_entradas = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_entradas.pack(pady=10, padx=20, fill="x")
        self.frame_entradas.columnconfigure(0, weight=1)
        self.frame_entradas.columnconfigure(1, weight=1)

        # Lambda
        ctk.CTkLabel(self.frame_entradas, text="λ (media):", **estilo_label).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_lambda = ctk.CTkEntry(self.frame_entradas, width=100)
        self.entry_lambda.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.entry_lambda.insert(0, "5.0")

        # k max
        ctk.CTkLabel(self.frame_entradas, text="k máximo:", **estilo_label).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_kmax = ctk.CTkEntry(self.frame_entradas, width=100)
        self.entry_kmax.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.entry_kmax.insert(0, "15")

        # Botón calcular
        self.boton_calcular = ctk.CTkButton(self.frame_entradas, text="Calcular y Graficar", command=self.calcular_poisson)
        self.boton_calcular.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para resultado (gráfica)
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_resultado.pack(pady=10, padx=20)
        self.label_resultado_title = ctk.CTkLabel(self.frame_resultado, text="Resultado:", **estilo_label)
        self.label_resultado_title.pack(pady=5)
        self.frame_resultado_grid = ctk.CTkFrame(self.frame_resultado, width=800, height=500, fg_color=("white", "gray10"))
        self.frame_resultado_grid.pack(pady=(10, 0))

    def calcular_poisson(self):
        # Limpiar resultado anterior
        for widget in self.frame_resultado_grid.winfo_children():
            widget.destroy()
        try:
            lam = float(self.entry_lambda.get())
            kmax = int(self.entry_kmax.get())
            if lam <= 0 or kmax <= 0:
                raise ValueError("λ y k máximo deben ser positivos.")
            k = np.arange(0, kmax+1)
            
            pmf = poisson.pmf(k, lam)
            # Graficar
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(k, pmf, color="#4a90e2", alpha=0.8)
            ax.plot(k, pmf, 'r.-', color="red")  
            ax.set_xlabel("k")
            ax.set_ylabel("P(X = k)")
            ax.set_title(f"Distribución de Poisson (λ = {lam})")
            ax.grid(True, axis="y", linestyle=":", alpha=0.5)
            for i, v in enumerate(pmf):
                if v > 0.01:
                    ax.text(k[i], v, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.frame_resultado_grid)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            canvas.draw()
        except Exception as e:
            ctk.CTkLabel(self.frame_resultado_grid, text=f"Error: {e}", text_color="red").pack(pady=10)