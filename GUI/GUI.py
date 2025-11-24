import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re

class FactorWidget:
    """Representa un factor individual en un término"""
    def __init__(self, parent_frame, parent_termino, on_change_callback):
        self.parent_termino = parent_termino
        self.on_change = on_change_callback
        
        # Frame principal del factor
        self.frame = tk.Frame(parent_frame, relief=tk.RIDGE, borderwidth=1, bg="#f0f0f0")
        self.frame.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Tipo de factor
        self.tipo_var = tk.StringVar(value="numero")
        
        # Frame para selector de tipo
        tipo_frame = tk.Frame(self.frame, bg="#f0f0f0")
        tipo_frame.pack(padx=5, pady=2)
        
        tk.Label(tipo_frame, text="Tipo:", bg="#f0f0f0", font=("Arial", 8)).pack(side=tk.LEFT)
        self.tipo_combo = ttk.Combobox(tipo_frame, textvariable=self.tipo_var, 
                                       values=["numero", "variable", "funcion", "potencia"],
                                       state="readonly", width=10, font=("Arial", 8))
        self.tipo_combo.pack(side=tk.LEFT, padx=2)
        self.tipo_combo.bind("<<ComboboxSelected>>", self.on_tipo_changed)
        
        # Frame para contenido específico del tipo
        self.contenido_frame = tk.Frame(self.frame, bg="#f0f0f0")
        self.contenido_frame.pack(padx=5, pady=2)
        
        # Botón eliminar
        btn_frame = tk.Frame(self.frame, bg="#f0f0f0")
        btn_frame.pack(padx=5, pady=2)
        tk.Button(btn_frame, text="❌", command=self.eliminar, 
                 bg="#ff6b6b", fg="white", font=("Arial", 8)).pack()
        
        # Inicializar contenido
        self.widgets_especificos = {}
        self.crear_contenido_numero()
    
    def on_tipo_changed(self, event=None):
        """Cambio en el tipo de factor"""
        # Limpiar contenido anterior
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        self.widgets_especificos.clear()
        
        tipo = self.tipo_var.get()
        if tipo == "numero":
            self.crear_contenido_numero()
        elif tipo == "variable":
            self.crear_contenido_variable()
        elif tipo == "funcion":
            self.crear_contenido_funcion()
        elif tipo == "potencia":
            self.crear_contenido_potencia()
        
        self.on_change()
    
    def crear_contenido_numero(self):
        """Input para número"""
        # Función de validación
        def validar_numero(char):
            return char in '0123456789.eπ'
        
        vcmd = (self.contenido_frame.register(validar_numero), '%S')
        
        self.widgets_especificos['entry'] = tk.Entry(self.contenido_frame, width=8, 
                                                      font=("Arial", 10),
                                                      validate='key',
                                                      validatecommand=vcmd)
        self.widgets_especificos['entry'].pack()
        self.widgets_especificos['entry'].insert(0, "0")
        self.widgets_especificos['entry'].bind("<KeyRelease>", lambda e: self.on_change())
        
        # Botones para constantes
        const_frame = tk.Frame(self.contenido_frame, bg="#f0f0f0")
        const_frame.pack()
        tk.Button(const_frame, text="π", command=lambda: self.insertar_constante("π"),
                 font=("Arial", 8), width=3).pack(side=tk.LEFT, padx=1)
        tk.Button(const_frame, text="e", command=lambda: self.insertar_constante("e"),
                 font=("Arial", 8), width=3).pack(side=tk.LEFT, padx=1)
    
    def insertar_constante(self, const):
        entry = self.widgets_especificos.get('entry')
        if entry:
            entry.delete(0, tk.END)
            entry.insert(0, const)
            self.on_change()
    
    def crear_contenido_variable(self):
        """Selector para x o y con derivadas"""
        # Solo permitir x en lado derecho, todo en lado izquierdo
        permitir_y = self.parent_termino.parent_expresion.permitir_y
        
        if permitir_y:
            valores = ["x", "y", "y'", "y''", "y'''", "y''''"]
        else:
            valores = ["x"]
        
        var_var = tk.StringVar(value="x")
        self.widgets_especificos['var'] = var_var
        
        combo = ttk.Combobox(self.contenido_frame, textvariable=var_var,
                            values=valores, state="readonly", width=8, font=("Arial", 10))
        combo.pack()
        combo.bind("<<ComboboxSelected>>", lambda e: self.on_change())
    
    def crear_contenido_funcion(self):
        """Selector de función + expresión interna"""
        # Selector de función
        func_var = tk.StringVar(value="S")
        self.widgets_especificos['func'] = func_var
        
        funciones = {
            "sen": "S", "cos": "C", "tan": "T", 
            "ln": "L", "√": "R", "|x|": "A",
            "sec": "s", "csc": "c", "cot": "t",
            "arc": "I", "e^": "E", "1/": "/"
        }
        
        func_frame = tk.Frame(self.contenido_frame, bg="#f0f0f0")
        func_frame.pack()
        
        tk.Label(func_frame, text="Función:", bg="#f0f0f0", font=("Arial", 8)).pack(side=tk.LEFT)
        func_combo = ttk.Combobox(func_frame, textvariable=func_var,
                                 values=list(funciones.values()), 
                                 state="readonly", width=6, font=("Arial", 9))
        func_combo.pack(side=tk.LEFT)
        func_combo.bind("<<ComboboxSelected>>", lambda e: self.on_change())
        
        # Mapeo de nombres amigables
        self.widgets_especificos['func_map'] = funciones
        
        # Expresión interna (recursiva)
        tk.Label(self.contenido_frame, text="Argumento:", bg="#f0f0f0", 
                font=("Arial", 8, "bold")).pack()
        
        # Crear una mini-expresión dentro
        from_function = True  # Flag para expresión anidada
        self.widgets_especificos['expresion'] = ExpresionWidget(
            self.contenido_frame, 
            permitir_y=self.parent_termino.parent_expresion.permitir_y,
            on_change_callback=self.on_change,
            compact=True  # Modo compacto para funciones
        )
    
    def crear_contenido_potencia(self):
        """Potencia: (base)^(exponente)"""
        tk.Label(self.contenido_frame, text="(  )^(  )", bg="#f0f0f0",
                font=("Arial", 10, "bold")).pack()
        
        # Frame para base
        base_frame = tk.LabelFrame(self.contenido_frame, text="Base", 
                                   bg="#f0f0f0", font=("Arial", 8))
        base_frame.pack(padx=2, pady=2, fill=tk.BOTH)
        self.widgets_especificos['base'] = FactorWidget(base_frame, self.parent_termino, self.on_change)
        
        # Frame para exponente
        exp_frame = tk.LabelFrame(self.contenido_frame, text="Exponente",
                                  bg="#f0f0f0", font=("Arial", 8))
        exp_frame.pack(padx=2, pady=2, fill=tk.BOTH)
        self.widgets_especificos['exponente'] = FactorWidget(exp_frame, self.parent_termino, self.on_change)
    
    def eliminar(self):
        """Eliminar este factor"""
        self.parent_termino.eliminar_factor(self)
    
    def to_string(self):
        """Generar string del factor"""
        tipo = self.tipo_var.get()
        
        if tipo == "numero":
            valor = self.widgets_especificos['entry'].get().strip()
            return valor if valor else "0"
        
        elif tipo == "variable":
            return self.widgets_especificos['var'].get()
        
        elif tipo == "funcion":
            func_letra = self.widgets_especificos['func'].get()
            expr = self.widgets_especificos['expresion'].to_string()
            return f"{func_letra}({expr})"
        
        elif tipo == "potencia":
            base = self.widgets_especificos['base'].to_string()
            exp = self.widgets_especificos['exponente'].to_string()
            return f"({base})^({exp})"
        
        return ""


class TerminoWidget:
    """Representa un término completo"""
    def __init__(self, parent_frame, parent_expresion, derivada_orden, on_change_callback):
        self.parent_expresion = parent_expresion
        self.on_change = on_change_callback
        self.derivada_orden = derivada_orden
        self.factores = []
        
        # Frame principal
        self.frame = tk.Frame(parent_frame, relief=tk.SUNKEN, borderwidth=2, bg="#e8f4f8")
        self.frame.pack(fill=tk.X, padx=5, pady=3)
        
        # Header con checkbox negativo y label de derivada
        header_frame = tk.Frame(self.frame, bg="#e8f4f8")
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.negativo_var = tk.BooleanVar(value=False)
        tk.Checkbutton(header_frame, text="Negativo (-)", variable=self.negativo_var,
                      command=self.on_change, bg="#e8f4f8", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Mostrar derivada
        derivada_texto = self.get_derivada_texto()
        tk.Label(header_frame, text=f"Término de {derivada_texto}", 
                font=("Arial", 10, "bold"), bg="#e8f4f8", fg="#0066cc").pack(side=tk.LEFT, padx=10)
        
        # Botón eliminar término
        tk.Button(header_frame, text="🗑️ Eliminar término", command=self.eliminar,
                 bg="#ff4444", fg="white", font=("Arial", 8)).pack(side=tk.RIGHT)
        
        # Frame para factores
        self.factores_frame = tk.Frame(self.frame, bg="#e8f4f8")
        self.factores_frame.pack(fill=tk.BOTH, padx=5, pady=2)
        
        # Agregar primer factor
        self.agregar_factor()
        
        # Botón agregar factor
        tk.Button(self.frame, text="✚ Agregar factor (multiplicar)", 
                 command=self.agregar_factor, bg="#4CAF50", fg="white",
                 font=("Arial", 9)).pack(pady=3)
        
        # Mostrar derivada al final SOLO si permite y
        if self.parent_expresion.permitir_y:
            tk.Label(self.frame, text=f"× {derivada_texto}", 
                    font=("Arial", 11, "bold"), bg="#e8f4f8", fg="#cc0000").pack(pady=2)
    
    def get_derivada_texto(self):
        """Obtener texto de la derivada según orden"""
        if self.derivada_orden == 0:
            return "y"
        else:
            return "y" + "'" * self.derivada_orden
    
    def agregar_factor(self):
        """Agregar nuevo factor al término"""
        factor = FactorWidget(self.factores_frame, self, self.on_change)
        self.factores.append(factor)
        self.on_change()
    
    def eliminar_factor(self, factor):
        """Eliminar un factor específico"""
        if len(self.factores) > 1:
            self.factores.remove(factor)
            factor.frame.destroy()
            self.on_change()
        else:
            messagebox.showwarning("Advertencia", "Un término debe tener al menos un factor")
    
    def eliminar(self):
        """Eliminar este término completo"""
        self.parent_expresion.eliminar_termino(self)
    
    def to_string(self):
        """Generar string del término"""
        # Unir factores con *
        factores_str = "*".join(f.to_string() for f in self.factores)
        
        # Agregar derivada SOLO si permite y
        if self.parent_expresion.permitir_y:
            derivada_str = self.get_derivada_texto()
            if factores_str and factores_str != "0":
                resultado = f"{factores_str}*{derivada_str}"
            else:
                return ""
        else:
            # Lado derecho: sin derivadas
            resultado = factores_str if factores_str else "0"
        
        # Agregar signo negativo si aplica
        if self.negativo_var.get():
            resultado = "-" + resultado
        
        return resultado


class ExpresionWidget:
    """Representa una expresión completa (suma de términos)"""
    def __init__(self, parent_frame, permitir_y=True, on_change_callback=None, compact=False):
        self.permitir_y = permitir_y
        self.on_change = on_change_callback if on_change_callback else lambda: None
        self.terminos = []
        self.compact = compact
        
        # Frame principal
        self.frame = tk.Frame(parent_frame, bg="#ffffff")
        if compact:
            self.frame.pack(fill=tk.BOTH, padx=2, pady=2)
        else:
            self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botón agregar término (ARRIBA DEL CANVAS)
        if not compact:
            tk.Button(self.frame, text="➕ Agregar término (sumar)", 
                     command=lambda: self.agregar_termino(), 
                     bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=5, fill=tk.X)
        
        # Scrollable frame para términos
        canvas = tk.Canvas(self.frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.terminos_frame = tk.Frame(canvas, bg="#ffffff")
        
        self.terminos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.terminos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not compact:
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            canvas.pack(fill="both", expand=True)
        
        # Agregar primer término
        if permitir_y:
            # Lado izquierdo: empezar con y (orden 0)
            self.agregar_termino(orden_inicial=0 if not compact else 0)
        else:
            # Lado derecho: solo constantes/x
            self.agregar_termino(orden_inicial=None)
    
    def agregar_termino(self, orden_inicial=None):
        """Agregar nuevo término"""
        if orden_inicial is None:
            # Calcular siguiente orden de derivada
            if self.permitir_y and self.terminos:
                ultimo_orden = self.terminos[-1].derivada_orden
                nuevo_orden = ultimo_orden + 1  # Incrementar (y, y', y'', ...)
            elif self.permitir_y:
                nuevo_orden = 0  # Empezar con y (sin derivadas)
            else:
                nuevo_orden = -1  # Lado derecho, sin derivadas
        else:
            nuevo_orden = orden_inicial
        
        termino = TerminoWidget(self.terminos_frame, self, nuevo_orden, self.on_change)
        self.terminos.append(termino)
        self.on_change()
    
    def eliminar_termino(self, termino):
        """Eliminar término específico"""
        if len(self.terminos) > 1:
            self.terminos.remove(termino)
            termino.frame.destroy()
            self.on_change()
        else:
            messagebox.showwarning("Advertencia", "Una expresión debe tener al menos un término")
    
    def to_string(self):
        """Generar string de la expresión"""
        terminos_str = []
        for termino in self.terminos:
            t_str = termino.to_string()
            if t_str:  # Ignorar términos vacíos
                terminos_str.append(t_str)
        
        if not terminos_str:
            return "0"
        
        # Unir con +, manejando signos negativos
        resultado = terminos_str[0]
        for t in terminos_str[1:]:
            if t.startswith("-"):
                resultado += "+" + t
            else:
                resultado += "+" + t
        
        return resultado


class EDitorGUI:
    """Interfaz principal del editor de ecuaciones diferenciales"""
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Ecuaciones Diferenciales")
        self.root.geometry("1200x800")
        
        # Frame principal con división VERTICAL
        main_paned = tk.PanedWindow(root, orient=tk.VERTICAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior: Editor
        editor_frame = tk.Frame(main_paned, bg="#f5f5f5")
        main_paned.add(editor_frame, height=500)
        
        # Título
        tk.Label(editor_frame, text="📝 Editor de Ecuaciones Diferenciales",
                font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)
        
        # Frame para ecuación
        ecuacion_frame = tk.Frame(editor_frame, bg="#f5f5f5")
        ecuacion_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Lado izquierdo
        izq_label_frame = tk.LabelFrame(ecuacion_frame, text="📌 Lado Izquierdo (con y y derivadas)",
                                       font=("Arial", 12, "bold"), bg="#e3f2fd", fg="#1565c0")
        izq_label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.expresion_izq = ExpresionWidget(izq_label_frame, permitir_y=True, 
                                     on_change_callback=None)  # Sin callback por ahora
        
        # Símbolo igual
        tk.Label(ecuacion_frame, text="=", font=("Arial", 36, "bold"),
                bg="#f5f5f5", fg="#d32f2f").pack(side=tk.LEFT, padx=10)
        
        # Lado derecho
        der_label_frame = tk.LabelFrame(ecuacion_frame, text="📌 Lado Derecho (solo x, números, funciones)",
                                       font=("Arial", 12, "bold"), bg="#fff3e0", fg="#e65100")
        der_label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.expresion_der = ExpresionWidget(der_label_frame, permitir_y=False,
                                     on_change_callback=None)  # Sin callback por ahora
        
        # Ahora sí asignar los callbacks
        self.expresion_izq.on_change = self.actualizar_preview
        self.expresion_der.on_change = self.actualizar_preview

        # Panel derecho: Preview y validación
        preview_frame = tk.Frame(main_paned, bg="#ffffff")
        main_paned.add(preview_frame, width=400)
        
        tk.Label(preview_frame, text="🔍 Vista Previa y Validación",
                font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        # Preview del string
        tk.Label(preview_frame, text="String generado:", 
                font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=10)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=8, 
                                                      font=("Courier", 11), 
                                                      bg="#f0f0f0", wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Botón validar
        tk.Button(preview_frame, text="✓ Validar Ecuación Diferencial",
                 command=self.validar_ed, bg="#4CAF50", fg="white",
                 font=("Arial", 12, "bold"), height=2).pack(pady=10, padx=10, fill=tk.X)
        
        # Resultado de validación
        tk.Label(preview_frame, text="Resultado:", 
                font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=10)
        
        self.resultado_text = scrolledtext.ScrolledText(preview_frame, height=10,
                                                       font=("Arial", 10),
                                                       bg="#fffef0", wrap=tk.WORD)
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Instrucciones
        instrucciones = """
📖 INSTRUCCIONES:
• Lado izquierdo: contiene términos con y y sus derivadas
• Lado derecho: solo puede tener x, números y funciones
• Cada término se multiplica automáticamente por una derivada de y
• Use "Agregar factor" para multiplicar dentro de un término
• Use "Agregar término" para sumar términos
• Marque "Negativo" para términos con signo menos
        """
        tk.Label(preview_frame, text=instrucciones, font=("Arial", 8),
                bg="#ffffff", justify=tk.LEFT, anchor="w").pack(padx=10, pady=5)
        
        # Actualizar preview inicial
        self.actualizar_preview()
    
    def actualizar_preview(self):
        """Actualizar vista previa del string"""
        izq_str = self.expresion_izq.to_string()
        der_str = self.expresion_der.to_string()
        
        ecuacion = f"{izq_str}={der_str}"
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, ecuacion)
    
    def validar_ed(self):
        """Validar la ecuación con la MT"""
        ecuacion = self.preview_text.get(1.0, tk.END).strip()
        
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, f"Validando: {ecuacion}\n\n")
        
        # Aquí integrarías con tu MT
        # Por ahora, simulación simple
        tiene_y = 'y' in ecuacion
        tiene_derivada = "'" in ecuacion
        tiene_igual = '=' in ecuacion
        
        if tiene_y and tiene_derivada and tiene_igual:
            self.resultado_text.insert(tk.END, "✅ ACEPTA\n\n", "success")
            self.resultado_text.insert(tk.END, "Esta cadena tiene la estructura de una ecuación diferencial válida.\n")
            self.resultado_text.tag_config("success", foreground="green", font=("Arial", 12, "bold"))
        else:
            self.resultado_text.insert(tk.END, "❌ RECHAZA\n\n", "error")
            self.resultado_text.insert(tk.END, "Esta cadena NO es una ecuación diferencial válida.\n\n")
            if not tiene_y:
                self.resultado_text.insert(tk.END, "• Falta la variable dependiente 'y'\n")
            if not tiene_derivada:
                self.resultado_text.insert(tk.END, "• No hay derivadas (falta al menos un ')\n")
            if not tiene_igual:
                self.resultado_text.insert(tk.END, "• Falta el símbolo de igualdad '='\n")
            self.resultado_text.tag_config("error", foreground="red", font=("Arial", 12, "bold"))
        
        # Aquí llamarías a tu MT real:
        # resultado = MT_Validador_ED.accepts_input(ecuacion)


if __name__ == "__main__":
    root = tk.Tk()
    app = EDitorGUI(root)
    root.mainloop()