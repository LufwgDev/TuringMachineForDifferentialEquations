import tkinter as tk
from tkinter import ttk, messagebox

# --- CONSTANTES Y MAPEO ---
FONT_MAIN = ("Consolas", 10)

# Mapeo de Etiqueta (GUI) -> Símbolo (MTM)
FUNCTION_MAP = {
    "sen": "S",
    "cos": "C",
    "tan": "T",
    "ln": "L",
    "raiz": "R",     # √
    "abs": "A",      # Valor absoluto
    "sec": "s",
    "csc": "c",
    "cot": "t",
    "arcsin": "IS",  # Ejemplo para Inversa Seno (I + S)
    "arccos": "IC",
    "arctan": "IT",
    "exp": "E",      # e^...
    "1/( )": "/"     # Recíproco
}

class ScrollableFrame(tk.Frame):
    """ Frame con scrollbars automáticas """
    def __init__(self, parent, bg_color="#ffffff", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, background=bg_color)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollable_content = tk.Frame(self.canvas, background=bg_color)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        
        self.scrollable_content.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class FactorBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, relief="solid", borderwidth=1, *args, **kwargs)
        self.allow_y = allow_y
        self.has_exponent = False
        
        # --- HEADER ---
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=2, pady=1)
        
        tk.Label(top_frame, text="Factor:", font=("Arial", 7, "bold")).pack(side="left")
        
        # Selector de Tipo
        options = ["Número", "Variable X", "Función", "Constante"]
        if self.allow_y:
            options.append("Variable Y")
            
        self.type_var = tk.StringVar(value="Número")
        self.combo = ttk.Combobox(top_frame, textvariable=self.type_var, values=options, state="readonly", width=8)
        self.combo.pack(side="left", padx=2)
        self.combo.bind("<<ComboboxSelected>>", self.update_content)
        
        # Botón Potencia (^)
        self.btn_pow = tk.Button(top_frame, text="^", command=self.toggle_exponent, font=("Consolas", 8, "bold"), bg="#ddd", width=2)
        self.btn_pow.pack(side="left", padx=2)
        
        # Botón Cerrar (x)
        tk.Button(top_frame, text="x", bg="#ffcccc", command=self.destroy, font=("Arial", 6), width=2).pack(side="right")

        # --- CONTENIDO PRINCIPAL ---
        self.main_content = tk.Frame(self, padx=5, pady=2)
        self.main_content.pack(side="left", fill="both")
        
        # --- CONTENEDOR DE EXPONENTE (Oculto inicialmente) ---
        self.exponent_frame = tk.Frame(self, padx=2, pady=2, bg="#eef")
        # Se empacará cuando se active la potencia

        self.vcmd = (self.register(self.validate_number), '%P')
        self.update_content()

    def validate_number(self, new_value):
        if new_value == "": return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def toggle_exponent(self):
        self.has_exponent = not self.has_exponent
        if self.has_exponent:
            self.btn_pow.config(bg="#aaffaa", relief="sunken")
            self.exponent_frame.pack(side="right", anchor="n", padx=2)
            tk.Label(self.exponent_frame, text="^", font=("Arial", 8)).pack(side="left", anchor="n")
            # El exponente es una Expresión completa (permite y^(x+1))
            self.exponent_expr = ExpressionBlock(self.exponent_frame, allow_y=self.allow_y, vertical_stack=False, is_exponent=True)
            self.exponent_expr.pack(side="left")
        else:
            self.btn_pow.config(bg="#ddd", relief="raised")
            self.exponent_frame.forget()
            for widget in self.exponent_frame.winfo_children():
                widget.destroy()

    def update_content(self, event=None):
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
        selection = self.type_var.get()
        
        if selection == "Número":
            self.current_widget = tk.Entry(self.main_content, width=6, validate="key", validatecommand=self.vcmd)
            self.current_widget.insert(0, "1")
            self.current_widget.pack()
            
        elif selection == "Constante":
            self.const_var = tk.StringVar(value="π")
            ttk.Combobox(self.main_content, textvariable=self.const_var, values=["π", "e"], state="readonly", width=3).pack()
            
        elif selection == "Variable X":
            tk.Label(self.main_content, text="x", font=("Times", 14, "italic")).pack()
            
        elif selection == "Variable Y":
            f = tk.Frame(self.main_content)
            f.pack()
            tk.Label(f, text="y", font=("Times", 14, "italic")).pack(side="left")
            self.deriv_spin = tk.Spinbox(f, from_=0, to=10, width=2)
            self.deriv_spin.pack(side="left")
            
        elif selection == "Función":
            f = tk.Frame(self.main_content)
            f.pack()
            # Usamos las llaves del diccionario para la lista visual
            funcs = list(FUNCTION_MAP.keys())
            self.func_selector = ttk.Combobox(f, values=funcs, state="readonly", width=7)
            self.func_selector.set("sen")
            self.func_selector.pack(side="left")
            
            tk.Label(f, text="(").pack(side="left")
            self.inner_expr = ExpressionBlock(f, allow_y=self.allow_y, vertical_stack=False) 
            self.inner_expr.pack(side="left")
            tk.Label(f, text=")").pack(side="left")

    def get_string(self):
        sel = self.type_var.get()
        base_str = ""
        
        if sel == "Número":
            val = self.current_widget.get().strip()
            base_str = val if val else "0"
        elif sel == "Constante":
            base_str = self.const_var.get() # π o e
        elif sel == "Variable X":
            base_str = "x"
        elif sel == "Variable Y":
            derivs = int(self.deriv_spin.get())
            base_str = "y" + ("'" * derivs)
        elif selection := "Función": 
            display_name = self.func_selector.get()
            mtm_symbol = FUNCTION_MAP.get(display_name, "?")
            inner_str = self.inner_expr.get_string()
            base_str = f"{mtm_symbol}({inner_str})"

        # Manejo de Exponente
        if self.has_exponent:
            exp_str = self.exponent_expr.get_string()
            return f"({base_str})^({exp_str})"
        
        return base_str

class TermBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, relief="groove", borderwidth=2, bg="#e0e0e0", *args, **kwargs)
        self.allow_y = allow_y
        
        # Control
        ctrl_frame = tk.Frame(self, bg="#d0d0d0")
        ctrl_frame.pack(side="top", fill="x")
        
        self.sign_var = tk.StringVar(value="+")
        tk.Button(ctrl_frame, textvariable=self.sign_var, command=self.toggle_sign, width=2, font=("Consolas", 8, "bold")).pack(side="left")
        
        tk.Button(ctrl_frame, text="* Factor", command=self.add_factor, font=("Arial", 7)).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="Eliminar", bg="#ffaaaa", command=self.destroy, font=("Arial", 7)).pack(side="right")
        
        # Area Factores
        self.factors_area = tk.Frame(self, bg="#e0e0e0")
        self.factors_area.pack(side="top", fill="x", padx=2, pady=2)
        self.factors = []
        self.add_factor()

    def toggle_sign(self):
        self.sign_var.set("-" if self.sign_var.get() == "+" else "+")

    def add_factor(self):
        if self.factors:
            tk.Label(self.factors_area, text="*", font=("Arial", 10, "bold"), bg="#e0e0e0").pack(side="left")
        f = FactorBlock(self.factors_area, allow_y=self.allow_y)
        f.pack(side="left", padx=2)
        self.factors.append(f)

    def get_string(self):
        sign = "-" if self.sign_var.get() == "-" else ""
        parts = [f.get_string() for f in self.factors if f.winfo_exists()]
        if not parts: return ""
        return f"{sign}{'*'.join(parts)}"

class ExpressionBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, vertical_stack=True, is_exponent=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.allow_y = allow_y
        self.vertical_stack = vertical_stack
        
        # --- CORRECCIÓN AQUÍ: Inicializar la lista antes de llamar a add_term ---
        self.terms = [] 
        
        self.terms_area = tk.Frame(self)
        self.terms_area.pack(side="top", fill="both", expand=True)
        
        btn_text = "+" if not vertical_stack else "+ Término"
        self.btn_add = tk.Button(self, text=btn_text, command=self.add_term, bg="#ccffcc", font=("Arial", 7))
        pack_side = "bottom" if vertical_stack else "right"
        self.btn_add.pack(side=pack_side, fill="x" if vertical_stack else "y")
        
        self.add_term()

    def add_term(self):
        t = TermBlock(self.terms_area, allow_y=self.allow_y)
        if self.vertical_stack:
            t.pack(side="top", fill="x", pady=2, anchor="w")
        else:
            t.pack(side="left", padx=2, anchor="n")
        self.terms.append(t)

    def get_string(self):
        valid = [t for t in self.terms if t.winfo_exists()]
        if not valid: return "0"
        res = ""
        for i, t in enumerate(valid):
            s = t.get_string()
            if not s: continue
            if i > 0 and not s.startswith("-"):
                res += "+" + s
            else:
                res += s
        return res if res else "0"

class DifferentialEquationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Constructor ED - MTM")
        self.root.geometry("1200x750")
        
        # --- HEADER ---
        tk.Label(root, text="Entrada de Ecuación Diferencial (MTM Parsing)", font=("Arial", 14, "bold")).pack(pady=5)
        
        # --- SPLIT PANE PRINCIPAL ---
        main_split = tk.PanedWindow(root, orient="horizontal", sashwidth=5, bg="#999")
        main_split.pack(fill="both", expand=True, padx=10, pady=5)
        
        # --- LHS (Izquierda) ---
        lhs_c = tk.LabelFrame(main_split, text="Lado Izquierdo (Contiene Y)", font=FONT_MAIN, bg="#eef")
        main_split.add(lhs_c, minsize=450)
        self.lhs_scroll = ScrollableFrame(lhs_c, bg_color="#eef")
        self.lhs_scroll.pack(fill="both", expand=True)
        self.lhs_editor = ExpressionBlock(self.lhs_scroll.scrollable_content, allow_y=True, vertical_stack=True)
        self.lhs_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- IGUALDAD ---
        eq_f = tk.Frame(main_split, bg="white")
        main_split.add(eq_f, minsize=40)
        tk.Label(eq_f, text="=", font=("Arial", 26, "bold")).pack(expand=True)
        
        # --- RHS (Derecha) ---
        rhs_c = tk.LabelFrame(main_split, text="Lado Derecho (f(x) o Constantes)", font=FONT_MAIN, bg="#fee")
        main_split.add(rhs_c, minsize=450)
        self.rhs_scroll = ScrollableFrame(rhs_c, bg_color="#fee")
        self.rhs_scroll.pack(fill="both", expand=True)
        self.rhs_editor = ExpressionBlock(self.rhs_scroll.scrollable_content, allow_y=False, vertical_stack=True)
        self.rhs_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- FOOTER (Output) ---
        bot = tk.Frame(root, pady=10, bg="#444")
        bot.pack(fill="x", side="bottom")
        
        tk.Button(bot, text="GENERAR CADENA MTM", font=("Arial", 11, "bold"), bg="orange", command=self.generate).pack()
        self.out_vis = tk.Entry(bot, font=("Consolas", 12), justify="center", width=80)
        self.out_vis.pack(pady=10)
        tk.Label(bot, text="Cadena para la Máquina de Turing:", fg="white", bg="#444").pack()

    def generate(self):
        try:
            lhs = self.lhs_editor.get_string()
            rhs = self.rhs_editor.get_string()
            final = f"{lhs}={rhs}"
            self.out_vis.delete(0, tk.END)
            self.out_vis.insert(0, final)
            print(f"MTM Input: {final}") # Para debug en consola
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DifferentialEquationGUI(root)
    root.mainloop()