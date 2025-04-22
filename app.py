# app.py
import customtkinter as ctk
from utils import estilo_label, estilo_boton

from matrices import OperacionesMatrices
from ecuaciones import OperacionesEcuaciones
from grafica2d import GraficaEcuaciones2D
from grafica3d import GraficaEcuaciones3D
from acerca_de import AcercaDe

ctk.set_appearance_mode("System") # Establece el modo de apariencia de la aplicación para que coincida con el sistema operativo (claro u oscuro).
ctk.set_default_color_theme("blue") # Establece el tema de color predeterminado de la aplicación a azul.

# Ventana principal
app = ctk.CTk() # Crea la ventana principal de la aplicación usando la clase CTk().
app.geometry("1000x600") # Establece el tamaño inicial de la ventana a 1000 píxeles de ancho y 600 píxeles de alto.
app.title("Mini programa de modelos matemáticos") # Establece el título de la ventana.

# Menu lateral Izquierdo
menu_frame = ctk.CTkFrame(app, width=200) # Crea un frame (contenedor) para el menú lateral izquierdo, con un ancho de 200 píxeles.
menu_frame.pack(side="left", fill="y", padx=10, pady=10) # Empaqueta el frame a la izquierda de la ventana, lo rellena verticalmente y añade un padding horizontal y vertical de 10 píxeles.

menu_label = ctk.CTkLabel(menu_frame, text="Menú de opciones", **estilo_label(font_size=16)) # Crea una etiqueta para el título del menú, utilizando la función estilo_label del archivo utils.py con un tamaño de fuente de 16.
menu_label.pack(pady=10) # Empaqueta la etiqueta con un padding vertical de 10 píxeles.

# Area derecha
workspace_frame = ctk.CTkFrame(app) # Crea un frame para el área de trabajo principal, que se mostrará a la derecha del menú.
workspace_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10) # Empaqueta el frame a la derecha, hace que se expanda para llenar el espacio restante y lo rellena tanto horizontal como verticalmente, con un padding de 10 píxeles.


# Instancias de las clases
operaciones_matrices = OperacionesMatrices(workspace_frame) 
operacionesEcuaciones = OperacionesEcuaciones(workspace_frame) 
graficaEcuaciones2D = GraficaEcuaciones2D(workspace_frame)
graficaEcuaciones3D = GraficaEcuaciones3D(workspace_frame) 
acerca_de = AcercaDe(workspace_frame) 


# Botones del menú
menu_buttons = {
    "Operaciones con matrices y vectores": operaciones_matrices.mostrar_contenido, 
    "Operaciones con ecuaciones": operacionesEcuaciones.mostrar_contenido, 
    "Gráfica de ecuaciones en 2D": graficaEcuaciones2D.mostrar_contenido, 
    "Gráfica de ecuaciones en 3D": graficaEcuaciones3D.mostrar_contenido, 
    "Acerca de": acerca_de.mostrar_contenido, 
}


# Mostrar los botones
for option, command in menu_buttons.items():
    button = ctk.CTkButton(
        menu_frame,
        text=option,
        command=command,
        **estilo_boton() #
    )
    button.pack(pady=5, padx=20, fill="x") 


# Inicializar la app
app.mainloop() # Inicia el bucle principal de la aplicación Tkinter, que es necesario para que la interfaz de usuario sea interactiva y se mantenga en pantalla.