
#pip install vpython
from vpython import *
import numpy as np

# -------------------------------------------------
# ESCENA BASE
# -------------------------------------------------
scene = canvas(title="Sistema Masa-Resorte-Amortiguador",
               width=1200, height=700, background=color.white)

# Gráfica
graph_window = graph(title="Posición vs Tiempo", 
                     xtitle="Tiempo (s)", ytitle="Posición (m)",
                     width=600, height=400, align="right")
pos_curve = gcurve(color=color.blue, width=2, label="x(t)")

# lista para llevar los objetos creados en cada ejecución
created_objects = []

wtext(text="\n--- Parámetros del Sistema ---\n")

# Sliders con valores dinámicos
# --- Masa ---
texto_m = wtext(text="Masa (m): 1.00 kg\n")
def actualizar_m(s):
    texto_m.text = f"Masa (m): {s.value:.2f} kg\n"
slider_m = slider(min=0.1, max=5.0, value=1.0, step=0.1, bind=actualizar_m)

# --- Constante del resorte ---
texto_k = wtext(text="\nConstante del resorte (k): 4.00 N/m\n")
def actualizar_k(s):
    texto_k.text = f"\nConstante del resorte (k): {s.value:.2f} N/m\n"
slider_k = slider(min=0.5, max=20.0, value=4.0, step=0.5, bind=actualizar_k)

# --- Coeficiente de amortiguamiento ---
texto_b = wtext(text="\nCoeficiente de amortiguamiento (b): 0.30\n")
def actualizar_b(s):
    texto_b.text = f"\nCoeficiente de amortiguamiento (b): {s.value:.2f}\n"
slider_b = slider(min=0.0, max=2.0, value=0.3, step=0.05, bind=actualizar_b)

# --- Posición inicial ---
texto_x0 = wtext(text="\nPosición inicial (x₀): 1.00 m\n")
def actualizar_x0(s):
    texto_x0.text = f"\nPosición inicial (x₀): {s.value:.2f} m\n"
slider_x0 = slider(min=-2.0, max=2.0, value=1.0, step=0.1, bind=actualizar_x0)

# --- Velocidad inicial ---
texto_v0 = wtext(text="\nVelocidad inicial (v₀): 0.00 m/s\n")
def actualizar_v0(s):
    texto_v0.text = f"\nVelocidad inicial (v₀): {s.value:.2f} m/s\n"
slider_v0 = slider(min=-5.0, max=5.0, value=0.0, step=0.1, bind=actualizar_v0)

# --- Amplitud de fuerza externa ---
texto_A = wtext(text="\nAmplitud fuerza externa (A): 1.00\n")
def actualizar_A(s):
    texto_A.text = f"\nAmplitud fuerza externa (A): {s.value:.2f}\n"
slider_A = slider(min=0.0, max=3.0, value=1.0, step=0.1, bind=actualizar_A)

# --- Frecuencia de fuerza externa ---
texto_w = wtext(text="\nFrecuencia fuerza externa (ω): 1.50 rad/s\n")
def actualizar_w(s):
    texto_w.text = f"\nFrecuencia fuerza externa (ω): {s.value:.2f} rad/s\n"
slider_w = slider(min=0.0, max=5.0, value=1.5, step=0.1, bind=actualizar_w)

wtext(text="\n")

# Mostrar ecuación diferencial general
ecuacion_text = wtext(text="\nEcuación general: m·x'' + b·x' + k·x = A·cos(ω·t)\n")

# Ecuación con parámetros sustituidos
ecuacion_params = wtext(text="\nEcuación con parámetros: (calculando...)\n")

# Análisis de la ecuación característica
analisis_ec = wtext(text="\nAnálisis de la ecuación característica:\n")

# Salidas numéricas
salida_info = wtext(text="\nTiempo actual: 0.00 s\n")

# -------------------------------------------------
# FUNCIONES DE ANÁLISIS
# -------------------------------------------------

def analizar_ecuacion(m, b, k, A, w):
    """
    Analiza la ecuación diferencial y determina el tipo de solución
    Ecuación homogénea: m·x'' + b·x' + k·x = 0
    Ecuación característica: m·r² + b·r + k = 0
    """
    # Ecuación con parámetros
    if A == 0:
        ec_texto = f"({m:.2f})·x'' + ({b:.2f})·x' + ({k:.2f})·x = 0\n"
    else:
        ec_texto = f"({m:.2f})·x'' + ({b:.2f})·x' + ({k:.2f})·x = ({A:.2f})·cos(({w:.2f})·t)\n"
    
    # Ecuación característica: m·r² + b·r + k = 0
    # r = (-b ± sqrt(b² - 4mk)) / (2m)
    discriminante = b**2 - 4*m*k
    
    analisis = "\n--- Análisis de la Ecuación Característica ---\n"
    analisis += f"Ecuación característica: ({m:.2f})·r² + ({b:.2f})·r + ({k:.2f}) = 0\n"
    analisis += f"Discriminante Δ = b² - 4mk = {discriminante:.4f}\n\n"
    
    if discriminante > 0:
        # Dos raíces reales distintas
        r1 = (-b + np.sqrt(discriminante)) / (2*m)
        r2 = (-b - np.sqrt(discriminante)) / (2*m)
        analisis += "🔹 Caso: Sobreamortiguado (dos raíces reales distintas)\n"
        analisis += f"   r₁ = {r1:.4f}\n"
        analisis += f"   r₂ = {r2:.4f}\n"
        analisis += f"   Solución homogénea: x_h(t) = C₁·e^({r1:.4f}·t) + C₂·e^({r2:.4f}·t)\n"
    elif discriminante == 0:
        # Raíz real doble
        r = -b / (2*m)
        analisis += "🔹 Caso: Críticamente amortiguado (raíz real doble)\n"
        analisis += f"   r = {r:.4f}\n"
        analisis += f"   Solución homogénea: x_h(t) = (C₁ + C₂·t)·e^({r:.4f}·t)\n"
    else:
        # Raíces complejas conjugadas
        parte_real = -b / (2*m)
        parte_imag = np.sqrt(-discriminante) / (2*m)
        analisis += "🔹 Caso: Subamortiguado (raíces complejas conjugadas)\n"
        analisis += f"   r = {parte_real:.4f} ± {parte_imag:.4f}i\n"
        analisis += f"   Solución homogénea: x_h(t) = e^({parte_real:.4f}·t)·[C₁·cos({parte_imag:.4f}·t) + C₂·sin({parte_imag:.4f}·t)]\n"
        
        # Frecuencia natural y factor de amortiguamiento
        w_n = np.sqrt(k/m)
        zeta = b / (2*np.sqrt(m*k))
        analisis += f"\n   Frecuencia natural: ω_n = {w_n:.4f} rad/s\n"
        analisis += f"   Factor de amortiguamiento: ζ = {zeta:.4f}\n"
    
    if A > 0:
        analisis += f"\n🔹 Solución particular (forzamiento): x_p(t) depende de cos({w:.2f}·t)\n"
        analisis += "   Solución completa: x(t) = x_h(t) + x_p(t)\n"
    
    return ec_texto, analisis

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
    global created_objects, pos_curve

    # Leer parámetros desde sliders
    m = float(slider_m.value)
    k = float(slider_k.value)
    b = float(slider_b.value)
    x0 = float(slider_x0.value)
    v0 = float(slider_v0.value)
    A = float(slider_A.value)
    w = float(slider_w.value)

    # Analizar ecuación
    ec_texto, analisis = analizar_ecuacion(m, b, k, A, w)
    ecuacion_params.text = f"\nEcuación con parámetros:\n{ec_texto}"
    analisis_ec.text = analisis

    # Limpiar gráfica anterior
    pos_curve.delete()
    pos_curve = gcurve(color=color.blue, width=2, label="x(t)")

    # Ocultar objetos previos
    hide_previous_objects()

    # Función de fuerza externa
    def F(t):
        return A * np.cos(w * t)

    # ============================
    # CONFIGURACIÓN DE ESCENA
    # ============================
    
    # Fixed wall
    wall = box(pos=vector(-3, 0, 0), size=vector(0.2, 1, 1), color=color.gray(0.5))
    
    # Mass
    mass = box(pos=vector(x0, 0, 0), size=vector(0.4, 0.4, 0.4), 
               color=color.red, make_trail=True, trail_type="points", 
               trail_radius=0.02, interval=10, retain=200)
    
    # Spring (initial)
    spring = helix(pos=wall.pos + vector(0.1, 0, 0),
                   axis=mass.pos - (wall.pos + vector(0.1, 0, 0)),
                   radius=0.15, coils=12, thickness=0.03,
                   color=color.blue)
    
    # Equilibrium marker
    eq_marker = cylinder(pos=vector(0, -0.5, 0), axis=vector(0, 1.0, 0),
                         radius=0.02, color=color.green)
    
    # Labels informativos
    label_pos = label(text=f"Posición: {x0:.2f} m", pos=vector(0, 1.5, 0), 
                      box=False, height=16)
    label_vel = label(text=f"Velocidad: {v0:.2f} m/s", pos=vector(0, 1.2, 0), 
                      box=False, height=16)
    label_energia = label(text=f"Energía: calculando...", pos=vector(0, 0.9, 0),
                         box=False, height=16)
    
    created_objects.extend([wall, mass, spring, eq_marker, label_pos, label_vel, label_energia])

    # ============================
    # VARIABLES DE SIMULACIÓN
    # ============================
    t = 0
    dt = 0.01
    x = x0
    v = v0

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
    
    while running:
        rate(200)  # control animation speed

        # ODE: m x'' + b x' + k x = F(t)
        a = (F(t) - b*v - k*x) / m

        # Update velocity & position
        v += a * dt
        x += v * dt

        # Update mass position
        mass.pos = vector(x, 0, 0)

        # Update spring axis
        spring.axis = mass.pos - spring.pos

        # Calcular energía total (aproximada)
        E_cinetica = 0.5 * m * v**2
        E_potencial = 0.5 * k * x**2
        E_total = E_cinetica + E_potencial

        # Update labels
        label_pos.text = f"Posición: {x:.2f} m"
        label_vel.text = f"Velocidad: {v:.2f} m/s"
        label_energia.text = f"Energía: {E_total:.2f} J (Ec={E_cinetica:.2f}, Ep={E_potencial:.2f})"
        
        # Update time display
        salida_info.text = f"\nTiempo actual: {t:.2f} s\n"

        # Agregar punto a la gráfica (cada cierto tiempo para no saturar)
        if int(t/dt) % 2 == 0:  # cada 2 iteraciones
            pos_curve.plot(t, x)

        t += dt
        
        # Detener después de un tiempo razonable
        if t > 20:
            running = False

    # Limpiar botón de detener
    boton_detener.delete()

# Botón para iniciar simulación
boton_iniciar = button(text="Iniciar simulación", bind=simular)

# Evita que el script se cierre
input("Presiona ENTER para salir...")