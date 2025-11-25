import sys
import os

# Aseguramos que Python pueda ver la carpeta TuringMachines
sys.path.append(os.path.join(os.path.dirname(__file__), 'TuringMachines'))

# Importaciones de tus Módulos de Máquinas de Turing
try:
    from TuringMachines.DFValidator import MT_Validador_ED
    from TuringMachines.Order import obtener_orden_mtm
    from TuringMachines.Linearity import es_linealec
    from TuringMachines.ConstantCoefficients import ConstantCoefficients
    # from TuringMachines.Homogeneous import es_homogenea (Aún no implementado, simulamos abajo)
except ImportError as e:
    print(f"Error crítico importando módulos: {e}")
    # Esto permite que el programa no se cierre de golpe si falta un archivo, 
    # pero mostrará error en consola.

class SystemController:
    def __init__(self):
        pass

    def analizar_cadena(self, cadena):
        """
        Recibe la cadena cruda (ej: "y''+S(x)=0") y la pasa por 
        la tubería (pipeline) de autómatas.
        Retorna un diccionario con los resultados.
        """
        resultados = {
            "es_valida": False,
            "orden": 0,
            "linealidad": "N/A",
            "coeficientes": "N/A",
            "homogeneidad": "N/A",
            "mensaje": ""
        }

        # --- PASO 1: VALIDACIÓN ESTRUCTURAL ---
        try:
            # Usamos accepts_input del DFValidator.py
            es_valida = MT_Validador_ED.accepts_input(cadena)
            resultados["es_valida"] = es_valida
            
            if not es_valida:
                resultados["mensaje"] = "La cadena no tiene estructura de Ecuación Diferencial válida."
                return resultados # Si no es válida, abortamos el resto
        except Exception as e:
            resultados["mensaje"] = f"Error en Validador: {str(e)}"
            return resultados

        # --- PASO 2: DETERMINAR ORDEN (GRADO) ---
        try:
            # Usamos la función robusta de Order.py
            orden = obtener_orden_mtm(cadena)
            resultados["orden"] = orden
        except Exception as e:
            resultados["orden"] = -1 # Código de error visual

        # --- PASO 3: LINEALIDAD ---
        es_lineal = False
        try:
            # Usamos la función es_linealec de Linearity.py
            es_lineal = es_linealec(cadena)
            resultados["linealidad"] = "Lineal" if es_lineal else "No Lineal"
        except Exception as e:
            resultados["linealidad"] = "Error"

        # --- PASO 4: COEFICIENTES (Solo si es Lineal) ---
        if es_lineal:
            try:
                # Usamos ConstantCoefficients.accepts_input
                # Nota: Asumimos que la máquina acepta si son constantes
                es_cte = ConstantCoefficients.accepts_input(cadena)
                resultados["coeficientes"] = "Constantes" if es_cte else "Variables"
            except Exception as e:
                # Si la máquina rechaza o falla, asumimos variables o error
                # Dependiendo de tu lógica 'accepts', ajusta esto.
                # Si tu MT rechaza cuando hay coef variables, esto captura el False.
                if isinstance(e, Exception): # Si fue crash
                     resultados["coeficientes"] = "Error"
                else:
                     resultados["coeficientes"] = "Variables"
        else:
            resultados["coeficientes"] = "-" # No aplica si no es lineal

        # --- PASO 5: HOMOGENEIDAD ---
        # (Placeholder hasta que termines Homogeneous.py)
        # Lógica temporal simple: Si termina en "=0" es homogénea
        if cadena.endswith("=0") or cadena.endswith("= 0"):
            resultados["homogeneidad"] = "Homogénea"
        else:
            resultados["homogeneidad"] = "No Homogénea"

        resultados["mensaje"] = "Análisis Completado Exitosamente."
        return resultados