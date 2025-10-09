import sys
import math
from PyQt5 import QtWidgets, QtCore, QtGui

# Safe math dictionary
SAFE_MATH = {
    'sin': lambda x: math.sin(math.radians(x)),
    'cos': lambda x: math.cos(math.radians(x)),
    'tan': lambda x: math.tan(math.radians(x)),
    'log': math.log10,
    'ln': math.log,
    'sqrt': math.sqrt,
    'pi': math.pi,
    'abs': abs,
    'e': math.e,
    'factorial': math.factorial
}

class SciCalcApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator")
        self.setFixedSize(600, 650)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.init_ui()
        self.apply_style()
        self.bind_shortcuts()

    def init_ui(self):
        # Display
        self.text_box = QtWidgets.QLineEdit()
        self.text_box.setFixedHeight(70)
        self.text_box.setAlignment(QtCore.Qt.AlignRight)
        self.text_box.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Weight.Bold))
        self.text_box.returnPressed.connect(self.evaluate_expression)

        # Buttons layout
        buttons_layout = [
            ["7","8","9","/","sin","cos","tan"],
            ["4","5","6","*","log","ln","√"],
            ["1","2","3","-","(",")","π"],
            ["0",".","=","+","Clear","Delete"]
        ]

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(15)
        self.grid.setContentsMargins(8, 8, 8, 8)

        self.buttons = {}
        for r,row in enumerate(buttons_layout):
            for c,label in enumerate(row):
                btn = QtWidgets.QPushButton(label)
                btn.setFixedSize(75,70)
                btn.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
                btn.clicked.connect(self.button_clicked)
                self.grid.addWidget(btn,r,c)
                self.buttons[label]=btn

        # Container frame
        container = QtWidgets.QFrame()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(16,16,16,16)
        container_layout.setSpacing(15)
        container_layout.addWidget(self.text_box)
        container_layout.addLayout(self.grid)

        # Drop shadow for glass effect
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0,0,0,150))
        container.setGraphicsEffect(shadow)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(container)

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                color: #ffffff;
                font-family: "Segoe UI";
            }

            QFrame {
                background: rgba(255, 255, 255, 0.12);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.25);
                backdrop-filter: blur(20px);
            }

            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 14px;
                padding: 10px 14px;
                color: #ffffff;
            }

            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: #ffffff;
                transition: all 0.2s;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.25); }
            QPushButton:pressed { background-color: rgba(255, 255, 255, 0.35); }

            QPushButton[role="operator"] { background-color: rgba(0, 123, 255, 0.35); }
            QPushButton[role="operator"]:hover { background-color: rgba(0, 123, 255, 0.55); }

            QPushButton[role="="] { background-color: rgba(0, 200, 83, 0.45); font-weight:700; }
            QPushButton[role="="]:hover { background-color: rgba(0, 200, 83, 0.65); }

            QPushButton[role="clear"] { background-color: rgba(244, 67, 54, 0.45); }
            QPushButton[role="clear"]:hover { background-color: rgba(244, 67, 54, 0.65); }

            QPushButton[role="delete"] { background-color: rgba(3, 169, 244, 0.45); }
            QPushButton[role="delete"]:hover { background-color: rgba(3, 169, 244, 0.65); }

            QPushButton[role="func"] { background-color: rgba(255, 193, 7, 0.35); }
            QPushButton[role="func"]:hover { background-color: rgba(255, 193, 7, 0.55); }
        """)

        # Assign roles for buttons dynamically
        for label, btn in self.buttons.items():
            if label in {"/", "*", "-", "+", "="}:
                btn.setProperty("role", "operator" if label != "=" else "=")
            elif label in {"Clear"}:
                btn.setProperty("role", "clear")
            elif label in {"Delete"}:
                btn.setProperty("role", "delete")
            elif label in {"sin","cos","tan","log","ln","√","π","(",")"}:
                btn.setProperty("role", "func")
            else:
                btn.setProperty("role", "digit")

    def bind_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self, self.text_box.clear)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self, self.delete_last)
        for key in "0123456789+-*/.=()":
            QtWidgets.QShortcut(QtGui.QKeySequence(key), self, lambda k=key: self.key_pressed(k))
        QtWidgets.QShortcut(QtGui.QKeySequence("Return"), self, self.evaluate_expression)

    def key_pressed(self, key):
        if key=="=":
            self.evaluate_expression()
        else:
            self.text_box.setText(self.text_box.text()+key)

    def button_clicked(self):
        btn = self.sender()
        text = btn.text()
        if text=="=":
            self.evaluate_expression()
        elif text=="Clear":
            self.text_box.clear()
        elif text=="Delete":
            self.delete_last()
        elif text=="π":
            self.text_box.setText(self.text_box.text()+str(math.pi))
        elif text=="√":
            self.text_box.setText(self.text_box.text()+"sqrt(")
        else:
            self.text_box.setText(self.text_box.text()+text)

    def delete_last(self):
        self.text_box.setText(self.text_box.text()[:-1])

    def evaluate_expression(self):
        expr = self.text_box.text()
        if not expr: return
        try:
            result = eval(expr, {"__builtins__":None}, SAFE_MATH)
            self.text_box.setText(str(result))
        except Exception:
            self.text_box.setText("Error")


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = SciCalcApp()
    main_window.show()
    sys.exit(app.exec_())


