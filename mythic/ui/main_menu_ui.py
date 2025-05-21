from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFrame, QSizePolicy, QLineEdit, 
QTextEdit)
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
        self.title_label = QLabel("Mythic GM Emulator", self)
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
        from views.main_menu import NewStoryView, ExistingStoryView, OraclesTablesView, GalleryView, ArtifactsView

        # Define menu buttons dynamically
        self.buttons = [
            ("New Story", NewStoryView),
            ("Existing Story", ExistingStoryView),
            ("Oracles / Tables", OraclesTablesView),
            ("Gallery", GalleryView),
            ("Artifacts", ArtifactsView),
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
        title_font_size = max(20, int(width / 50))
        self.title_label.setFont(QFont("Arial", title_font_size))
        button_font_size = max(8, int(width / 80))
        for btn in self.button_frame.findChildren(QPushButton):
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(int(width / 6), int(height / 12))

class NewStoryUI(QWidget):
    """UI Layout for New Story screen."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.bg_image_path = "assets/new_story.jpg"

        # Stretch rows and columns for responsiveness
        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # **Title Label (Centered)**
        self.title_label = QLabel("New Story", self)
        self.title_label.setFont(QFont("Arial", 28))
        self.title_label.setStyleSheet("""
            background-color: transparent;
            padding: 10px;
            color: maroon;
            font-weight: bold;
            font-style: italic;
        """)
        self.layout.addWidget(self.title_label, 1, 1, 1, 1)

        # **Text Input Section**
        self.text_frame = QFrame(self)
        self.text_layout = QVBoxLayout(self.text_frame)
        self.text_layout.setContentsMargins(100, 10, 100, 70)

        self.title_input = self.create_input_field("Title / Label", QLineEdit)
        self.description_input = self.create_input_field("Description", QTextEdit)

        self.text_layout.addWidget(self.title_input)
        self.text_layout.addSpacing(5)  
        self.text_layout.addWidget(self.description_input)

        self.layout.addWidget(self.text_frame, 1, 2, 3, 3)

        # **Button Section**
        self.button_frame = QFrame(self)
        self.button_layout = QVBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(0, 100, 0, 20)
        self.layout.addWidget(self.button_frame, 3, 1, 1, 2, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.create_buttons()

    def create_input_field(self, label_text, widget_class):
        """Creates a labeled input field dynamically."""
        label = QLabel(label_text, self.text_frame)
        label.setFont(QFont("Arial", 17))
        label.setStyleSheet("color: black; font-weight: bold;")

        input_widget = widget_class(self.text_frame)
        input_widget.setFont(QFont("Arial", 15))
        input_widget.setPlaceholderText(f"Enter {label_text.lower()}...")  
        input_widget.setStyleSheet("padding: 10px; font-style: italic;")

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(input_widget)

        container = QFrame(self.text_frame)
        container.setLayout(layout)

        return container

    def create_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        from views.main_menu import MainMenu
        from views.game_dashboard import GameDashboardUI

        buttons_data = [("Create", GameDashboardUI), ("Back", MainMenu)]

        for text, view in buttons_data:
            btn = QPushButton(text, self.button_frame)
            btn.setFont(QFont("Arial", 20))
            btn.setMinimumSize(250, 60)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda checked, v=view: self.controller.show_view(v))
            self.button_layout.setSpacing(10)
            self.button_layout.addWidget(btn)

    def update_dimensions(self, width, height):
        """Updates font sizes dynamically when the main window resizes."""
        title_font_size = max(20, width // 50)
        self.title_label.setFont(QFont("Arial", title_font_size))
        
        button_font_size = max(8, width // 80)
        button_size = (width // 6, height // 12)

        for btn in self.button_frame.findChildren(QPushButton):
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(*button_size)

class ExistingStoryUI(QWidget):
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
        self.title_label = QLabel("Mythic GM Emulator", self)
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
        from views.main_menu import NewStoryView, ExistingStoryView, OraclesTablesView, GalleryView, ArtifactsView

        # Define menu buttons dynamically
        self.buttons = [
            ("New Story", NewStoryView),
            ("Existing Story", ExistingStoryView),
            ("Oracles / Tables", OraclesTablesView),
            ("Gallery", GalleryView),
            ("Artifacts", ArtifactsView),
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


class OraclesTablesUI(QWidget):
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
        self.title_label = QLabel("Mythic GM Emulator", self)
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
        from views.main_menu import NewStoryView, ExistingStoryView, OraclesTablesView, GalleryView, ArtifactsView

        # Define menu buttons dynamically
        self.buttons = [
            ("New Story", NewStoryView),
            ("Existing Story", ExistingStoryView),
            ("Oracles / Tables", OraclesTablesView),
            ("Gallery", GalleryView),
            ("Artifacts", ArtifactsView),
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


class ArtifactsUI(QWidget):
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
        self.title_label = QLabel("Mythic GM Emulator", self)
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
        from views.main_menu import NewStoryView, ExistingStoryView, OraclesTablesView, GalleryView, ArtifactsView

        # Define menu buttons dynamically
        self.buttons = [
            ("New Story", NewStoryView),
            ("Existing Story", ExistingStoryView),
            ("Oracles / Tables", OraclesTablesView),
            ("Gallery", GalleryView),
            ("Artifacts", ArtifactsView),
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

