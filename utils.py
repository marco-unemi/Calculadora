# utils.py
import customtkinter as ctk

def estilo_label(font_family=None, font_size=None, font_weight=None):
    """
    Define y devuelve un diccionario de estilo para las etiquetas (CTkLabel).

    Args:
        font_family (str, opcional): La familia de la fuente. Por defecto es None.
        font_size (int, opcional): El tamaño de la fuente. Por defecto es None.
        font_weight (str, opcional): El peso de la fuente ('normal', 'bold', etc.). Por defecto es None.

    Returns:
        dict: Un diccionario con la clave 'font' que contiene una tupla con la familia, tamaño y peso de la fuente.
    """
    estilo = {
        "font": ("Arial", 12, "bold")  # Estilo de fuente base: Arial, tamaño 12, negrita.
    }
    if font_family:
        estilo["font"] = (font_family,) + estilo["font"][1:] # Si se proporciona una familia de fuente, se reemplaza la existente, manteniendo el tamaño y el peso.
    if font_size:
        estilo["font"] = (estilo["font"][0], font_size) + estilo["font"][2:] # Si se proporciona un tamaño de fuente, se reemplaza el existente, manteniendo la familia y el peso.
    if font_weight:
        estilo["font"] = estilo["font"][:2] + (font_weight,) # Si se proporciona un peso de fuente, se reemplaza el existente, manteniendo la familia y el tamaño.
    return estilo


def estilo_boton(fg_color=None, hover_color=None, text_color=None, font=None):
    """
    Define y devuelve un diccionario de estilo para los botones (CTkButton).

    Args:
        fg_color (str, opcional): El color de fondo del botón. Por defecto es None.
        hover_color (str, opcional): El color de fondo al pasar el ratón. Por defecto es None.
        text_color (str, opcional): El color del texto del botón. Por defecto es None.
        font (tuple, opcional): La tupla de la fuente (familia, tamaño, peso). Por defecto es None.

    Returns:
        dict: Un diccionario con claves para el color de fondo, color al pasar el ratón, color del texto y la fuente.
    """
    estilo = {
        "fg_color": "#0d6efb",      # Color de fondo predeterminado: azul.
        "hover_color": "#0b5ed7",   # Color de fondo al pasar el ratón predeterminado: azul más oscuro.
        "text_color": "white",      # Color de texto predeterminado: blanco.
        "font": ("Arial", 12, "bold") # Fuente predeterminada: Arial, tamaño 12, negrita.
    }

    if fg_color:
        estilo["fg_color"] = fg_color # Si se proporciona un color de fondo, se reemplaza el predeterminado.
    if hover_color:
        estilo["hover_color"] = hover_color # Si se proporciona un color al pasar el ratón, se reemplaza el predeterminado.
    if text_color:
        estilo["text_color"] = text_color # Si se proporciona un color de texto, se reemplaza el predeterminado.
    if font:
        estilo["font"] = font # Si se proporciona una fuente, se reemplaza la predeterminada.
    return estilo

def crear_scrollable_frame(parent):
    """Crea y devuelve un CTkScrollableFrame.

    Args:
        parent (ctk.CTkBaseClass): El widget padre donde se empaquetará el frame con scroll.

    Returns:
        ctk.CTkScrollableFrame: Una instancia de CTkScrollableFrame empaquetada para expandirse y llenar su padre.
    """
    scrollable_frame = ctk.CTkScrollableFrame(parent) # Crea una instancia de CTkScrollableFrame con el widget padre especificado.
    scrollable_frame.pack(fill="both", expand=True) # Empaqueta el frame con scroll para que se expanda en ambas direcciones (horizontal y vertical) y llene el espacio disponible en su padre.
    return scrollable_frame








########################################
import numpy as np
x1 = np.arange(0, 100, 1)
x2 = np.linspace(0, 10, 100)
x3 = np.logspace(1, 5, 7)

#########################################
import numpy as np

# Define la matriz como un array de NumPy
# matriz_a = np.array([[1, 2], [3, 4]])
matriz_a = np.array([[2, -1], [-1, 2]])

# Calcula los valores propios y los vectores propios
valores_propios, vectores_propios = np.linalg.eig(matriz_a)

# Imprime los resultados
# print("Valores propios:")
# print(f'λ1: {valores_propios[0]} \nλ2: {valores_propios[1]}')
# print("\nVectores propios:")
# print(vectores_propios)

##################################################
import numpy as np

# Define la matriz de coeficientes A
A = np.array([[1, -3, 2],
              [5, 6, 1],
              [4, -1, 3]])

# Define el vector de términos independientes B
B = np.array([[-3],
              [13],
              [8]])

# Resuelve el sistema de ecuaciones Ax = B para encontrar x
solucion = np.linalg.solve(A, B)

# Imprime la solución
# print("Solución del sistema de ecuaciones:")
# print(solucion)

####################################################################
######### Ecuaciones ############
import numpy as np
import sympy as sp
from sympy.abc import x
# Raiz de un polinomio p=[5 2 3]; r=roots(p) p(x)=5x2+2x+3
p = [5, 2, 3]
r = np.roots(p)
# print('\nlas raices del polinomio son', r)

# pcomp = sum(c*x**i for i, c in enumerate(p[::-1]))
# print('\nel polinomio es: ', pcomp)

#############
# DERIVADA DE UNA FUNCION
import numpy as np
import sympy as sp
from sympy.abc import x

# DEFINIMOS LA FUNCION f = 1 / (1+exp(-x))
f = 1/(1+sp.exp(-x))
df = sp.diff(f, x)

k1 = df.subs(x, 2).evalf()

# print('Derivada ', df)
# print('Evaluar en x = 2 ', k1)

##########
# INTEGRAL DE UNA FUNCION
import numpy as np
import sympy as sp
from sympy.abc import x

f2 = sp.exp(x)*x
f2_ind = sp.integrate(f2, x)

f2_def = sp.integrate(f2, (x, 1, 2))

# print('integral indefinida', f2_ind)
# print('integral definida', f2_def)

###################
x_val = np.linspace(0.1, 10, 200)
y_val = (x_val**2) * np.exp(x_val)*np.log(x_val+1)

# print(f'\nX = {x_val}')
# print(f'\nY = {y_val}')







