from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from utils.utils_functions import align_dialog_to_button


class OptionsWithCancelDialog(QDialog):
    def __init__(self, parent=None, button_labels_list=None):
        super().__init__(parent)
        # self.setWindowTitle("Start a New Scene")
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #666;
                border: 1px solid black;
            }
            QLabel {
                color: #800000;
                font-weight: bold;
                font-size: 28px;
            }
            QPushButton {
                background-color: #fffbe6;
                color: #800000;
                border: 1px solid #800000;
                padding: 12px 24px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
            }
        """)

        self.button_1_label = button_labels_list[0]
        self.button_2_label = button_labels_list[1]

        layout = QVBoxLayout(self)

        button_row = QHBoxLayout()
        self.button_1 = QPushButton(self.button_1_label, self)
        self.button_2 = QPushButton(self.button_2_label, self)
        button_row.addWidget(self.button_1)
        button_row.addWidget(self.button_2)
        layout.addLayout(button_row)

        cancel_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel", self)
        cancel_row.addStretch(1)        
        cancel_row.addWidget(self.cancel_btn)
        cancel_row.addStretch(1)        
        layout.addLayout(cancel_row)

        self.button_1.clicked.connect(lambda: self.choose_and_accept(self.button_1_label))
        self.button_2.clicked.connect(lambda: self.choose_and_accept(self.button_2_label))
        self.cancel_btn.clicked.connect(lambda: self.choose_and_accept(None))

        if self.button_2_label == "Cancel":
            self.cancel_btn.setVisible(False)

    def showEvent(self, event):
        super().showEvent(event)
        align_dialog_to_button(self, self.parent())

    def choose_and_accept(self, label):
        self.selected_label = label
        self.accept()


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