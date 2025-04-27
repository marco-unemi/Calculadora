import customtkinter as ctk
from styles.styles import estilo_label_titulos


class Ecuacion:
    def __init__(self, workspace_frame):
        self.workspace_frame = workspace_frame
        
    def limpiar_workspace(self):
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        
    def mostrar_contenido(self):
        self.limpiar_workspace()
        
        ctk.CTkLabel(self.workspace_frame, text="Sistema de ecuaciones", **estilo_label_titulos).pack(pady=20)