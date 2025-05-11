from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class NewStoryUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Define background image path (now managed here)
        self.bg_image_path = "assets/page1_bg.jpg"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # Title Label (Centered)
        self.title_label = QLabel("New Story", self)
        self.title_label.setFont(QFont("Arial", 28))
        self.title_label.setStyleSheet("background-color: lightblue; padding: 10px;")
        self.layout.addWidget(self.title_label, 1, 1, 1, 1)

    def update_dimensions(self, width, height):
        """Updates font sizes dynamically when the main window resizes."""
        font_size = max(20, int(width / 50))
        self.title_label.setFont(QFont("Arial", font_size))

        button_font_size = max(16, int(width / 80))
        for btn in self.button_frame.findChildren(QPushButton):
            btn.setFont(QFont("Arial", button_font_size))
