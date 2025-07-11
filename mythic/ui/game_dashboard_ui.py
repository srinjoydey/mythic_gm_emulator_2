from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QScrollArea, QLineEdit, QComboBox, QListWidget, QListWidgetItem, QDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QIcon, QColor, QPixmap, QPainter, QRadialGradient
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QPropertyAnimation, QEasingCurve, Property, QEvent, QObject
from utils.utils_functions import align_dialog_to_button, get_dice_roll_result


class GameDashboardUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    oracles_tables_button_clicked = Signal()
    characters_button_clicked = Signal()
    threads_button_clicked = Signal()
    gallery_modal_button_clicked = Signal()
    main_menu_button_clicked = Signal()
    existing_stories_button_clicked = Signal()
    chaos_factor_changed = Signal(int)
    start_scene_action_selected = Signal(str)
    start_scene_action_resolution = Signal(str)
    roll_for_chaos_factor = Signal()

    def __init__(self, parent, controller, story_index):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        self.chaos_factor = self.parent().chaos_factor

        # Define background image path (now managed here)
        self.bg_image_path = "visuals/backgrounds/game_dashboard.png"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)

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
            padding-top: 47px;          
        """)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title_label, 0, 0, 2, 6, alignment=Qt.AlignCenter | Qt.AlignVCenter)

        self.chaos_factor_frame = QFrame(self)
        self.chaos_factor_button_layout = QHBoxLayout(self.chaos_factor_frame)
        self.chaos_factor_button_layout.setContentsMargins(0, 0, 0, 25)
        self.layout.addWidget(self.chaos_factor_frame, 2, 0, 1, 6, alignment=Qt.AlignCenter)
        self.create_chaos_factor_counter(self.chaos_factor_frame)

        # Button Frame (Middle-Left placement)
        self.left_content_frame = QFrame(self)
        self.left_content_button_layout = QVBoxLayout(self.left_content_frame)
        self.left_content_button_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.left_content_frame, 3, 0, 2, 2, alignment=Qt.AlignCenter)
        self.create_left_content_buttons()

        # Button Frame (Center)
        self.center_content_frame = QFrame(self)
        self.center_content_button_layout = QVBoxLayout(self.center_content_frame)
        self.center_content_button_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.center_content_frame, 3, 2, 2, 2, alignment=Qt.AlignCenter)
        self.create_center_content_buttons()

        # Button Frame (Middle-Right placement)
        self.right_content_frame = QFrame(self)
        self.right_content_button_layout = QVBoxLayout(self.right_content_frame)
        self.right_content_button_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.right_content_frame, 3, 4, 2, 2, alignment=Qt.AlignCenter)
        self.create_right_content_buttons()

        # Bottom Content Frame (for additional content)
        self.bottom_content_frame = QFrame(self)
        self.bottom_layout = QHBoxLayout(self.bottom_content_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.bottom_content_frame, 5, 0, 4, 6)
        self.create_bottom_content()


    def create_left_content_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        # Define menu buttons dynamically
        signals = [
            ("Oracles / Tables", self.oracles_tables_button_clicked),
            ("Gallery Modal", self.gallery_modal_button_clicked),            
        ]
        button_width, button_height = 250, 60
        button_font_size = 20

        self.left_content_button_layout.setSpacing(15)

        for text, signal in signals:
            btn = QPushButton(text, self.left_content_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(signal.emit)
            self.left_content_button_layout.addWidget(btn)

    def create_center_content_buttons(self):
        button_width, button_height = 265, 60
        button_font_size = 20

        self.center_content_button_layout.setSpacing(15)

        buttons = [
            ("Start a Scene", self.start_scene_dialog),
            ("End a Scene", self.end_scene_dialog),
            ("Edit Chaos Factor", self.show_chaos_factor_buttons),
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
        ]
        button_width, button_height = 250, 60
        button_font_size = 20

        self.right_content_button_layout.setSpacing(15)

        for text, signal in signals:
            btn = QPushButton(text, self.right_content_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(signal.emit)
            self.right_content_button_layout.addWidget(btn)

    def create_bottom_content(self):
        buttons = [
            ("Main Menu", self.main_menu_button_clicked),  
            ("Existing Stories", self.existing_stories_button_clicked),
        ]

        button_width, button_height = 250, 60
        button_font_size = 20

        self.right_content_button_layout.setSpacing(10)

        for text, signal in buttons:
            btn = QPushButton(text, self.right_content_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(signal.emit)
            self.bottom_layout.addWidget(btn)

    def create_chaos_factor_counter(self, parent_widget):
        # --- Counter Widget ---
        counter_widget = QWidget(self.chaos_factor_frame)
        counter_layout = QHBoxLayout(counter_widget)
        counter_layout.setContentsMargins(0, 0, 0, 0)
        counter_layout.setSpacing(5)

        self.minus_btn = QPushButton("-", counter_widget)
        self.minus_btn.setFixedSize(32, 32)
        self.minus_btn.setFont(QFont("Arial", 18, QFont.Bold))

        self.counter_label = HaloLabel(str(self.chaos_factor), counter_widget)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setFixedSize(200, 130)
        self.counter_label.setFont(QFont("Arial", 23, QFont.Bold))
        self.counter_label.setStyleSheet("padding: 8px; color: maroon;")

        self.plus_btn = QPushButton("+", counter_widget)
        self.plus_btn.setFixedSize(32, 32)
        self.plus_btn.setFont(QFont("Arial", 18, QFont.Bold))

        counter_layout.addWidget(self.minus_btn)
        counter_layout.addWidget(self.counter_label)
        counter_layout.addWidget(self.plus_btn)
        self.chaos_factor_button_layout.addWidget(counter_widget, alignment=Qt.AlignCenter)

        # Counter logic
        def update_counter(delta):
            value = int(self.counter_label.text()) + delta
            self.counter_label.setText(str(value))
            self.chaos_factor = value
            self.chaos_factor_changed.emit(value)
            

        self.minus_btn.clicked.connect(lambda: update_counter(-1))
        self.plus_btn.clicked.connect(lambda: update_counter(1))
        self.minus_btn.setVisible(False)
        self.plus_btn.setVisible(False)

    def start_scene_dialog(self):
        button_labels = ["Test the Expected Scene", "Go to Fate Chart / Oracle", "Cancel"]
        dlg = OptionsWithCancelDialog(self, button_labels)
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
            dlg.highlight_and_close(row_to_highlight)

        QTimer.singleShot(500, after_func)  # Simulate delay; replace as needed
        dlg.exec()

    def end_scene_dialog(self):
        self.roll_for_chaos_factor.emit()

    def show_chaos_factor_roll_result(self, colour):
        QTimer.singleShot(3500, lambda: self.counter_label.set_halo(False))
        QTimer.singleShot(1500, lambda: self.counter_label.set_halo(True, colour))

    def show_chaos_factor_buttons(self):
        self.minus_btn.setVisible(True)
        self.plus_btn.setVisible(True)

        # Cancel any previous timer
        if hasattr(self, "_chaos_factor_hide_timer") and self._chaos_factor_hide_timer is not None:
            self._chaos_factor_hide_timer.stop()

        # Helper to hide buttons
        def hide_buttons():
            self.minus_btn.setVisible(False)
            self.plus_btn.setVisible(False)

        # Store the timer as an attribute so it can be restarted
        self._chaos_factor_hide_timer = QTimer(self)
        self._chaos_factor_hide_timer.setSingleShot(True)
        self._chaos_factor_hide_timer.timeout.connect(hide_buttons)
        self._chaos_factor_hide_timer.start(5000)  # 5 seconds

        # Restart timer on button press
        def restart_timer():
            self._chaos_factor_hide_timer.start(5000)

        self.minus_btn.clicked.connect(restart_timer)
        self.plus_btn.clicked.connect(restart_timer)


class OptionsWithCancelDialog(QDialog):
    def __init__(self, parent=None, button_labels_list=None):
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

        self.button_1_label = button_labels_list[0]
        self.button_2_label = button_labels_list[1]

        layout = QVBoxLayout(self)

        button_row = QHBoxLayout()
        self.button_1 = QPushButton(self.button_1_label, self)
        self.button_2 = QPushButton(self.button_2_label, self)
        button_row.addWidget(self.button_1)
        button_row.addWidget(self.button_2)
        layout.addLayout(button_row)

        cancel_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel", self)
        cancel_row.addStretch(1)        
        cancel_row.addWidget(self.cancel_btn)
        cancel_row.addStretch(1)        
        layout.addLayout(cancel_row)

        self.button_1.clicked.connect(lambda: self.choose_and_accept(self.button_1_label))
        self.button_2.clicked.connect(lambda: self.choose_and_accept(self.button_2_label))
        self.cancel_btn.clicked.connect(lambda: self.choose_and_accept(None))

        if self.button_2_label == "Cancel":
            self.cancel_btn.setVisible(False)

    def showEvent(self, event):
        super().showEvent(event)
        align_dialog_to_button(self, self.parent())

    def choose_and_accept(self, label):
        self.selected_label = label
        self.accept()


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
    clear_all_rows = Signal()
    search_for_suggestions = Signal(dict)
    row_clicked = Signal(dict)
    section_label_double_clicked = Signal(int, str)

    def __init__(self, parent, controller, table_label, story_index, existing_data):
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
        clear_all_button = QPushButton(close_row_container)
        clear_all_button.setIcon(QIcon("assets/icons/close_icon.png"))
        clear_all_button.setIconSize(QSize(25, 25))
        clear_all_button.setFont(QFont("Arial", 14, QFont.Bold))
        clear_all_button.setStyleSheet("""
            padding: 0px;
            background-color: white;
            color: maroon;
        """)

        close_button.clicked.connect(self.close_table)
        # clear_all_button.clicked.connect(self.clear_all_rows)
        clear_all_button.clicked.connect(self.clear_all_rows_confirmation)
        close_row_layout = QHBoxLayout(close_row_container)
        close_row_layout.addWidget(clear_all_button, alignment=Qt.AlignLeft)
        close_row_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(70, 30, 90, 5)
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

        for section_idx, section_label in enumerate(section_labels):
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
            section_label_widget.setProperty("row_index", 1 + section_idx * 5)
            scroll_layout.addWidget(section_label_widget, row_index, 0, 5, 3)

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
                row_label.setProperty("row_index", row_index)
                row_label.setProperty("original_stylesheet", row_label.styleSheet())
                scroll_layout.addWidget(row_label, row_index, 3, 1, 3)

                clear_out_row_button = ClickableLabel(scroll_widget)
                clear_out_row_button.setFixedSize(28, 28)
                clear_out_row_button.setAlignment(Qt.AlignCenter)
                clear_out_row_button.setCursor(Qt.PointingHandCursor)
                icon_pixmap = QPixmap("assets/icons/close_icon.png")
                clear_out_row_button.setPixmap(icon_pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))

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
                table_cell.setProperty("original_stylesheet", table_cell.styleSheet())

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
                    dropdown_cell.setProperty("original_stylesheet", dropdown_cell.styleSheet())

                    if row_index in rows_to_be_updated:
                        table_cell.setText(self.existing_data[row_index]["name"])
                        dropdown_cell.setCurrentText(self.existing_data[row_index]["type"])

                    # --- Editable logic ---
                    section_label_widget.mouseDoubleClickEvent = self.make_section_label_double_click_handler(section_label_widget)
                    row_label.mousePressEvent = self.make_table_cell_mouse_press_handler(table_cell, dropdown_cell)
                    table_cell.mousePressEvent = self.make_table_cell_mouse_press_handler(table_cell, dropdown_cell)
                    table_cell.mouseDoubleClickEvent = self.make_table_cell_mouse_double_click_handler(table_cell, dropdown_cell)
                    table_cell.textEdited.connect(self.debounced_emit_search_for_suggestions)
                    table_cell.editingFinished.connect(self.finish_edit_handler(table_cell, dropdown_cell))
                    dropdown_cell.currentIndexChanged.connect(self.edited_row_data)
                    dropdown_cell.currentIndexChanged.connect(self.dropdown_selection_handler(dropdown_cell, table_cell))

                    scroll_layout.addWidget(dropdown_cell, row_index, 16, 1, 3)

                elif self.table_label == "threads":
                    table_cell = ThreadLineEdit(scroll_widget)
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
                    table_cell.setProperty("original_stylesheet", table_cell.styleSheet())

                    if row_index in rows_to_be_updated:
                        table_cell.setText(self.existing_data[row_index]["thread"])

                    section_label_widget.mouseDoubleClickEvent = self.make_section_label_double_click_handler(section_label_widget)
                    row_label.mousePressEvent = self.make_table_cell_mouse_press_handler(table_cell)
                    table_cell.mousePressEvent = self.make_table_cell_mouse_press_handler(table_cell)
                    table_cell.mouseDoubleClickEvent = self.make_table_cell_mouse_double_click_handler(table_cell)
                    table_cell.textEdited.connect(self.debounced_emit_search_for_suggestions)
                    table_cell.enter_or_escape_pressed.connect(self.edited_row_data)

                clear_out_row_button.clicked.connect(lambda row=row_index: self.emit_deleted_row_data(row))
                scroll_layout.addWidget(clear_out_row_button, row_index, 6, 1, 1)
                if self.table_label == "characters":
                    scroll_layout.addWidget(table_cell, row_index, 7, 1, 9)
                else:
                    scroll_layout.addWidget(table_cell, row_index, 7, 1, 12)
                row_index += 1

        scroll_area.setWidget(scroll_widget)
        table_container_layout.addWidget(scroll_area)
        self.layout.addWidget(table_container)
        self.setLayout(self.layout)

        # --- Hide any FocusLineEdit cells from ThreadsList if present (after UI is built) ---
        if self.table_label == "threads":
            for le in self.scroll_widget.findChildren(FocusLineEdit):
                le.setVisible(False)


    def make_table_cell_mouse_press_handler(self, table_cell, dropdown_cell=None):
        def handler(event):
            # Start a single-click timer; if double-click occurs, timer will be stopped
            if not hasattr(self, "_single_click_timers"):
                self._single_click_timers = {}
            # Stop any existing timer for this cell
            timer = self._single_click_timers.get(table_cell)
            if timer:
                timer.stop()
            # Create a new timer for this cell
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self._on_table_cell_single_click(table_cell, dropdown_cell))
            self._single_click_timers[table_cell] = timer
            timer.start(250)  # 250 ms is a typical double-click interval
        return handler

    def make_table_cell_mouse_double_click_handler(self, table_cell, dropdown_cell=None):
        def handler(event):
            # If a single-click timer is running, stop it (so single-click won't fire)
            if hasattr(self, "_single_click_timers"):
                timer = self._single_click_timers.get(table_cell)
                if timer:
                    timer.stop()
            # Now handle double-click logic
            self._on_table_cell_double_click(table_cell, dropdown_cell)
        return handler

    def make_section_label_double_click_handler(self, section_label_widget):
        def handler(event):
            # Find the last row_index with data in any table_cell
            last_row_with_data = None
            for le in self.scroll_widget.findChildren(QLineEdit):
                row_idx = le.property("row_index")
                if le.text().strip():
                    last_row_with_data = row_idx

            if last_row_with_data is not None:
                # Find the section label text for this row
                section_label_text = None
                for section_label in self.scroll_widget.findChildren(QLabel):
                    # Only consider section labels (not row labels)
                    if section_label.property("row_index") is not None:
                        start_row = section_label.property("row_index")
                        if start_row <= last_row_with_data < start_row + 5:
                            section_label_text = section_label.text()
                            break
                if section_label_text is not None:
                    self.section_label_double_clicked.emit(last_row_with_data, section_label_text)
        return handler

    def _on_table_cell_single_click(self, table_cell, dropdown_cell=None):
        # Your single-click logic here (was in row_click_handler)
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

    def _on_table_cell_double_click(self, table_cell, dropdown_cell=None):
        # Your double-click logic here (was in double_click_handler)
        if table_cell.isReadOnly():
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
        self.debounce_timers[sender].start(1200)

    def show_suggestions_popup(self, table_cell, suggestions):
            # Remove old popup if any
            if hasattr(self, "_suggestions_popup") and self._suggestions_popup is not None:
                try:
                    self._suggestions_popup.close()
                except RuntimeError:
                    pass
                self._suggestions_popup = None

            if not suggestions:
                return

            popup = QListWidget(self)
            popup.setAttribute(Qt.WA_DeleteOnClose)
            popup.setWindowFlags(Qt.Popup)
            popup.setFocusPolicy(Qt.NoFocus)
            popup.setStyleSheet("background: #fffbe6; color: #800000; font-size: 16px; border: 1px solid #800000;")
            for id, name in suggestions:
                item = QListWidgetItem(name)
                popup.addItem(item)

            pos = table_cell.mapToGlobal(table_cell.rect().bottomLeft())
            popup.move(pos)
            popup.setFixedWidth(table_cell.width())
            popup.show()
            self._suggestions_popup = popup

            # Ensure _suggestions_popup is set to None when popup is destroyed
            popup.destroyed.connect(lambda: setattr(self, "_suggestions_popup", None))

            def on_item_clicked(item):
                table_cell.setText(item.text())
                popup.close()
                # self._suggestions_popup = None  # Not needed, handled by destroyed signal

            popup.itemClicked.connect(on_item_clicked)

            class PopupEventFilter(QObject):
                def __init__(self, popup, table_cell):
                    super().__init__(popup)
                    self.table_cell = table_cell

                def eventFilter(self, obj, event):
                    if event.type() == QEvent.KeyPress:
                        cursor_pos = self.table_cell.cursorPosition()
                        # If Escape or Enter, close popup and return focus/cursor
                        if event.key() == Qt.Key_Escape or event.key() in (Qt.Key_Return, Qt.Key_Enter):
                            popup.close()
                            self.table_cell.setFocus()
                            self.table_cell.setCursorPosition(cursor_pos)
                            return True
                        # If it's a printable character or Backspace, close popup, focus cell, and type
                        if (event.text() and event.text().isprintable()) or event.key() == Qt.Key_Backspace:
                            popup.close()
                            self.table_cell.setFocus()
                            text = self.table_cell.text()
                            if event.key() == Qt.Key_Backspace:
                                # Remove character before cursor if possible
                                if cursor_pos > 0:
                                    new_text = text[:cursor_pos-1] + text[cursor_pos:]
                                    self.table_cell.setText(new_text)
                                    self.table_cell.setCursorPosition(cursor_pos - 1)
                                else:
                                    # Nothing to delete, just keep cursor at start
                                    self.table_cell.setCursorPosition(0)
                            else:
                                new_text = text[:cursor_pos] + event.text() + text[cursor_pos:]
                                self.table_cell.setText(new_text)
                                self.table_cell.setCursorPosition(cursor_pos + 1)
                            return True
                    if event.type() == QEvent.MouseButtonPress:
                        if not popup.rect().contains(event.pos()):
                            popup.close()
                            self.table_cell.setFocus()
                            return True
                    return False

            filter = PopupEventFilter(popup, table_cell)
            popup.installEventFilter(filter)

    def finish_edit_handler(self, table_cell, dropdown_cell=None):
        def handler():
            table_cell.setReadOnly(True)
        return handler

    def edited_row_data(self):
        sender = self.sender()
        row_index = sender.property("row_index")
        table_cell = None

        if self.table_label == "characters":
            # Find the table_cell and dropdown_cell for this row
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break
            if table_cell and sender.currentText():
                data = {
                    "row": row_index,
                    "name": table_cell.text(),
                    "type": sender.currentText(),
                    "master_id": self.existing_data[row_index]["master_id"] if row_index in self.existing_data else None
                }
                self.row_data_edited.emit(data)
                table_cell.clearFocus()
        elif self.table_label == "threads":
            # Find the table_cell for this row
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break
            if table_cell and sender.text():
                data = {
                    "row": row_index,
                    "thread": sender.text(),
                    "master_id": self.existing_data[row_index]["master_id"] if row_index in self.existing_data else None
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

    def prompt_deletion_type(self):
        button_labels = ["Delete from Story", "Delete from Game"]
        dlg = OptionsWithCancelDialog(self, button_labels)
        result = dlg.exec()
        if result == QDialog.Accepted:
            return dlg.selected_label

    def prompt_duplicate_action(self, name):
        dlg = DuplicateListItemDialog(self)
        result = dlg.exec()
        if result == QDialog.Accepted:
            return dlg.selected_label

    def emit_deleted_row_data(self, row_index):
        # Prepare the data dict as in edited_row_data
        if self.table_label == "characters":
            # Find the table_cell and dropdown_cell for this row
            table_cell = None
            dropdown_cell = None
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break
            for cb in self.scroll_widget.findChildren(QComboBox):
                if cb.property("row_index") == row_index:
                    dropdown_cell = cb
                    break
            if table_cell and dropdown_cell:
                data = {
                    "row": row_index,
                    "name": table_cell.text(),
                    "type": dropdown_cell.currentText(),
                    "master_id": self.existing_data[row_index]["master_id"] if row_index in self.existing_data else None,
                    "action": "delete"
                }
                self.row_data_edited.emit(data)
        elif self.table_label == "threads":
            table_cell = None
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break
            if table_cell:
                data = {
                    "row": row_index,
                    "thread": table_cell.text(),
                    "master_id": self.existing_data[row_index]["master_id"] if row_index in self.existing_data else None,
                    "action": "delete"
                }
                self.row_data_edited.emit(data)

    def highlight_rolled_row(self, section_label_result, row_label_result):
        def clear_highlights():
            for row_label in self.scroll_widget.findChildren(ClickableLabel):
                orig = row_label.property("original_stylesheet")
                if orig:
                    row_label.setStyleSheet(orig)
            for le in self.scroll_widget.findChildren(QLineEdit):
                orig = le.property("original_stylesheet")
                if orig:
                    le.setStyleSheet(orig)
            for cb in self.scroll_widget.findChildren(QComboBox):
                orig = cb.property("original_stylesheet")
                if orig:
                    cb.setStyleSheet(orig)

        def highlight_row_in_section(section_label_str, row_label_str):
            highlight_override = "background-color: #ffe066; color: black;"
            # Find the section's starting row index
            section_start_row = None
            for section_label in self.scroll_widget.findChildren(QLabel):
                if section_label.property("row_index") is not None and section_label.text() == section_label_str:
                    section_start_row = section_label.property("row_index")
                    break
            if section_start_row is None:
                return  # Section not found

            # Find the row index for the row_label_str in this section
            target_row_index = None
            for i in range(5):
                row_idx = section_start_row + i
                for row_label in self.scroll_widget.findChildren(ClickableLabel):
                    if row_label.property("row_index") == row_idx and row_label.text() == row_label_str:
                        # Highlight the row label
                        orig = row_label.property("original_stylesheet")
                        if orig:
                            row_label.setStyleSheet(orig + highlight_override)
                        else:
                            row_label.setStyleSheet(highlight_override)
                        target_row_index = row_idx
                        break
                if target_row_index is not None:
                    break

            if target_row_index is None:
                return  # Row label not found in section

            # Highlight the table cell for this row
            for le in self.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == target_row_index:
                    orig = le.property("original_stylesheet")
                    if orig:
                        le.setStyleSheet(orig + highlight_override)
                    else:
                        le.setStyleSheet(highlight_override)
            # Highlight dropdown cell (if present)
            for cb in self.scroll_widget.findChildren(QComboBox):
                if cb.property("row_index") == target_row_index:
                    orig = cb.property("original_stylesheet")
                    if orig:
                        cb.setStyleSheet(orig + highlight_override)
                    else:
                        cb.setStyleSheet(highlight_override)

        # Only use the first section_label_result (per your requirement)
        if isinstance(section_label_result, (list, tuple)):
            section_label_str = section_label_result[0]
        else:
            section_label_str = section_label_result

        # Ensure row_label_result is a list
        if not isinstance(row_label_result, (list, tuple)):
            row_label_result = [row_label_result]

        # Only highlight rows within the section
        valid_row_labels = []
        # Find the 5 row_labels in this section
        section_start_row = None
        for section_label in self.scroll_widget.findChildren(QLabel):
            if section_label.property("row_index") is not None and section_label.text() == section_label_str:
                section_start_row = section_label.property("row_index")
                break
        section_row_labels = []
        if section_start_row is not None:
            for i in range(5):
                row_idx = section_start_row + i
                for row_label in self.scroll_widget.findChildren(ClickableLabel):
                    if row_label.property("row_index") is not None and row_label.text().strip():
                        if row_label.property("row_index") == row_idx:
                            section_row_labels.append(row_label.text())
                            break

        # Only keep row_label_results that are present in this section
        for r in row_label_result:
            if r in section_row_labels:
                valid_row_labels.append(r)

        # If nothing to highlight, return
        if not valid_row_labels:
            return

        self._highlight_sequence = valid_row_labels
        self._highlight_sequence_pos = 0

        def highlight_next():
            clear_highlights()
            highlight_row_in_section(section_label_str, self._highlight_sequence[self._highlight_sequence_pos])
            self._highlight_sequence_pos += 1
            if self._highlight_sequence_pos < len(self._highlight_sequence):
                QTimer.singleShot(1200, highlight_next)
            # Keep the last highlight (do not clear after last)

        highlight_next()

    def clear_all_rows_confirmation(self):
        """Prompts the user to confirm clearing all rows."""
        button_labels = ["Clear All Rows", "Cancel"]
        dlg = OptionsWithCancelDialog(self, button_labels)
        result = dlg.exec()
        if result == QDialog.Accepted and dlg.selected_label == "Clear All Rows":
            self.clear_all_rows.emit()

class ThreadLineEdit(QLineEdit):
    enter_or_escape_pressed = Signal()
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Escape):
            self.enter_or_escape_pressed.emit()
        super().keyPressEvent(event)
    
class DuplicateListItemDialog(QDialog):
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
                min-width: 165px;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 20, 20, 15)

        first_button_row = QHBoxLayout()
        first_button_row.setSpacing(15)
        self.create_new_btn = QPushButton("Create New", self)
        self.select_existing_btn = QPushButton("Select Existing", self)
        first_button_row.addWidget(self.create_new_btn)
        first_button_row.addWidget(self.select_existing_btn)
        layout.addLayout(first_button_row)

        second_button_row = QHBoxLayout()
        second_button_row.setSpacing(15)
        self.remove_entry_btn = QPushButton("Remove Entry", self)
        self.overwrite_existing_btn = QPushButton("Overwrite Existing", self)
        second_button_row.addStretch(1)        
        second_button_row.addWidget(self.remove_entry_btn)
        second_button_row.addWidget(self.overwrite_existing_btn)
        second_button_row.addStretch(1)        
        layout.addLayout(second_button_row)

        self.create_new_btn.clicked.connect(lambda: self.duplicate_entry_action(self.create_new_btn.text()))
        self.select_existing_btn.clicked.connect(lambda: self.duplicate_entry_action(self.select_existing_btn.text()))
        self.remove_entry_btn.clicked.connect(lambda: self.duplicate_entry_action(self.remove_entry_btn.text()))
        self.overwrite_existing_btn.clicked.connect(lambda: self.duplicate_entry_action(self.overwrite_existing_btn.text()))

    def duplicate_entry_action(self, label):
        self.selected_label = label  # Store the label if you want to access it after exec()
        self.accept()


class HaloLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.halo_enabled = False
        self._halo_colour = QColor(255, 255, 255, 180)  # Start as white
        self._target_colour = QColor(255, 255, 255, 180)
        self._animation = None

    def set_halo(self, enabled=True, colour=None):
        self.halo_enabled = enabled
        if enabled and colour is not None:
            # Animate from white to the target colour
            if not isinstance(colour, QColor):
                colour = QColor(colour)
            self._target_colour = colour
            self._start_colour_animation()
        else:
            self._halo_colour = QColor(255, 255, 255, 180)
            self.update()
        self.update()  # Trigger repaint

    def _get_halo_colour(self):
        return self._halo_colour

    def _set_halo_colour(self, colour):
        self._halo_colour = colour
        self.update()

    halo_colour = Property(QColor, _get_halo_colour, _set_halo_colour)

    def _start_colour_animation(self):
        if self._animation:
            self._animation.stop()
        self._animation = QPropertyAnimation(self, b"halo_colour")
        self._animation.setDuration(2700)
        self._animation.setStartValue(QColor(255, 255, 255, 180))
        self._animation.setEndValue(self._target_colour)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._animation.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.halo_enabled:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            center = self.rect().center()
            rx = int(self.width() * 0.51)
            ry = int(self.height() * 0.41)
            inner_radius_ratio = 0.91

            painter.save()
            painter.translate(center)
            painter.scale(rx / max(rx, ry), ry / max(rx, ry))
            gradient = QRadialGradient(0, 0, max(rx, ry))
            gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
            gradient.setColorAt(inner_radius_ratio, self._halo_colour)
            gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(-max(rx, ry), -max(rx, ry), 2 * max(rx, ry), 2 * max(rx, ry))
            painter.restore()