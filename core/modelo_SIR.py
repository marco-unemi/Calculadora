import numpy as np
from scipy.integrate import solve_ivp

# --- Función del Modelo SIR (como antes) ---
def sir_model_equations(t, y, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# --- Función para ejecutar la simulación y obtener resultados (sin graficar directamente aquí) ---
def simular_sir(S0, I0, R0, N, beta, gamma, t_dias):
    y0 = S0, I0, R0
    t_span = [0, t_dias]
    t_eval = np.linspace(t_span[0], t_span[1], t_dias * 5) # Más puntos para una curva suave
    
    sol = solve_ivp(sir_model_equations, t_span, y0, args=(N, beta, gamma), 
                    dense_output=True, t_eval=t_eval)
    
    return sol.t, sol.y[0], sol.y[1], sol.y[2] # Devuelve tiempo, S, I, R

