from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import math

# ضبط خلفية التطبيق
Window.clearcolor = (0.97, 0.98, 0.99, 1)

class CalculatorApp(App):
    def build(self):
        self.title = "Google Scientific Calculator"
        self.expression = ""
        self.paren_toggle = False

        # الحاوية الرئيسية
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. شاشة عرض النتيجة
        self.display = Label(
            text="0",
            font_size='36sp',
            halign='right',
            valign='middle',
            color=(0.11, 0.11, 0.12, 1),
            size_hint=(1, 0.25)
        )
        self.display.bind(size=self.display.setter('text_size'))
        main_layout.add_widget(self.display)

        # 2. شبكة الأزرار (8 صفوف × 4 أعمدة)
        grid = GridLayout(cols=4, spacing=6, size_hint=(1, 0.75))

        # تعريف الأزرار وأنواعها
        buttons = [
            ('√', 'fn'), ('π', 'fn'), ('^', 'fn'), ('!', 'fn'),
            ('Deg', 'fn'), ('sin', 'fn'), ('cos', 'fn'), ('tan', 'fn'),
            ('Inv', 'fn'), ('e', 'fn'), ('ln', 'fn'), ('log', 'fn'),
            ('AC', 'fn'), ('()', 'fn'), ('%', 'fn'), ('÷', 'fn'),
            ('7', 'num'), ('8', 'num'), ('9', 'num'), ('×', 'fn'),
            ('4', 'num'), ('5', 'num'), ('6', 'num'), ('-', 'fn'),
            ('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'fn'),
            ('0', 'num'), (',', 'num'), ('⌫', 'num'), ('=', 'eq')
        ]

        # الألوان المخصصة (RGBA)
        fn_bg = (0.82, 0.89, 0.99, 1)    # أزرق فاتح
        num_bg = (0.91, 0.93, 0.96, 1)   # رمادي فاتح
        eq_bg = (0.36, 0.31, 0.43, 1)    # بنفسجي داكن

        for text, btn_type in buttons:
            if btn_type == 'fn':
                bg = fn_bg
                fg = (0.11, 0.11, 0.12, 1)
            elif btn_type == 'eq':
                bg = eq_bg
                fg = (1, 1, 1, 1)
            else:
                bg = num_bg
                fg = (0.11, 0.11, 0.12, 1)

            btn = Button(
                text=text,
                background_normal='',
                background_color=bg,
                color=fg,
                font_size='20sp',
                bold=True
            )
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        return main_layout

    def on_button_press(self, instance):
        key = instance.text

        if key == '()':
            if not self.paren_toggle:
                self.expression += '('
                self.paren_toggle = True
            else:
                self.expression += ')'
                self.paren_toggle = False

        elif key == 'AC':
            self.expression = ""
            self.paren_toggle = False

        elif key == '⌫':
            if len(self.expression) > 0:
                removed = self.expression[-1]
                if removed == '(':
                    self.paren_toggle = False
                elif removed == ')':
                    self.paren_toggle = True
                self.expression = self.expression[:-1]

        elif key == '=':
            try:
                expr = self.expression.replace('×', '*').replace('÷', '/').replace(',', '.')
                expr = expr.replace('π', 'math.pi').replace('e', 'math.e')
                expr = expr.replace('√', 'math.sqrt').replace('^', '**')
                expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
                expr = expr.replace('ln', 'math.log').replace('log', 'math.log10')

                res = eval(expr)
                self.expression = str(round(res, 8)) if isinstance(res, float) else str(res)
            except Exception:
                self.expression = "خطأ"
            self.paren_toggle = False

        else:
            if self.expression == "خطأ":
                self.expression = ""

            if key in ['sin', 'cos', 'tan', 'ln', 'log', '√']:
                self.expression += key + '('
                self.paren_toggle = True
            elif key not in ['Deg', 'Inv', '!']:
                self.expression += key

        self.display.text = self.expression if self.expression else "0"

if __name__ == '__main__':
    CalculatorApp().run()
    
