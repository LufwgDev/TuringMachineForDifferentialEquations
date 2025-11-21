
#pip install vpython
from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Tanque de mezcla: concentración y nivel",
               width=1000, height=700, background=color.gray(0.2))
scene.center = vector(0, 2, 0)

# Gráficas
graph_altura = graph(title="Altura vs Tiempo", 
                     xtitle="Tiempo (s)", ytitle="Altura (m)",
                     width=650, height=300, align="right")
curve_altura = gcurve(color=color.cyan, width=2, label="H(t)")
curve_altura_teorica = gcurve(color=color.yellow, width=2, label="H(t) - Teórica", dot=True, dot_radius=3)

graph_concentracion = graph(title="Concentración vs Tiempo", 
                            xtitle="Tiempo (s)", ytitle="Concentración (g/L)",
                            width=650, height=300, align="right")
curve_conc = gcurve(color=color.orange, width=2, label="C(t)")
curve_conc_teorica = gcurve(color=color.red, width=2, label="C(t) - Teórica", dot=True, dot_radius=3)

# lista para llevar los objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del Tanque de Mezcla ---\n")

# Sliders con valores dinámicos
# --- Caudal de entrada ---
texto_Qin = wtext(text="Caudal de entrada (Qin): 0.025 m³/s\n")
def actualizar_Qin(s):
    texto_Qin.text = f"Caudal de entrada (Qin): {s.value:.3f} m³/s\n"
slider_Qin = slider(min=0.005, max=0.1, value=0.025, step=0.005, bind=actualizar_Qin)

# --- Caudal de salida ---
texto_Qout = wtext(text="\nCaudal de salida (Qout): 0.015 m³/s\n")
def actualizar_Qout(s):
    texto_Qout.text = f"\nCaudal de salida (Qout): {s.value:.3f} m³/s\n"
slider_Qout = slider(min=0.005, max=0.1, value=0.015, step=0.005, bind=actualizar_Qout)

# --- Concentración de entrada ---
texto_Cin = wtext(text="\nConcentración de entrada (Cin): 8.00 g/L\n")
def actualizar_Cin(s):
    texto_Cin.text = f"\nConcentración de entrada (Cin): {s.value:.2f} g/L\n"
slider_Cin = slider(min=0.0, max=20.0, value=8.0, step=0.5, bind=actualizar_Cin)

# --- Altura inicial del agua ---
texto_h0 = wtext(text="\nAltura inicial del agua: 0.50 m\n")
def actualizar_h0(s):
    texto_h0.text = f"\nAltura inicial del agua: {s.value:.2f} m\n"
slider_h0 = slider(min=0.1, max=3.5, value=0.5, step=0.1, bind=actualizar_h0)

# --- Radio del tanque ---
texto_radio = wtext(text="\nRadio del tanque: 1.50 m\n")
def actualizar_radio(s):
    texto_radio.text = f"\nRadio del tanque: {s.value:.2f} m\n"
slider_radio = slider(min=0.5, max=3.0, value=1.5, step=0.1, bind=actualizar_radio)

wtext(text="\n")

# Mostrar ecuaciones diferenciales generales
ecuacion_text = wtext(text="\n--- Ecuaciones Diferenciales ---\n")
ecuacion_text2 = wtext(text="Sistema acoplado:\n")
ecuacion_text3 = wtext(text="  dC/dt = (Qin·Cin - Qout·C) / V(t)\n")
ecuacion_text4 = wtext(text="  dH/dt = (Qin - Qout) / A\n")
ecuacion_text5 = wtext(text="donde V(t) = A·H(t)\n\n")

# Ecuaciones con parámetros
ecuacion_params = wtext(text="Ecuaciones con parámetros: (presiona 'Iniciar simulación')\n\n")

# Análisis de las ecuaciones
analisis_ec = wtext(text="")

# Salidas numéricas
salida_info = wtext(text="\nTiempo: 0.0 s | Nivel: 0.0 m | Concentración: 0.0 g/L\n")

# -------------------------------------------------
# ANÁLISIS DE LAS ECUACIONES
# -------------------------------------------------
def analizar_ecuaciones(Qin, Qout, Cin, h0, A):
    """
    Analiza el sistema de ecuaciones diferenciales del tanque de mezcla.
    
    Sistema:
    1) dH/dt = (Qin - Qout) / A
    2) dC/dt = (Qin·Cin - Qout·C) / (A·H)
    
    Soluciones analíticas:
    """
    
    texto = "\n--- Análisis del Sistema ---\n\n"
    
    # Ecuación de altura (independiente, lineal)
    texto += "🔹 Ecuación de Altura (EDO lineal de primer orden):\n"
    texto += f"   dH/dt = ({Qin:.3f} - {Qout:.3f}) / {A:.4f}\n"
    
    delta_Q = Qin - Qout
    
    if abs(delta_Q) < 1e-6:
        texto += f"   dH/dt = 0 (nivel constante)\n"
        texto += f"   Solución: H(t) = {h0:.2f} m (constante)\n\n"
        H_final = h0
        comportamiento_H = "constante"
    else:
        k_H = delta_Q / A
        texto += f"   dH/dt = {k_H:.6f} m/s\n"
        texto += f"   Solución: H(t) = {h0:.2f} + {k_H:.6f}·t\n"
        
        if delta_Q > 0:
            texto += f"   ⬆️ El tanque se LLENA (Qin > Qout)\n\n"
            comportamiento_H = "llenado"
            H_final = None  # dependerá de cuándo se llene
        else:
            t_vaciado = -h0 / k_H
            texto += f"   ⬇️ El tanque se VACÍA (Qin < Qout)\n"
            texto += f"   Tiempo de vaciado: {t_vaciado:.2f} s\n\n"
            comportamiento_H = "vaciado"
            H_final = 0
    
    # Ecuación de concentración (depende de H(t))
    texto += "🔹 Ecuación de Concentración (EDO no lineal):\n"
    texto += f"   dC/dt = ({Qin:.3f}·{Cin:.2f} - {Qout:.3f}·C) / (A·H(t))\n"
    
    if abs(delta_Q) < 1e-6:
        # Caso especial: volumen constante
        texto += f"   Con H(t) constante, V = {A*h0:.4f} m³:\n"
        tau = (A * h0) / Qout
        C_eq = (Qin / Qout) * Cin
        texto += f"   dC/dt = ({Qin*Cin:.4f} - {Qout:.3f}·C) / {A*h0:.4f}\n"
        texto += f"   Solución (exponencial):\n"
        texto += f"   C(t) = {C_eq:.2f}·(1 - e^(-t/{tau:.2f}))\n"
        texto += f"   Concentración de equilibrio: C_eq = {C_eq:.2f} g/L\n"
        texto += f"   Constante de tiempo: τ = {tau:.2f} s\n\n"
    else:
        texto += f"   Solución compleja (depende de H(t) variable)\n"
        if Qin > Qout:
            C_final_estimado = Cin * (Qin / Qout)
            texto += f"   C(t) → {Cin:.2f} g/L (tiende a Cin al llenarse)\n\n"
        else:
            texto += f"   C(t) evoluciona hasta vaciarse\n\n"
    
    return texto, comportamiento_H, delta_Q / A if abs(delta_Q) > 1e-6 else 0


def altura_teorica(t, h0, k_H):
    """Calcula H(t) = h0 + k_H·t"""
    return h0 + k_H * t


def concentracion_teorica_volumen_constante(t, Cin, Qin, Qout, V):
    """
    Para volumen constante (Qin = Qout):
    C(t) = C_eq·(1 - e^(-t/τ))
    donde C_eq = (Qin/Qout)·Cin y τ = V/Qout
    """
    C_eq = (Qin / Qout) * Cin
    tau = V / Qout
    return C_eq * (1 - np.exp(-t / tau))


# -------------------------------------------------
# FUNCIONES DE SIMULACIÓN
# -------------------------------------------------

# Limpiar objetos anteriores
def hide_previous_objects():
    global created_objects
    for obj in created_objects:
        try:
            obj.visible = False
        except:
            pass
    created_objects = []

# Conversión de concentración a color
def concentration_to_color(C, Cmax=20):
    """Color entre azul (0 g/L) y rojo (Cmax g/L)."""
    ratio = min(max(C / Cmax, 0), 1)
    return vector(ratio, 0.4 + 0.4*(1 - ratio), 1 - ratio)

# Simulación
def simular(ev):
    global created_objects, curve_altura, curve_conc, curve_altura_teorica, curve_conc_teorica

    # Leer parámetros desde sliders
    Qin = float(slider_Qin.value)
    Qout = float(slider_Qout.value)
    Cin = float(slider_Cin.value)
    water_height0 = float(slider_h0.value)
    tank_radius = float(slider_radio.value)
    
    # Parámetros calculados
    tank_height = 4.0      # m
    A = np.pi * tank_radius**2  # área transversal (m²)
    V0 = A * water_height0  # volumen inicial

    # Construir ecuaciones con parámetros
    ec_texto = (f"Ecuaciones con parámetros:\n"
                f"  dC/dt = ({Qin:.3f}·{Cin:.2f} - {Qout:.3f}·C) / (A·H)\n"
                f"  dH/dt = ({Qin:.3f} - {Qout:.3f}) / {A:.4f}\n"
                f"  dH/dt = {(Qin-Qout)/A:.6f} m/s\n\n")
    ecuacion_params.text = ec_texto
    
    # Análisis del sistema
    texto_analisis, comportamiento_H, k_H = analizar_ecuaciones(Qin, Qout, Cin, water_height0, A)
    analisis_ec.text = texto_analisis

    # Limpiar gráficas anteriores
    curve_altura.delete()
    curve_conc.delete()
    curve_altura_teorica.delete()
    curve_conc_teorica.delete()
    curve_altura = gcurve(color=color.cyan, width=2, label="H(t)")
    curve_conc = gcurve(color=color.orange, width=2, label="C(t)")
    curve_altura_teorica = gcurve(color=color.yellow, width=2, label="H(t) - Teórica", dot=True, dot_radius=3)
    curve_conc_teorica = gcurve(color=color.red, width=2, label="C(t) - Teórica", dot=True, dot_radius=3)

    # Ocultar objetos previos
    hide_previous_objects()

    # ============================
    # CONFIGURACIÓN DE ESCENA
    # ============================
    
    # Crear tanque
    tank = cylinder(pos=vector(0, 0, 0), axis=vector(0, tank_height, 0),
                    radius=tank_radius, opacity=0.15, color=color.white)
    
    # Crear líquido
    water = cylinder(pos=vector(0, 0, 0), axis=vector(0, water_height0, 0),
                     radius=tank_radius*0.99, color=color.cyan, opacity=0.8)
    
    # Entradas y salidas
    inlet = cylinder(pos=vector(-tank_radius-0.5, tank_height*0.9, 0),
                     axis=vector(0.6, 0, 0), radius=0.05, color=color.blue)
    outlet = cylinder(pos=vector(tank_radius+0.1, 0, 0),
                      axis=vector(0.6, 0, 0), radius=0.05, color=color.red)
    
    # Gota de entrada
    drop = sphere(pos=inlet.pos + vector(0.6, 0, 0),
                  radius=0.06, color=color.blue, make_trail=True, retain=10)
    
    # Texto informativo
    info = label(pos=vector(0, tank_height + 0.7, 0),
                 text="", height=16, box=False, color=color.white)
    
    # Indicador de concentración (barra de color)
    conc_indicator = box(pos=vector(tank_radius+1, tank_height/2, 0), 
                         size=vector(0.3, tank_height, 0.3), 
                         color=concentration_to_color(0))
    conc_label = label(pos=vector(tank_radius+1.5, tank_height+0.3, 0),
                       text="Conc.", height=12, box=False, color=color.white)
    
    created_objects.extend([tank, water, inlet, outlet, drop, info, conc_indicator, conc_label])

    # ============================
    # VARIABLES DE SIMULACIÓN
    # ============================
    t = 0
    dt = 0.05
    C = 0.0        # g/L (inicialmente pura)
    water_height = water_height0
    contador_graficas = 0

    # ============================
    # BUCLE DE SIMULACIÓN
    # ============================
    running = True
    
    def stop_simulation(ev):
        nonlocal running
        running = False
    
    # Botón para detener
    boton_detener = button(text="Detener simulación", bind=stop_simulation)
    created_objects.append(boton_detener)
    
    volumen_constante = abs(Qin - Qout) < 1e-6
    
    while running:
        rate(60)

        # EDO de concentración
        V_actual = A * water_height
        dCdt = (Qin*Cin - Qout*C) / V_actual if V_actual > 0 else 0
        C += dCdt * dt

        # EDO de nivel (balance de volumen)
        dHdt = (Qin - Qout) / A
        water_height += dHdt * dt
        t += dt

        # Condiciones de parada
        if water_height <= 0:
            water_height = 0
            info.text = f"Tanque vacío.\nTiempo: {t:.1f}s\nC: {C:.2f} g/L"
            break
        if water_height >= tank_height:
            water_height = tank_height
            info.text = f"Tanque lleno.\nTiempo: {t:.1f}s\nC: {C:.2f} g/L"
            break

        # Actualiza color del líquido
        water.color = concentration_to_color(C)

        # Actualiza nivel del agua
        water.axis = vector(0, water_height, 0)

        # Actualiza indicador de concentración
        conc_indicator.color = concentration_to_color(C)

        # Movimiento de la gota
        drop.pos.x += 0.08
        if drop.pos.x > inlet.pos.x + 0.6:
            drop.pos = inlet.pos + vector(0, 0, 0)
            drop.clear_trail()

        # Calcular valores teóricos
        H_teorica = altura_teorica(t, water_height0, k_H)
        H_teorica = max(0, min(H_teorica, tank_height))
        
        if volumen_constante:
            C_teorica = concentracion_teorica_volumen_constante(t, Cin, Qin, Qout, V0)
        else:
            C_teorica = C  # Aproximación (la solución exacta es compleja)

        # Texto informativo
        info.text = (f"t = {t:.1f} s\n"
                     f"Nivel: {water_height:.2f} m\n"
                     f"C(t): {C:.2f} g/L")
        
        # Actualizar información general
        salida_info.text = f"\nTiempo: {t:.1f} s | Nivel: {water_height:.2f} m | Concentración: {C:.2f} g/L\n"

        # Agregar puntos a las gráficas
        contador_graficas += 1
        if contador_graficas % 3 == 0:
            curve_altura.plot(t, water_height)
            curve_conc.plot(t, C)
            # Graficar soluciones teóricas
            if contador_graficas % 6 == 0:
                curve_altura_teorica.plot(t, H_teorica)
                if volumen_constante:
                    curve_conc_teorica.plot(t, C_teorica)
        
        # Límite de tiempo de simulación
        if t > 200:
            break

    # Limpiar botón de detener
    boton_detener.delete()

# Botón para iniciar simulación
boton_iniciar = button(text="▶ Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")