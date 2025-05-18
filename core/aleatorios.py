import customtkinter as ctk
from styles.styles import estilo_label_titulos, estilo_label

class Aleatorios:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.entry_a = None
        self.entry_c = None
        self.entry_m = None
        self.entry_n = None
        self.entry_x0 = None
        
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
    
    def _build_ui(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Generación de Números Aleatorios Congruencial Lineal", **estilo_label_titulos).pack(pady=20)
        
        self.frame = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"), width=700, height=200)
        self.frame.pack(pady=10, padx=10)  # Expandir para ocupar todo el espacio
        
        # Configurar el grid del frame principal para centrar el contenido
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Crear un sub-frame para los elementos
        self.sub_frame = ctk.CTkFrame(self.frame, fg_color=("white", "gray10"), width=700, height=200)
        self.sub_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")  # Centrar el sub-frame
        
        # Añadir los elementos al sub-frame
        self.label_n = ctk.CTkLabel(self.sub_frame, text="Cantidad de Números:", **estilo_label)
        self.label_n.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_n = ctk.CTkEntry(self.sub_frame, width=100)
        self.entry_n.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_n.insert(0, "6")  # Valor por defecto para n
        
        self.label_x0 = ctk.CTkLabel(self.sub_frame, text=f"Semilla (X{"\u2080"}):", **estilo_label)
        self.label_x0.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_x0 = ctk.CTkEntry(self.sub_frame, width=100)
        self.entry_x0.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_x0.insert(0, "7")  # Valor por defecto para x0
        
        self.label_a = ctk.CTkLabel(self.sub_frame, text="Multiplicador (a):", **estilo_label)
        self.label_a.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_a = ctk.CTkEntry(self.sub_frame, width=100)
        self.entry_a.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.entry_a.insert(0, "3")  # Valor por defecto para a
        
        self.label_c = ctk.CTkLabel(self.sub_frame, text="Incremento (c):", **estilo_label)
        self.label_c.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_c = ctk.CTkEntry(self.sub_frame, width=100)
        self.entry_c.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.entry_c.insert(0, "5")  # Valor por defecto para c
        
        self.label_m = ctk.CTkLabel(self.sub_frame, text="Modulo (m):", **estilo_label)
        self.label_m.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_m = ctk.CTkEntry(self.sub_frame, width=100)
        self.entry_m.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.entry_m.insert(0, "8")  # Valor por defecto para m
        
        
        # --- Botón para generar números aleatorios ---
        self.boton_generar = ctk.CTkButton(self.sub_frame, text="Generar Números", command=self.generar_numeros)
        self.boton_generar.grid(row=5, column=0, columnspan=2, pady=(50, 10), padx=5, sticky="n")  # Centrar el botón
        
        
        self.frame_resultado = ctk.CTkFrame(self.workspace_frame, fg_color=("white", "gray10"), width=600, height=200)
        self.frame_resultado.pack(pady=20, padx=20)
        
        # Configurar el grid del frame_resultado para centrar el contenido
        self.frame_resultado.grid_rowconfigure(0, weight=1)
        self.frame_resultado.grid_rowconfigure(1, weight=1)
        self.frame_resultado.grid_columnconfigure(0, weight=1)
        
        self.label_resultado_title = ctk.CTkLabel(self.frame_resultado, text="Resultado:", **estilo_label)
        self.label_resultado_title.grid(row=0, column=0, pady=5, padx=5, sticky="n")  # Centrar en la parte superior
        
        self.resultado = ctk.CTkTextbox(self.frame_resultado, width=600, height=200, fg_color=("gray93", "gray12"))
        self.resultado.grid(row=1, column=0, padx=5, pady=5, sticky="n")  # Centrar debajo del label
        self.resultado.configure(state="disabled")


    def leer_entradas(self):
        try:
            n = int(self.entry_n.get())
            x0 = int(self.entry_x0.get())
            a = int(self.entry_a.get())
            c = int(self.entry_c.get())
            m = int(self.entry_m.get())
            return n, x0, a, c, m
        except ValueError:
            return None
        
    def generar_numeros(self):
        entradas = self.leer_entradas()
        if entradas is None:
            self.resultado.configure(state="normal")
            self.resultado.delete("1.0", ctk.END)
            self.resultado.insert(ctk.END, "Error: Por favor, ingrese valores válidos.")
            self.resultado.configure(state="disabled")
            return
        
        n, x0, a, c, m = entradas
        
        # Generar números aleatorios
        numeros = []
        x = x0
        for i in range(n):
            x = (a * x + c) % m
            # u = x / m
            numeros.append(x)
        # Normalizar los números entre 0 y 1
        numeros = [x / m for x in numeros]
        
        # Mostrar resultado
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", ctk.END)
        self.resultado.insert(ctk.END, "Números generados:\n\n\n" + ", ".join(map(str, numeros)))
        self.resultado.configure(state="disabled")