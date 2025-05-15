# core/metodo_analitico.py
import sympy as sp
import numpy as np
import re

def normalizar_raices(expr_str, func_name, indep_var):
    """Normaliza diferentes notaciones de raíces a formato SymPy."""
    patrones = [
        (fr'sqrt\s*\(\s*{func_name}\s*\)', f'Pow({func_name}({indep_var}), Rational(1, 2))'),
        (fr'raiz\s*\(\s*{func_name}\s*\)', f'Pow({func_name}({indep_var}), Rational(1, 2))'),
        (r'sqrt\s*\(([^)]+)\)', r'Pow(\1, Rational(1, 2))'),
        (r'raiz\s*\(([^)]+)\)', r'Pow(\1, Rational(1, 2))')
    ]

    for patron, reemplazo in patrones:
        expr_str = re.sub(patron, reemplazo, expr_str, flags=re.IGNORECASE)

    # Manejar potencias fraccionarias
    expr_str = re.sub(
        r'(\w+|\([^)]+\))\s*[\^*]{1,2}\s*\((\d+)/(\d+)\)',
        lambda m: f'Pow({m.group(1)}{"(" + indep_var + ")" if m.group(1) == func_name else ""}, Rational({m.group(2)}, {m.group(3)}))',
        expr_str
    )

    return expr_str

def preparar_ecuacion(ecuacion_str, func_name, indep_var):
    """Prepara la ecuación para su resolución."""
    # Eliminar espacios
    ecuacion_str = ecuacion_str.replace(' ', '')

    # Convertir notación de Leibniz a Derivative
    ecuacion_str = re.sub(
        fr'd2{func_name}/d{indep_var}2',
        f'Derivative({func_name}({indep_var}), {indep_var}, {indep_var})',
        ecuacion_str
    )
    ecuacion_str = re.sub(
        fr'd{func_name}/d{indep_var}',
        f'Derivative({func_name}({indep_var}), {indep_var})',
        ecuacion_str
    )

    # Normalizar raíces
    ecuacion_str = normalizar_raices(ecuacion_str, func_name, indep_var)

    # Asegurar que la función tenga sus argumentos
    ecuacion_str = re.sub(fr'\b{func_name}\b(?!\()', f'{func_name}({indep_var})', ecuacion_str)

    return ecuacion_str

def obtener_condiciones_iniciales(condiciones, x, y, x0):
    """Procesa las condiciones iniciales."""
    ics = {}
    y0 = None
    for ci_str, valor in condiciones.items():
        if 'd' + y.name in ci_str:
            ics[y.diff(x).subs(x, x0)] = valor
        elif y.name in ci_str:
            ics[y.subs(x, x0)] = valor
            y0 = valor
    return ics, y0

def evaluar_solucion(sol_candidata, x0, h, y0, x):
    """Evalúa si una solución candidata es válida."""
    test_points = [x0, x0 + h, x0 + 2*h]
    for test_x in test_points:
        try:
            test_val = sol_candidata.rhs.subs(x, test_x)
            if isinstance(test_val, sp.Pow):
                # Para expresiones con potencias, evaluar numéricamente
                test_y = complex(test_val.evalf())
                if abs(test_y.imag) > 1e-10:  # Tolerancia para parte imaginaria
                    return False
                test_y = test_y.real
            else:
                test_y = float(test_val.evalf())

            if not np.isfinite(test_y):
                return False

            if test_x == x0 and y0 is not None:
                if (y0 > 0 and test_y < 0) or (y0 < 0 and test_y > 0):
                    return False
        except:
            return False
    return True

def resolver_ecuacion_diferencial(ecuacion_str, x0, y0, t_total, h, func_name, indep_var):
    """Resuelve una EDO analíticamente y retorna tiempos, valores y solución simbólica."""
    try:
        x = sp.Symbol(indep_var)
        y_func = sp.Function(func_name)
        y = y_func(x)

        ecuacion_str = preparar_ecuacion(ecuacion_str, func_name, indep_var)
        print(f"Ecuación procesada: {ecuacion_str}")

        local_dict = {
            'Derivative': sp.Derivative,
            'Pow': sp.Pow,
            'Rational': sp.Rational,
            'sqrt': sp.sqrt,
            func_name: y_func,
            indep_var: x
        }

        if '=' in ecuacion_str:
            lhs, rhs = ecuacion_str.split('=', 1)
            lhs_expr = sp.parse_expr(lhs, local_dict=local_dict)
            rhs_expr = sp.parse_expr(rhs, local_dict=local_dict)
            expr = sp.Eq(lhs_expr, rhs_expr)
        else:
            expr = sp.parse_expr(ecuacion_str, local_dict=local_dict)

        # Resolver con condición inicial
        solucion = sp.dsolve(expr, y, ics={y.subs(x, x0): y0})

        # Evaluar solución
        tiempos = np.arange(x0, x0 + t_total + h, h)
        f = sp.lambdify(x, solucion.rhs, 'numpy')
        valores = f(tiempos)

        return tiempos, valores, solucion

    except Exception as e:
        print(f"Error en resolver_ecuacion_diferencial: {str(e)}")
        return None, None, None
    