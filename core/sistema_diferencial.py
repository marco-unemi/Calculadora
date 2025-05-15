import sympy as sp
import numpy as np
import pandas as pd

def resolver_sistema_diferencial(A_numeric, X0, t0=0, tf=5, h=0.1):
    """
    Resuelve el sistema dX/dt = A*X con condiciones iniciales X0.
    Devuelve: (tabla pandas, valores_propios, vectores_propios, funciones_lambdify)
    """
    t = sp.symbols('t', real=True)
    n = A_numeric.shape[0]
    X_syms = sp.symbols(f'x0:{n}')
    X_funcs = sp.Matrix([sp.Function(f'x{i}')(t) for i in range(n)])
    A = sp.Matrix(A_numeric)
    dXdt = X_funcs.diff(t)
    eqs = [sp.Eq(dXdt[i], (A * X_funcs)[i]) for i in range(n)]

    # Valores y vectores propios
    eigen_data = A.eigenvects()
    valores_propios = [val.evalf() for val, _, _ in eigen_data]
    vectores_propios = [v[0].evalf() for _, _, v in eigen_data]

    # Solución general
    sol = sp.dsolve(eqs)
    sol_matrix = sp.Matrix([s.rhs for s in sol])

    # Condiciones iniciales
    ics = {X_funcs[i].subs(t, t0): X0[i] for i in range(n)}
    consts = sp.solve([s.rhs.subs(t, t0) - ics[s.lhs.subs(t, t0)] for s in sol], dict=True)[0]
    sol_num = sol_matrix.subs(consts)

    # Funciones numéricas
    funcs = [sp.lambdify(t, sol_num[i], 'numpy') for i in range(n)]

    # Tabla de valores
    n_puntos = int((tf - t0) / h) + 1
    t_vals = np.linspace(t0, tf, n_puntos)
    var_names = ['x', 'y', 'z', 'w']  # Puedes extender si quieres más dimensiones
    data = {f'{var_names[i]}(t)': funcs[i](t_vals) for i in range(n)}
    data['t'] = t_vals
    tabla = pd.DataFrame(data)

    return tabla, valores_propios, vectores_propios, funcs
