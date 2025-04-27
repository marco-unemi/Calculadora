import customtkinter 
from styles.styles import estilo_label_titulos, estilo_label


class AcercaDe:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        self.scrollable_frame = None
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        customtkinter.CTkLabel(self.workspace_frame, text="Acerca de", **estilo_label_titulos).pack(pady=20)
        
        self.frame_info = customtkinter.CTkFrame(self.workspace_frame, fg_color=("gray95", "gray12"))
        self.frame_info.pack(pady=150, padx=150, fill="both")
        self.frame_info.grid_columnconfigure(0, weight=1)
        self.frame_info.grid_columnconfigure(1, weight=1)
        
        # Datos para la "tabla"
        data = {
            "Nombre Autor:": "Marco Arteaga",
            "Carrera:": "Ingeniería en Software",
            "Semestre:": "Sexto semestre",
            "Año Académico:": "Abril 2025 - Julio 2025",
            "Profesor:": "Ing. Isidro Fabricio Morales Torres",
            "Materia:": "Modelos matemáticos y simulación"
        }

        # Crear etiquetas en forma de tabla
        for i, (clave, valor) in enumerate(data.items()):
            customtkinter.CTkLabel(self.frame_info, text=clave, anchor="w", **estilo_label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            customtkinter.CTkLabel(self.frame_info, text=valor, anchor="w").grid(row=i, column=1, sticky="w", padx=10, pady=5)
