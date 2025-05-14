from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFrame, QSizePolicy, QScrollArea
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


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
        from views.new_story import CharactersList, ThreadsList, ScrollCheck

        # Define menu buttons dynamically
        self.buttons = [
            # ("New Story", new_story.NewStoryView),
            ("Characters", CharactersList),
            ("Threads", ThreadsList),
            ("Scroll Check", ScrollCheck),
            # ("Artifacts", artifacts.ArtifactsView),
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


class CharactersThreadsTablesUI(QWidget):
    """UI Layout for a structured table with sections and labels."""
    def __init__(self, parent, controller):
        from views.new_story import NewStoryView

        super().__init__(parent)
        self.controller = controller

        # Apply plain white background to the entire page
        self.setStyleSheet("background-color: white;")

        # **Main Layout (Non-Scrollable)**
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Keep margins fixed

        # **Create Scrollable Area for Table**
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Allow resizing
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show vertical scrollbar

        # **Create a Container Widget for the Scrollable Table**
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(0)  # No spacing between cells for a clean table look
        scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins inside the scrollable area

        # **Add Close Button**
        close_button = QPushButton(scroll_widget)
        close_button.setIcon(QIcon("assets/icons/close_icon.png"))  # Add an icon
        close_button.setFont(QFont("Arial", 14, QFont.Bold))
        close_button.setStyleSheet("""
            padding: 10px;
            background-color: maroon;
            color: white;
            border: 2px solid black;
        """)
        close_button.clicked.connect(lambda: self.controller.show_view(NewStoryView))  # Navigate back
        scroll_layout.addWidget(close_button, 0, 10, 1, 2, alignment=Qt.AlignCenter)  # Positioning button        

        # Define section labels (spanning 5 rows each)
        section_labels = ["1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]

        # Create table structure
        row_index = 1
        for section_index, section_label in enumerate(section_labels):
            # Add section label (spans 5 rows, 2 columns)
            section_label_widget = QLabel(section_label, scroll_widget)
            section_label_widget.setFont(QFont("Arial", 14, QFont.Bold))
            section_label_widget.setAlignment(Qt.AlignCenter)
            section_label_widget.setStyleSheet("""
                border-top: 1px solid black; 
                border-bottom: 1.5px solid black; 
                border-left: 2px solid black; 
                border-right: 2px solid black; 
                padding: 5px; 
                background-color: white; 
                color: black; 
                font-weight: bold;
            """)
            scroll_layout.addWidget(section_label_widget, row_index, 0, 5, 2)  # Spanning 5 rows, 2 columns

            # Add row labels within the section (each row spans 2 columns)
            for i in range(5):
                # Determine border thickness
                border_bottom = "2px solid black" if i == 4 else "0.1px solid black"

                # Second column (row labels within section, spans 2 columns)
                row_label = QLabel(section_labels[i], scroll_widget)
                row_label.setFont(QFont("Arial", 12, QFont.Bold))
                row_label.setAlignment(Qt.AlignCenter)
                row_label.setStyleSheet(f"""
                    border-top: 1px solid black; 
                    border-bottom: {border_bottom}; 
                    border-left: 2px solid black; 
                    border-right: 2px solid black; 
                    padding: 5px; 
                    background-color: white; 
                    color: black; 
                    font-weight: bold;
                """)
                scroll_layout.addWidget(row_label, row_index, 2, 1, 2)  # Spanning 2 columns

                # Third column (table content, spans remaining 8 columns)
                table_cell = QLabel("", scroll_widget)
                table_cell.setStyleSheet(f"""
                    border-top: 1px solid black; 
                    border-bottom: {border_bottom}; 
                    border-left: 2px solid black; 
                    border-right: 2px solid black; 
                    padding: 10px; 
                    background-color: white;
                """)
                scroll_layout.addWidget(table_cell, row_index, 4, 1, 8)  # Spanning 8 columns

                row_index += 1  # Move to the next row

        # **Set Scrollable Widget Inside Scroll Area**
        scroll_area.setWidget(scroll_widget)

        # **Add Scroll Area to Main Layout (Margins Stay Fixed)**
        self.main_layout.addWidget(scroll_area)

        self.setLayout(self.main_layout)  # Ensure full layout usage


class ScrollCheckUI(QWidget):
    """UI Layout with both horizontal and vertical scrolling."""
    def __init__(self, parent, controller):
        from views.new_story import NewStoryView

        super().__init__(parent)
        self.controller = controller

        # Apply plain white background
        self.setStyleSheet("background-color: white;")

        # **Initialize Layout Properly**
        self.layout = QGridLayout(self)  # Ensure it's a valid QGridLayout
        self.setLayout(self.layout)  # Set the layout before adding widgets

        # **Create Scroll Area**
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Allow resizing
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Enable vertical scrolling
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Enable horizontal scrolling

        # **Create Scrollable Content Widget**
        scroll_widget = QWidget()
        scroll_widget.setAutoFillBackground(False)  # Prevent background filling
        scroll_widget.setAttribute(Qt.WA_TranslucentBackground, True)  # Allow transparency
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(0)
        scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins inside the scrollable area

        # **Create Transparent Container for Close Button Row**
        close_row_container = QWidget(scroll_widget)
        close_row_container.setStyleSheet("background-color: transparent;")  # Make only this row transparent
        close_row_container.setAttribute(Qt.WA_TranslucentBackground, True)  # Ensure transparency

        # **Add Close Button Inside Transparent Container**
        close_button = QPushButton(close_row_container)
        close_button.setIcon(QIcon("assets/icons/close_icon.png"))  # Add an icon
        close_button.setFont(QFont("Arial", 14, QFont.Bold))
        close_button.setStyleSheet("""
            padding: 10px;
            background-color: transparent;
            color: maroon;
            border: 2px solid black;
        """)
        close_button.clicked.connect(lambda: self.controller.show_view(NewStoryView))  # Navigate back

        # **Add Close Button to Transparent Container**
        close_row_container_layout = QVBoxLayout(close_row_container)
        close_row_container_layout.setContentsMargins(0, 0, 0, 0)
        close_row_container_layout.addWidget(close_button, alignment=Qt.AlignCenter)

        # **Add Transparent Container to Scroll Layout (Now Part of Original Layout)**
        scroll_layout.addWidget(close_row_container, 0, 0, 1, 12)  # Spanning full width

        # Define section labels (spanning 5 rows each)
        section_labels = ["1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]

        # Create table structure
        row_index = 1
        for section_index, section_label in enumerate(section_labels):
            # Add section label (spans 5 rows, 2 columns)
            section_label_widget = QLabel(section_label, scroll_widget)
            section_label_widget.setFont(QFont("Arial", 14, QFont.Bold))
            section_label_widget.setAlignment(Qt.AlignCenter)
            section_label_widget.setStyleSheet("""
                border-top: 1px solid black; 
                border-bottom: 1.5px solid black; 
                border-left: 2px solid black; 
                border-right: 2px solid black; 
                padding: 5px; 
                background-color: white; 
                color: black; 
                font-weight: bold;
            """)
            scroll_layout.addWidget(section_label_widget, row_index, 0, 5, 2)  # Spanning 5 rows, 2 columns

            # Add row labels within the section (each row spans 2 columns)
            for i in range(5):
                # Determine border thickness
                border_bottom = "2px solid black" if i == 4 else "1px solid black"

                # Second column (row labels within section, spans 2 columns)
                row_label = QLabel(section_labels[i], scroll_widget)
                row_label.setFont(QFont("Arial", 12, QFont.Bold))
                row_label.setAlignment(Qt.AlignCenter)
                row_label.setStyleSheet(f"""
                    border-top: 1px solid black; 
                    border-bottom: {border_bottom}; 
                    border-left: 2px solid black; 
                    border-right: 2px solid black; 
                    padding: 5px; 
                    background-color: white; 
                    color: black; 
                    font-weight: bold;
                """)
                scroll_layout.addWidget(row_label, row_index, 2, 1, 2)  # Spanning 2 columns

                # Third column (table content, spans remaining 8 columns)
                table_cell = QLabel("", scroll_widget)
                table_cell.setStyleSheet(f"""
                    border-top: 1px solid black; 
                    border-bottom: {border_bottom}; 
                    border-left: 2px solid black; 
                    border-right: 2px solid black; 
                    padding: 10px; 
                    background-color: white;
                """)
                scroll_layout.addWidget(table_cell, row_index, 4, 1, 8)  # Spanning 8 columns

                row_index += 1  # Move to the next row

        # **Set Scrollable Widget Inside Scroll Area**
        scroll_area.setWidget(scroll_widget)

        # **Add Scroll Area to Main Layout (Margins Stay Fixed)**
        self.layout.addWidget(scroll_area, 0, 0, 1, 1)  # Ensure correct positioning

        self.setLayout(self.layout)  # Ensure full layout usage
