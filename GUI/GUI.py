import tkinter as tk
from tkinter import ttk, messagebox

# --- CONSTANTES ---
FONT_MAIN = ("Consolas", 10)
BG_COLOR = "#f0f0f0"
PAD = 5

class FactorBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, relief="solid", borderwidth=1, *args, **kwargs)
        self.allow_y = allow_y
        
        # Header del Factor
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=2, pady=2)
        
        tk.Label(top_frame, text="Factor:", font=("Arial", 8, "bold")).pack(side="left")
        
        # Selector de Tipo
        options = ["Número", "Variable X", "Función"]
        if self.allow_y:
            options.append("Variable Y")
            
        self.type_var = tk.StringVar(value="Número")
        self.combo = ttk.Combobox(top_frame, textvariable=self.type_var, values=options, state="readonly", width=10)
        self.combo.pack(side="left", padx=5)
        self.combo.bind("<<ComboboxSelected>>", self.update_content)
        
        # Botón eliminar factor
        btn_del = tk.Button(top_frame, text="X", bg="#ffcccc", command=self.destroy_self, font=("Arial", 7))
        btn_del.pack(side="right")

        # Contenido dinámico
        self.content_frame = tk.Frame(self, padx=5, pady=5)
        self.content_frame.pack(side="top", fill="x")
        
        # Inicializar vista
        self.current_widget = None
        self.update_content()

    def destroy_self(self):
        self.destroy()

    def update_content(self, event=None):
        # Limpiar frame anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        selection = self.type_var.get()
        
        if selection == "Número":
            self.current_widget = tk.Entry(self.content_frame, width=8)
            self.current_widget.insert(0, "1")
            self.current_widget.pack()
            
        elif selection == "Variable X":
            self.current_widget = tk.Label(self.content_frame, text="x", font=("Times", 14, "italic"))
            self.current_widget.pack()
            
        elif selection == "Variable Y":
            frame = tk.Frame(self.content_frame)
            frame.pack()
            tk.Label(frame, text="y", font=("Times", 14, "italic")).pack(side="left")
            # Selector de derivadas
            tk.Label(frame, text="Derivada:").pack(side="left", padx=5)
            self.deriv_spin = tk.Spinbox(frame, from_=0, to=10, width=3) # 0 = y, 1 = y', etc.
            self.deriv_spin.pack(side="left")
            self.current_widget = "y_complex" # Marcador lógico
            
        elif selection == "Función":
            frame = tk.Frame(self.content_frame)
            frame.pack()
            
            # Selector de función
            funcs = ["sen", "cos", "tan", "ln", "exp", "sqrt"]
            self.func_selector = ttk.Combobox(frame, values=funcs, state="readonly", width=5)
            self.func_selector.set("sen")
            self.func_selector.pack(side="left")
            
            tk.Label(frame, text="(").pack(side="left")
            
            # RECURSIVIDAD: Aquí metemos una Expresión completa dentro de la función
            # NOTA: Dentro de una función, ¿permitimos 'y'? 
            # Si quieres ecuaciones lineales estrictas, NO permitas 'y' dentro de funciones.
            # Si quieres permitir No-Lineales, pon allow_y=True. 
            # Según tu descripción, "Linealidad" la revisa la MTM, así que dejemos True o self.allow_y
            self.inner_expr = ExpressionBlock(frame, allow_y=self.allow_y) 
            self.inner_expr.pack(side="left", padx=2)
            
            tk.Label(frame, text=")").pack(side="left")
            self.current_widget = "func_complex"

    def get_string(self):
        sel = self.type_var.get()
        if sel == "Número":
            return self.current_widget.get().strip()
        elif sel == "Variable X":
            return "x"
        elif sel == "Variable Y":
            derivs = int(self.deriv_spin.get())
            return "y" + ("'" * derivs)
        elif sel == "Función":
            func_name = self.func_selector.get()
            # Mapeo de nombres si tu gramática usa S, C, etc.
            # Por ahora uso nombres completos. Ajustar a tu gramática:
            grammar_map = {"sen": "sen", "cos": "cos", "tan": "tan", "ln": "ln", "exp": "exp", "sqrt": "sqrt"}
            inner = self.inner_expr.get_string()
            return f"{grammar_map[func_name]}({inner})"
        return ""

class TermBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, relief="groove", borderwidth=2, bg="#e0e0e0", *args, **kwargs)
        self.allow_y = allow_y
        
        # Control del Término
        ctrl_frame = tk.Frame(self, bg="#d0d0d0")
        ctrl_frame.pack(side="top", fill="x")
        
        # Signo
        self.sign_var = tk.StringVar(value="+")
        tk.Button(ctrl_frame, textvariable=self.sign_var, command=self.toggle_sign, width=3).pack(side="left")
        
        tk.Label(ctrl_frame, text="Término", bg="#d0d0d0").pack(side="left", padx=5)
        
        # Botón agregar factor
        tk.Button(ctrl_frame, text="Agrega Factor (*)", command=self.add_factor, font=("Arial", 8)).pack(side="left", padx=5)
        
        # Botón eliminar término completo
        tk.Button(ctrl_frame, text="Eliminar Término", bg="#ffaaaa", command=self.destroy, font=("Arial", 8)).pack(side="right")
        
        # Area de Factores
        self.factors_area = tk.Frame(self)
        self.factors_area.pack(side="top", fill="x", padx=5, pady=5)
        
        self.factors = []
        # Agregar un factor por defecto
        self.add_factor()

    def toggle_sign(self):
        self.sign_var.set("-" if self.sign_var.get() == "+" else "+")

    def add_factor(self):
        # Separador visual si no es el primero
        if self.factors:
            tk.Label(self.factors_area, text="*", font=("Arial", 12, "bold")).pack(side="left")
            
        f = FactorBlock(self.factors_area, allow_y=self.allow_y)
        f.pack(side="left", padx=2)
        self.factors.append(f)

    def get_string(self):
        sign = "-" if self.sign_var.get() == "-" else "" # Si es +, no ponemos nada o ponemos + segun gramatica
        # Tu gramatica: <término> => <factor> | -<factor>
        # Vamos a construir: factor * factor * factor
        parts = [f.get_string() for f in self.factors if f.winfo_exists()] # Check si no fue borrado manualmente
        term_str = "*".join(parts)
        return f"{sign}{term_str}"

class ExpressionBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.allow_y = allow_y
        self.terms = []
        
        # Botón para añadir término
        self.btn_add = tk.Button(self, text="+ Añadir Término", command=self.add_term, bg="#ccffcc")
        self.btn_add.pack(side="bottom", fill="x", pady=2)
        
        # Area de términos
        self.terms_area = tk.Frame(self)
        self.terms_area.pack(side="top", fill="both", expand=True)
        
        # Primer término
        self.add_term()

    def add_term(self):
        # Si ya hay términos, visualmente poner un "+" entre ellos seria ideal, 
        # pero el TermBlock ya maneja su propio signo +/-.
        t = TermBlock(self.terms_area, allow_y=self.allow_y)
        t.pack(side="left", padx=5, pady=5, anchor="n")
        self.terms.append(t)

    def get_string(self):
        # Filtrar términos eliminados
        valid_terms = [t for t in self.terms if t.winfo_exists()]
        if not valid_terms:
            return "0"
            
        result = ""
        for i, term in enumerate(valid_terms):
            s = term.get_string()
            # Logica de signos para concatenar
            # Si el termino devuelve "-5*x", y no es el primero, queda "... -5*x"
            # Si el termino devuelve "5*x" (positivo implícito), necesitamos poner el + si no es el primero
            if i > 0 and not s.startswith("-"):
                result += "+" + s
            else:
                result += s
        return result

class DifferentialEquationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Constructor de Ecuaciones Diferenciales para MTM")
        self.root.geometry("1100x600")
        
        # --- TITULO ---
        lbl_title = tk.Label(root, text="Ingrese la Ecuación Diferencial (Estructura de Bloques)", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=10)
        
        # --- AREA PRINCIPAL (Scrollable si se necesita, simplificado aquí con Frames) ---
        main_container = tk.Frame(root)
        main_container.pack(fill="both", expand=True, padx=10)
        
        # LADO IZQUIERDO (Con Y permitida)
        lhs_frame = tk.LabelFrame(main_container, text="Lado Izquierdo (Expresión)", font=FONT_MAIN, bg="#eef")
        lhs_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.lhs_editor = ExpressionBlock(lhs_frame, allow_y=True)
        self.lhs_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # IGUALDAD
        eq_label = tk.Label(main_container, text="=", font=("Arial", 24, "bold"))
        eq_label.pack(side="left", padx=5)
        
        # LADO DERECHO (Sin Y permitida)
        rhs_frame = tk.LabelFrame(main_container, text="Lado Derecho (Solo f(x) o constantes)", font=FONT_MAIN, bg="#fee")
        rhs_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.rhs_editor = ExpressionBlock(rhs_frame, allow_y=False)
        self.rhs_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- AREA INFERIOR ---
        bottom_panel = tk.Frame(root, pady=10, bg="gray")
        bottom_panel.pack(fill="x", side="bottom")
        
        btn_generate = tk.Button(bottom_panel, text="ANALIZAR (Generar String)", font=("Arial", 12, "bold"), 
                                 bg="orange", command=self.generate_string)
        btn_generate.pack()
        
        self.output_lbl = tk.Entry(bottom_panel, font=("Consolas", 14), justify="center")
        self.output_lbl.pack(fill="x", padx=20, pady=10)

    def generate_string(self):
        try:
            lhs_str = self.lhs_editor.get_string()
            rhs_str = self.rhs_editor.get_string()
            
            final_string = f"{lhs_str}={rhs_str}"
            
            # Limpiar y mostrar
            self.output_lbl.delete(0, tk.END)
            self.output_lbl.insert(0, final_string)
            
            # AQUI: Llamarías a tu clase TuringMachine con 'final_string'
            # MTM_Validator.process(final_string)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error construyendo la ecuación: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DifferentialEquationGUI(root)
    root.mainloop()