from functools import partial
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QScrollArea, QLineEdit, QComboBox, QMessageBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QEvent


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
        self.bg_image_path = "visuals/backgrounds/game_dashboard.png"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        for i in range(5):
            self.layout.setColumnStretch(i, 1)
            self.layout.setRowStretch(i, 1)

        # Title Label (Centered)
        self.title_label = QLabel(parent.story_name, self)
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


class ClickableLabel(QLabel):
    # Utility wrapper for QLabel to emit a signal on click
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class FocusLineEdit(QLineEdit):
    # Utility wrapper for QLineEdit to emit a signal when focused
    focused = Signal()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()


class CharactersThreadsTablesUI(QWidget):
    """UI Layout with both horizontal and vertical scrolling."""
    search_for_suggestions = Signal(dict)
    row_clicked = Signal(dict)

    def __init__(self, parent, controller, table_label, story_index, existing_data):
        from views.game_dashboard import GameDashboardView
        super().__init__(parent)
        self.controller = controller
        self.table_label = table_label
        self.story_index = story_index
        self.existing_data = existing_data
        self.edited_rows_data_dict = {}

        rows_to_be_updated = self.existing_data.keys()
        self.setStyleSheet("background-color: white;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # --- Close Row ---
        close_row_container = QWidget(self)
        close_row_container.setStyleSheet("background-color: transparent;")
        title_label = QLabel(self.table_label.title(), close_row_container)
        title_label.setFont(QFont("Arial", 28))
        title_label.setStyleSheet("""
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
        close_button.clicked.connect(lambda: (
            self.controller.current_view.receive_edited_rows_data(
                self.send_edited_rows_data_dict()),
            self.controller.show_view(
                GameDashboardView, story_index=self.story_index)
        ))
        close_row_layout = QHBoxLayout(close_row_container)
        close_row_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(420, 30, 90, 5)
        self.layout.addWidget(close_row_container)

        # --- Table Container ---
        table_container = QWidget(self)
        table_container_layout = QVBoxLayout(table_container)
        table_container_layout.setContentsMargins(50, 0, 50, 0)

        scroll_area = QScrollArea(table_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")

        scroll_widget = QWidget()
        self.scroll_widget = scroll_widget  # Store reference for handlers
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(0)

        section_labels = ["1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]

        # Create table structure
        row_index = 1

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

            for i in range(5):
                border_bottom = "2px solid black" if i == 4 else "0.1px solid black"
                row_label = ClickableLabel(section_labels[i], scroll_widget)
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

                table_cell = FocusLineEdit(scroll_widget)
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
                table_cell.setReadOnly(True)
                table_cell.setProperty("row_index", row_index)

                dropdown_cell = None
                if self.table_label == "characters":
                    dropdown_cell = QComboBox(scroll_widget)
                    dropdown_cell.addItems([None, "character", "place", "item"])
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
                    dropdown_cell.setProperty("row_index", row_index)

                    if row_index in rows_to_be_updated:
                        table_cell.setText(self.existing_data[row_index]["name"])
                        dropdown_cell.setCurrentText(self.existing_data[row_index]["type"])

                    # --- Editable logic ---
                    row_label.clicked.connect(self.row_click_handler(table_cell, dropdown_cell))
                    table_cell.focused.connect(self.row_click_handler(table_cell, dropdown_cell))
                    table_cell.mouseDoubleClickEvent = self.double_click_handler(table_cell)
                    table_cell.textEdited.connect(self.debounced_emit_search_for_suggestions)
                    table_cell.editingFinished.connect(self.finish_edit_handler(table_cell, dropdown_cell))
                    dropdown_cell.currentIndexChanged.connect(self.edited_row_data)
                    dropdown_cell.currentIndexChanged.connect(self.dropdown_selection_handler(dropdown_cell, table_cell))

                    scroll_layout.addWidget(dropdown_cell, row_index, 10, 1, 2)

                elif self.table_label == "threads":
                    if row_index in rows_to_be_updated:
                        table_cell.setText(self.existing_data[row_index]["thread"])

                    row_label.mousePressEvent = self.row_click_handler(table_cell)
                    table_cell.mousePressEvent = self.row_click_handler(table_cell)
                    table_cell.mouseDoubleClickEvent = self.double_click_handler(table_cell)
                    table_cell.textEdited.connect(self.debounced_emit_search_for_suggestions)
                    table_cell.editingFinished.connect(self.finish_edit_handler(table_cell))
                    table_cell.editingFinished.connect(self.edited_row_data)

                scroll_layout.addWidget(table_cell, row_index, 4, 1, 6)
                row_index += 1

        scroll_area.setWidget(scroll_widget)
        table_container_layout.addWidget(scroll_area)
        self.layout.addWidget(table_container)
        self.setLayout(self.layout)


    def row_click_handler(self, table_cell, dropdown_cell=None):
        def handler():
            if table_cell.isReadOnly():
                row_index = table_cell.property("row_index")
                if dropdown_cell:
                    data = {
                        "name": table_cell.text(),
                        "type": dropdown_cell.currentText(),
                        "row_index": row_index
                    }
                    self.row_clicked.emit(data)
                else:
                    data = {
                        "thread": table_cell.text(),
                        "row_index": row_index
                    }
                    self.row_clicked.emit(data)
        return handler

    def double_click_handler(self, table_cell):
        def handler(event):
            if event.type() == QEvent.MouseButtonDblClick and table_cell.isReadOnly():
                # Set all table_cells to read-only and all dropdowns to disabled
                for le in self.scroll_widget.findChildren(QLineEdit):
                    le.setReadOnly(True)
                for cb in self.scroll_widget.findChildren(QComboBox):
                    cb.setEnabled(False)
                # Now enable only the current cell and dropdown
                table_cell.setReadOnly(False)
                table_cell.setFocus()
                table_cell.setCursorPosition(len(table_cell.text()))
                row_index = table_cell.property("row_index")
                for cb in self.scroll_widget.findChildren(QComboBox):
                    if cb.property("row_index") == row_index:
                        cb.setEnabled(True)
        return handler
    
    def emit_search_for_suggestions(self, row_index, table_cell, text_from_signal):
        self.search_for_suggestions.emit({
            "row": row_index,
            "data": table_cell.text()
        })

    def debounced_emit_search_for_suggestions(self, text):
        sender = self.sender()
        row_index = sender.property("row_index")
        if not hasattr(self, "debounce_timers"):
            self.debounce_timers = {}
        # Stop any existing timer for this sender
        if sender in self.debounce_timers:
            self.debounce_timers[sender].stop()
        else:
            self.debounce_timers[sender] = QTimer(self)
            self.debounce_timers[sender].setSingleShot(True)
            # Use a lambda to capture the current sender and row_index
            self.debounce_timers[sender].timeout.connect(
                lambda s=sender, r=row_index: self.search_for_suggestions.emit({
                    "row": r,
                    "data": s.text()
                })
            )
        self.debounce_timers[sender].start(400)

    def finish_edit_handler(self, table_cell, dropdown_cell=None):
        def handler():
            table_cell.setReadOnly(True)
        return handler

    def edited_row_data(self):
        sender = self.sender()
        row_index = sender.property("row_index")
        if self.table_label == "characters":
            # sender is dropdown_cell
            table_cell = None
            # Find the table_cell for this row
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break
            if table_cell and sender.currentText():
                self.edited_rows_data_dict[row_index] = {
                    "name": table_cell.text(),
                    "type": sender.currentText()
                }
                table_cell.clearFocus()
        elif self.table_label == "threads":
            # sender is table_cell
            if sender.text():
                self.edited_rows_data_dict[row_index] = {
                    "thread": sender.text()
                }
                sender.clearFocus()

    def dropdown_selection_handler(self, dropdown_cell, table_cell):
        def handler(index):
            # Only disable if a valid selection is made (not None or empty)
            if dropdown_cell.currentText():
                dropdown_cell.setEnabled(False)
                table_cell.setReadOnly(True)
        return handler

    def send_edited_rows_data_dict(self):
        return self.edited_rows_data_dict
    
    def prompt_duplicate_action(self, name):
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Possible Duplicate?")
            msg_box.setText(f"The name '{name}' already exists for this story.")
            create_new_btn = msg_box.addButton("Create New", QMessageBox.ActionRole)
            overwrite_btn = msg_box.addButton("Overwrite", QMessageBox.AcceptRole)
            remove_dup_btn = msg_box.addButton("Remove Duplicate", QMessageBox.DestructiveRole)
            msg_box.setDefaultButton(overwrite_btn)
            msg_box.exec()

            if msg_box.clickedButton() == create_new_btn:
                return "create"
            elif msg_box.clickedButton() == overwrite_btn:
                return "overwrite"
            elif msg_box.clickedButton() == remove_dup_btn:
                return "remove"
            return None    