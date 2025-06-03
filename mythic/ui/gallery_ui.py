from PySide6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize


class GalleryModalUI(QWidget):
    """A modal dialog with a left-hand vertical navigation pane and a close button row."""

    def __init__(self, parent, controller, nav_items, on_close):
        from views.game_dashboard import GameDashboardView

        super().__init__(parent)
        self.controller = controller
        self.nav_buttons = []

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setMinimumSize(600, 400)

        # Main grid layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(50, 20, 50, 50)
        self.layout.setSpacing(0)

        # --- Top Row: Title and Close Button ---
        close_row_container = QWidget(self)
        close_row_container.setStyleSheet("background-color: transparent;")

        self.title_label = QLabel("Gallery", close_row_container)
        self.title_label.setFont(QFont("Arial", 28))
        self.title_label.setStyleSheet("""
            background-color: transparent;
            padding: 10px;                                  
            color: maroon;
            font-weight: bold;
            font-style: italic;
        """)

        close_button = QPushButton(close_row_container)
        close_button.setIcon(QIcon("assets/icons/close_icon.png"))
        close_button.setIconSize(QSize(25, 25))
        close_button.setFont(QFont("Arial", 14, QFont.Bold))
        close_button.setStyleSheet("""
            padding: 0px;
            background-color: white;
            color: maroon;
        """)
        close_button.clicked.connect(lambda: (self.controller.show_view(
            GameDashboardView, story_index=self.story_index)
        ))

        close_row_layout = QHBoxLayout(close_row_container)
        close_row_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(440, 5, 40, 5)

        self.layout.addWidget(close_row_container, 0, 0, 1, 13)

        # --- Left Navigation Pane with Scroll ---
        self.nav_scroll_area = QScrollArea(self)
        self.nav_scroll_area.setWidgetResizable(True)
        self.nav_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.nav_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.nav_frame = QFrame(self.nav_scroll_area)
        self.nav_layout = QVBoxLayout(self.nav_frame)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(0)

        for nav_item in nav_items:
            btn = QPushButton(nav_item, self.nav_frame)
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                padding: 10px;
                color: white;
            """)
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.nav_layout.addStretch()
        self.nav_scroll_area.setWidget(self.nav_frame)
        self.layout.addWidget(self.nav_scroll_area, 1, 0, 10, 3)

        # --- Right Content Area ---
        content_frame = QFrame(self)
        content_layout = QGridLayout(content_frame)
        content_layout.setContentsMargins(10, 0, 0, 0)

        # --- Image ---
        image_placeholder = QLabel("Image block", content_frame)
        image_placeholder.setAlignment(Qt.AlignCenter)
        image_placeholder.setFont(QFont("Arial", 16))
        image_placeholder.setStyleSheet("""
            background-color: green;
            color: black;
        """)
        content_layout.addWidget(image_placeholder, 0, 0, 3, 3)

        # --- Details ---
        details_placeholder = QLabel("Details block", content_frame)
        details_placeholder.setAlignment(Qt.AlignCenter)
        details_placeholder.setFont(QFont("Arial", 16))
        details_placeholder.setStyleSheet("""
            background-color: yellow;
            color: black;
        """)
        content_layout.addWidget(details_placeholder, 0, 3, 3, 2)

        # --- Text ---
        text_placeholder = QLabel("Text block", content_frame)
        text_placeholder.setAlignment(Qt.AlignCenter)
        text_placeholder.setFont(QFont("Arial", 16))
        text_placeholder.setStyleSheet("""
            background-color: pink;
            color: black;
        """)                
        content_layout.addWidget(text_placeholder, 3, 0, 2, 5)

        self.layout.addWidget(content_frame, 1, 3, 10, 10)

    # def update_dimensions(self, width, height):
    #     """Updates font sizes and button sizes dynamically when the main window resizes."""
    #     title_font_size = max(20, width // 50)
    #     self.title_label.setFont(QFont("Arial", title_font_size))

    #     btn_height = max(40, min(150, int(height / 11)))
    #     button_font_size = max(8, width // 90)

    #     for btn in self.nav_buttons:
    #         btn.setFont(QFont("Arial", button_font_size))
    #         btn.setFixedHeight(btn_height)