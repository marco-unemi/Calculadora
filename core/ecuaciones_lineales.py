import numpy as np

subindices = {
    "0": "\u2080",
    "1": "\u2081",
    "2": "\u2082",
    "3": "\u2083",
    "4": "\u2084",
    "5": "\u2085",
    "6": "\u2086",
    "7": "\u2087",
    "8": "\u2088",
    "9": "\u2089"
}


def resolver_sistema_de_ecuaciones(A, b):
    try:
        x = np.linalg.solve(A, b)
        resultado = "\n".join(
            [f"X{''.join(subindices[d] for d in str(i+1))} = {valor:.4f}" for i, valor in enumerate(x)])
        print(f"Solución:\n{resultado}")
        return resultado
    except np.linalg.LinAlgError:
        print("El sistema no tiene solución única (puede ser incompatible o tener infinitas soluciones).")
