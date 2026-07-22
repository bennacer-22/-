import tkinter as tk
import math

class GoogleScientificCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Scientific Calculator")
        self.root.geometry("400x720")
        
        # الألوان الدقيقة المستخرجة من صورتك
        self.bg_color = "#F8F9FE"      # الخلفية العامة
        self.num_btn_bg = "#E9EEF6"    # أزرار الأرقام (رمادي فاتح)
        self.fn_btn_bg = "#D3E3FD"     # أزرار العمليات والدوال (أزرق سماوي فاتح)
        self.eq_btn_bg = "#5C4E6F"     # زر اليساوي (بنفسجي داكن)
        
        self.text_dark = "#1C1B1E"     # لون النصوص
        self.text_eq = "#FFFFFF"       # لون نص زر اليساوي

        self.root.configure(bg=self.bg_color)
        self.expression = ""
        self.paren_toggle = False  # متابعة حالة القوس (False = فتح, True = إغلاق)

        # 1. شاشة عرض الأرقام
        self.display_label = tk.Label(
            root, text="", font=("Arial", 38), bg=self.bg_color, 
            fg=self.text_dark, anchor="e", padx=20
        )
        self.display_label.pack(fill="both", expand=True, pady=(30, 10))

        # 2. شبكة الأزرار (7 صفوف × 4 أعمدة)
        self.btns_frame = tk.Frame(root, bg=self.bg_color)
        self.btns_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # قائمة الأزرار مطابقة للصورة تماماً
        buttons = [
            # الصف 1 (علمي)
            ('√', 0, 0, 'fn'), ('π', 0, 1, 'fn'), ('^', 0, 2, 'fn'), ('!', 0, 3, 'fn'),
            # الصف 2 (علمي)
            ('Deg', 1, 0, 'fn'), ('sin', 1, 1, 'fn'), ('cos', 1, 2, 'fn'), ('tan', 1, 3, 'fn'),
            # الصف 3 (علمي)
            ('Inv', 2, 0, 'fn'), ('e', 2, 1, 'fn'), ('ln', 2, 2, 'fn'), ('log', 2, 3, 'fn'),
            # الصف 4 (أساسي)
            ('AC', 3, 0, 'fn'), ('()', 3, 1, 'fn'), ('%', 3, 2, 'fn'), ('÷', 3, 3, 'fn'),
            # الصف 5 (أرقام)
            ('7', 4, 0, 'num'), ('8', 4, 1, 'num'), ('9', 4, 2, 'num'), ('×', 4, 3, 'fn'),
            # الصف 6 (أرقام)
            ('4', 5, 0, 'num'), ('5', 5, 1, 'num'), ('6', 5, 2, 'num'), ('-', 5, 3, 'fn'),
            # الصف 7 (أرقام)
            ('1', 6, 0, 'num'), ('2', 6, 1, 'num'), ('3', 6, 2, 'num'), ('+', 6, 3, 'fn'),
            # الصف 8 (أرقام وسفلي)
            ('0', 7, 0, 'num'), (',', 7, 1, 'num'), ('⌫', 7, 2, 'num'), ('=', 7, 3, 'eq')
        ]

        # ضبط مرونة الشبكة
        for i in range(8):
            self.btns_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.btns_frame.grid_columnconfigure(i, weight=1)

        # رسم الأزرار
        for text, row, col, btn_type in buttons:
            self.create_rounded_button(text, row, col, btn_type)

    def create_rounded_button(self, text, row, col, btn_type):
        if btn_type == 'fn':
            bg_color, fg_color = self.fn_btn_bg, self.text_dark
        elif btn_type == 'eq':
            bg_color, fg_color = self.eq_btn_bg, self.text_eq
        else:
            bg_color, fg_color = self.num_btn_bg, self.text_dark

        # استخدام Canvas لضبط الشكل البيضاوي/الدائري الناعم
        canvas = tk.Canvas(
            self.btns_frame, bg=self.bg_color, bd=0, 
            highlightthickness=0, width=65, height=50
        )
        canvas.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        # رسم الزر البيضاوي
        oval = canvas.create_oval(3, 3, 62, 47, fill=bg_color, outline="")
        font_size = 14 if len(text) > 2 else 18
        text_id = canvas.create_text(32, 25, text=text, fill=fg_color, font=("Arial", font_size))

        def on_click(event):
            self.handle_click(text)

        canvas.bind("<Button-1>", on_click)

    def handle_click(self, key):
        # 1. منطق القوس الذكي ()
        if key == '()':
            if not self.paren_toggle:
                self.expression += '('
                self.paren_toggle = True
            else:
                self.expression += ')'
                self.paren_toggle = False
        
        # 2. مسح الكل
        elif key == 'AC':
            self.expression = ""
            self.paren_toggle = False
            
        # 3. التراجع خطوة
        elif key == '⌫':
            if len(self.expression) > 0:
                removed = self.expression[-1]
                if removed == '(':
                    self.paren_toggle = False
                elif removed == ')':
                    self.paren_toggle = True
                self.expression = self.expression[:-1]

        # 4. الحساب وسلسلة المعالجة العلميّة
        elif key == '=':
            try:
                # استبدال الرموز بما يفهمه البايثون
                expr = self.expression.replace('×', '*').replace('÷', '/').replace(',', '.')
                expr = expr.replace('π', 'math.pi').replace('e', 'math.e')
                expr = expr.replace('√', 'math.sqrt').replace('^', '**')
                expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
                expr = expr.replace('ln', 'math.log').replace('log', 'math.log10')
                
                res = eval(expr)
                self.expression = str(round(res, 8)) if isinstance(res, float) else str(res)
            except:
                self.expression = "خطأ"
            self.paren_toggle = False

        # 5. باقي الأزرار
        else:
            if self.expression == "خطأ":
                self.expression = ""
            
            if key in ['sin', 'cos', 'tan', 'ln', 'log', '√']:
                self.expression += key + '('
                self.paren_toggle = True
            else:
                self.expression += key
        
        self.display_label.config(text=self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleScientificCalc(root)
    root.mainloop()
      
