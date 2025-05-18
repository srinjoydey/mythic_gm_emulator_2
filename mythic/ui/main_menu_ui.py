from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFrame, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from views.game_dashboard import GameDashboardView


class MainMenuUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Define background image path (now managed here)
        self.bg_image_path = "assets/main_menu.jpg"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # Title Label (Centered)
        self.title_label = QLabel("GM Mythic Emulator", self)
        self.title_label.setFont(QFont("Arial", 28))
        # Apply transparent background
        self.title_label.setStyleSheet("""
            background-color: transparent;
            padding: 10px;
            color: maroon;
            font-weight: bold;
            font-style: italic;            
        """)
        self.layout.addWidget(self.title_label, 1, 1, 1, 1)

        # Button Frame (Bottom-right placement)
        self.button_frame = QFrame(self)
        self.button_layout = QVBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(0, 100, 0, 0) 
        self.layout.addWidget(self.button_frame, 1, 2, 2, 2, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.create_buttons()

        # **Call update_dimensions() on initialization**
        self.update_dimensions(self.width(), self.height())

    def create_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        # Define menu buttons dynamically
        from views.main_menu import NewStoryView, ExistingStoryView, OraclesTablesView, GalleryView, ArtifactsView

        self.buttons = [
            ("New Story", NewStoryView),
            ("Existing Story", ExistingStoryView),
            ("Oracles / Tables", OraclesTablesView),
            ("Gallery", GalleryView),
            ("Artifacts", ArtifactsView),
        ]

        button_width, button_height = 250, 60
        button_font_size = 10

        for text, view in self.buttons:
            btn = QPushButton(text, self.button_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda checked, v=view: self.controller.show_view(v))
            self.button_layout.addWidget(btn)

    def update_dimensions(self, width, height):
        """Updates font sizes dynamically when the main window resizes."""
        font_size = max(20, int(width / 50))
        self.title_label.setFont(QFont("Arial", font_size))

        button_font_size = max(8, int(width / 80))
        for btn in self.button_frame.findChildren(QPushButton):
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(int(width / 6), int(height / 12))


class NewStoryUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Define background image path (now managed here)
        self.bg_image_path = "assets/new_story.jpg"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # Title Label (Centered)
        self.title_label = QLabel("New Story", self)
        self.title_label.setFont(QFont("Arial", 28))
        # Apply transparent background
        self.title_label.setStyleSheet("""
            background-color: transparent;
            padding: 10px;
            color: maroon;
            font-weight: bold;
            font-style: italic;            
        """)
        self.layout.addWidget(self.title_label, 1, 1, 1, 1)

        # Button Frame (Bottom-right placement)
        self.button_frame = QFrame(self)
        self.button_layout = QVBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(0, 100, 0, 0) 
        self.layout.addWidget(self.button_frame, 1, 2, 2, 2, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.create_buttons()      

    def create_buttons(self):
        """Creates buttons dynamically with optimized layout."""

        # Define menu buttons dynamically
        self.buttons = [
            ("Create a new Story", GameDashboardView),
        ]        
        button_width, button_height = 250, 60
        button_font_size = 20

        for text, view in self.buttons:
            btn = QPushButton(text, self.button_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda checked, v=view: self.controller.show_view(v))
            self.button_layout.addWidget(btn)

    def update_dimensions(self, width, height):
        """Updates font sizes dynamically when the main window resizes."""
        font_size = max(20, int(width / 50))
        self.title_label.setFont(QFont("Arial", font_size))

        button_font_size = max(8, int(width / 80))
        for btn in self.button_frame.findChildren(QPushButton):
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(int(width / 6), int(height / 12))


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


class OraclesTablesUI(QWidget):
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


class GalleryUI(QWidget):
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


class ArtifactsUI(QWidget):
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