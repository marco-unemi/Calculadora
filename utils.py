import customtkinter as ctk


def scrollable_frame(parent):
    """Crea y devuelve un CTkScrollableFrame.

    Args:
        parent (ctk.CTkBaseClass): El widget padre donde se empaquetará el frame con scroll.

    Returns:
        ctk.CTkScrollableFrame: Una instancia de CTkScrollableFrame empaquetada para expandirse y llenar su padre.
    """
    scrollable_frame = ctk.CTkScrollableFrame(parent, corner_radius=0, fg_color=("white", "gray10")) # Crea una instancia de CTkScrollableFrame con el widget padre especificado.
    scrollable_frame.pack(fill="both", expand=True) # Empaqueta el frame con scroll para que se expanda en ambas direcciones (horizontal y vertical) y llene el espacio disponible en su padre.
    return scrollable_frame

