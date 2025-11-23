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

MT_Validador_ED = NTM(
    # Definición de estados
    states={'q0', 'q1', 'q2', 'qaccept'},

    # Símbolos de entrada: alfabeto completo de ecuaciones diferenciales
    input_symbols={
        'y', 'x', "'",                           # Variables y derivadas
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  # Dígitos
        'e', 'π', '.',                           # Constantes y decimal
        '+', '-', '*', '/', '^',                 # Operadores
        '(', ')', '=',                           # Paréntesis e igualdad
        'S', 'C', 'T', 'L', 'R', 'A',           # Funciones (mayúsculas)
        's', 'c', 't', 'I', 'E'                  # Funciones (minúsculas)
    },

    # Símbolos de cinta: incluye símbolos de entrada + símbolo blanco
    tape_symbols={
        'y', 'x', "'",
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'e', 'π', '.',
        '+', '-', '*', '/', '^',
        '(', ')', '=',
        'S', 'C', 'T', 'L', 'R', 'A',
        's', 'c', 't', 'I', 'E',
        'B'  # Símbolo blanco
    },

    # Definición de transiciones
    transitions={
        # q0: Buscar 'y' (ignorar todo lo demás, avanzar a la derecha)
        'q0': {
            'y': {('q1', 'y', 'R')},  # Encontró 'y', ir a q1
            'x': {('q0', 'x', 'R')},
            "'": {('q0', "'", 'R')},
            '0': {('q0', '0', 'R')},
            '1': {('q0', '1', 'R')},
            '2': {('q0', '2', 'R')},
            '3': {('q0', '3', 'R')},
            '4': {('q0', '4', 'R')},
            '5': {('q0', '5', 'R')},
            '6': {('q0', '6', 'R')},
            '7': {('q0', '7', 'R')},
            '8': {('q0', '8', 'R')},
            '9': {('q0', '9', 'R')},
            'e': {('q0', 'e', 'R')},
            'π': {('q0', 'π', 'R')},
            '.': {('q0', '.', 'R')},
            '+': {('q0', '+', 'R')},
            '-': {('q0', '-', 'R')},
            '*': {('q0', '*', 'R')},
            '/': {('q0', '/', 'R')},
            '^': {('q0', '^', 'R')},
            '(': {('q0', '(', 'R')},
            ')': {('q0', ')', 'R')},
            '=': {('q0', '=', 'R')},
            'S': {('q0', 'S', 'R')},
            'C': {('q0', 'C', 'R')},
            'T': {('q0', 'T', 'R')},
            'L': {('q0', 'L', 'R')},
            'R': {('q0', 'R', 'R')},
            'A': {('q0', 'A', 'R')},
            's': {('q0', 's', 'R')},
            'c': {('q0', 'c', 'R')},
            't': {('q0', 't', 'R')},
            'I': {('q0', 'I', 'R')},
            'E': {('q0', 'E', 'R')},
            # No hay transición para 'B' (blanco) → rechaza si llega al final sin 'y'
        },

        # q1: Encontró 'y', buscar al menos un apóstrofe (')
        'q1': {
            "'": {('q2', "'", 'R')},  # Encontró y' → ir a q2
            # Si encuentra otra 'y', podría ser otra variable (volver a q1)
            'y': {('q1', 'y', 'R')},
            # Cualquier otro símbolo que no sea ' → seguir buscando otra 'y'
            'x': {('q0', 'x', 'R')},
            '0': {('q0', '0', 'R')},
            '1': {('q0', '1', 'R')},
            '2': {('q0', '2', 'R')},
            '3': {('q0', '3', 'R')},
            '4': {('q0', '4', 'R')},
            '5': {('q0', '5', 'R')},
            '6': {('q0', '6', 'R')},
            '7': {('q0', '7', 'R')},
            '8': {('q0', '8', 'R')},
            '9': {('q0', '9', 'R')},
            'e': {('q0', 'e', 'R')},
            'π': {('q0', 'π', 'R')},
            '.': {('q0', '.', 'R')},
            '+': {('q0', '+', 'R')},
            '-': {('q0', '-', 'R')},
            '*': {('q0', '*', 'R')},
            '/': {('q0', '/', 'R')},
            '^': {('q0', '^', 'R')},
            '(': {('q0', '(', 'R')},
            ')': {('q0', ')', 'R')},
            '=': {('q0', '=', 'R')},
            'S': {('q0', 'S', 'R')},
            'C': {('q0', 'C', 'R')},
            'T': {('q0', 'T', 'R')},
            'L': {('q0', 'L', 'R')},
            'R': {('q0', 'R', 'R')},
            'A': {('q0', 'A', 'R')},
            's': {('q0', 's', 'R')},
            'c': {('q0', 'c', 'R')},
            't': {('q0', 't', 'R')},
            'I': {('q0', 'I', 'R')},
            'E': {('q0', 'E', 'R')},
        },

        # q2: Encontró y', ahora buscar '=' en cualquier parte restante
        'q2': {
            '=': {('qaccept', '=', 'R')},  # Encontró '=' → ACEPTA (ir a qaccept)
            # Ignorar todos los demás símbolos mientras busca '='
            'y': {('q2', 'y', 'R')},
            'x': {('q2', 'x', 'R')},
            "'": {('q2', "'", 'R')},
            '0': {('q2', '0', 'R')},
            '1': {('q2', '1', 'R')},
            '2': {('q2', '2', 'R')},
            '3': {('q2', '3', 'R')},
            '4': {('q2', '4', 'R')},
            '5': {('q2', '5', 'R')},
            '6': {('q2', '6', 'R')},
            '7': {('q2', '7', 'R')},
            '8': {('q2', '8', 'R')},
            '9': {('q2', '9', 'R')},
            'e': {('q2', 'e', 'R')},
            'π': {('q2', 'π', 'R')},
            '.': {('q2', '.', 'R')},
            '+': {('q2', '+', 'R')},
            '-': {('q2', '-', 'R')},
            '*': {('q2', '*', 'R')},
            '/': {('q2', '/', 'R')},
            '^': {('q2', '^', 'R')},
            '(': {('q2', '(', 'R')},
            ')': {('q2', ')', 'R')},
            'S': {('q2', 'S', 'R')},
            'C': {('q2', 'C', 'R')},
            'T': {('q2', 'T', 'R')},
            'L': {('q2', 'L', 'R')},
            'R': {('q2', 'R', 'R')},
            'A': {('q2', 'A', 'R')},
            's': {('q2', 's', 'R')},
            'c': {('q2', 'c', 'R')},
            't': {('q2', 't', 'R')},
            'I': {('q2', 'I', 'R')},
            'E': {('q2', 'E', 'R')},
            # Si llega a 'B' sin encontrar '=' → rechaza (no hay transición)
        },

        # qaccept: Estado de aceptación - NO TIENE TRANSICIONES
        # La MT se detiene automáticamente al llegar aquí
    },

    initial_state='q0',      # Estado inicial
    blank_symbol='B',         # Símbolo blanco
    final_states={'qaccept'}  # qaccept es el único estado de aceptación
)

# ===================================================================
# PRUEBAS
# ===================================================================

print("=" * 70)
print("PRUEBAS DE LA MÁQUINA DE TURING - VALIDADOR DE ED")
print("=" * 70)

# Lista de cadenas de prueba
pruebas = [
    # Casos que DEBEN ACEPTAR (EDs válidas)
    ("y'=0", True, "ED más simple posible"),
    ("y''+y'=0", True, "ED de segundo orden homogénea"),
    ("y'''+2*y''+y'=0", True, "ED de tercer orden"),
    ("S(y''')+-y''+3*y=0", True, "ED con función seno y signo +-"),
    ("C(x)*y'=3*E(2*x)", True, "ED con coseno y exponencial"),
    ("y''''+y'=0", True, "ED de cuarto orden"),
    ("3*y''+/(x)*y'=0", True, "ED con función recíproca"),

    # Casos que DEBEN RECHAZAR (NO son EDs)
    ("y=0", False, "Solo y, sin derivadas"),
    ("x+3=0", False, "Sin y ni derivadas"),
    ("y'", False, "Falta el símbolo ="),
    ("y'+3*x", False, "Falta el símbolo ="),
    ("=0", False, "Falta y'"),
    ("3*x=5", False, "Sin variable dependiente y"),
    ("", False, "Cadena vacía"),
]

# Ejecutar pruebas
for i, (cadena, debe_aceptar, descripcion) in enumerate(pruebas, 1):
    print(f"\n{i}. Prueba: {descripcion}")
    print(f"   Cadena: '{cadena}'")
    print(f"   Se espera: {'ACEPTAR' if debe_aceptar else 'RECHAZAR'}")

    try:
        resultado = MT_Validador_ED.accepts_input(cadena)
        print(f"   Resultado: {'✓ ACEPTA' if resultado else '✗ RECHAZA'}")

        # Verificar si el resultado coincide con lo esperado
        if resultado == debe_aceptar:
            print(f"   Estado: ✓✓ CORRECTO")
        else:
            print(f"   Estado: ✗✗ ERROR - No coincide con lo esperado")
    except Exception as e:
        print(f"   ERROR en ejecución: {e}")
        print(f"   Estado: ✗✗ FALLO")

print("\n" + "=" * 70)
print("FIN DE PRUEBAS")
print("=" * 70)

# ===================================================================
# Ejemplo detallado de ejecución paso a paso
# ===================================================================
print("\n" + "=" * 70)
print("EJEMPLO DETALLADO: Traza de ejecución para 'y'=0'")
print("=" * 70)

# Ejecutar con read_input para ver la traza completa
try:
    resultado_detallado = MT_Validador_ED.read_input("y'=0")
    print("\nConfiguración final de la cinta:")
    print(resultado_detallado)
except Exception as e:
    print(f"Error en ejecución detallada: {e}")