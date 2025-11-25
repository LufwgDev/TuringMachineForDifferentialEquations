#pip install automata-lib
from automata.tm.ntm import NTM
# ===================================================================
# MTM1: Validador Básico de Ecuaciones Diferenciales
# ===================================================================
# Objetivo: Verificar si una cadena tiene la estructura mínima de una ED
#
# Condiciones para ACEPTAR:
# 1. Debe existir al menos una 'y' seguida de al menos un apóstrofe (')
# 2. Debe existir un símbolo de igualdad (=) en algún lugar de la cadena
#
# Estados:
# - q0: Estado inicial, buscando 'y'
# - q1: Encontró 'y', esperando al menos un apóstrofe (')
# - q2: Encontró 'y' con derivada (y'), ahora busca '='
# - qaccept: Encontró '=' después de haber visto y' → ACEPTA (sin transiciones)
#
# Notas:
# - El GUI garantiza paréntesis balanceados y un solo '='
# - El GUI coloca todas las y's a la izquierda del '='
# - Esta MT solo valida estructura mínima, no sintaxis completa
# ===================================================================




from automata.tm.ntm import NTM

# ===================================================================
# MTM1: Validador Básico de Ecuaciones Diferenciales
# ===================================================================

MT_Validador_ED = NTM(
    states={'q0', 'q1', 'q2', 'qaccept'},
    input_symbols={
        'y', 'x', "'", 
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'e', 'π', '.', 
        '+', '-', '*', '/', '^', 
        '(', ')', '=', 
        'S', 'C', 'T', 'L', 'R', 'A', 
        's', 'c', 't', 'I', 'E'
    },
    tape_symbols={
        'y', 'x', "'",
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'e', 'π', '.',
        '+', '-', '*', '/', '^',
        '(', ')', '=',
        'S', 'C', 'T', 'L', 'R', 'A',
        's', 'c', 't', 'I', 'E',
        'B'
    },
    transitions={
        'q0': {
            'y': {('q1', 'y', 'R')},
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
            '*': {('q0', '*', 'R')}, '/': {('q0', '/', 'R')},
            '^': {('q0', '^', 'R')},
            '(': {('q0', '(', 'R')}, ')': {('q0', ')', 'R')},
            '=': {('q0', '=', 'R')},
            'S': {('q0', 'S', 'R')}, 'C': {('q0', 'C', 'R')},
            'T': {('q0', 'T', 'R')}, 'L': {('q0', 'L', 'R')},
            'R': {('q0', 'R', 'R')}, 'A': {('q0', 'A', 'R')},
            's': {('q0', 's', 'R')}, 'c': {('q0', 'c', 'R')},
            't': {('q0', 't', 'R')}, 'I': {('q0', 'I', 'R')},
            'E': {('q0', 'E', 'R')},
        },
        'q1': {
            "'": {('q2', "'", 'R')},
            'y': {('q1', 'y', 'R')},
            'x': {('q0', 'x', 'R')},
            '0': {('q0', '0', 'R')}, '1': {('q0', '1', 'R')},
            '2': {('q0', '2', 'R')}, '3': {('q0', '3', 'R')},
            '4': {('q0', '4', 'R')}, '5': {('q0', '5', 'R')},
            '6': {('q0', '6', 'R')}, '7': {('q0', '7', 'R')},
            '8': {('q0', '8', 'R')}, '9': {('q0', '9', 'R')},
            'e': {('q0', 'e', 'R')}, 'π': {('q0', 'π', 'R')},
            '.': {('q0', '.', 'R')},
            '+': {('q0', '+', 'R')}, '-': {('q0', '-', 'R')},
            '*': {('q0', '*', 'R')}, '/': {('q0', '/', 'R')},
            '^': {('q0', '^', 'R')},
            '(': {('q0', '(', 'R')}, ')': {('q0', ')', 'R')},
            '=': {('q0', '=', 'R')},
            'S': {('q0', 'S', 'R')}, 'C': {('q0', 'C', 'R')},
            'T': {('q0', 'T', 'R')}, 'L': {('q0', 'L', 'R')},
            'R': {('q0', 'R', 'R')}, 'A': {('q0', 'A', 'R')},
            's': {('q0', 's', 'R')}, 'c': {('q0', 'c', 'R')},
            't': {('q0', 't', 'R')}, 'I': {('q0', 'I', 'R')},
            'E': {('q0', 'E', 'R')},
        },
        'q2': {
            '=': {('qaccept', '=', 'R')},
            'y': {('q2', 'y', 'R')}, 'x': {('q2', 'x', 'R')},
            "'": {('q2', "'", 'R')},
            '0': {('q2', '0', 'R')}, '1': {('q2', '1', 'R')},
            '2': {('q2', '2', 'R')}, '3': {('q2', '3', 'R')},
            '4': {('q2', '4', 'R')}, '5': {('q2', '5', 'R')},
            '6': {('q2', '6', 'R')}, '7': {('q2', '7', 'R')},
            '8': {('q2', '8', 'R')}, '9': {('q2', '9', 'R')},
            'e': {('q2', 'e', 'R')}, 'π': {('q2', 'π', 'R')},
            '.': {('q2', '.', 'R')},
            '+': {('q2', '+', 'R')}, '-': {('q2', '-', 'R')},
            '*': {('q2', '*', 'R')}, '/': {('q2', '/', 'R')},
            '^': {('q2', '^', 'R')},
            '(': {('q2', '(', 'R')}, ')': {('q2', ')', 'R')},
            'S': {('q2', 'S', 'R')}, 'C': {('q2', 'C', 'R')},
            'T': {('q2', 'T', 'R')}, 'L': {('q2', 'L', 'R')},
            'R': {('q2', 'R', 'R')}, 'A': {('q2', 'A', 'R')},
            's': {('q2', 's', 'R')}, 'c': {('q2', 'c', 'R')},
            't': {('q2', 't', 'R')}, 'I': {('q2', 'I', 'R')},
            'E': {('q2', 'E', 'R')},
        },
    },
    initial_state='q0',
    blank_symbol='B',
    final_states={'qaccept'}
)

# --- Bloque de pruebas protegido ---
if __name__ == "__main__":
    print("=" * 70)
    print("PRUEBAS DE LA MÁQUINA DE TURING - VALIDADOR DE ED")
    print("=" * 70)
    pruebas = [
        ("y'=0", True),
        ("y''+y'=0", True),
        ("y=0", False),
        ("x+3=0", False),
    ]
    for cadena, esperado in pruebas:
        try:
            res = MT_Validador_ED.accepts_input(cadena)
            print(f"'{cadena}': {'✓' if res == esperado else '✗'} (Obtenido: {res})")
        except:
            print(f"'{cadena}': Error de ejecución")

print("se está ejecutando DFValidator")