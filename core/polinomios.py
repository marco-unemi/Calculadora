import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from styles.styles import estilo_label_titulos, estilo_label
import re


class Polinomio:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.polinomio_a = None
        self.polinomio_b = None
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        self.polinomio_a = None
        self.polinomio_b = None
        
    def parse_polinomio(self, texto):
        # Eliminar espacios y paréntesis
        texto = texto.replace(" ", "").replace("(", "").replace(")", "")
        if not texto:
            return np.array([0])

        # Dividir en términos
        terminos = []
        # Agregar un + al inicio si no hay signo
        if texto[0] not in ['+', '-']:
            texto = '+' + texto
        
        # Encontrar todos los términos con su signo
        patron = r'[+-][^+-]*'
        terminos_raw = re.findall(patron, texto)
        
        # Procesar cada término
        coeficientes = {}
        max_grado = 0
        
        for termino in terminos_raw:
            # Separar signo del resto del término
            signo = 1 if termino[0] == '+' else -1
            termino = termino[1:]  # Eliminar el signo
            
            if not termino:  # Si solo hay signo, ignorar
                continue
                
            # Buscar el coeficiente y el exponente
            if 'x' in termino:
                partes = termino.split('x')
                # Coeficiente
                if partes[0] == '':
                    coef = 1
                else:
                    try:
                        coef = float(partes[0])
                    except ValueError:
                        continue
                
                # Exponente
                if len(partes) > 1:
                    if partes[1].startswith('^'):
                        try:
                            exp = int(partes[1][1:])
                        except ValueError:
                            continue
                    elif partes[1] == '':
                        exp = 1
                    else:
                        continue
                else:
                    exp = 1
            else:
                # Término independiente
                try:
                    coef = float(termino)
                    exp = 0
                except ValueError:
                    continue
            
            # Aplicar el signo al coeficiente
            coef *= signo
            
            # Actualizar el grado máximo
            max_grado = max(max_grado, exp)
            
            # Agregar o actualizar el coeficiente
            if exp in coeficientes:
                coeficientes[exp] += coef
            else:
                coeficientes[exp] = coef
        
        # Crear el array de coeficientes
        resultado = np.zeros(max_grado + 1)
        for exp, coef in coeficientes.items():
            resultado[exp] = coef
            
        return resultado
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Polinomios", **estilo_label_titulos).pack(pady=20)
        
        # ------ Fila 1: contenedor de polinomios A y B ------ #
        self.frame_polinomios = ctk.CTkFrame(self.workspace_frame, fg_color=("gray93", "gray12"))
        self.frame_polinomios.pack(pady=10, padx=20, fill="x")
        self.frame_polinomios.columnconfigure(0, weight=1)
        self.frame_polinomios.columnconfigure(1, weight=1)
        
        # --- Sección de Polinomio A (Columna 0) --- #
        self.frame_polinomio_a = ctk.CTkFrame(self.frame_polinomios, fg_color=("white", "gray10"))
        self.frame_polinomio_a.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_polinomio_a_title = ctk.CTkLabel(self.frame_polinomio_a, text="Polinomio A", **estilo_label)
        self.label_polinomio_a_title.pack(pady=5)
        
        self.entry_polinomio_a = ctk.CTkEntry(self.frame_polinomio_a, width=200, textvariable=self.polinomio_a)
        self.entry_polinomio_a.pack(pady=5, padx=10)
        self.entry_polinomio_a.insert(0, "2x^2-1")
        
        # --- Boton de vaciar --- #
        self.vaciar_a_button = ctk.CTkButton(self.frame_polinomio_a, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_polinomio_a)
        self.vaciar_a_button.pack(pady=5)
        
        # --- Sección de Polinomio B (Columna 1) --- #
        self.frame_polinomio_b = ctk.CTkFrame(self.frame_polinomios, fg_color=("white", "gray10"))
        self.frame_polinomio_b.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.label_polinomio_b_title = ctk.CTkLabel(self.frame_polinomio_b, text="Polinomio B", **estilo_label)
        self.label_polinomio_b_title.pack(pady=5)
        
        self.entry_polinomio_b = ctk.CTkEntry(self.frame_polinomio_b, width=200, textvariable=self.polinomio_b)
        self.entry_polinomio_b.pack(pady=5, padx=10)
        self.entry_polinomio_b.insert(0, "5x-6")
        
        # --- Boton de vaciar --- #
        self.vaciar_b_button = ctk.CTkButton(self.frame_polinomio_b, text="Vaciar", fg_color="#df0000", hover_color='#b81414', command=self.vaciar_polinomio_b)
        self.vaciar_b_button.pack(pady=5)
        
        # ------ Fila 2: Botones de Operaciones ------ #
        self.frame_operaciones = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"))
        self.frame_operaciones.pack(pady=10, padx=20, fill="x")
        self.frame_operaciones.columnconfigure(0, weight=1)
        self.frame_operaciones.columnconfigure(1, weight=1)
        self.frame_operaciones.columnconfigure(2, weight=1)
        
        # --- Botones --- #
        self.sumar_button = ctk.CTkButton(self.frame_operaciones, text="Sumar", command=self.sumar)
        self.sumar_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.restar_button = ctk.CTkButton(self.frame_operaciones, text="Restar", command=self.restar)
        self.restar_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.multiplicar_button = ctk.CTkButton(self.frame_operaciones, text="Multiplicar", command=self.multiplicar)
        self.multiplicar_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
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


    def vaciar_polinomio_a(self):
        self.polinomio_a = None
        self.entry_polinomio_a.delete(0, ctk.END)

    def vaciar_polinomio_b(self):
        self.polinomio_b = None
        self.entry_polinomio_b.delete(0, ctk.END)

    def _leer_entradas_polinomios(self):
        try:
            texto_a = self.entry_polinomio_a.get().strip()
            texto_b = self.entry_polinomio_b.get().strip()
            if not texto_a:
                raise ValueError("Debe ingresar el Polinomio A.")
            if not texto_b:
                raise ValueError("Debe ingresar el Polinomio B.")
            polinomio_a = self.parse_polinomio(texto_a)
            polinomio_b = self.parse_polinomio(texto_b)
            return polinomio_a, polinomio_b
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error en las entradas: {e}")
            return None

    def sumar(self):
        entradas = self._leer_entradas_polinomios()
        if entradas is None:
            return
        polinomio_a, polinomio_b = entradas
        try:
            max_grado = max(len(polinomio_a) - 1, len(polinomio_b) - 1)
            resultado = np.zeros(max_grado + 1)
            resultado[:len(polinomio_a)] += polinomio_a
            resultado[:len(polinomio_b)] += polinomio_b
            print(f"Resultado de la suma (array): {resultado}")
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A + B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al sumar polinomios: {e}")

    def restar(self):
        entradas = self._leer_entradas_polinomios()
        if entradas is None:
            return
        polinomio_a, polinomio_b = entradas
        try:
            max_grado = max(len(polinomio_a) - 1, len(polinomio_b) - 1)
            resultado = np.zeros(max_grado + 1)
            resultado[:len(polinomio_a)] += polinomio_a
            resultado[:len(polinomio_b)] -= polinomio_b
            print(f"Resultado de la resta (array): {resultado}")
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A - B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al restar polinomios: {e}")

    def multiplicar(self):
        entradas = self._leer_entradas_polinomios()
        if entradas is None:
            return
        polinomio_a, polinomio_b = entradas
        try:
            resultado = np.convolve(polinomio_a, polinomio_b)
            print(f"Resultado de la multiplicación (array): {resultado}")
            self.mostrar_resultado(resultado, self.frame_resultado_grid, 'A × B =')
        except Exception as e:
            self.mostrar_error(self.frame_resultado_grid, f"Error al multiplicar polinomios: {e}")
            
    # def raiz(self):
    #     polinomio_texto = self.entry_polinomio_a.get()
        
    #     try:
            
    #         ecuacion = sp.sympify(polinomio_texto)
            
    #         soluciones = sp.solve(ecuacion, x)

    #         self.mostrar_resultado_ecuacion(soluciones)

    #     except (SyntaxError, TypeError):
    #         messagebox.showerror("Error", "Error al interpretar la ecuación. Asegúrese de usar una sintaxis válida.")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Ocurrió un error al calcular la raíz: {e}")


    def mostrar_error(self, frame, text):
        for widget in frame.winfo_children():
            widget.destroy()
        self.label_err = ctk.CTkLabel(frame, text=text, text_color="red")
        self.label_err.pack()

    def polinomio_a_unicode(self, polinomio):
        super_map = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
        texto_resultado = ""
        terminos_encontrados = False
        for i in range(len(polinomio)-1, 0, -1):
            coef = polinomio[i]
            if coef != 0:
                terminos_encontrados = True
                if texto_resultado and coef > 0:
                    texto_resultado += "+"
                elif coef < 0:
                    texto_resultado += "-"
                if abs(coef) != 1:
                    texto_resultado += str(abs(int(coef)) if coef.is_integer() else abs(coef))
                texto_resultado += "x"
                if i > 1:
                    texto_resultado += str(i).translate(super_map)
        coef = polinomio[0]
        if coef != 0:
            if texto_resultado and coef > 0:
                texto_resultado += "+"
            elif coef < 0:
                texto_resultado += "-"
            texto_resultado += str(abs(int(coef)) if coef.is_integer() else abs(coef))
        elif not terminos_encontrados:
            texto_resultado = "0"
        return texto_resultado

    def mostrar_resultado(self, polinomio, frame, label=None):
        # Limpiar frames
        for widget in self.frame_resultado_grid.winfo_children():
            widget.destroy()
        for widget in self.frame_resultado_label.winfo_children():
            widget.destroy()

        if polinomio is not None:
            if label:
                # Mostrar etiqueta
                self.frame_resultado_label.grid_rowconfigure(0, weight=1)
                self.frame_resultado_label.grid_columnconfigure(0, weight=1)
                label_widget = ctk.CTkLabel(self.frame_resultado_label, text=label)
                label_widget.grid(row=0, column=0, sticky="nsew")

            # Convertir el polinomio a texto Unicode bonito
            texto_resultado = self.polinomio_a_unicode(polinomio)
            resultado = ctk.CTkLabel(self.frame_resultado_grid, text=texto_resultado, 
                                   fg_color=("white", "gray10"))
            resultado.pack(padx=5, pady=5)
        else:
            # Centrar mensaje de no hay resultado
            label_vacio = ctk.CTkLabel(self.frame_resultado_grid, text="No hay resultado para mostrar.")
            label_vacio.pack(padx=5, pady=5)
            
            