#busca que no hay una y entre parentesis, 
# esto es que no esté en una función S(y) o /(y) 
# ni sea una potencia (y)^(3) o (x)^(y), 
# y que no haya un termino que tenga una y multiplicado a otra y como y*y'''

from automata.tm.ntm import NTM

# ===================================================================
# MT: Detector de Linealidad
# ===================================================================
# NO LINEAL si:
# 1. Hay 'y' dentro de una función: S(y), /(y), etc
# 2. Hay 'y' en potencia: (y)^(...) o (...)^(y)
# 3. Hay y*y (dos 'y' multiplicándose)
#
# Estrategia:
# - Buscar patrones: FUNCION(... y ...) o (y)^ o ^(...y...)
# - Si encontramos '(' verificar si antes hay una letra de función
# - Dentro de esos paréntesis, si hay 'y' → NO LINEAL
# ===================================================================




from automata.tm.ntm import NTM

# ===================================================================
# MT: Detector de Linealidad
# ===================================================================

MT_Linealidad = NTM(
    states={'q0', 'q_func', 'q_in_func', 'q_paren', 'q_in_paren', 
            'q_check_mult', 'qlineal', 'qno_lineal'},
    
    input_symbols={
        'y', 'x', "'",
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'e', 'π', '.', '+', '-', '*', '/', '^',
        '(', ')', '=',
        'S', 'C', 'T', 'L', 'R', 'A', 's', 'c', 't', 'I', 'E'
    },
    
    tape_symbols={
        'y', 'x', "'",
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'e', 'π', '.', '+', '-', '*', '/', '^',
        '(', ')', '=',
        'S', 'C', 'T', 'L', 'R', 'A', 's', 'c', 't', 'I', 'E',
        'B', 'Y'
    },
    
    transitions={
        'q0': {
            'S': {('q_func', 'S', 'R')}, 'C': {('q_func', 'C', 'R')},
            'T': {('q_func', 'T', 'R')}, 'L': {('q_func', 'L', 'R')},
            'R': {('q_func', 'R', 'R')}, 'A': {('q_func', 'A', 'R')},
            's': {('q_func', 's', 'R')}, 'c': {('q_func', 'c', 'R')},
            't': {('q_func', 't', 'R')}, 'I': {('q_func', 'I', 'R')},
            'E': {('q_func', 'E', 'R')}, '/': {('q_func', '/', 'R')},
            
            '(': {('q_paren', '(', 'R')},
            'y': {('q_check_mult', 'Y', 'R')},
            
            'x': {('q0', 'x', 'R')},
            "'": {('q0', "'", 'R')},
            '0': {('q0', '0', 'R')}, '1': {('q0', '1', 'R')},
            '2': {('q0', '2', 'R')}, '3': {('q0', '3', 'R')},
            '4': {('q0', '4', 'R')}, '5': {('q0', '5', 'R')},
            '6': {('q0', '6', 'R')}, '7': {('q0', '7', 'R')},
            '8': {('q0', '8', 'R')}, '9': {('q0', '9', 'R')},
            'e': {('q0', 'e', 'R')}, 'π': {('q0', 'π', 'R')},
            '.': {('q0', '.', 'R')},
            '+': {('q0', '+', 'R')}, '-': {('q0', '-', 'R')},
            '*': {('q0', '*', 'R')}, '^': {('q0', '^', 'R')},
            ')': {('q0', ')', 'R')}, '=': {('q0', '=', 'R')},
            
            'B': {('qlineal', 'B', 'N')},
        },
        
        'q_func': {
            '(': {('q_in_func', '(', 'R')},
            **{s: {('q0', s, 'R')} for s in ['y', 'x', "'", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e', 'π', '.', '+', '-', '*', '/', '^', ')', '=', 'B']}
        },
        
        'q_in_func': {
            'y': {('qno_lineal', 'y', 'N')},
            ')': {('q0', ')', 'R')},
            **{s: {('q_in_func', s, 'R')} for s in ['x', "'", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e', 'π', '.', '+', '-', '*', '/', '^', '(', '=', 'S', 'C', 'T', 'L', 'R', 'A', 's', 'c', 't', 'I', 'E']}
        },
        
        'q_paren': {
            'y': {('qno_lineal', 'y', 'N')},
            ')': {('q0', ')', 'R')},
            **{s: {('q_paren', s, 'R')} for s in ['x', "'", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e', 'π', '.', '+', '-', '*', '/', '^', '(', '=', 'S', 'C', 'T', 'L', 'R', 'A', 's', 'c', 't', 'I', 'E']}
        },
        
        'q_check_mult': {
            '*': {('q_check_mult', '*', 'R')},
            'y': {('qno_lineal', 'y', 'N')},
            "'": {('q_check_mult', "'", 'R')},
            **{s: {('q0', s, 'R')} for s in ['x', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e', 'π', '.', '+', '-', '/', '^', '(', ')', '=', 'S', 'C', 'T', 'L', 'R', 'A', 's', 'c', 't', 'I', 'E', 'B']}
        },
    },
    
    initial_state='q0',
    blank_symbol='B',
    final_states={'qlineal', 'qno_lineal'}
)

def es_linealec(cadena):
    """
    Función helper para el Controlador.
    Devuelve True solo si la máquina termina en el estado 'qlineal'.
    """
    try:
        # read_input devuelve un set de configuraciones en NTM
        configs = MT_Linealidad.read_input(cadena) 
        for config in configs:
            if config.state == 'qlineal':
                return True
        return False
    except Exception:
        # Si la cadena se rechaza (no llega a ningún final)
        return False

# --- Bloque de pruebas protegido ---
if __name__ == "__main__":
    print("PRUEBAS Linearity.py")
    pruebas = [
        ("y'+2*y=0", True),
        ("S(x)*y''+y=0", True),
        ("S(y)*y'=0", False),
    ]
    for expr, esperado in pruebas:
        resultado = es_linealec(expr)
        print(f"{expr} => {'Lineal' if resultado else 'No lineal'} [{'OK' if resultado == esperado else 'FAIL'}]")

print("se está ejecutando Linearity")