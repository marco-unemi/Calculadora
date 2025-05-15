# core/numerical_solver.py
import math

def evaluate_fxy_numerical(f_str, x_val, y_val):
    """
    Evalúa la función f(x,y) de forma segura.
    """
    allowed_names = {
        "math": math, "x": x_val, "y": y_val,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
        "exp": math.exp, "log": math.log, "log10": math.log10, "sqrt": math.sqrt,
        "pow": math.pow, "fabs": math.fabs,
        "pi": math.pi, "e": math.e,
    }
    try:
        # Cuidado con eval. Aquí está restringido por allowed_names.
        return eval(f_str, {"__builtins__": {}}, allowed_names)
    except ZeroDivisionError:
        raise ZeroDivisionError(f"División por cero al evaluar f(x,y)='{f_str}' con x={x_val:.4f}, y={y_val:.4f}")
    except Exception as e:
        raise ValueError(f"Error al evaluar f(x,y)='{f_str}' con x={x_val:.4f}, y={y_val:.4f}\n{type(e).__name__}: {e}")

def _paso_euler(f_str, x_actual, y_actual, h):
    f_evaluada = evaluate_fxy_numerical(f_str, x_actual, y_actual)
    return y_actual + h * f_evaluada

def _paso_runge_kutta_4(f_str, x_actual, y_actual, h):
    k1 = evaluate_fxy_numerical(f_str, x_actual, y_actual)
    k2 = evaluate_fxy_numerical(f_str, x_actual + h/2, y_actual + (h/2)*k1)
    k3 = evaluate_fxy_numerical(f_str, x_actual + h/2, y_actual + (h/2)*k2)
    k4 = evaluate_fxy_numerical(f_str, x_actual + h, y_actual + h*k3)
    return y_actual + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

def solve_numerical_method(f_str, x0, y0, x_final, h, step_function):
    """
    Resuelve una EDO usando un método numérico genérico.
    step_function: la función que calcula el siguiente paso (e.g., _paso_euler).
    Retorna una lista de tuplas (x, y) y un posible mensaje de advertencia.
    """
    puntos_solucion = []
    x_actual = x0
    y_actual = y0
    iter_count = 0
    max_iter = 100000  # Límite de seguridad
    epsilon = 1e-9  # Tolerancia para la comparación con x_final
    warning_message = ""

    while x_actual < x_final + epsilon and iter_count <= max_iter:
        puntos_solucion.append((x_actual, y_actual))
        
        if abs(x_actual - x_final) < epsilon:
            break

        y_actual = step_function(f_str, x_actual, y_actual, h) # Usa la función de paso inyectada
        x_actual_prev = x_actual
        x_actual += h
        
        if x_actual > x_final and abs(x_actual - (x_actual_prev + h)) < epsilon :
            x_actual = x_final # forzamos el ultimo x a ser x_final


        iter_count += 1
    
    # Si el último punto calculado no es exactamente x_final pero debería serlo
    # (ej: x_final = 5, h = 0.5, último x_actual fue 4.5, y_actual calculado para x=5)
    # y no se añadió porque el bucle terminó, lo añadimos si es necesario.
    # Esto es más complejo si el paso h no divide exactamente el intervalo.
    # La lógica actual lo maneja bien si x_final se alcanza "exactamente" o se pasa ligeramente.
    # Si el último punto es x_final, pero y_actual aún no ha sido calculado para ESE punto
    # (lo cual no debería pasar con la lógica actual que calcula y_actual ANTES de incrementar x_actual
    # para el SIGUIENTE paso), entonces se necesita añadir.
    # Consideramos el último punto ya añadido. Si x_actual_prev fue el último antes de x_final, y_actual
    # ya corresponde a ese x_final.
    
    # Si se sale por max_iter, se añade un mensaje
    if iter_count > max_iter:
        warning_message = "\nAdvertencia: Se alcanzó el número máximo de iteraciones."

    return puntos_solucion, warning_message


def solve_euler(f_str, x0, y0, x_final, h):
    return solve_numerical_method(f_str, x0, y0, x_final, h, 
                                  lambda fs, xa, ya, hi: _paso_euler(fs, xa, ya, hi))

def solve_runge_kutta(f_str, x0, y0, x_final, h):
    return solve_numerical_method(f_str, x0, y0, x_final, h,
                                  lambda fs, xa, ya, hi: _paso_runge_kutta_4(fs, xa, ya, hi))
    
