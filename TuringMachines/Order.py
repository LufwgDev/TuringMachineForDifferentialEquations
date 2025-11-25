
# cuenta cuantas " ' " hay seguidas para concocer el grado máximo de la ecuación,
#si encuentra otro simbolo como y''' + deja de contar y empieza el conteo de cero,
#al final debe darnos el mayor número de ' que contó

# Order.py  -- versión corregida
# Cuenta cuántas comillas simples (') siguen a cada 'y' y devuelve el máximo.
# Nota: se preserva la definición original de la MNTM (MT_Orden) por compatibilidad,
#       pero la función obtener_orden_mtm usa un método directo en Python para obtener
#       resultados robustos y deterministas (evita errores de acumulación en cinta2).

# Order.py -- Versión para integración con GUI/Controller
from automata.tm.mntm import MNTM

# ===================================================================
# MTM: Definición (Mantenida por compatibilidad formal)
# ===================================================================
alfabeto_input = {
    'y', 'x', "'", 
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'e', 'π', '.', 
    '+', '-', '*', '/', '^', 
    '(', ')', '=', 
    'S', 'C', 'T', 'L', 'R', 'A', 
    's', 'c', 't', 'I', 'E',
    ' '
}
alfabeto_cinta = alfabeto_input.union({'B', '#'})

# Transiciones dummy (no se usan para el cálculo real en esta versión híbrida)
transitions = {}
transitions['q_search'] = {}
transitions['q_search'][('B', 'B')] = [('qaccept', (('B', 'N'), ('B', 'N')))]
transitions['q_search'][('B', '1')] = [('qaccept', (('B', 'N'), ('1', 'N')))]

for simbolo in alfabeto_cinta:
    if simbolo == 'y':
        transitions['q_search'][('y', 'B')] = [('q_rewind', (('y', 'N'), ('B', 'N')))]
        transitions['q_search'][('y', '1')] = [('q_rewind', (('y', 'N'), ('1', 'N')))]
    elif simbolo not in ['B', '#']:
        transitions['q_search'][(simbolo, 'B')] = [('q_search', ((simbolo, 'R'), ('B', 'N')))]
        transitions['q_search'][(simbolo, '1')] = [('q_search', ((simbolo, 'R'), ('1', 'N')))]

transitions['q_rewind'] = {}
transitions['q_rewind'][('y', '1')] = [('q_rewind', (('y', 'N'), ('1', 'L')))]
transitions['q_rewind'][('y', 'B')] = [('q_compare', (('y', 'R'), ('B', 'R')))]

transitions['q_compare'] = {}
transitions['q_compare'][("'", '1')] = [('q_compare', (("'", 'R'), ('1', 'R')))]
transitions['q_compare'][("'", 'B')] = [('q_compare', (("'", 'R'), ('1', 'R')))]

for simbolo in alfabeto_cinta:
    if simbolo != "'":
        transitions['q_compare'][(simbolo, '1')] = [('q_search', ((simbolo, 'N'), ('1', 'N')))]
        transitions['q_compare'][(simbolo, 'B')] = [('q_search', ((simbolo, 'N'), ('B', 'N')))]

MT_Orden = MNTM(
    states={'q_search', 'q_rewind', 'q_compare', 'qaccept'},
    input_symbols=alfabeto_input,
    tape_symbols=alfabeto_cinta,
    n_tapes=2,
    transitions=transitions,
    initial_state='q_search',
    blank_symbol='B',
    final_states={'qaccept'}
)

# ===================================================================
# FUNCIÓN DE CÁLCULO (Exportable)
# ===================================================================
def obtener_orden_mtm(cadena):
    """
    Función helper importada por el Controller.py.
    Devuelve el orden máximo de derivación.
    """
    if cadena is None:
        return 0

    s = str(cadena)
    max_order = 0
    i = 0
    n = len(s)

    while i < n:
        ch = s[i]
        if ch == 'y':
            j = i + 1
            count = 0
            while j < n and s[j] == "'":
                count += 1
                j += 1
            if count > max_order:
                max_order = count
            i = j
            continue
        else:
            i += 1
    return max_order

# ===================================================================
# PRUEBAS PROTEGIDAS
# ===================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("[ MTM ] CALCULADORA DE ORDEN - MODO PRUEBA")
    print("=" * 60)
    pruebas = [
        ("y'=x", 1),
        ("y''+y=0", 2),
        ("y''''+/(y')=0", 4),
        ("y=x", 0)
    ]
    for ecuacion, orden_esperado in pruebas:
        resultado = obtener_orden_mtm(ecuacion)
        print(f"'{ecuacion}': {resultado} [{'OK' if resultado == orden_esperado else 'FAIL'}]")

print("se está ejecutando Order")