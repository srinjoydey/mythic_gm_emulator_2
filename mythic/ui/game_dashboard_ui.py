from functools import partial
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QScrollArea, QLineEdit, QComboBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize, Signal, QTimer


class GameDashboardUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    characters_button_clicked = Signal()
    threads_button_clicked = Signal()
    gallery_modal_button_clicked = Signal()
    main_menu_button_clicked = Signal()

    def __init__(self, parent, controller, story_index):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index

        # Define background image path (now managed here)
        self.bg_image_path = "assets/game_dashboard.png"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # Title Label (Centered)
        self.title_label = QLabel("Game Dashboard", self)
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
        self.signals = [
            ("Characters", self.characters_button_clicked),
            ("Threads", self.threads_button_clicked),
            ("Gallery Modal", self.gallery_modal_button_clicked),
            ("Main Menu", self.main_menu_button_clicked),            
        ]
        button_width, button_height = 250, 60
        button_font_size = 20

        for text, signal in self.signals:
            btn = QPushButton(text, self.button_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(signal.emit)
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
    """UI Layout with both horizontal and vertical scrolling."""
    search_for_suggestions = Signal(dict)

    def __init__(self, parent, controller, table_label, story_index, existing_data):
        from views.game_dashboard import GameDashboardView

        super().__init__(parent)
        self.controller = controller
        self.table_label = table_label
        self.story_index = story_index
        self.existing_data = existing_data
        self.edited_rows_data_dict = {}

        rows_to_be_updated = self.existing_data.keys()

        # Apply plain white background
        self.setStyleSheet("background-color: white;")

        # **Main Layout (Non-Scrollable)**
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Keep margins fixed

        # **Create Transparent Container for Close Button Row**
        close_row_container = QWidget(self)
        close_row_container.setStyleSheet("background-color: transparent;")

        # Title Label (Centered)
        title_label = QLabel(self.table_label.title(), close_row_container)
        title_label.setFont(QFont("Arial", 28))
        # Apply transparent background
        title_label.setStyleSheet("""
            background-color: transparent;
            padding: 10px;
            color: maroon;
            font-weight: bold;
            font-style: italic;            
        """)

        # **Add Close Button Inside Transparent Container**
        close_button = QPushButton(close_row_container)
        close_button.setIcon(QIcon("assets/icons/close_icon.png"))
        close_button.setIconSize(QSize(25, 25))  # Increase icon size
        close_button.setFont(QFont("Arial", 14, QFont.Bold))
        close_button.setStyleSheet("""
            padding: 0px;
            background-color: white;
            color: maroon;
        """)
        close_button.clicked.connect(lambda: (
            self.controller.current_view.receive_edited_rows_data(
                self.send_edited_rows_data_dict()),
            self.controller.show_view(
                GameDashboardView, story_index=self.story_index)
        ))

        # **Add Close Button to Transparent Container**
        close_row_layout = QHBoxLayout(close_row_container)
        # Change to AlignCenter if needed
        close_row_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(
            420, 30, 90, 5)  # Left, Top, Right, Bottom

        # **Add Transparent Row to Main Layout**
        self.layout.addWidget(close_row_container)

        # **Create a Container for the Table (Adds Left & Right Margins)**
        table_container = QWidget(self)
        table_container_layout = QVBoxLayout(table_container)
        table_container_layout.setContentsMargins(
            50, 0, 50, 0)  # Adds space on left & right

        # **Create Scroll Area**
        scroll_area = QScrollArea(table_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setStyleSheet(
            "border: none; background-color: transparent;")

        # **Create Scrollable Content Widget**
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(0)

        # Define section labels (spanning 5 rows each)
        section_labels = ["1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]

        # Create table structure
        row_index = 0
        for section_label in section_labels:
            # **Section Label (Spans 5 Rows, 2 Columns)**
            section_label_widget = QLabel(section_label, scroll_widget)
            section_label_widget.setFont(QFont("Arial", 14, QFont.Bold))
            section_label_widget.setAlignment(Qt.AlignCenter)
            section_label_widget.setStyleSheet("""
                border-top: 1px solid black;
                border-bottom: 2px solid black;
                border-right: 1px solid black;
                border-left: 1px solid black;
                padding: 5px;
                background-color: white;
                color: black;
                font-weight: bold;
            """)
            scroll_layout.addWidget(section_label_widget, row_index, 0, 5, 2)

            # **Row Labels & Table Cells**
            for i in range(5):
                border_bottom = "2px solid black" if i == 4 else "0.1px solid black"

                row_label = QLabel(section_labels[i], scroll_widget)
                row_label.setFont(QFont("Arial", 12, QFont.Bold))
                row_label.setAlignment(Qt.AlignCenter)
                row_label.setStyleSheet(f"""
                    border-top: 1px solid black;
                    border-bottom: {border_bottom};
                    border-right: 1px solid black;
                    border-left: 1px solid black;
                    padding: 5px;
                    background-color: white;
                    color: black;
                    font-weight: bold;
                """)
                scroll_layout.addWidget(row_label, row_index, 2, 1, 2)

                table_cell = QLineEdit(scroll_widget)
                table_cell.setStyleSheet(f"""
                    border-top: 1px solid black;
                    border-bottom: {border_bottom};
                    border-right: 1px solid black;
                    border-left: 1px solid black;
                    padding: 10px;
                    color: black;
                    font-size: 16px;
                    background-color: white;
                """)

                scroll_layout.addWidget(table_cell, row_index, 4, 1, 6)

                # Add dropdowns column if Characters Table
                if self.table_label == "characters":

                    dropdown_cell = QComboBox(scroll_widget)
                    dropdown_cell.addItems(
                        [None, "character", "place", "item"])
                    # dropdown_cell.setAlignment(Qt.AlignCenter)
                    dropdown_cell.setStyleSheet(f"""
                        border-top: 1px solid black;
                        border-bottom: {border_bottom};
                        border-right: 1px solid black;
                        border-left: 1px solid black;
                        padding: 10px;
                        color: black;
                        font-size: 16px;
                        background-color: white;
                        text-align: center;
                    """)
                    dropdown_cell.setEditable(False)
                    dropdown_cell.setEnabled(False)

                    if row_index in rows_to_be_updated:
                        # If row exists in existing data, set initial values
                        table_cell.setText(self.existing_data[row_index]["name"])
                        dropdown_cell.setCurrentText(
                            self.existing_data[row_index]["type"])

                    # **Signal to Send Updated Text to View**
                    # table_cell.textEdited.connect(partial(self.emit_search_for_suggestions, row_index, table_cell))
                    table_cell.textEdited.connect(partial(self.debounced_emit_search_for_suggestions, row_index, table_cell))
                    table_cell.editingFinished.connect(
                        partial(self.enable_dropdown, table_cell, dropdown_cell))
                    dropdown_cell.currentIndexChanged.connect(
                        partial(self.edited_row_data, row_index, name=table_cell, type=dropdown_cell))
                    scroll_layout.addWidget(dropdown_cell, row_index, 10, 1, 2)

                elif self.table_label == "threads":

                    if row_index in rows_to_be_updated:
                        # If row exists in existing data, set initial values
                        table_cell.setText(self.existing_data[row_index]["thread"])

                    # table_cell.textEdited.connect(partial(self.emit_search_for_suggestions, row_index, table_cell))
                    table_cell.textEdited.connect(partial(self.debounced_emit_search_for_suggestions, row_index, table_cell))
                    table_cell.editingFinished.connect(
                        partial(self.edited_row_data, row_index, thread=table_cell))

                row_index += 1

        # **Set Scrollable Widget Inside Scroll Area**
        scroll_area.setWidget(scroll_widget)

        # **Add Scroll Area to Table Container**
        table_container_layout.addWidget(scroll_area)

        # **Add Table Container to Main Layout**
        self.layout.addWidget(table_container)

        self.setLayout(self.layout)  # Ensure full layout usage


    def emit_search_for_suggestions(self, row_index, table_cell, text_from_signal):
        self.search_for_suggestions.emit({
            "row": row_index,
            "data": table_cell.text()
        })

    def debounced_emit_search_for_suggestions(self, row_index, table_cell, text_from_signal):
        # Debounce timer dictionary on self
        if not hasattr(self, "debounce_timers"):
            self.debounce_timers = {}
        # Stop any existing timer for this cell
        if table_cell in self.debounce_timers:
            self.debounce_timers[table_cell].stop()
        else:
            self.debounce_timers[table_cell] = QTimer(self)
            self.debounce_timers[table_cell].setSingleShot(True)
            self.debounce_timers[table_cell].timeout.connect(
                partial(self.emit_search_for_suggestions, row_index, table_cell, text_from_signal)
            )
        # Start/restart the timer (e.g., 400 ms delay)
        self.debounce_timers[table_cell].start(400)

    def enable_dropdown(self, field, dropdown):
        """Enable dropdown only after text is entered in QLineEdit."""
        if field.text().strip():  # Ensure field is not empty
            dropdown.setEnabled(True)

    def edited_row_data(self, row, *args, **kwargs):
        """Stores the edited row data and removes cursor focus."""
        if self.table_label == "characters":
            if kwargs.get("type").currentText():
                self.edited_rows_data_dict[row] = {
                    "name": kwargs.get("name").text(),  # Store the edited text
                    # Store selected dropdown value
                    "type": kwargs.get("type").currentText()
                }
                # Removes focus so the cursor disappears
                kwargs.get("name").clearFocus()

        elif self.table_label == "threads":
            self.edited_rows_data_dict[row] = {
                "thread": kwargs.get("thread").text(),  # Store the edited text
            }
            # Removes focus so the cursor disappears
            kwargs.get("thread").clearFocus()

    def send_edited_rows_data_dict(self):
        return self.edited_rows_data_dict
