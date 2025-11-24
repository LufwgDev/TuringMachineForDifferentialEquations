
# cuenta cuantas " ' " hay seguidas para concocer el grado máximo de la ecuación,
#si encuentra otro simbolo como y''' + deja de contar y empieza el conteo de cero,
#al final debe darnos el mayor número de ' que contó
from automata.tm.mntm import MNTM

# ===================================================================
# MTM: Calculadora de Orden de Ecuación Diferencial
# ===================================================================

# 1. Definimos el alfabeto
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

# Alfabeto de cinta (Input + Blanco + Símbolo de conteo #)
alfabeto_cinta = alfabeto_input.union({'B', '#'})

# 2. Construcción de Transiciones
transitions = {}

# --- ESTADO q_search ---
# Objetivo: Buscar la 'y'. Ignorar el resto.
transitions['q_search'] = {}

# CASO ESPECIAL (CORRECCIÓN): Fin de Cadena
# Si Cinta 1 lee Blanco (B), hemos terminado de leer toda la ecuación.
# Vamos a qaccept. Cinta 2 puede tener Blancos o Unos, no importa.
transitions['q_search'][('B', 'B')] = [('qaccept', (('B', 'N'), ('B', 'N')))]
transitions['q_search'][('B', '1')] = [('qaccept', (('B', 'N'), ('1', 'N')))]

# Generación automática para el resto de símbolos
for simbolo in alfabeto_cinta:
    if simbolo == 'y':
        # Si encuentra 'y', vamos a REBOBINAR la cinta 2 para comparar
        transitions['q_search'][('y', 'B')] = [('q_rewind', (('y', 'N'), ('B', 'N')))]
        transitions['q_search'][('y', '1')] = [('q_rewind', (('y', 'N'), ('1', 'N')))]
    elif simbolo not in ['B', '#']:
        # Cualquier otro símbolo (x, +, S, 1, etc.) lo ignoramos y avanzamos T1
        transitions['q_search'][(simbolo, 'B')] = [('q_search', ((simbolo, 'R'), ('B', 'N')))]
        transitions['q_search'][(simbolo, '1')] = [('q_search', ((simbolo, 'R'), ('1', 'N')))]

# --- ESTADO q_rewind ---
# Objetivo: Mover la cabeza de Cinta 2 a la izquierda hasta tocar el borde (B)
transitions['q_rewind'] = {}

# Mientras haya 1s en Cinta 2, muévete a la izquierda (L) en Cinta 2
transitions['q_rewind'][('y', '1')] = [('q_rewind', (('y', 'N'), ('1', 'L')))]

# Cuando lleguemos al Blanco (B) a la izquierda de los unos, estamos listos.
# Avanzamos Cinta 1 una vez (R) para ver qué hay después de la 'y'.
transitions['q_rewind'][('y', 'B')] = [('q_compare', (('y', 'R'), ('B', 'R')))]


# --- ESTADO q_compare ---
# Objetivo: Contar comillas (') en T1 y compararlas con unos (1) en T2
transitions['q_compare'] = {}

# CASO 1: Empate (Hay ' en T1 y hay 1 en T2)
# Acción: Avanzar ambas a la derecha. No escribimos nada nuevo.
transitions['q_compare'][("'", '1')] = [('q_compare', (("'", 'R'), ('1', 'R')))]

# CASO 2: Nuevo Récord (Hay ' en T1 pero se acabaron los 1 en T2 - leemos B)
# Acción: Escribir '1' en T2 (guardar récord) y avanzar ambas.
transitions['q_compare'][("'", 'B')] = [('q_compare', (("'", 'R'), ('1', 'R')))]

# CASO 3: Fin de derivadas (No hay ' en T1)
# Acción: Volver a q_search.
for simbolo in alfabeto_cinta:
    if simbolo != "'":
        # Si T1 lee algo que no es comilla (ej: +, =, x), volvemos a buscar.
        transitions['q_compare'][(simbolo, '1')] = [('q_search', ((simbolo, 'N'), ('1', 'N')))]
        transitions['q_compare'][(simbolo, 'B')] = [('q_search', ((simbolo, 'N'), ('B', 'N')))]


# 3. Instancia de la MTM
MT_Orden = MNTM(
    states={'q_search', 'q_rewind', 'q_compare', 'qaccept'},
    input_symbols=alfabeto_input,
    tape_symbols=alfabeto_cinta,
    n_tapes=2,
    transitions=transitions,
    initial_state='q_search',
    blank_symbol='B',
    # CORRECCIÓN: Solo qaccept es estado final
    final_states={'qaccept'} 
)

# ===================================================================
# FUNCIÓN AUXILIAR PARA OBTENER EL ORDEN
# ===================================================================
def obtener_orden_mtm(cadena):
    """
    Ejecuta la MTM y cuenta cuántos '1' quedaron en la Cinta 2.
    """
    try:
        configuracion_final = None
        
        # read_input_stepwise ejecuta paso a paso hasta que la máquina se detiene
        for config in MT_Orden.read_input_stepwise(cadena):
            configuracion_final = config
        
        # CORRECCIÓN: Si configuracion_final es un set, tomar el primer elemento
        if isinstance(configuracion_final, set):
            configuracion_final = next(iter(configuracion_final))
        
        # Obtenemos Cinta 2 (índice 1)
        cinta_2 = configuracion_final.tapes[1]
        
        # Contamos cuántos '1' hay en la cinta 2
        contenido_cinta = "".join(str(s) for s in cinta_2.tape)
        orden = contenido_cinta.count('1')
        return orden
        
    except Exception as e:
        return f"Error: {e}"
    
# ===================================================================
# PRUEBAS (Solo se ejecutan si corres este archivo directamente)
# ===================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("[ MTM ] CALCULADORA DE ORDEN DE ECUACIONES DIFERENCIALES")
    print("=" * 60)

    pruebas = [
        ("y'=x", 1),
        ("y''+y=0", 2),
        ("y+y'''=S(x)", 3),
        ("y''''+/(y')=0", 4),
        ("y=x", 0), # Orden 0
        ("S(y'')+y'''''=0", 5), # Orden 5, detecta el segundo término
        ("y'+y''+y'=0", 2), # El del medio es el mayor
    ]

    for ecuacion, orden_esperado in pruebas:
        resultado = obtener_orden_mtm(ecuacion)
        match = "CORRECTO" if resultado == orden_esperado else "FALLO"
        print(f"Ecuación: {ecuacion:<20} | Esperado: {orden_esperado} | MTM Dice: {resultado} -> {match}")