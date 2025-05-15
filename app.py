import customtkinter
import os
from PIL import Image
from styles.styles import estilo_label_menu, estilo_boton_menu
from utils import scrollable_frame
from core.matrices import Matriz
from core.polinomios import Polinomio
from core.vectores import Vector
from core.grafica2d import Grafica2D
from core.grafica3d import Grafica3D
from core.derivacion import Derivacion
from core.integracion import Integracion
from core.acerca_de import AcercaDe

from UI.UI_Ecuaciones_dif import UIEcuacionDiferencial
from UI.UI_Sistema_de_ecuaciones import UISistemaEcuaciones
from UI.UI_Modelo_matematico import UIModeloMatematico
from UI.UI_SistemaDiferencial import UISistemaDiferencial

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self._set_appearance_mode("System")
        self.title("TotalMath")
        self.scrollable_frame = None

        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "assets/icons")
        light_img = Image.open(os.path.join(
            image_path, "info_dark.png")).resize((20, 20))
        dark_img = Image.open(os.path.join(
            image_path, "info_light.png")).resize((20, 20))

        self.info_image = customtkinter.CTkImage(
            light_image=light_img, dark_image=dark_img, size=(20, 20))

        # Frame contenedor para el menú y el borde
        self.menu_container_frame = customtkinter.CTkFrame(
            self, corner_radius=0)
        self.menu_container_frame.pack(side="left", fill="y")
        self.menu_container_frame.grid_rowconfigure(0, weight=1)
        self.menu_container_frame.grid_columnconfigure(0, weight=1)
        self.menu_container_frame.grid_columnconfigure(1, weight=0)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(
            # Ligeramente más angosto
            self.menu_container_frame, corner_radius=0, width=198, fg_color=("white", "gray10"))
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(12, weight=1)

        border_right_frame = customtkinter.CTkFrame(
            self.menu_container_frame, width=2, fg_color="gray50", corner_radius=0)
        border_right_frame.grid(row=0, column=1, sticky="ns")

        # Label del menu
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="TOTALMATH", compound="left", **estilo_label_menu)
        self.navigation_frame_label.grid(row=0, column=0, padx=40, pady=20)

        # Botones del menú
        self.menu_buttons = {
            "Matrices": self.matrices_button_event,
            "Polinomios": self.polinomios_button_event,
            "Vectores": self.vectores_button_event,
            "Gráficas 2D": self.graficas_2D_button_event,
            "Gráficas 3D": self.graficas_3D_button_event,
            "Derivación": self.derivacion_button_event,
            "Integración": self.integracion_button_event,
            "Ecuaciones Diferenciales": self.ecuacion_diferencial_button_event,
            "Sistemas de Ecuaciones": self.sistema_ecuaciones_button_event,
            "Sistema Diferencial": self.sistema_diferencial_button_event,
            "Modelo Matematico": self.modelo_matematico_button_event,
            "Acerca de": self.acerca_de_button_event
        }

        self.menu_buttons_widgets = {}

        # Mostrar los botones
        row = 1
        for option, command in self.menu_buttons.items():

            if option.lower().replace(" ", "_") == "acerca_de":
                row += 2

            button = customtkinter.CTkButton(
                self.navigation_frame,
                text=option,
                command=command,
                **estilo_boton_menu,
                image=self.info_image if option.lower().replace(
                    " ", "_") == "acerca_de" else None
            )

            button.grid(row=row, column=0, sticky="ew")
            self.menu_buttons_widgets[option.lower().replace(
                " ", "_")] = button

            row += 1

        # create workspace frame
        self.workspace_frame = customtkinter.CTkFrame(self)
        self.workspace_frame.pack(side="right", expand=True, fill="both")

        self.scrollable_frame = scrollable_frame(self.workspace_frame)

        # Instancias
        self.matrices = Matriz(self.scrollable_frame)
        self.polinomios = Polinomio(self.scrollable_frame)
        self.vectores = Vector(self.scrollable_frame)
        self.graficas_2D = Grafica2D(self.scrollable_frame)
        self.graficas_3D = Grafica3D(self.scrollable_frame)
        self.derivacion = Derivacion(self.scrollable_frame)
        self.integracion = Integracion(self.scrollable_frame)
        self.ecuaciones_diferenciales = UIEcuacionDiferencial(self.scrollable_frame)
        self.sistemas_de_ecuaciones = UISistemaEcuaciones(self.scrollable_frame)
        self.modelo_matematico = UIModeloMatematico(self.scrollable_frame)
        self.acerca_de = AcercaDe(self.scrollable_frame)
        self.sistema_diferencial = UISistemaDiferencial(self.scrollable_frame)

        self.selected_button = None

    def select_frame_by_name(self, name):
        if self.selected_button:
            self.selected_button.configure(
                fg_color="transparent", border_width=0)

        # Obtiene el nuevo botón
        button = self.menu_buttons_widgets.get(name.lower().replace(" ", "_"))

        if button:
            button.configure(fg_color=("gray75", "gray25"),
                             border_color=("black", "white"), border_width=1)
            self.selected_button = button

    # Eventos de botones

    def matrices_button_event(self):
        self.select_frame_by_name("matrices")
        self.matrices.mostrar_contenido()

    def polinomios_button_event(self):
        self.select_frame_by_name("polinomios")
        self.polinomios.mostrar_contenido()

    def vectores_button_event(self):
        self.select_frame_by_name("vectores")
        self.vectores.mostrar_contenido()

    def graficas_2D_button_event(self):
        self.select_frame_by_name("gráficas_2d")
        self.graficas_2D.mostrar_contenido()

    def graficas_3D_button_event(self):
        self.select_frame_by_name("gráficas_3d")
        self.graficas_3D.mostrar_contenido()

    def derivacion_button_event(self):
        self.select_frame_by_name("derivación")
        self.derivacion.mostrar_contenido()

    def integracion_button_event(self):
        self.select_frame_by_name("integración")
        self.integracion.mostrar_contenido()

    def ecuacion_diferencial_button_event(self):
        self.select_frame_by_name("ecuaciones_diferenciales")
        self.ecuaciones_diferenciales._build_ui()

    def sistema_ecuaciones_button_event(self):
        self.select_frame_by_name("sistemas_de_ecuaciones")
        self.sistemas_de_ecuaciones._build_ui()
        
    def modelo_matematico_button_event(self):
        self.select_frame_by_name("modelo_matematico")
        self.modelo_matematico._build_ui()

    def acerca_de_button_event(self):
        self.select_frame_by_name("acerca_de")
        self.acerca_de.mostrar_contenido()

    def sistema_diferencial_button_event(self):
        self.select_frame_by_name("sistema_diferencial")
        self.sistema_diferencial._build_ui()

