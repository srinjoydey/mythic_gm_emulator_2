from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class ExistingStoryUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # Title Label (Centered)
        self.title_label = QLabel("GM Mythic Emulator", self)
        self.title_label.setFont(QFont("Arial", 28))
        self.title_label.setStyleSheet("background-color: lightblue; padding: 10px;")
        self.layout.addWidget(self.title_label, 1, 1, 1, 1)
