
#pip install vpython
from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Vaciado de un tanque cilíndrico",
               width=900, height=600, background=color.white)

# Gráficas
graph_altura = graph(title="Altura vs Tiempo", 
                     xtitle="Tiempo (s)", ytitle="Altura (m)",
                     width=650, height=300, align="right")
curve_altura = gcurve(color=color.blue, width=2, label="h(t) - Numérica")
curve_altura_teorica = gcurve(color=color.red, width=2, label="h(t) - Teórica", dot=True, dot_radius=3)

graph_volumen = graph(title="Volumen vs Tiempo", 
                      xtitle="Tiempo (s)", ytitle="Volumen (m³)",
                      width=650, height=300, align="right")
curve_volumen = gcurve(color=color.green, width=2, label="V(t)")

# Constante gravitacional
g = 9.8  # m/s²

# lista para llevar los objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del modelo ---\n")

# Sliders con valores dinámicos
# --- Altura inicial ---
texto_h0 = wtext(text="Altura inicial (h₀): 2.00 m\n")
def actualizar_h0(s):
    texto_h0.text = f"Altura inicial (h₀): {s.value:.2f} m\n"
slider_h0 = slider(min=0.5, max=10, value=2, step=0.1, bind=actualizar_h0)

# --- Radio del tanque ---
texto_R = wtext(text="\nRadio del tanque (R): 0.50 m\n")
def actualizar_R(s):
    texto_R.text = f"\nRadio del tanque (R): {s.value:.2f} m\n"
slider_R = slider(min=0.2, max=2.5, value=0.5, step=0.05, bind=actualizar_R)

# --- Radio del orificio de salida ---
texto_r = wtext(text="\nRadio del orificio (r): 0.05 m\n")
def actualizar_r(s):
    texto_r.text = f"\nRadio del orificio (r): {s.value:.4f} m\n"
slider_r = slider(min=0.005, max=0.2, value=0.05, step=0.005, bind=actualizar_r)

# --- Coeficiente de descarga ---
texto_Cd = wtext(text="\nCoeficiente de descarga (Cd): 0.62\n")
def actualizar_Cd(s):
    texto_Cd.text = f"\nCoeficiente de descarga (Cd): {s.value:.2f}\n"
slider_Cd = slider(min=0.3, max=1.0, value=0.62, step=0.02, bind=actualizar_Cd)

wtext(text="\n")

# Mostrar ecuación diferencial general
ecuacion_general = wtext(text="\n--- Ecuación Diferencial ---\n")
ecuacion_general2 = wtext(text="Forma general: dh/dt = -(Cd·A_orificio/A_tanque)·√(2gh)\n")
ecuacion_general3 = wtext(text="donde: A_orificio = π·r², A_tanque = π·R²\n\n")

# Ecuación con parámetros sustituidos
ecuacion_params = wtext(text="Ecuación con parámetros: (presiona 'Iniciar simulación')\n\n")

# Solución analítica
solucion_analitica = wtext(text="")

# Salidas numéricas
salida_info = wtext(text="Tiempo total: ---\n")
salida_areas = wtext(text="")

# -------------------------------------------------
# ANÁLISIS DE LA ECUACIÓN
# -------------------------------------------------
def analizar_ecuacion(h0, Cd, A_orificio, A_tanque, g):
    """
    Analiza la ecuación diferencial y encuentra su solución analítica.
    
    Ecuación: dh/dt = -k·√h  donde k = Cd·(A_orificio/A_tanque)·√(2g)
    
    Solución por separación de variables:
    ∫ dh/√h = -k ∫ dt
    2√h = -kt + C
    
    Con condición inicial h(0) = h₀:
    2√h₀ = C
    
    Por lo tanto:
    √h = √h₀ - (k/2)·t
    h(t) = (√h₀ - (k/2)·t)²
    
    El tanque se vacía cuando h = 0:
    √h₀ - (k/2)·t_final = 0
    t_final = 2√h₀ / k
    """
    
    k = Cd * (A_orificio / A_tanque) * np.sqrt(2 * g)
    
    # Tiempo teórico de vaciado
    t_final_teorico = 2 * np.sqrt(h0) / k
    
    texto = "\n--- Solución Analítica ---\n"
    texto += f"Simplificando: dh/dt = -k·√h\n"
    texto += f"donde k = Cd·(A_orificio/A_tanque)·√(2g) = {k:.6f}\n\n"
    
    texto += "📐 Resolución por separación de variables:\n"
    texto += "∫ dh/√h = -k ∫ dt\n"
    texto += "2√h = -kt + C\n"
    texto += f"Con h(0) = {h0:.2f}, obtenemos C = {2*np.sqrt(h0):.4f}\n\n"
    
    texto += "🎯 Solución general:\n"
    texto += f"h(t) = (√{h0:.2f} - {k/2:.6f}·t)²\n"
    texto += f"h(t) = ({np.sqrt(h0):.4f} - {k/2:.6f}·t)²\n\n"
    
    texto += "⏱️  Tiempo teórico de vaciado:\n"
    texto += f"t_final = 2√h₀ / k = 2√{h0:.2f} / {k:.6f}\n"
    texto += f"t_final = {t_final_teorico:.2f} segundos\n\n"
    
    return texto, k, t_final_teorico


def solucion_teorica(t, h0, k):
    """
    Calcula la altura teórica en el tiempo t usando la solución analítica.
    h(t) = (√h₀ - (k/2)·t)²
    """
    raiz = np.sqrt(h0) - (k/2) * t
    if raiz < 0:
        return 0
    return raiz**2


# -------------------------------------------------
# ECUACIÓN DIFERENCIAL
# -------------------------------------------------
def dhdt(h, Cd, A_orificio, A_tanque, g):
    """
    Ecuación de Torricelli para vaciado de tanque:
    dh/dt = -(Cd·A_orificio/A_tanque)·√(2gh)
    """
    if h <= 0:
        return 0
    return -(Cd * A_orificio / A_tanque) * np.sqrt(2 * g * h)


# Limpiar objetos anteriores
def hide_previous_objects():
    global created_objects
    for obj in created_objects:
        try:
            obj.visible = False
        except:
            pass
    created_objects = []


# Simulación
def simular(ev):
    global created_objects, curve_altura, curve_volumen, curve_altura_teorica

    # Leer parámetros desde sliders
    h0 = float(slider_h0.value)
    R = float(slider_R.value)
    r = float(slider_r.value)
    Cd = float(slider_Cd.value)

    # Calcular áreas
    A_tanque = np.pi * R**2
    A_orificio = np.pi * r**2
    
    # Mostrar información de áreas
    salida_areas.text = (f"Área del tanque: {A_tanque:.4f} m²\n"
                        f"Área del orificio: {A_orificio:.6f} m²\n"
                        f"Relación A_orificio/A_tanque: {A_orificio/A_tanque:.6f}\n\n")
    
    # Construir ecuación con parámetros sustituidos
    coef = Cd * A_orificio / A_tanque
    ec_texto = (f"Ecuación con parámetros:\n"
                f"dh/dt = -({Cd:.2f}·{A_orificio:.6f}/{A_tanque:.4f})·√(2·{g}·h)\n"
                f"dh/dt = -({coef:.6f})·√({2*g:.2f}·h)\n"
                f"dh/dt ≈ -{coef:.6f}·√({2*g:.1f}h)\n\n")
    ecuacion_params.text = ec_texto
    
    # Análisis de la ecuación
    texto_analisis, k, t_final_teorico = analizar_ecuacion(h0, Cd, A_orificio, A_tanque, g)
    solucion_analitica.text = texto_analisis

    # Limpiar gráficas anteriores
    curve_altura.delete()
    curve_volumen.delete()
    curve_altura_teorica.delete()
    curve_altura = gcurve(color=color.blue, width=2, label="h(t) - Numérica")
    curve_volumen = gcurve(color=color.green, width=2, label="V(t)")
    curve_altura_teorica = gcurve(color=color.red, width=2, label="h(t) - Teórica", dot=True, dot_radius=3)

    # Ocultar objetos previos
    hide_previous_objects()

    # Crear tanque cilíndrico exterior (solo el borde)
    tanque = cylinder(pos=vector(0, 0, 0), axis=vector(0, h0*1.2, 0),
                      radius=R, opacity=0.15, color=color.gray(0.5))
    
    # Crear agua
    agua = cylinder(pos=vector(0, 0, 0), axis=vector(0, h0, 0),
                    radius=R * 0.98, color=color.cyan, opacity=0.7)
    
    # Crear orificio de salida (visual)
    orificio = cylinder(pos=vector(R*0.7, 0, 0), axis=vector(0.3, 0, 0),
                       radius=r, color=color.red, opacity=0.8)
    orificio_label = label(pos=vector(R*0.85, -0.3, 0),
                          text=f"Orificio: r={r:.3f}m", 
                          height=10, box=False, color=color.red)
    
    # Etiquetas
    label_h = label(text=f"Altura: {h0:.2f} m",
                    pos=vector(0, h0*1.3, 0), box=False, height=16)
    label_v = label(text=f"Volumen: {A_tanque*h0:.3f} m³",
                    pos=vector(0, h0*1.2, 0), box=False, height=14)
    label_t = label(text=f"Tiempo: 0.00 s",
                    pos=vector(0, h0*1.1, 0), box=False, height=14)
    label_error = label(text=f"Error: 0.00%",
                       pos=vector(0, h0*1.0, 0), box=False, height=12, color=color.orange)

    # Línea de referencia del fondo
    fondo = cylinder(pos=vector(-R*1.2, 0, 0), axis=vector(R*2.4, 0, 0),
                    radius=0.02, color=color.green)

    created_objects.extend([tanque, agua, orificio, orificio_label, 
                           label_h, label_v, label_t, label_error, fondo])

    # Variables de simulación
    h = h0
    dt = 0.01
    tiempo_total = 0.0
    contador_graficas = 0
    
    # Botón para detener
    running = True
    def stop_simulation(ev):
        nonlocal running
        running = False
    
    boton_detener = button(text="Detener simulación", bind=stop_simulation)
    created_objects.append(boton_detener)

    # Loop de simulación
    while h > 0.001 and running:
        rate(100)

        # Método de Euler para resolver dh/dt
        dh = dhdt(h, Cd, A_orificio, A_tanque, g) * dt
        h = max(h + dh, 0)

        tiempo_total += dt

        # Calcular volumen actual
        volumen = A_tanque * h
        
        # Calcular altura teórica
        h_teorica = solucion_teorica(tiempo_total, h0, k)
        
        # Calcular error porcentual
        if h_teorica > 0:
            error = abs(h - h_teorica) / h_teorica * 100
        else:
            error = 0

        # Actualizar visualización del agua
        agua.axis = vector(0, h, 0)
        
        # Actualizar etiquetas
        label_h.text = f"Altura: {h:.3f} m"
        label_v.text = f"Volumen: {volumen:.4f} m³"
        label_t.text = f"Tiempo: {tiempo_total:.2f} s"
        label_error.text = f"Error vs teórica: {error:.2f}%"

        # Agregar puntos a las gráficas (cada cierto tiempo para no saturar)
        contador_graficas += 1
        if contador_graficas % 5 == 0:  # cada 5 iteraciones
            curve_altura.plot(tiempo_total, h)
            curve_volumen.plot(tiempo_total, volumen)
            # Graficar solución teórica cada 10 puntos
            if contador_graficas % 10 == 0:
                curve_altura_teorica.plot(tiempo_total, h_teorica)

    # Limpiar botón de detener
    boton_detener.delete()

    # Mostrar resultados finales
    diferencia_tiempo = abs(tiempo_total - t_final_teorico)
    porcentaje_dif = (diferencia_tiempo / t_final_teorico) * 100
    
    salida_info.text = (f"⏱️  Tiempo de vaciado (numérico): {tiempo_total:.2f} s\n"
                       f"⏱️  Tiempo teórico: {t_final_teorico:.2f} s\n"
                       f"📊 Diferencia: {diferencia_tiempo:.2f} s ({porcentaje_dif:.2f}%)\n"
                       f"📊 Volumen inicial: {A_tanque*h0:.4f} m³\n"
                       f"📉 Velocidad promedio de vaciado: {h0/tiempo_total:.4f} m/s\n\n")


# Botón para iniciar simulación
boton = button(text="▶ Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")