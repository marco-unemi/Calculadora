import customtkinter as ctk
from tkinter import messagebox
from utils import estilo_label, estilo_boton, crear_scrollable_frame
import numpy as np
import time
import sympy as sp
from sympy.abc import x

class OperacionesEcuaciones:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.scrollable_frame = None
        self.ecuacion_var = ctk.StringVar()
        self.evaluar_en_var = ctk.StringVar()
        self.limite_a_var = ctk.StringVar()
        self.limite_b_var = ctk.StringVar()

    def limpiar_workspace(self):
        # Limpia el contenido previo
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        self.scrollable_frame = None


    def mostrar_contenido(self):
        # Limpia el área antes de agregar contenido nuevo
        self.limpiar_workspace()

        # Crear el frame con scroll usando la función de utils
        self.scrollable_frame = crear_scrollable_frame(self.workspace_frame)

        # Título principal
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Operaciones con Ecuaciones", **estilo_label(font_size=16))
        title_label.pack(pady=20)


        # --- Fila 1 ---
        frame_ecuacion = ctk.CTkFrame(self.scrollable_frame)
        frame_ecuacion.pack(pady=10, padx=20, fill="x")

        label_ecuacion = ctk.CTkLabel(frame_ecuacion, text="Ecuacion:", **estilo_label())
        label_ecuacion.pack(padx=5, pady=(5, 0))
        entry_ecuacion = ctk.CTkEntry(frame_ecuacion, width=600, textvariable=self.ecuacion_var)
        entry_ecuacion.pack(padx=5, pady=(0, 5))

        # Campos para los límites de integración
        frame_limites = ctk.CTkFrame(frame_ecuacion)
        frame_limites.pack(padx=5, pady=10)
        frame_limites.columnconfigure(0, weight=0)
        frame_limites.columnconfigure(1, weight=0)
        frame_limites.columnconfigure(2, weight=0)

        label_evaluar_en = ctk.CTkLabel(frame_limites, text="Definir Integral: ", **estilo_label(font_size=16))
        label_evaluar_en.grid(row=0, column=0, padx=(0, 5))

        label_limite_a = ctk.CTkLabel(frame_limites, text="Límite inferior (a):", **estilo_label())
        label_limite_a.grid(row=0, column=1, padx=(0, 5), sticky="w")
        self.limite_a_var = ctk.StringVar()
        entry_limite_a = ctk.CTkEntry(frame_limites, width=100, textvariable=self.limite_a_var)
        entry_limite_a.grid(row=0, column=2, padx=(0, 10), sticky="ew")

        label_limite_b = ctk.CTkLabel(frame_limites, text="Límite superior (b):", **estilo_label())
        label_limite_b.grid(row=0, column=3, padx=(10, 5), sticky="w")
        self.limite_b_var = ctk.StringVar()
        entry_limite_b = ctk.CTkEntry(frame_limites, width=100, textvariable=self.limite_b_var)
        entry_limite_b.grid(row=0, column=4, padx=(0, 5), sticky="ew")

        frame_evaluar = ctk.CTkFrame(frame_ecuacion)
        frame_evaluar.pack(padx=5, pady=5)
        frame_evaluar.columnconfigure(0, weight=0)
        frame_evaluar.columnconfigure(1, weight=0)

        label_evaluar_en = ctk.CTkLabel(frame_evaluar, text="Evaluar derivada:", **estilo_label(font_size=16))
        label_evaluar_en.pack(side="left", padx=(5, 5))
        label_evaluar_en = ctk.CTkLabel(frame_evaluar, text="x =", **estilo_label())
        label_evaluar_en.pack(side="left", padx=(5, 0))
        entry_evaluar_en = ctk.CTkEntry(frame_evaluar, width=100, textvariable=self.evaluar_en_var)
        entry_evaluar_en.pack(side="left", padx=5)
        evaluar_button = ctk.CTkButton(frame_evaluar, text="Evaluar", command=self.evaluar_derivada, **estilo_boton())
        evaluar_button.pack(side="left", padx=10)

        vaciar_a_button = ctk.CTkButton(frame_ecuacion, text="Vaciar", command=self.vaciar, **estilo_boton(fg_color="#df0000", hover_color='#b81414'))
        vaciar_a_button.pack(padx=5, pady=20)

        # --- Fila 2: Botones de Operaciones ---
        frame_operaciones = ctk.CTkFrame(self.scrollable_frame)
        frame_operaciones.pack(pady=10, padx=20, fill="x")
        frame_operaciones.columnconfigure(0, weight=1)
        frame_operaciones.columnconfigure(1, weight=1)
        frame_operaciones.columnconfigure(2, weight=1)

        raiz_button = ctk.CTkButton(frame_operaciones, text="Raiz", command=self.raiz, **estilo_boton())
        raiz_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        derivada_button = ctk.CTkButton(frame_operaciones, text="Derivada", command=self.derivada, **estilo_boton())
        derivada_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        integral_d_button = ctk.CTkButton(frame_operaciones, text="Integral Definida", command=self.integral_definida, **estilo_boton())
        integral_d_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        integral_i_button = ctk.CTkButton(frame_operaciones, text="Integral Indefinida", command=self.integral_indefinida, **estilo_boton())
        integral_i_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        operacion_polinomio_button = ctk.CTkButton(frame_operaciones, text="Operacion con un polinomio", command=self.operacion_polinomio, **estilo_boton())
        operacion_polinomio_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # --- Fila 3: Resultado ---
        frame_resultado = ctk.CTkFrame(self.scrollable_frame)
        frame_resultado.pack(pady=20, padx=20, fill="x")

        label_resultado_title = ctk.CTkLabel(frame_resultado, text="Resultado:", **estilo_label(font_size=16))
        label_resultado_title.pack(pady=5)

        self.grid_frame_resultado = ctk.CTkFrame(frame_resultado, width=400)
        self.grid_frame_resultado.pack(pady=10)

    def vaciar(self):
        self.ecuacion_var.set("")
        time.sleep(0.01)
        for widget in self.grid_frame_resultado.winfo_children():
            widget.destroy()

    def raiz(self):
        ecuacion_texto = self.ecuacion_var.get()
        try:
            # sp.sympify convierte la cadena de texto de la ecuación a una expresión simbólica de SymPy.
            ecuacion = sp.sympify(ecuacion_texto)
            # sp.solve resuelve la ecuación simbólica para la variable 'x'.
            soluciones = sp.solve(ecuacion, x)

            self.mostrar_resultado_ecuacion(soluciones)

        except (SyntaxError, TypeError):
            messagebox.showerror("Error", "Error al interpretar la ecuación. Asegúrese de usar una sintaxis válida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular la raíz: {e}")

    def derivada(self):
        ecuacion_texto = self.ecuacion_var.get()
        try:
            # sp.sympify convierte la cadena de texto de la ecuación a una expresión simbólica de SymPy.
            ecuacion = sp.sympify(ecuacion_texto)
            # sp.diff calcula la derivada de la ecuación simbólica con respecto a 'x'.
            solucion = sp.diff(ecuacion, x)
            self.mostrar_resultado_ecuacion(solucion)
        except (SyntaxError, TypeError):
            messagebox.showerror("Error", "Error al interpretar la ecuación. Asegúrese de usar una sintaxis válida (ej: 5*x**2 + 2*x + 3).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular la derivada: {e}")

    def evaluar_derivada(self):
        ecuacion_texto = self.ecuacion_var.get()
        valor_evaluacion_str = self.evaluar_en_var.get()
        try:
            # sp.sympify convierte la cadena de texto de la ecuación a una expresión simbólica de SymPy.
            ecuacion = sp.sympify(ecuacion_texto)
            # sp.diff calcula la derivada de la ecuación simbólica con respecto a 'x'.
            derivada_sympy = sp.diff(ecuacion, x)

            try:
                # sp.sympify convierte la cadena de texto del valor de evaluación a una expresión simbólica.
                valor_evaluacion = sp.sympify(valor_evaluacion_str)

                # .subs(x, valor_evaluacion) sustituye la variable 'x' en la derivada con el valor de evaluación.
                # .evalf() evalúa numéricamente la expresión resultante.
                resultado_evaluacion = derivada_sympy.subs(x, valor_evaluacion).evalf()
                self.mostrar_resultado_ecuacion(f"f'({valor_evaluacion}) = {resultado_evaluacion}")
            except (SyntaxError, TypeError):
                messagebox.showerror("Error", "Error al interpretar el valor para evaluar.")

        except (SyntaxError, TypeError):
            messagebox.showerror("Error", "Error al interpretar la ecuación.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al evaluar la derivada: {e}")

    def integral_definida(self):
        ecuacion_texto = self.ecuacion_var.get()
        limite_a_str = self.limite_a_var.get()
        limite_b_str = self.limite_b_var.get()
        try:
            # sp.sympify convierte la cadena de texto de la ecuación y los límites a expresiones simbólicas de SymPy.
            ecuacion = sp.sympify(ecuacion_texto)
            a = sp.sympify(limite_a_str)
            b = sp.sympify(limite_b_str)
            # sp.integrate calcula la integral definida de la ecuación simbólica con respecto a 'x' desde 'a' hasta 'b'.
            solucion = sp.integrate(ecuacion, (x, a, b))
            self.mostrar_resultado_ecuacion(solucion)
        except (SyntaxError, TypeError):
            messagebox.showerror("Error", "Error al interpretar la ecuación. Asegúrese de usar una sintaxis válida (ej: 5*x**2 + 2*x + 3).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular la Integral: {e}")

    def integral_indefinida(self):
        ecuacion_texto = self.ecuacion_var.get()
        try:
            # sp.sympify convierte la cadena de texto de la ecuación a una expresión simbólica de SymPy.
            ecuacion = sp.sympify(ecuacion_texto)
            # sp.integrate calcula la integral indefinida de la ecuación simbólica con respecto a 'x'.
            solucion = sp.integrate(ecuacion, x)
            self.mostrar_resultado_ecuacion(solucion)
        except (SyntaxError, TypeError):
            messagebox.showerror("Error", "Error al interpretar la ecuación. Asegúrese de usar una sintaxis válida (ej: 5*x**2 + 2*x + 3).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular la Integral: {e}")

    def operacion_polinomio(self):
        ecuacion_texto = self.ecuacion_var.get()
        try:
            # sp.sympify convierte la cadena de texto de la ecuación a una expresión simbólica de SymPy.
            ecuacion = sp.sympify(ecuacion_texto)
            # np.linspace crea un array de números espaciados uniformemente en un intervalo.
            x_val = np.linspace(0.1, 10, 200)
            # Evalúa la ecuación simbólica (sustituyendo 'x' por los valores numéricos de x_val) y realiza operaciones numéricas con NumPy.
            y_val = (x_val**2) * np.exp(x_val)*np.log(x_val+1)

            print(f'\nX = {x_val}')
            print(f'\nY = {y_val}')
        except (SyntaxError, TypeError):
            messagebox.showerror("Error", "Error al interpretar la ecuación.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular el Polinomio: {e}")

    def mostrar_resultado_ecuacion(self, resultado):
        # Limpiar el frame de resultados
        for widget in self.grid_frame_resultado.winfo_children():
            widget.destroy()

        if resultado is not None:
            if isinstance(resultado, list): # Si es una lista (como las soluciones de solve)
                for i, sol in enumerate(resultado):
                    resultado_str = str(sol).replace('sqrt(', '√(')
                    resultado_label = ctk.CTkLabel(self.grid_frame_resultado, text=f"x{i+1} = {resultado_str}", **estilo_label())
                    resultado_label.pack(pady=5)
                if not resultado:
                    no_resultado_label = ctk.CTkLabel(self.grid_frame_resultado, text="No se encontraron soluciones.", **estilo_label())
                    no_resultado_label.pack(pady=5)
            else:
                resultado_str = str(resultado).replace('sqrt(', '√(')
                resultado_label = ctk.CTkLabel(self.grid_frame_resultado, text=f"f'(x) = {resultado_str}", **estilo_label())
                resultado_label.pack(pady=5)
        else:
            no_resultado_label = ctk.CTkLabel(self.grid_frame_resultado, text="No se encontraron soluciones.")
            no_resultado_label.pack(pady=5)