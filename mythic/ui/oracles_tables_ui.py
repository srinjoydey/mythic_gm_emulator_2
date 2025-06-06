from PySide6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize, Signal, QTimer


class OraclesTablesUI(QWidget):
    """A fullscreen view with a left-hand vertical navigation pane and a close button row."""
    nav_item_selected = Signal(str)

    def __init__(self, parent, controller, nav_items):
        super().__init__(parent)
        self.parent_view = parent
        self.controller = controller
        self.nav_buttons = []
        self.selected_nav_btn = None
        self.nav_btn_map = {}

        # Make the UI fill the entire parent window
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main grid layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # --- Top Row: Title and Close Button ---
        close_row_container = QWidget(self)
        close_row_container.setStyleSheet("background-color: #333;")

        self.title_label = QLabel("Gallery", close_row_container)
        self.title_label.setFont(QFont("Arial", 28))
        self.title_label.setStyleSheet("""
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
        # close_button.clicked.connect(self.emit_details_data_and_close)

        close_row_layout = QHBoxLayout(close_row_container)
        close_row_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(40, 5, 40, 5)

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
            btn.setFont(QFont("Arial", 13))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                padding: 10px;
                color: white;
            """)
            btn.clicked.connect(lambda checked, b=btn, item=nav_item: self.handle_nav_click(b, item))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.nav_btn_map[nav_item] = btn


        self.nav_layout.addStretch()
        self.nav_scroll_area.setWidget(self.nav_frame)
        self.layout.addWidget(self.nav_scroll_area, 1, 0, 10, 3)

        # --- Right Content Area ---

        # --- Center content Navigation Pane with Scroll ---
        self.content_nav_scroll_area = QScrollArea(self)
        self.content_nav_scroll_area.setWidgetResizable(True)
        self.content_nav_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.content_nav_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.content_nav_frame = QFrame(self.content_nav_scroll_area)
        content_layout = QGridLayout(self.content_nav_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.content_nav_frame.setStyleSheet("""
            background-color: white;
        """)

        self.content_nav_scroll_area.setWidget(self.content_nav_frame)
        self.layout.addWidget(self.content_nav_scroll_area, 1, 3, 10, 10)

        if self.nav_buttons:
            first_nav_item = nav_items[0]
            first_btn = self.nav_btn_map.get(first_nav_item)
            QTimer.singleShot(0, lambda: self.handle_nav_click(first_btn, first_nav_item))

    def handle_nav_click(self, btn, nav_item):
        # Highlight the selected button
        for b in self.nav_buttons:
            b.setStyleSheet("""
                padding: 10px;
                color: white;
            """)
        btn.setStyleSheet("""
            padding: 10px;
            color: white;
            background-color: #0078d7;  /* Highlight color */
            font-weight: bold;
        """)
        self.selected_nav_btn = btn

        # Emit signal or call method to get data from the view
        self.nav_item_selected.emit(nav_item)
        # self.update_content_for_nav(nav_item)

    def update_content_for_nav(self, nav_item, table):
        # Remove previous content
        for i in reversed(range(self.content_nav_frame.layout().count())):
            widget = self.content_nav_frame.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Create a new layout for the table
        table_layout = QGridLayout()
        table_layout.setSpacing(2)
        table_layout.setContentsMargins(10, 10, 10, 10)

        for row_idx, row_tuple in enumerate(table):
            # First column: the string
            label = QLabel(str(row_tuple[0]), self.content_nav_frame)
            label.setFont(QFont("Arial", 13, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa; padding: 6px;")
            table_layout.addWidget(label, row_idx, 0)

            # Next columns: each is a tuple of 3 values
            for col_idx, cell_tuple in enumerate(row_tuple[1:], start=1):
                cell_widget = QWidget(self.content_nav_frame)
                cell_layout = QVBoxLayout(cell_widget)
                cell_layout.setContentsMargins(2, 2, 2, 2)
                cell_layout.setSpacing(0)

                # Top value (smaller)
                top_label = QLabel(str(cell_tuple[0]), cell_widget)
                top_label.setFont(QFont("Arial", 9))
                top_label.setAlignment(Qt.AlignCenter)
                # Middle value (larger)
                mid_label = QLabel(str(cell_tuple[1]), cell_widget)
                mid_label.setFont(QFont("Arial", 16, QFont.Bold))
                mid_label.setAlignment(Qt.AlignCenter)
                # Bottom value (smaller)
                bot_label = QLabel(str(cell_tuple[2]), cell_widget)
                bot_label.setFont(QFont("Arial", 9))
                bot_label.setAlignment(Qt.AlignCenter)

                cell_layout.addWidget(top_label)
                cell_layout.addWidget(mid_label)
                cell_layout.addWidget(bot_label)

                cell_widget.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa;")
                table_layout.addWidget(cell_widget, row_idx, col_idx)

        # Set the new layout to the content_nav_frame
        # Remove any existing layout first
        old_layout = self.content_nav_frame.layout()
        if old_layout:
            QWidget().setLayout(old_layout)
        self.content_nav_frame.setLayout(table_layout)
