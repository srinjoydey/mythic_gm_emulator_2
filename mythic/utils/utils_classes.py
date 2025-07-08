from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class DiceResultDialog(QDialog):
    def __init__(self, parent, colour, dice_result, fate_result):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setFixedSize(200, 200)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {colour};
                border: 2px solid black;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        dice_label = QLabel(str(dice_result), self)
        dice_label.setAlignment(Qt.AlignCenter)
        dice_label.setFont(QFont("Arial", 54, QFont.Bold))
        dice_label.setStyleSheet("""
            color: white;
            border: 0;
            background: transparent;
            padding: 8px;
        """)

        fate_label = QLabel(str(fate_result), self)
        fate_label.setAlignment(Qt.AlignCenter)
        fate_label.setFont(QFont("Arial", 16, QFont.Bold))
        fate_label.setStyleSheet("""
            color: white;
            border: 0;
            background: transparent;
            padding: 4px;
        """)

        layout.addWidget(dice_label, stretch=3)
        layout.addWidget(fate_label, stretch=1)

    def mousePressEvent(self, event):
        self.accept()

    def keyPressEvent(self, event):
        self.accept()