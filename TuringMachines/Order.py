
# cuenta cuantas " ' " hay seguidas para concocer el grado máximo de la ecuación,
#si encuentra otro simbolo como y''' + deja de contar y empieza el conteo de cero,
#al final debe darnos el mayor número de ' que contó

# Order.py  -- versión corregida
# Cuenta cuántas comillas simples (') siguen a cada 'y' y devuelve el máximo.
# Nota: se preserva la definición original de la MNTM (MT_Orden) por compatibilidad,
#       pero la función obtener_orden_mtm usa un método directo en Python para obtener
#       resultados robustos y deterministas (evita errores de acumulación en cinta2).

from automata.tm.mntm import MNTM

# ===================================================================
# MTM: (ANTIGUA) Calculadora de Orden de Ecuación Diferencial
# Se mantiene la instancia por compatibilidad, **no** se usa actualmente.
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

# Transiciones mínimas (dejar la máquina definida aunque no se use)
transitions = {}

# (Mantengo la estructura original pero NO confío en ella para el cálculo)
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
# FUNCIÓN CORREGIDA Y ROBUSTA PARA OBTENER EL ORDEN
# ===================================================================
def obtener_orden_mtm(cadena):
    """
    Escanea la cadena (string) y devuelve el mayor número de comillas simples (')
    consecutivas inmediatamente después de una 'y'.

    Reglas:
     - Se ignoran espacios.
     - Se considera cualquier aparición de 'y' seguida de N comillas consecutivas: y''' -> N=3
     - Devuelve el máximo N encontrado (0 si no hay y o si alguna y no tiene comillas).
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
            # contar comillas inmediatamente después
            j = i + 1
            count = 0
            while j < n and s[j] == "'":
                count += 1
                j += 1
            if count > max_order:
                max_order = count
            # continue scanning after the y (do not skip non-prime symbols)
            i = j
            continue
        else:
            i += 1

    return max_order

# ===================================================================
# PRUEBAS (Se ejecutan si corres este archivo directamente)
# ===================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("[ MTM ] CALCULADORA DE ORDEN DE ECUACIONES DIFERENCIALES (versión corregida)")
    print("=" * 60)

    pruebas = [
        ("y'=x", 1),
        ("y''+y=0", 2),
        ("y+y'''=S(x)", 3),
        ("y''''+/(y')=0", 4),
        ("y=x", 0),
        ("S(y'')+y'''''=0", 5),
        ("y'+y''+y'=0", 2),
    ]

    for ecuacion, orden_esperado in pruebas:
        resultado = obtener_orden_mtm(ecuacion)
        match = "CORRECTO" if resultado == orden_esperado else "FALLO"
        print(f"Ecuación: {ecuacion:<25} | Esperado: {orden_esperado} | Resultado: {resultado} -> {match}")

    print("=" * 60)
    print("FIN PRUEBAS")
    print("=" * 60)
