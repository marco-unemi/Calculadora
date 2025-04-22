import customtkinter as ctk
from utils import estilo_label, crear_scrollable_frame


class AcercaDe:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        self.scrollable_frame = None
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        self.scrollable_frame = None
        
    def mostrar_contenido(self):
        self.limpiar_workspace()

        self.scrollable_frame = crear_scrollable_frame(self.workspace_frame)

        title_label = ctk.CTkLabel(self.scrollable_frame, text="Acerca de:", **estilo_label(font_size=16))
        title_label.pack(pady=20)
        
        frame_info = ctk.CTkFrame(self.scrollable_frame)
        frame_info.pack(pady=40, padx=20, fill="x")

        label_info = ctk.CTkLabel(frame_info, text="Nombre Autor:", **estilo_label(font_size=14)).pack(padx=5, pady=(5, 0))
        label_info = ctk.CTkLabel(frame_info, text="Marco Arteaga", **estilo_label()).pack(padx=5, pady=(0, 5))

        label_info = ctk.CTkLabel(frame_info, text="Carrera:", **estilo_label(font_size=14)).pack(padx=5, pady=(5, 0))
        label_info = ctk.CTkLabel(frame_info, text="Ingenieria en software", **estilo_label()).pack(padx=5, pady=(0, 5))
        
        label_info = ctk.CTkLabel(frame_info, text="Semestre:", **estilo_label(font_size=14)).pack(padx=5, pady=(5, 0))
        label_info = ctk.CTkLabel(frame_info, text="Sexto semestre", **estilo_label()).pack(padx=5, pady=(0, 5))
        
        label_info = ctk.CTkLabel(frame_info, text="Año Academico:", **estilo_label(font_size=14)).pack(padx=5, pady=(5, 0))
        label_info = ctk.CTkLabel(frame_info, text="Abril 2025 - Julio 2025", **estilo_label()).pack(padx=5, pady=(0, 5))
        
        label_info = ctk.CTkLabel(frame_info, text="Profesor:", **estilo_label(font_size=14)).pack(padx=5, pady=(5, 0))
        label_info = ctk.CTkLabel(frame_info, text="Ing. ISIDRO FABRICIO MORALES TORRES", **estilo_label()).pack(padx=5, pady=(0, 5))
        
        label_info = ctk.CTkLabel(frame_info, text="Materia:", **estilo_label(font_size=14)).pack(padx=5, pady=(5, 0))
        label_info = ctk.CTkLabel(frame_info, text="Modelos matematicos y simulacion", **estilo_label()).pack(padx=5, pady=(0, 5))
