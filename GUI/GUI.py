import tkinter as tk
from tkinter import ttk, messagebox

# --- CONSTANTES DE ESTILO ---
FONT_MAIN = ("Consolas", 10)
BG_COLOR = "#f0f0f0"

class ScrollableFrame(tk.Frame):
    """
    Un contenedor que permite scroll vertical y horizontal.
    Se usa para contener los ExpressionBlocks grandes.
    """
    def __init__(self, parent, bg_color="#ffffff", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Canvas y Scrollbars
        self.canvas = tk.Canvas(self, borderwidth=0, background=bg_color)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        # Layout de scrollbars
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Frame interno (donde irán los widgets reales)
        self.scrollable_content = tk.Frame(self.canvas, background=bg_color)
        
        # Ventana dentro del canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        
        # Bindings para actualizar el scroll
        self.scrollable_content.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_frame_configure(self, event):
        """Ajusta la región de scroll al tamaño del contenido interno"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Opcional: Ajustar ancho del frame interno si se desea (aquí lo dejamos libre para scroll horizontal)"""
        pass

class FactorBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, relief="solid", borderwidth=1, *args, **kwargs)
        self.allow_y = allow_y
        
        # Header del Factor
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=2, pady=2)
        
        tk.Label(top_frame, text="Factor:", font=("Arial", 7, "bold")).pack(side="left")
        
        # Selector de Tipo
        options = ["Número", "Variable X", "Función"]
        if self.allow_y:
            options.append("Variable Y")
            
        self.type_var = tk.StringVar(value="Número")
        self.combo = ttk.Combobox(top_frame, textvariable=self.type_var, values=options, state="readonly", width=9)
        self.combo.pack(side="left", padx=2)
        self.combo.bind("<<ComboboxSelected>>", self.update_content)
        
        # Botón eliminar
        tk.Button(top_frame, text="x", bg="#ffcccc", command=self.destroy, font=("Arial", 6), width=2).pack(side="right")

        # Contenido dinámico
        self.content_frame = tk.Frame(self, padx=5, pady=5)
        self.content_frame.pack(side="top", fill="x")
        
        # Registro de validación para números
        self.vcmd = (self.register(self.validate_number), '%P')
        
        self.update_content()

    def validate_number(self, new_value):
        """Permite solo dígitos y un punto decimal"""
        if new_value == "": return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def update_content(self, event=None):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        selection = self.type_var.get()
        
        if selection == "Número":
            # AQUI: Se aplica la validación
            self.current_widget = tk.Entry(self.content_frame, width=8, validate="key", validatecommand=self.vcmd)
            self.current_widget.insert(0, "1")
            self.current_widget.pack()
            
        elif selection == "Variable X":
            self.current_widget = tk.Label(self.content_frame, text="x", font=("Times", 14, "italic"))
            self.current_widget.pack()
            
        elif selection == "Variable Y":
            frame = tk.Frame(self.content_frame)
            frame.pack()
            tk.Label(frame, text="y", font=("Times", 14, "italic")).pack(side="left")
            tk.Label(frame, text="Derivada:").pack(side="left", padx=2)
            self.deriv_spin = tk.Spinbox(frame, from_=0, to=10, width=2)
            self.deriv_spin.pack(side="left")
            self.current_widget = "y_complex"
            
        elif selection == "Función":
            frame = tk.Frame(self.content_frame)
            frame.pack()
            funcs = ["sen", "cos", "tan", "ln", "exp", "sqrt"]
            self.func_selector = ttk.Combobox(frame, values=funcs, state="readonly", width=5)
            self.func_selector.set("sen")
            self.func_selector.pack(side="left")
            
            tk.Label(frame, text="(").pack(side="left")
            # Recursividad sin scrollbars internos (demasiado ruido visual)
            self.inner_expr = ExpressionBlock(frame, allow_y=self.allow_y, vertical_stack=False) 
            self.inner_expr.pack(side="left", padx=2)
            tk.Label(frame, text=")").pack(side="left")
            self.current_widget = "func_complex"

    def get_string(self):
        sel = self.type_var.get()
        if sel == "Número":
            val = self.current_widget.get().strip()
            return val if val else "0"
        elif sel == "Variable X":
            return "x"
        elif sel == "Variable Y":
            derivs = int(self.deriv_spin.get())
            return "y" + ("'" * derivs)
        elif sel == "Función":
            func_name = self.func_selector.get()
            # Mapeo simple para demostración
            return f"{func_name}({self.inner_expr.get_string()})"
        return ""

class TermBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, *args, **kwargs):
        super().__init__(parent, relief="groove", borderwidth=2, bg="#e0e0e0", *args, **kwargs)
        self.allow_y = allow_y
        
        # Fila de control (Signo, Título, Botones)
        ctrl_frame = tk.Frame(self, bg="#d0d0d0")
        ctrl_frame.pack(side="top", fill="x", anchor="w")
        
        self.sign_var = tk.StringVar(value="+")
        tk.Button(ctrl_frame, textvariable=self.sign_var, command=self.toggle_sign, width=3, font=("Consolas", 8, "bold")).pack(side="left")
        
        # Botón agregar factor
        tk.Button(ctrl_frame, text="+ Factor (*)", command=self.add_factor, font=("Arial", 8)).pack(side="left", padx=10)
        
        # Botón eliminar término
        tk.Button(ctrl_frame, text="Eliminar Término", bg="#ffaaaa", command=self.destroy, font=("Arial", 8)).pack(side="right")
        
        # Area de Factores (Horizontal)
        self.factors_area = tk.Frame(self, bg="#e0e0e0")
        self.factors_area.pack(side="top", fill="x", padx=5, pady=5, anchor="w")
        
        self.factors = []
        self.add_factor()

    def toggle_sign(self):
        self.sign_var.set("-" if self.sign_var.get() == "+" else "+")

    def add_factor(self):
        if self.factors:
            tk.Label(self.factors_area, text="*", font=("Arial", 12, "bold"), bg="#e0e0e0").pack(side="left")
        f = FactorBlock(self.factors_area, allow_y=self.allow_y)
        f.pack(side="left", padx=2, anchor="w")
        self.factors.append(f)

    def get_string(self):
        sign = "-" if self.sign_var.get() == "-" else ""
        parts = [f.get_string() for f in self.factors if f.winfo_exists()]
        if not parts: return ""
        term_str = "*".join(parts)
        return f"{sign}{term_str}"

class ExpressionBlock(tk.Frame):
    def __init__(self, parent, allow_y=True, vertical_stack=True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.allow_y = allow_y
        self.vertical_stack = vertical_stack # Controla si apilamos vertical u horizontal
        self.terms = []
        
        self.terms_area = tk.Frame(self)
        self.terms_area.pack(side="top", fill="both", expand=True)
        
        # Botón añadir término
        self.btn_add = tk.Button(self, text="+ Añadir Término (+)", command=self.add_term, bg="#ccffcc", font=("Arial", 9, "bold"))
        # Si es vertical, el botón va abajo, si es horizontal (dentro de función), va al lado
        pack_side = "bottom" if vertical_stack else "right"
        self.btn_add.pack(side=pack_side, fill="x", pady=2)
        
        self.add_term()

    def add_term(self):
        t = TermBlock(self.terms_area, allow_y=self.allow_y)
        
        if self.vertical_stack:
            # AQUI: Cambio clave para apilar verticalmente
            t.pack(side="top", fill="x", pady=5, anchor="w")
        else:
            # Comportamiento antiguo para dentro de funciones (ahorra espacio)
            t.pack(side="left", padx=5, anchor="n")
            
        self.terms.append(t)

    def get_string(self):
        valid_terms = [t for t in self.terms if t.winfo_exists()]
        if not valid_terms: return "0"
        result = ""
        for i, term in enumerate(valid_terms):
            s = term.get_string()
            if not s: continue
            if i > 0 and not s.startswith("-"):
                result += "+" + s
            else:
                result += s
        return result if result else "0"

class DifferentialEquationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Constructor ED - MTM")
        self.root.geometry("1200x700")
        
        # Título
        tk.Label(root, text="Ingrese la Ecuación Diferencial", font=("Arial", 14, "bold")).pack(pady=5)
        
        # --- CONTENEDOR PRINCIPAL ---
        main_split = tk.PanedWindow(root, orient="horizontal", sashwidth=5, bg="#999")
        main_split.pack(fill="both", expand=True, padx=10, pady=5)
        
        # --- LADO IZQUIERDO (LHS) ---
        lhs_container = tk.LabelFrame(main_split, text="Lado Izquierdo (Expresión General)", font=FONT_MAIN, bg="#eef")
        main_split.add(lhs_container, minsize=400)
        
        # Usamos ScrollableFrame para el contenedor principal izquierdo
        self.lhs_scroll = ScrollableFrame(lhs_container, bg_color="#eef")
        self.lhs_scroll.pack(fill="both", expand=True)
        
        # El editor se pone DENTRO del contenido scrolleable
        self.lhs_editor = ExpressionBlock(self.lhs_scroll.scrollable_content, allow_y=True, vertical_stack=True)
        self.lhs_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- SEPARADOR CENTRAL (=) ---
        # Para que el igual no quede perdido, lo ponemos en un frame intermedio pequeño
        eq_frame = tk.Frame(main_split, bg="white")
        main_split.add(eq_frame, minsize=50)
        tk.Label(eq_frame, text="=", font=("Arial", 30, "bold")).pack(expand=True)

        # --- LADO DERECHO (RHS) ---
        rhs_container = tk.LabelFrame(main_split, text="Lado Derecho (Sin variable Y)", font=FONT_MAIN, bg="#fee")
        main_split.add(rhs_container, minsize=400)
        
        # Usamos ScrollableFrame para el contenedor principal derecho
        self.rhs_scroll = ScrollableFrame(rhs_container, bg_color="#fee")
        self.rhs_scroll.pack(fill="both", expand=True)
        
        self.rhs_editor = ExpressionBlock(self.rhs_scroll.scrollable_content, allow_y=False, vertical_stack=True)
        self.rhs_editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- AREA DE SALIDA ---
        bottom_panel = tk.Frame(root, pady=10, bg="#444")
        bottom_panel.pack(fill="x", side="bottom")
        
        btn_gen = tk.Button(bottom_panel, text="ANALIZAR (Generar String)", font=("Arial", 12, "bold"), bg="orange", command=self.generate_string)
        btn_gen.pack()
        
        self.output_lbl = tk.Entry(bottom_panel, font=("Consolas", 14), justify="center")
        self.output_lbl.pack(fill="x", padx=20, pady=10)

    def generate_string(self):
        try:
            lhs = self.lhs_editor.get_string()
            rhs = self.rhs_editor.get_string()
            final = f"{lhs}={rhs}"
            self.output_lbl.delete(0, tk.END)
            self.output_lbl.insert(0, final)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DifferentialEquationGUI(root)
    root.mainloop()