
#pip install vpython
from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Simulación de Circuito RLC",
               width=1000, height=700, background=color.white)

# Gráficas
graph_carga = graph(title="Carga vs Tiempo", 
                    xtitle="Tiempo (s)", ytitle="Carga Q (C)",
                    width=650, height=300, align="right")
curve_carga = gcurve(color=color.blue, width=2, label="Q(t)")

graph_corriente = graph(title="Corriente vs Tiempo", 
                        xtitle="Tiempo (s)", ytitle="Corriente I (A)",
                        width=650, height=300, align="right")
curve_corriente = gcurve(color=color.red, width=2, label="I(t)")

# Lista para objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del Circuito RLC ---\n")

# Sliders con valores dinámicos
# --- Resistencia ---
texto_R = wtext(text="Resistencia (R): 5.00 Ω\n")
def actualizar_R(s):
    texto_R.text = f"Resistencia (R): {s.value:.2f} Ω\n"
slider_R = slider(min=0.1, max=50.0, value=5.0, step=0.5, bind=actualizar_R)

# --- Inductancia ---
texto_L = wtext(text="\nInductancia (L): 0.50 H\n")
def actualizar_L(s):
    texto_L.text = f"\nInductancia (L): {s.value:.2f} H\n"
slider_L = slider(min=0.1, max=5.0, value=0.5, step=0.1, bind=actualizar_L)

# --- Capacitancia ---
texto_C = wtext(text="\nCapacitancia (C): 0.10 F\n")
def actualizar_C(s):
    texto_C.text = f"\nCapacitancia (C): {s.value:.2f} F\n"
slider_C = slider(min=0.01, max=1.0, value=0.1, step=0.01, bind=actualizar_C)

# --- Carga inicial ---
texto_Q0 = wtext(text="\nCarga inicial (Q₀): 1.00 C\n")
def actualizar_Q0(s):
    texto_Q0.text = f"\nCarga inicial (Q₀): {s.value:.2f} C\n"
slider_Q0 = slider(min=0.0, max=5.0, value=1.0, step=0.1, bind=actualizar_Q0)

# --- Corriente inicial ---
texto_I0 = wtext(text="\nCorriente inicial (I₀): 0.00 A\n")
def actualizar_I0(s):
    texto_I0.text = f"\nCorriente inicial (I₀): {s.value:.2f} A\n"
slider_I0 = slider(min=-2.0, max=2.0, value=0.0, step=0.1, bind=actualizar_I0)

# --- Voltaje de fuente ---
texto_V0 = wtext(text="\nVoltaje fuente (V₀): 0.00 V\n")
def actualizar_V0(s):
    texto_V0.text = f"\nVoltaje fuente (V₀): {s.value:.2f} V\n"
slider_V0 = slider(min=0.0, max=20.0, value=0.0, step=0.5, bind=actualizar_V0)

# --- Frecuencia de fuente ---
texto_omega = wtext(text="\nFrecuencia fuente (ω): 2.00 rad/s\n")
def actualizar_omega(s):
    texto_omega.text = f"\nFrecuencia fuente (ω): {s.value:.2f} rad/s\n"
slider_omega = slider(min=0.0, max=10.0, value=2.0, step=0.5, bind=actualizar_omega)

wtext(text="\n")

# Mostrar ecuación diferencial general
ecuacion_text = wtext(text="\n--- Ecuación Diferencial ---\n")
ecuacion_text2 = wtext(text="Forma general: L·Q'' + R·Q' + Q/C = V₀·cos(ω·t)\n")
ecuacion_text3 = wtext(text="donde Q es la carga e I = Q' es la corriente\n\n")

# Ecuación con parámetros
ecuacion_params = wtext(text="Ecuación con parámetros: (presiona 'Iniciar simulación')\n\n")

# Análisis de la ecuación característica
analisis_ec = wtext(text="")

# Salidas numéricas
salida_info = wtext(text="\nTiempo actual: 0.00 s\n")

# -------------------------------------------------
# ANÁLISIS DE LA ECUACIÓN
# -------------------------------------------------
def analizar_ecuacion_rlc(R, L, C, Q0, I0, V0, omega):
    """
    Analiza la ecuación diferencial del circuito RLC.
    
    Ecuación: L·Q'' + R·Q' + Q/C = V₀·cos(ω·t)
    
    Para la parte homogénea (V₀ = 0):
    Ecuación característica: L·r² + R·r + 1/C = 0
    r = [-R ± √(R² - 4L/C)] / (2L)
    """
    
    # Ecuación con parámetros
    if V0 == 0:
        ec_texto = f"({L:.2f})·Q'' + ({R:.2f})·Q' + Q/({C:.2f}) = 0\n"
        ec_texto += f"Simplificando: ({L:.2f})·Q'' + ({R:.2f})·Q' + ({1/C:.2f})·Q = 0\n\n"
    else:
        ec_texto = f"({L:.2f})·Q'' + ({R:.2f})·Q' + Q/({C:.2f}) = ({V0:.2f})·cos(({omega:.2f})·t)\n"
        ec_texto += f"Simplificando: ({L:.2f})·Q'' + ({R:.2f})·Q' + ({1/C:.2f})·Q = ({V0:.2f})·cos(({omega:.2f})·t)\n\n"
    
    # Análisis de la ecuación característica homogénea
    analisis = "\n--- Análisis de la Ecuación Característica ---\n"
    analisis += f"Ecuación característica: ({L:.2f})·r² + ({R:.2f})·r + ({1/C:.2f}) = 0\n"
    
    # Discriminante
    discriminante = R**2 - 4*L*(1/C)
    analisis += f"Discriminante Δ = R² - 4L/C = {discriminante:.4f}\n\n"
    
    if discriminante > 0:
        # Sobreamortiguado - dos raíces reales
        r1 = (-R + np.sqrt(discriminante)) / (2*L)
        r2 = (-R - np.sqrt(discriminante)) / (2*L)
        analisis += "🔹 Caso: SOBREAMORTIGUADO (dos raíces reales distintas)\n"
        analisis += f"   r₁ = {r1:.4f}\n"
        analisis += f"   r₂ = {r2:.4f}\n"
        analisis += f"   Solución homogénea: Q_h(t) = C₁·e^({r1:.4f}·t) + C₂·e^({r2:.4f}·t)\n"
        analisis += "   Comportamiento: Decaimiento exponencial SIN oscilaciones\n"
        tipo = "sobreamortiguado"
        
    elif abs(discriminante) < 1e-10:
        # Críticamente amortiguado
        r = -R / (2*L)
        analisis += "🔹 Caso: CRÍTICAMENTE AMORTIGUADO (raíz real doble)\n"
        analisis += f"   r = {r:.4f}\n"
        analisis += f"   Solución homogénea: Q_h(t) = (C₁ + C₂·t)·e^({r:.4f}·t)\n"
        analisis += "   Comportamiento: Decaimiento más rápido posible sin oscilación\n"
        tipo = "critico"
        
    else:
        # Subamortiguado - raíces complejas
        alpha = -R / (2*L)
        beta = np.sqrt(-discriminante) / (2*L)
        analisis += "🔹 Caso: SUBAMORTIGUADO (raíces complejas conjugadas)\n"
        analisis += f"   r = {alpha:.4f} ± {beta:.4f}i\n"
        analisis += f"   Solución homogénea: Q_h(t) = e^({alpha:.4f}·t)·[C₁·cos({beta:.4f}·t) + C₂·sin({beta:.4f}·t)]\n"
        analisis += "   Comportamiento: Oscilaciones AMORTIGUADAS\n"
        tipo = "subamortiguado"
        
        # Parámetros adicionales
        omega_n = 1 / np.sqrt(L*C)
        zeta = R / (2 * np.sqrt(L/C))
        periodo = 2*np.pi / beta
        
        analisis += f"\n   📊 Parámetros del sistema:\n"
        analisis += f"   Frecuencia natural: ω₀ = {omega_n:.4f} rad/s\n"
        analisis += f"   Factor de amortiguamiento: ζ = {zeta:.4f}\n"
        analisis += f"   Frecuencia amortiguada: ω_d = {beta:.4f} rad/s\n"
        analisis += f"   Período de oscilación: T = {periodo:.4f} s\n"
    
    if V0 > 0:
        analisis += f"\n🔹 Solución particular (forzamiento externo):\n"
        analisis += f"   Debido a V₀·cos(ω·t), habrá una respuesta forzada\n"
        analisis += f"   Solución completa: Q(t) = Q_h(t) + Q_p(t)\n"
        analisis += f"   donde Q_p(t) es la solución particular (estado estacionario)\n"
    
    return ec_texto, analisis, tipo


# -------------------------------------------------
# FUNCIONES DE SIMULACIÓN
# -------------------------------------------------

def hide_previous_objects():
    global created_objects
    for obj in created_objects:
        try:
            obj.visible = False
        except:
            pass
    created_objects = []

def simular(ev):
    global created_objects, curve_carga, curve_corriente

    # Leer parámetros desde sliders
    R = float(slider_R.value)
    L = float(slider_L.value)
    C = float(slider_C.value)
    Q0 = float(slider_Q0.value)
    I0 = float(slider_I0.value)
    V0 = float(slider_V0.value)
    omega = float(slider_omega.value)

    # Analizar ecuación
    ec_texto, analisis, tipo = analizar_ecuacion_rlc(R, L, C, Q0, I0, V0, omega)
    ecuacion_params.text = f"Ecuación con parámetros:\n{ec_texto}"
    analisis_ec.text = analisis

    # Limpiar gráficas anteriores
    curve_carga.delete()
    curve_corriente.delete()
    curve_carga = gcurve(color=color.blue, width=2, label="Q(t)")
    curve_corriente = gcurve(color=color.red, width=2, label="I(t)")

    # Ocultar objetos previos
    hide_previous_objects()

    # Función de voltaje externo
    def V(t):
        return V0 * np.cos(omega * t)

    # ============================
    # CONFIGURACIÓN DE ESCENA
    # ============================
    
    # Dimensiones del circuito
    circuit_width = 6
    circuit_height = 3
    
    # Componentes del circuito
    source = cylinder(pos=vector(-circuit_width/2, 0, 0), 
                     axis=vector(0, circuit_height, 0),
                     radius=0.15, color=color.orange)
    source_label = label(pos=vector(-circuit_width/2 - 0.6, circuit_height/2, 0),
                        text="V(t)", height=12, box=False, color=color.black)
    
    resistor = box(pos=vector(0, circuit_height, 0),
                  size=vector(1.2, 0.25, 0.25),
                  color=color.red)
    resistor_label = label(pos=vector(0, circuit_height + 0.4, 0),
                          text=f"R={R:.1f}Ω", height=11, box=False, color=color.black)
    
    inductor = helix(pos=vector(circuit_width/2 - 0.8, circuit_height, 0),
                    axis=vector(0, -1.2, 0),
                    radius=0.25, coils=7, thickness=0.06,
                    color=color.blue)
    inductor_label = label(pos=vector(circuit_width/2 + 0.6, circuit_height - 0.6, 0),
                          text=f"L={L:.1f}H", height=11, box=False, color=color.black)
    
    cap1 = box(pos=vector(circuit_width/2, 0.8, 0),
              size=vector(0.25, 0.6, 0.5), color=color.green)
    cap2 = box(pos=vector(circuit_width/2, 0.4, 0),
              size=vector(0.25, 0.6, 0.5), color=color.green)
    capacitor_label = label(pos=vector(circuit_width/2 + 0.6, 0.6, 0),
                           text=f"C={C:.2f}F", height=11, box=False, color=color.black)
    
    # Cables
    wire1 = cylinder(pos=vector(-circuit_width/2, circuit_height, 0),
                    axis=vector(circuit_width/2 - 0.6, 0, 0),
                    radius=0.04, color=color.gray(0.3))
    wire2 = cylinder(pos=vector(circuit_width/2 - 0.6, circuit_height, 0),
                    axis=vector(0.6, 0, 0),
                    radius=0.04, color=color.gray(0.3))
    wire3 = cylinder(pos=vector(circuit_width/2, 0, 0),
                    axis=vector(-circuit_width, 0, 0),
                    radius=0.04, color=color.gray(0.3))
    
    # Múltiples partículas de carga (más visibles)
    num_charges = 8
    charges = []
    for i in range(num_charges):
        charge = sphere(radius=0.15, color=color.yellow,
                       make_trail=True, trail_type="points",
                       trail_radius=0.05, interval=3, retain=50)
        charges.append(charge)
    
    # Labels informativos
    label_Q = label(text=f"Carga: {Q0:.2f} C", pos=vector(0, -1.5, 0),
                   box=False, height=14, color=color.black)
    label_I = label(text=f"Corriente: {I0:.2f} A", pos=vector(0, -1.9, 0),
                   box=False, height=14, color=color.black)
    label_V = label(text=f"Voltaje: {V(0):.2f} V", pos=vector(0, -2.3, 0),
                   box=False, height=14, color=color.black)
    
    # Indicador de tipo de amortiguamiento
    label_tipo = label(text=f"Régimen: {tipo}", pos=vector(0, -2.7, 0),
                      box=True, height=12, color=color.black)
    if tipo == "sobreamortiguado":
        label_tipo.color = color.blue
    elif tipo == "subamortiguado":
        label_tipo.color = color.red
    else:
        label_tipo.color = color.green
    
    created_objects.extend([source, source_label, resistor, resistor_label,
                           inductor, inductor_label, cap1, cap2, capacitor_label,
                           wire1, wire2, wire3, label_Q, label_I, label_V, label_tipo])
    created_objects.extend(charges)

    # ============================
    # VARIABLES DE SIMULACIÓN
    # ============================
    t = 0
    dt = 0.005
    Q = Q0
    I = I0
    
    # Puntos del circuito
    circuit_path = []
    for y in np.linspace(0, circuit_height, 25):
        circuit_path.append(vector(-circuit_width/2, y, 0))
    for x in np.linspace(-circuit_width/2, circuit_width/2, 35):
        circuit_path.append(vector(x, circuit_height, 0))
    for y in np.linspace(circuit_height, 0, 25):
        circuit_path.append(vector(circuit_width/2, y, 0))
    for x in np.linspace(circuit_width/2, -circuit_width/2, 35):
        circuit_path.append(vector(x, 0, 0))
    
    # Índices iniciales para cada carga (distribuidas uniformemente)
    path_indices = [int(i * len(circuit_path) / num_charges) for i in range(num_charges)]
    for i, charge in enumerate(charges):
        charge.pos = circuit_path[path_indices[i]]
    
    contador_graficas = 0

    # ============================
    # BUCLE DE SIMULACIÓN
    # ============================
    running = True
    
    def stop_simulation(ev):
        nonlocal running
        running = False
    
    boton_detener = button(text="Detener simulación", bind=stop_simulation)
    created_objects.append(boton_detener)
    
    while running and t < 20:
        rate(200)

        # EDO: L·Q'' + R·Q' + Q/C = V(t)
        dI_dt = (V(t) - R*I - Q/C) / L

        # Actualizar corriente y carga
        I += dI_dt * dt
        Q += I * dt

        # Actualizar etiquetas
        label_Q.text = f"Carga: {Q:.3f} C"
        label_I.text = f"Corriente: {I:.3f} A"
        label_V.text = f"Voltaje: {V(t):.3f} V"
        
        salida_info.text = f"\nTiempo actual: {t:.2f} s\n"

        # Animar las cargas - velocidad proporcional a la corriente
        # Factor de escala mejorado para mejor visualización
        speed_factor = 15.0 * abs(I) + 0.5  # Mínimo 0.5 para que siempre se muevan un poco
        steps = max(1, int(speed_factor * dt * 100))
        
        for idx, charge in enumerate(charges):
            for _ in range(steps):
                if I > 0:
                    path_indices[idx] = (path_indices[idx] + 1) % len(circuit_path)
                else:
                    path_indices[idx] = (path_indices[idx] - 1) % len(circuit_path)
            
            charge.pos = circuit_path[path_indices[idx]]
            
            # Color según intensidad de corriente
            intensity = min(abs(I) / 1.5, 1.0)
            charge.color = vector(1, 1-intensity*0.7, 0.2)
            
            # Tamaño según intensidad
            charge.radius = 0.12 + intensity * 0.08

        # Agregar puntos a las gráficas
        contador_graficas += 1
        if contador_graficas % 3 == 0:
            curve_carga.plot(t, Q)
            curve_corriente.plot(t, I)

        t += dt

    boton_detener.delete()

# Botón para iniciar simulación
boton_iniciar = button(text="▶ Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")