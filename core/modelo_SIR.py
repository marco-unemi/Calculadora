import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.integrate import solve_ivp

class ModeloMatematico:
    @staticmethod
    def sir_model_equations(t, y, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    @staticmethod
    def simular_sir(S0, I0, R0, N, beta, gamma, t_dias):
        y0 = S0, I0, R0
        t_span = [0, t_dias]
        t_eval = np.linspace(t_span[0], t_span[1], t_dias * 5)
        sol = solve_ivp(ModeloMatematico.sir_model_equations, t_span, y0, args=(N, beta, gamma),
                        dense_output=True, t_eval=t_eval)
        return sol.t, sol.y[0], sol.y[1], sol.y[2]

    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.link = "https://www.sciencedirect.com/science/article/pii/S1198743X14630019"
        
        # --- Información Conceptual del Modelo SIR ---
        self.CONCEPTOS_SIR = {
            "titulo": "Modelo de Propagación de Epidemias: SIR",
            "descripcion_articulo": ( # <-- NUEVA ENTRADA
                "Los modelos matemáticos en el campo de las enfermedades infecciosas pueden proporcionar predicciones "
                "valiosas cuando el alcance del concepto de predicción está adecuadamente definido. Un modelo matemático "
                "es un micromundo imaginario donde las entidades se comportan según reglas precisas, permitiendo investigar "
                "su comportamiento global y extraer consecuencias de las suposiciones realizadas. Para que las predicciones "
                "sean relevantes, el modelo debe corresponder a la realidad, aunque todos los modelos son simplificaciones. "
                "La robustez de un modelo se prueba comparándolo con otros más elaborados, buscando que predicciones similares "
                "surjan a pesar de las diferencias en los detalles del modelo." 
                # NOTA: He resumido un poco el texto que proporcionaste para que sea un "pequeño párrafo".
                #       Asegúrate de que el resumen mantenga la esencia y considera citar la fuente.
            ),
            "introduccion": (
                "El modelo SIR es uno de los modelos compartimentales más simples para describir la "
                "propagación de una enfermedad infecciosa en una población. La población se divide "
                "en tres compartimentos:"
            ),
            "compartimentos": [
                ("S - Susceptibles:", "Individuos que aún no han sido infectados pero pueden contraer la enfermedad."),
                ("I - Infectados:", "Individuos que actualmente tienen la enfermedad y pueden transmitirla."),
                ("R - Recuperados/Removidos:", "Individuos que se han recuperado de la enfermedad y han desarrollado inmunidad, o que han fallecido.")
            ],
            "proceso": (
                "El modelo describe el flujo de individuos de Susceptibles a Infectados, y de Infectados a Recuperados. "
                "Se asume que la población total (N = S + I + R) es constante."
            ),
            "ecuaciones_titulo": "Ecuaciones Diferenciales del Modelo:",
            "ecuaciones": [
                ("dS/dt = -β * S * I / N", "Cambio en el número de susceptibles con el tiempo."),
                ("dI/dt = β * S * I / N - γ * I", "Cambio en el número de infectados con el tiempo."),
                ("dR/dt = γ * I", "Cambio en el número de recuperados con el tiempo.")
            ],
            "parametros_titulo": "Parámetros Clave:",
            "parametros": [
                ("β (beta):", "Tasa de transmisión. Representa la probabilidad de transmisión por contacto entre un susceptible y un infectado."),
                ("γ (gamma):", "Tasa de recuperación. Es la tasa a la cual los infectados se recuperan (1/duración de la infección)."),
                ("N:", "Población total.")
            ],
            "r0_titulo": "Número Básico de Reproducción (R₀):",
            "r0_explicacion": (
                "R₀ = β / γ. Es una medida clave que indica el número promedio de infecciones secundarias "
                "causadas por un solo individuo infectado en una población completamente susceptible. "
                "Si R₀ > 1, la epidemia tiende a propagarse. Si R₀ < 1, tiende a desaparecer."
            )
        }
        
        # --- Datos del Ejemplo Precargado ---
        self.DATOS_EJEMPLO_SIR = {
            "titulo": "Configuración del Ejemplo Precargado",
            "poblacion_total": 1000, # Ejemplo: N
            "infectados_iniciales": 1,  # Ejemplo: I0
            "recuperados_iniciales": 0, # Ejemplo: R0
            "susceptibles_iniciales_calculados": True, # Se calculará como N - I0 - R0
            "beta": 0.4, # Tasa de transmisión para el ejemplo
            "gamma": 0.1, # Tasa de recuperación para el ejemplo (1/10 días de infección)
            "dias_simulacion": 365
        }
        self.DATOS_EJEMPLO_SIR["susceptibles_iniciales"] = (
            self.DATOS_EJEMPLO_SIR["poblacion_total"] - 
            self.DATOS_EJEMPLO_SIR["infectados_iniciales"] - 
            self.DATOS_EJEMPLO_SIR["recuperados_iniciales"]
        )
        
        # Datos del ejemplo
        self.N_ej = self.DATOS_EJEMPLO_SIR["poblacion_total"]
        self.I0_ej = self.DATOS_EJEMPLO_SIR["infectados_iniciales"]
        self.R0_ej = self.DATOS_EJEMPLO_SIR["recuperados_iniciales"]
        self.S0_ej = self.N_ej - self.I0_ej - self.R0_ej
        self.beta_ej = self.DATOS_EJEMPLO_SIR["beta"]
        self.gamma_ej = self.DATOS_EJEMPLO_SIR["gamma"]
        self.dias_ej = self.DATOS_EJEMPLO_SIR["dias_simulacion"]
        
        self.t, self.S, self.I, self.R = self.simular_sir(self.S0_ej, self.I0_ej, self.R0_ej, self.N_ej, self.beta_ej, self.gamma_ej, self.dias_ej)
        
        

    def _build_ui(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.workspace_frame, text="Modelo Matematico Investigado", **estilo_label_titulos).pack(pady=20)
        
        self.frame_general = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_general.pack(pady=10, padx=20, fill="x")
        self.frame_general.grid_rowconfigure(0, weight=0)
        self.frame_general.grid_rowconfigure(1, weight=0)
        self.frame_general.grid_rowconfigure(2, weight=0)
        self.frame_general.grid_rowconfigure(3, weight=0)
        self.frame_general.grid_rowconfigure(4, weight=0)
        self.frame_general.grid_rowconfigure(5, weight=0)
        self.frame_general.grid_rowconfigure(6, weight=0)
        self.frame_general.grid_rowconfigure(7, weight=0)
        self.frame_general.grid_rowconfigure(8, weight=0)
        self.frame_general.grid_rowconfigure(9, weight=0)
        self.frame_general.grid_rowconfigure(10, weight=0)
        self.frame_general.grid_columnconfigure(0, weight=1)
        
        self.titulo_modelo = ctk.CTkLabel(self.frame_general, text=f"{self.CONCEPTOS_SIR['titulo']}", **estilo_label)
        self.titulo_modelo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.context = ctk.CTkTextbox(self.frame_general, font=("Arial", 14), height=240, fg_color=("white", "gray10"))
        self.context.grid(row=1, padx=10, pady=10, sticky="ew")
        texto = f"{self.CONCEPTOS_SIR['descripcion_articulo']}\n\n"
        texto += f"{self.CONCEPTOS_SIR['introduccion']}\n\n"
        for nombre, desc in self.CONCEPTOS_SIR['compartimentos']:
            texto += f"{nombre} {desc}\n"
            
        texto += f"\n{self.CONCEPTOS_SIR['proceso']}\n\n"
        self.context.insert("0.0", texto)
        self.context.configure(state="disabled")
        
        self.titulo_ecuaciones = ctk.CTkLabel(self.frame_general, text=f"{self.CONCEPTOS_SIR['ecuaciones_titulo']}", **estilo_label)
        self.titulo_ecuaciones.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.ecuaciones = ctk.CTkTextbox(self.frame_general, font=("Arial", 14), height=100, fg_color=("white", "gray10"))
        self.ecuaciones.grid(row=3, padx=10, pady=10, sticky="ew")
        
        texto_ecuaciones = ''
        for eq, desc_eq in self.CONCEPTOS_SIR['ecuaciones']:
            texto_ecuaciones += f"{eq} ({desc_eq})\n"
        self.ecuaciones.insert("0.0", texto_ecuaciones)
        self.ecuaciones.configure(state="disabled")
        
        self.titulo_parametros = ctk.CTkLabel(self.frame_general, text=f"{self.CONCEPTOS_SIR['parametros_titulo']}", **estilo_label)
        self.titulo_parametros.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        self.parametros = ctk.CTkTextbox(self.frame_general, font=("Arial", 14), height=100, fg_color=("white", "gray10"))
        self.parametros.grid(row=5, padx=10, pady=10, sticky="ew")
        
        texto_parametros = ''
        for param, desc_param in self.CONCEPTOS_SIR['parametros']:
            texto_parametros += f"{param} {desc_param}\n"
        self.parametros.insert("0.0", texto_parametros)
        self.parametros.configure(state="disabled")
        
        self.titulo_r0 = ctk.CTkLabel(self.frame_general, text=f"{self.CONCEPTOS_SIR['r0_titulo']}", **estilo_label)
        self.titulo_r0.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        self.r0 = ctk.CTkTextbox(self.frame_general, font=("Arial", 14), height=75, fg_color=("white", "gray10"))
        self.r0.grid(row=7, padx=10, pady=10, sticky="ew")  
        
        texto_r0 = f"{self.CONCEPTOS_SIR['r0_explicacion']}\n"
        self.r0.insert("0.0", texto_r0)
        self.r0.configure(state="disabled")
        
        
        self.titulo_datos_ejemplo = ctk.CTkLabel(self.frame_general, text=f"{self.DATOS_EJEMPLO_SIR['titulo']}", **estilo_label)
        self.titulo_datos_ejemplo.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        
        self.frame_datos_ejemplo = ctk.CTkFrame(self.frame_general, fg_color=("white", "gray10"))
        self.frame_datos_ejemplo.grid(row=9, column=0, padx=10, pady=10, sticky="ew")
        
        self.inputs_ejemplo = {}
        labels = [
            ("Población Total (N):", "poblacion_total"),
            ("Infectados Iniciales (I0):", "infectados_iniciales"),
            ("Recuperados Iniciales (R0):", "recuperados_iniciales"),
            ("Tasa de Transmisión (β):", "beta"),
            ("Tasa de Recuperación (γ):", "gamma"),
            ("Duración de la Simulación (días):", "dias_simulacion"),
        ]
        for i, (label, key) in enumerate(labels):
            ctk.CTkLabel(self.frame_datos_ejemplo, text=label, font=("Arial", 14)).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = ctk.CTkEntry(self.frame_datos_ejemplo, width=100)
            entry.insert(0, str(self.DATOS_EJEMPLO_SIR[key]))
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            self.inputs_ejemplo[key] = entry
        
        self.boton_actualizar = ctk.CTkButton(self.frame_datos_ejemplo, text="Actualizar Simulación", command=self.actualizar_simulacion)
        self.boton_actualizar.grid(row=len(labels), column=0, columnspan=2, pady=10)
        
        self.frame_grafica = ctk.CTkFrame(self.frame_general, fg_color=("white", "gray10"))
        self.frame_grafica.grid(row=10, column=0, padx=10, pady=10, sticky="ew")
        
        self.grafica = ctk.CTkCanvas(self.frame_grafica, height=400)
        self.grafica.grid(row=11, column=0, padx=10, pady=10, sticky="ew")
        
        self._build_grafica()

    def _build_grafica(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.t, self.S, label='Susceptibles')
        ax.plot(self.t, self.I, label='Infectados')
        ax.plot(self.t, self.R, label='Recuperados')
        ax.set_xlabel('Tiempo (días)')
        ax.set_ylabel('Población')
        ax.grid(True)
        ax.legend()
        ax.set_title('Modelo SIR: Población en función del tiempo')
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.grafica)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        canvas.draw()

    def actualizar_simulacion(self):
        for widget in self.grafica.winfo_children():
            widget.destroy()
        # Lee los valores de los inputs
        try:
            N = int(self.inputs_ejemplo["poblacion_total"].get())
            I0 = int(self.inputs_ejemplo["infectados_iniciales"].get())
            R0 = int(self.inputs_ejemplo["recuperados_iniciales"].get())
            S0 = N - I0 - R0
            beta = float(self.inputs_ejemplo["beta"].get())
            gamma = float(self.inputs_ejemplo["gamma"].get())
            dias = int(self.inputs_ejemplo["dias_simulacion"].get())
            # Simula
            self.t, self.S, self.I, self.R = self.simular_sir(S0, I0, R0, N, beta, gamma, dias)
            self._build_grafica()
        except Exception as e:
            # Puedes mostrar un mensaje de error si lo deseas
            print(f"Error en los datos: {e}")

    def r0_ejemplo(self):
        return self.beta_ej / self.gamma_ej
        
        