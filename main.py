import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout
)

class CalcApp(QWidget):
    def __init__(self):
        super().__init__()
        # App settings
        self.setWindowTitle("Calculator")
        self.resize(700, 600)

        # All object/Widget
        self.text_box = QLineEdit()
        self.grid = QGridLayout()

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        # Loop for button creation
        row = 0
        col = 0
        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_clicked)
            self.grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.clear = QPushButton("Clear")
        self.delete = QPushButton("Delete")
        self.clear.clicked.connect(self.button_clicked)
        self.delete.clicked.connect(self.button_clicked)

        # Connect Enter/Return key
        self.text_box.returnPressed.connect(self.evaluate_expression)

        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)
        master_layout.addLayout(button_row)

        self.setLayout(master_layout)

    def button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == "=":
            self.evaluate_expression()
        elif text == "Clear":
            self.text_box.clear()
        elif text == "Delete":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)

    def evaluate_expression(self):
        try:
            expression = self.text_box.text()
            result = eval(expression)
            self.text_box.setText(str(result))
        except Exception:
            self.text_box.setText("Error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CalcApp()
    main_window.show()
    sys.exit(app.exec_())

