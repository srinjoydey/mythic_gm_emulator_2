from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QScrollArea, QLineEdit, QComboBox, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QIcon, QColor
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QEvent
from utils.game_dashboard_utils import align_dialog_to_button, get_dice_roll_result


class GameDashboardUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    oracles_tables_button_clicked = Signal()
    characters_button_clicked = Signal()
    threads_button_clicked = Signal()
    gallery_modal_button_clicked = Signal()
    main_menu_button_clicked = Signal()
    chaos_factor_changed = Signal(int)
    start_scene_action_selected = Signal(str)
    start_scene_action_resolution = Signal(str)

    def __init__(self, parent, controller, story_index):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        self.chaos_factor = self.parent().chaos_factor

        # Define background image path (now managed here)
        self.bg_image_path = "visuals/backgrounds/game_dashboard.png"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        # Title Label (Centered)
        self.title_label = QLabel(parent.story_name, self)
        self.title_label.setFont(QFont("Arial", 28))
        # Apply transparent background
        self.title_label.setStyleSheet("""
            background-color: transparent;
            padding: 0px;
            color: maroon;
            font-weight: bold;
            font-style: italic;            
        """)
        self.layout.addWidget(self.title_label, 0, 0, 1, 6, alignment=Qt.AlignCenter)

        # Button Frame (Middle-Left placement)
        self.left_content_frame = QFrame(self)
        self.left_content_button_layout = QVBoxLayout(self.left_content_frame)
        self.left_content_button_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.left_content_frame, 1, 0, 2, 2, alignment=Qt.AlignCenter)
        self.create_left_content_buttons()

        # Button Frame (Center)
        self.center_content_frame = QFrame(self)
        self.center_content_button_layout = QVBoxLayout(self.center_content_frame)
        self.center_content_button_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.center_content_frame, 1, 2, 2, 2, alignment=Qt.AlignCenter)
        self.create_center_content_buttons()

        # Button Frame (Middle-Right placement)
        self.right_content_frame = QFrame(self)
        self.right_content_button_layout = QVBoxLayout(self.right_content_frame)
        self.right_content_button_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.right_content_frame, 1, 4, 2, 2, alignment=Qt.AlignCenter)
        self.create_right_content_buttons()

        # Bottom Content Frame (for additional content)
        self.bottom_content_frame = QFrame(self)
        self.bottom_content_frame.setStyleSheet("background-color: transparent;")
        self.bottom_layout = QHBoxLayout(self.bottom_content_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.bottom_content_frame, 3, 0, 1, 6)



    def create_left_content_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        # Define menu buttons dynamically
        signals = [
            ("Oracles / Tables", self.oracles_tables_button_clicked),
            ("Gallery Modal", self.gallery_modal_button_clicked),            
        ]
        button_width, button_height = 250, 60
        button_font_size = 20

        self.left_content_button_layout.setSpacing(10)

        for text, signal in signals:
            btn = QPushButton(text, self.left_content_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(signal.emit)
            self.left_content_button_layout.addWidget(btn)

    def create_center_content_buttons(self):
        button_width, button_height = 250, 60
        button_font_size = 20

        self.center_content_button_layout.setSpacing(65)
        self.create_chaos_factor_counter(self.center_content_frame)

        buttons = [
            ("Start a Scene", self.start_scene_dialog),
            ("End a Scene", self.end_scene_dialog),
        ]
        for text, dialog in buttons:
            btn = QPushButton(text, self.center_content_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(dialog)
            self.center_content_button_layout.addWidget(btn)

    def create_right_content_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        # Define menu buttons dynamically
        signals = [
            ("Characters", self.characters_button_clicked),
            ("Threads", self.threads_button_clicked),
            ("Main Menu", self.main_menu_button_clicked),            
        ]
        button_width, button_height = 250, 60
        button_font_size = 20

        self.right_content_button_layout.setSpacing(10)

        for text, signal in signals:
            btn = QPushButton(text, self.right_content_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(signal.emit)
            self.right_content_button_layout.addWidget(btn)

    def create_chaos_factor_counter(self, parent_widget):
        # --- Counter Widget ---
        counter_widget = QWidget(self.left_content_frame)
        counter_layout = QHBoxLayout(counter_widget)
        counter_layout.setContentsMargins(0, 0, 0, 0)
        counter_layout.setSpacing(5)

        minus_btn = QPushButton("-", counter_widget)
        minus_btn.setFixedSize(32, 32)
        minus_btn.setFont(QFont("Arial", 18, QFont.Bold))

        self.counter_label = QLabel(str(self.chaos_factor), counter_widget)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setFixedWidth(40)
        self.counter_label.setFont(QFont("Arial", 21, QFont.Bold))
        self.counter_label.setStyleSheet("padding: 5px; color: maroon;")

        plus_btn = QPushButton("+", counter_widget)
        plus_btn.setFixedSize(32, 32)
        plus_btn.setFont(QFont("Arial", 18, QFont.Bold))

        counter_layout.addWidget(minus_btn)
        counter_layout.addWidget(self.counter_label)
        counter_layout.addWidget(plus_btn)
        self.center_content_button_layout.addWidget(counter_widget, alignment=Qt.AlignCenter)

        # Counter logic
        def update_counter(delta):
            value = int(self.counter_label.text()) + delta
            self.counter_label.setText(str(value))
            self.chaos_factor_changed.emit(value)

        minus_btn.clicked.connect(lambda: update_counter(-1))
        plus_btn.clicked.connect(lambda: update_counter(1))

    def start_scene_dialog(self):
        dlg = CustomSceneDialog(self)
        result = dlg.exec()
        if result == 1:
            self.start_scene_action_selected.emit("expected_scene_test")
        elif result == 2:
            self.start_scene_action_selected.emit("oracles_tables")
        # No return needed; let the controller/view handle the result

    def test_expected_scene(self, test_expected_scene_table_data):
        dlg = SmallTableDialog(self, test_expected_scene_table_data)
        dlg.show()
        # Simulate async function call (replace with your real function)
        def after_func():
            dice_roll_result = get_dice_roll_result(10)[0]  # Should return 0, 1, or 2
            if dice_roll_result <= self.chaos_factor:
                if dice_roll_result%2 == 0:
                    row_to_highlight = 0
                else:
                    row_to_highlight = 1
            else:
                row_to_highlight = 2

            # dlg.highlight_and_close_signal.connect(self.start_scene_action_resolution)
            dlg.highlight_and_close_signal.connect(lambda action: self.start_scene_action_resolution.emit(action))
            # dlg.highlight_and_close_signal.connect(lambda action: print("Signal received:", action) or self.start_scene_action_resolution.emit(action))
            dlg.highlight_and_close(row_to_highlight)

        QTimer.singleShot(500, after_func)  # Simulate delay; replace as needed
        dlg.exec()

    def end_scene_dialog(self):
        pass

class CustomSceneDialog(QDialog):
    def __init__(self, parent=None):
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

        layout = QVBoxLayout(self)

        button_row = QHBoxLayout()
        self.test_btn = QPushButton("Test the Expected Scene", self)
        self.oracle_btn = QPushButton("Go to Fate Chart / Oracle", self)
        button_row.addWidget(self.test_btn)
        button_row.addWidget(self.oracle_btn)
        layout.addLayout(button_row)

        cancel_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel", self)
        cancel_row.addStretch(1)        
        cancel_row.addWidget(self.cancel_btn)
        cancel_row.addStretch(1)        
        layout.addLayout(cancel_row)

        self.test_btn.clicked.connect(lambda: self.done(1))
        self.oracle_btn.clicked.connect(lambda: self.done(2))
        self.cancel_btn.clicked.connect(lambda: self.done(0))

    def showEvent(self, event):
        super().showEvent(event)
        align_dialog_to_button(self, self.parent())


class SmallTableDialog(QDialog):
    highlight_and_close_signal = Signal(str)

    def __init__(self, parent=None, table_data=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setModal(True)
        self.setFixedSize(490, 275)
        layout = QVBoxLayout(self)

        self.table_data = table_data
        layout.setContentsMargins(0, 0, 0, 0)
        self.table = QTableWidget(3, 2, self)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setStyleSheet("background-color: white; border: 2px solid black;")

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Make columns and rows stretch to fill the dialog
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)
        # Fill with data
        if self.table_data:
            for row, (col1, col2) in enumerate(self.table_data):
                item1 = QTableWidgetItem(str(col1))
                item1.setTextAlignment(Qt.AlignCenter)
                item1.setFont(QFont("Arial", 14))
                item1.setForeground(QColor("black"))  # Black color
                self.table.setItem(row, 0, item1)
                item2 = QTableWidgetItem(str(col2))
                item2.setTextAlignment(Qt.AlignCenter)
                item2.setFont(QFont("Arial", 14))
                item2.setForeground(QColor("black"))  # Black color
                self.table.setItem(row, 1, item2)

    def showEvent(self, event):
        super().showEvent(event)
        align_dialog_to_button(self, self.parent())

    def highlight_and_close(self, row_idx, color="yellow"):
        for col in range(self.table.columnCount()):
            item = self.table.item(row_idx, col)
            if item:
                item.setBackground(QColor(color))
        # self.table.viewport().repaint()

        # Delay closing or emitting the signal
        QTimer.singleShot(1500, lambda: self.trigger_start_scene_action(row_idx))
        QTimer.singleShot(3300, self.accept)  # Or whatever delay you want

    def trigger_start_scene_action(self, row_idx):
        if row_idx == 0:
            # Expected Scene
            self.highlight_and_close_signal.emit("Fate Chart")
        elif row_idx == 1:
            # Altered Scene = Scene Adjustment Table
            self.highlight_and_close_signal.emit("Scene Adjustment Table")
        elif row_idx == 2:
            # Interrupt Scene = Random Event Table
            self.highlight_and_close_signal.emit("Random Event Focus Table")

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
    row_data_edited = Signal(dict)
    close_table = Signal()
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
        close_button.clicked.connect(self.close_table)
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
        # ...inside edited_row_data...
        if self.table_label == "characters":
            # sender is dropdown_cell
            table_cell = None
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break
            if table_cell and sender.currentText():
                data = {
                    "row": row_index,
                    "name": table_cell.text(),
                    "type": sender.currentText()
                }
                self.row_data_edited.emit(data)
                table_cell.clearFocus()
        elif self.table_label == "threads":
            if sender.text():
                data = {
                    "row": row_index,
                    "thread": sender.text()
                }
                self.row_data_edited.emit(data)
                sender.clearFocus()

    def dropdown_selection_handler(self, dropdown_cell, table_cell):
        def handler(index):
            # Only disable if a valid selection is made (not None or empty)
            if dropdown_cell.currentText():
                dropdown_cell.setEnabled(False)
                table_cell.setReadOnly(True)
        return handler
    
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