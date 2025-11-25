#buscar terminos y si hay alguno que no esté acompañada por una y 
# como + "3*S(x-2) +" o "+ -/((x)^(2)) =" entences no es homogenea


from automata.tm.mntm import MNTM

# ===================================================================
# MTM: Detector de Homogeneidad (2 Cintas)
# ===================================================================
# Cinta 1: Input.
# Cinta 2: Pila de paréntesis (Para ignorar + y - dentro de funciones).
#
# LÓGICA DE ESTADOS:
# 1. q_start: Inicio de un nuevo término. Limpiamos flags.
# 2. q_no_y: Estamos leyendo un término y AÚN NO hemos visto 'y'.
# 3. q_has_y: Estamos leyendo un término y YA vimos 'y' (este término es seguro).
# 4. q_zero_check: Vimos un '0' al inicio. Puede ser un 0 válido o un 0.5 (inválido).
#
# REGLAS DE RECHAZO:
# - Si en q_no_y encontramos un separador (+, -, =) y la Cinta 2 está vacía (#),
#   significa que el término terminó sin 'y'. -> RECHAZAR.
# ===================================================================

# Alfabetos
input_symbols = {
    'y', 'x', "'",
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'e', 'π', '.',
    '+', '-', '*', '/', '^',
    '(', ')', '=',
    'S', 'C', 'T', 'L', 'R', 'A',
    's', 'c', 't', 'I', 'E'
}
tape_symbols = input_symbols.union({'B', '#', 'X'}) # #=Inicio Pila, X=Marca Profundidad

transitions = {}

# --- HELPER: Generar transiciones por defecto ---
def add_default(state, source, target_state, tape2_move='N'):
    # source es (char_cinta1, char_cinta2)
    # Si la transición ya existe, no la sobrescribimos
    if state not in transitions: transitions[state] = {}
    if source not in transitions[state]:
        transitions[state][source] = [(target_state, ((source[0], 'R'), (source[1], tape2_move)))]

# -------------------------------------------------------------------
# 1. ESTADO q_start: Inicio de término
# -------------------------------------------------------------------
transitions['q_start'] = {}

# Caso: Encontramos 'y' inmediatamente -> Término Válido
transitions['q_start'][('y', '#')] = [('q_has_y', (('y', 'R'), ('#', 'N')))]

# Caso: Encontramos '0' -> Verificar si es el número 0 (válido) o parte de otro
transitions['q_start'][('0', '#')] = [('q_zero_check', (('0', 'R'), ('#', 'N')))]

# Caso: Signos unarios al inicio (+y...) -> Ignorar y seguir en start (o pasar a no_y)
transitions['q_start'][('+', '#')] = [('q_start', (('+', 'R'), ('#', 'N')))]
transitions['q_start'][('-', '#')] = [('q_start', (('-', 'R'), ('#', 'N')))]
transitions['q_start'][('=', '#')] = [('q_start', (('=', 'R'), ('#', 'N')))] # Raro, pero posible

# Caso: Paréntesis al inicio -> Entrar a no_y y marcar pila
transitions['q_start'][('(', '#')] = [('q_no_y', (('(', 'R'), ('#', 'R')))] # Movemos T2 a la derecha (Push)

# Caso: Fin de cadena en start -> Aceptar (cadena vacía o terminada en =)
transitions['q_start'][('B', '#')] = [('qaccept', (('B', 'N'), ('#', 'N')))]

# Default: Cualquier otra cosa (x, 1, S...) -> Término potencialmente inválido
for s in tape_symbols:
    if s not in ['y', '0', '+', '-', '=', '(', 'B', '#', 'X']:
        # T2 quieto en #
        transitions['q_start'][(s, '#')] = [('q_no_y', ((s, 'R'), ('#', 'N')))]

# -------------------------------------------------------------------
# 2. ESTADO q_no_y: Leyendo término sin 'y'
# -------------------------------------------------------------------
transitions['q_no_y'] = {}

# Si encontramos 'y' -> ¡Salvado! Pasamos a q_has_y
for s2 in ['#', 'B', 'X']: # Puede pasar con pila vacía o llena
    transitions['q_no_y'][('y', s2)] = [('q_has_y', (('y', 'R'), (s2, 'N')))]

# Manejo de Paréntesis (Cinta 2)
# Abrir (: Escribir X en T2, Mover R
for s2 in ['#', 'X', 'B']: 
    # Escribimos X donde estemos y avanzamos
    transitions['q_no_y'][('(', s2)] = [('q_no_y', (('(', 'R'), ('X', 'R')))]

# Cerrar ): Mover L en T2 (Pop simulado)
transitions['q_no_y'][(')', 'X')] = [('q_no_y', ((')', 'R'), ('B', 'L')))] # Borramos la X actual
transitions['q_no_y'][(')', 'B')] = [('q_no_y', ((')', 'R'), ('B', 'L')))] # Ajuste por si el head estaba en B

# Separadores (+, -, =)
# CRÍTICO: Si T2 lee '#', estamos en nivel 0 -> Fin de término SIN Y -> RECHAZAR (No hay transición)
# Si T2 lee 'X', estamos dentro de paréntesis -> Ignorar separador
transitions['q_no_y'][('+', 'X')] = [('q_no_y', (('+', 'R'), ('X', 'N')))]
transitions['q_no_y'][('-', 'X')] = [('q_no_y', (('-', 'R'), ('X', 'N')))]
transitions['q_no_y'][('=', 'X')] = [('q_no_y', (('=', 'R'), ('X', 'N')))]

# Resto de caracteres: Seguir buscando
for s in tape_symbols:
    if s not in ['y', '(', ')', '+', '-', '=', 'B', '#', 'X']:
        for s2 in ['#', 'X', 'B']:
            if (s, s2) not in transitions['q_no_y']:
                transitions['q_no_y'][(s, s2)] = [('q_no_y', ((s, 'R'), (s2, 'N')))]

# -------------------------------------------------------------------
# 3. ESTADO q_has_y: Leyendo término que YA tiene 'y'
# -------------------------------------------------------------------
transitions['q_has_y'] = {}

# Paréntesis (Igual lógica de pila, pero nos mantenemos en q_has_y)
for s2 in ['#', 'X', 'B']:
    transitions['q_has_y'][('(', s2)] = [('q_has_y', (('(', 'R'), ('X', 'R')))]
transitions['q_has_y'][(')', 'X')] = [('q_has_y', ((')', 'R'), ('B', 'L')))]
transitions['q_has_y'][(')', 'B')] = [('q_has_y', ((')', 'R'), ('B', 'L')))] # Safety

# Separadores
# Si estamos en nivel 0 (#), el término terminó bien. Vamos a q_start para el siguiente.
transitions['q_has_y'][('+', '#')] = [('q_start', (('+', 'R'), ('#', 'N')))]
transitions['q_has_y'][('-', '#')] = [('q_start', (('-', 'R'), ('#', 'N')))]
transitions['q_has_y'][('=', '#')] = [('q_start', (('=', 'R'), ('#', 'N')))]

# Si estamos dentro de paréntesis (X), ignorar
for sep in ['+', '-', '=']:
    transitions['q_has_y'][(sep, 'X')] = [('q_has_y', ((sep, 'R'), ('X', 'N')))]

# Fin de cadena -> ACEPTAR
transitions['q_has_y'][('B', '#')] = [('qaccept', (('B', 'N'), ('#', 'N')))]

# Resto
for s in tape_symbols:
    if s not in ['(', ')', '+', '-', '=', 'B', '#', 'X']:
        for s2 in ['#', 'X', 'B']:
            if (s, s2) not in transitions['q_has_y']:
                transitions['q_has_y'][(s, s2)] = [('q_has_y', ((s, 'R'), (s2, 'N')))]

# -------------------------------------------------------------------
# 4. ESTADO q_zero_check: Vimos un '0' al inicio
# -------------------------------------------------------------------
transitions['q_zero_check'] = {}

# Si sigue un separador o fin -> Era un 0 solitario (VÁLIDO). Reset a q_start o Accept.
transitions['q_zero_check'][('+', '#')] = [('q_start', (('+', 'R'), ('#', 'N')))]
transitions['q_zero_check'][('-', '#')] = [('q_start', (('-', 'R'), ('#', 'N')))]
transitions['q_zero_check'][('=', '#')] = [('q_start', (('=', 'R'), ('#', 'N')))]
transitions['q_zero_check'][('B', '#')] = [('qaccept', (('B', 'N'), ('#', 'N')))]

# Si sigue un punto (.) o número -> Es 0.5 o 01 -> NO tiene y -> Ir a q_no_y
transitions['q_zero_check'][('.', '#')] = [('q_no_y', (('.', 'R'), ('#', 'N')))]
for d in ['0','1','2','3','4','5','6','7','8','9']:
    transitions['q_zero_check'][(d, '#')] = [('q_no_y', ((d, 'R'), ('#', 'N')))]

# Si sigue una y -> Ir a has_y
transitions['q_zero_check'][('y', '#')] = [('q_has_y', (('y', 'R'), ('#', 'N')))]

# Otros (x, S...) -> Ir a no_y
for s in tape_symbols:
    if (s, '#') not in transitions['q_zero_check']:
        transitions['q_zero_check'][(s, '#')] = [('q_no_y', ((s, 'R'), ('#', 'N')))]

# ===================================================================
# INSTANCIA MTM
# ===================================================================
MT_Homogenea = MNTM(
    states={'q_start', 'q_no_y', 'q_has_y', 'q_zero_check', 'qaccept'},
    input_symbols=input_symbols,
    tape_symbols=tape_symbols,
    n_tapes=2,
    transitions=transitions,
    initial_state='q_start',
    blank_symbol='B',
    final_states={'qaccept'}
)

# ===================================================================
# FUNCIÓN HELPER PARA EL CONTROLADOR
# ===================================================================
def es_homogenea(cadena):
    """
    Verifica si todos los términos de la ecuación contienen 'y' o son cero.
    Usa Cinta 2 iniciada con '#' para simular la base de la pila.
    """
    try:
        # La librería MNTM requiere que las cintas se inicialicen.
        # Truco: Pasamos el input normal. Automata-lib llena la cinta 1.
        # Pero necesitamos que la Cinta 2 empiece con '#'.
        # La librería no soporta "contenido inicial" en cintas aux fácilmente en read_input.
        # SOLUCIÓN: Hacemos que q_start escriba '#' en el primer paso?
        # No, mejor ajustamos la lógica: Asumimos que 'B' es el fondo de pila
        # y usamos '#' solo conceptualmente en el código de arriba.
        # REAJUSTE RÁPIDO PARA QUE FUNCIONE EN AUTOMATA-LIB STANDARD:
        # Cambiaremos '#' por 'B' en las transiciones de arriba dinámicamente o
        # simplemente aceptamos que el estado inicial de T2 es B.
        
        # Como ya definí '#' arriba, vamos a envolver la cadena para que la MTM funcione:
        # No se puede.
        # SOLUCIÓN PRAGMÁTICA: Usar 'B' como marcador de fondo de pila en lugar de '#'.
        
        # Para que este código sea 'Copy-Paste' funcional, voy a redefinir
        # la máquina usando 'B' como fondo de pila en lugar de '#'.
        # (Ver abajo la corrección en caliente en el bloque __main__ o aquí mismo).
        pass 
    except:
        pass
    
    # NOTA: Debido a la complejidad de inicializar la Cinta 2 con '#',
    # la versión que funcionará usa 'B' como base.
    # El código de arriba usa '#' explícitamente.
    # Para el controlador, simplemente llamamos accept.
    
    # HACK: Modificamos las transiciones para que '#' sea tratado como 'B'
    # Esto es necesario porque automata-lib inicia las cintas auxiliares vacías (B).
    
    new_transitions = {}
    for state, trans in transitions.items():
        new_transitions[state] = {}
        for (in1, in2), result in trans.items():
            # Si la regla esperaba '#', la cambiamos para esperar 'B'
            key_in2 = 'B' if in2 == '#' else in2
            
            # El resultado también: si escribía/mantenía '#', ahora es 'B'
            next_state, ((out1, mov1), (out2, mov2)) = result[0]
            val_out2 = 'B' if out2 == '#' else out2
            
            new_transitions[state][(in1, key_in2)] = [(next_state, ((out1, mov1), (val_out2, mov2)))]
            
    MT_Homogenea_Final = MNTM(
        states={'q_start', 'q_no_y', 'q_has_y', 'q_zero_check', 'qaccept'},
        input_symbols=input_symbols,
        tape_symbols=tape_symbols,
        n_tapes=2,
        transitions=new_transitions, # Usamos las transiciones corregidas
        initial_state='q_start',
        blank_symbol='B',
        final_states={'qaccept'}
    )
    
    try:
        return MT_Homogenea_Final.accepts_input(cadena)
    except:
        return False

# ===================================================================
# PRUEBAS
# ===================================================================
if __name__ == "__main__":
    print("="*60)
    print("PRUEBAS DE HOMOGENEIDAD (MNTM)")
    print("="*60)
    
    cadenas = [
        ("y''+3*y=0", True),        # Homogénea (0 se acepta)
        ("y''+x=0", False),         # No homogénea (x no tiene y)
        ("y''+S(x+y)=0", True),     # Homogénea (y dentro de S)
        ("y''+S(x)=0", False),      # No Homogénea (S(x) no tiene y)
        ("y''+y=3", False),         # 3 no tiene y
        ("y=0", True),
        ("y'+y+ -8 = 0", False)     # -8 solitario -> Fail
    ]
    
    for c, esp in cadenas:
        res = es_homogenea(c)
        print(f"'{c}': {'Homogénea' if res else 'No Homogénea'} [{'OK' if res==esp else 'FAIL'}]")