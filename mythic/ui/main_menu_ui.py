from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFrame, QSizePolicy, QLineEdit, QTextEdit, QHBoxLayout, QScrollArea, QMessageBox, QDialog)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, Signal, QTimer, QSize, Slot
from views.game_dashboard import GameDashboardView
import warnings


# To suppress RuntimeWarning that arises when disconnecting signals that may not have been connected in ln 350
warnings.filterwarnings("ignore", category=RuntimeWarning)


class MainMenuUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    new_story_btn_clicked = Signal()
    existing_story_btn_clicked = Signal()
    oracles_tables_btn_clicked = Signal()
    gallery_btn_clicked = Signal()
    artifacts_btn_clicked = Signal()

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Define background image path (now managed here)
        self.bg_image_path = "visuals/backgrounds/main_menu.jpg"

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
        # Define menu buttons dynamically
        self.buttons = [
            ("New Story", self.new_story_btn_clicked),
            ("Existing Story", self.existing_story_btn_clicked),
            ("Oracles / Tables", self.oracles_tables_btn_clicked),
            ("Gallery", self.gallery_btn_clicked),
            ("Artifacts", self.artifacts_btn_clicked),
        ]
        button_width, button_height = 250, 60
        button_font_size = 20

        for text, signal in self.buttons:
            btn = QPushButton(text, self.button_frame)
            btn.setFont(QFont("Arial", button_font_size))
            btn.setMinimumSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(signal)
            self.button_layout.addWidget(btn)


class NewStoryUI(QWidget):
    """UI Layout for New Story screen."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.bg_image_path = "visuals/backgrounds/new_story.jpg"

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

        # Create Title Input
        self.title_label_widget = QLabel("Title / Label", self.text_frame)
        self.title_label_widget.setFont(QFont("Arial", 17))
        self.title_label_widget.setStyleSheet("color: black; font-weight: bold;")

        self.title_input = QLineEdit(self.text_frame)
        self.title_input.setFont(QFont("Arial", 15))
        self.title_input.setPlaceholderText("Enter title...")
        self.title_input.setStyleSheet("padding: 10px; font-style: italic;")

        # **Error Label (Initially Hidden)**
        self.title_error_label = QLabel("Title is required!", self.text_frame)
        self.title_error_label.setFont(QFont("Arial", 14))
        self.title_error_label.setStyleSheet("color: maroon; font-weight: bold;")
        self.title_error_label.setVisible(False)  # Hidden initially

        # **Description Input (Always Active)**
        self.description_label_widget = QLabel("Description", self.text_frame)
        self.description_label_widget.setFont(QFont("Arial", 17))
        self.description_label_widget.setStyleSheet("color: black; font-weight: bold;")

        self.description_input = QTextEdit(self.text_frame)
        self.description_input.setFont(QFont("Arial", 15))
        self.description_input.setPlaceholderText("Enter description...")
        self.description_input.setStyleSheet("padding: 10px; font-style: italic;")

        # Add widgets to layout
        self.text_layout.addWidget(self.title_label_widget)
        self.text_layout.addWidget(self.title_input)
        self.text_layout.addWidget(self.title_error_label)  # Error label beneath title        
        self.text_layout.addSpacing(50)  
        self.text_layout.addWidget(self.description_label_widget)
        self.text_layout.addWidget(self.description_input)

        self.layout.addWidget(self.text_frame, 1, 2, 3, 3)

        # **Button Section**
        self.button_frame = QFrame(self)
        self.button_layout = QVBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(0, 100, 0, 20)
        self.layout.addWidget(self.button_frame, 3, 1, 1, 2, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.create_buttons()

    def create_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        from views.main_menu import MainMenu

        # Create buttons
        create_btn = QPushButton("Create", self.button_frame)
        create_btn.setFont(QFont("Arial", 20))
        create_btn.setMinimumSize(250, 60)
        create_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        create_btn.clicked.connect(self.validate_and_submit)

        back_btn = QPushButton("Back", self.button_frame)
        back_btn.setFont(QFont("Arial", 20))
        back_btn.setMinimumSize(250, 60)
        back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_btn.clicked.connect(lambda checked: self.controller.show_view(MainMenu))

        # Add buttons to layout
        self.button_layout.addWidget(create_btn)
        self.button_layout.addSpacing(10)  # Add space between buttons
        self.button_layout.addWidget(back_btn)

    def validate_and_submit(self):
        """Validates title and submits data only if valid."""
        title_text = self.title_input.text().strip()
        description_text = self.description_input.toPlainText().strip()

        if not title_text:  # If title is empty, show error
            self.title_error_label.setVisible(True)
            return  # Stop execution without submitting

        # Hide error if title is valid
        self.title_error_label.setVisible(False)

        # Send data
        data = {
            "title": title_text,
            "description": description_text
        }
        self.controller.current_view.validate_new_story_data_setup_tables(data)

    def display_error_message(self, message):
        """Displays an error message under the title input."""
        self.title_error_label.setText(message)
        self.title_error_label.setVisible(True)  # Show the error message

    def navigate_to_game_dashboard(self, index_value):
        """Navigates to GameDashboardUI, passing the index value."""
        from views.game_dashboard import GameDashboardView

        # Pass index value to GameDashboardUI or GameDashboardView
        self.controller.show_view(GameDashboardView, story_index=index_value)


class ExistingStoryUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    select_btn_clicked = Signal(int)
    story_name_description_edited = Signal(int, str, str)
    delete_btn_clicked = Signal(int)
    back_btn_clicked = Signal()

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.existing_stories_data = parent.existing_stories_data
        self.button_mapping = {}
        self.selected_button = None

        # Define background image path (now managed here)
        self.bg_image_path = "visuals/backgrounds/main_menu.jpg"

        # Configure grid layout dynamically
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)

        # Title Label (Centered)
        self.title_label = QLabel("Existing Stories", self)
        self.title_label.setFont(QFont("Arial", 28))
        # Apply transparent background
        self.title_label.setStyleSheet("""
            background-color: transparent;
            padding: 0px;
            color: maroon;
            font-weight: bold;
            font-style: italic;            
        """)
        self.title_label.setContentsMargins(75, 0, 0, 0) 
        self.layout.addWidget(self.title_label, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        # Select Button Frame (Middle Left placement)
        self.select_button_frame = QFrame(self)
        self.select_button_layout = QVBoxLayout(self.select_button_frame)
        self.select_button_layout.setContentsMargins(75, 35, 0, 0)
        # self.layout.addWidget(self.select_button_frame, 1, 0, 3, 4, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.select_button_frame, 1, 0, 3, 1)

        # Description Frame (Middle Right placement)
        self.description_frame = QFrame(self)
        self.description_layout = QVBoxLayout(self.description_frame)
        self.description_layout.setContentsMargins(50, 35, 0, 0)
        self.layout.addWidget(self.description_frame, 1, 1, 3, 3)

        # Back Button Frame (Bottom Left placement)
        self.back_button_frame = QFrame(self)
        self.back_button_layout = QHBoxLayout(self.back_button_frame)
        self.back_button_layout.setContentsMargins(162, 0, 0, 0)  # Match left margin with select buttons
        self.back_button_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addWidget(self.back_button_frame, 4, 0, 2, 1, alignment=Qt.AlignLeft)

        # Action Button Frame (Bottom Right placement)
        self.action_button_frame = QFrame(self)
        self.action_button_layout = QHBoxLayout(self.action_button_frame)
        self.action_button_layout.setContentsMargins(50, 0, 0, 0)
        self.action_button_layout.setSpacing(50)
        self.layout.addWidget(self.action_button_frame, 4, 1, 2, 3, alignment=Qt.AlignLeft)

        self.create_buttons()      

    def create_buttons(self):
        """Creates buttons dynamically with optimized layout."""
        # Select Buttons and Descriptions
        self.select_buttons = []
        for index_data, story_data in self.existing_stories_data.items():
            self.select_buttons.append((index_data, story_data['story_name'], story_data['description']))
        select_button_width, select_button_height = 380, 65
        select_button_font_size = 18

        for index_value, story_title, story_description in self.select_buttons:
            btn = QPushButton(story_title, self.select_button_frame)
            btn.setFont(QFont("Arial", select_button_font_size))
            btn.setFixedSize(select_button_width, select_button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 0px;
                }
            """)
            self.select_button_layout.addWidget(btn)

            if story_description == None:
                story_description = " "
            description = QLabel(story_description, self.description_frame)
            description.setWordWrap(True)
            description.setFont(QFont("Arial", 14))
            description.setFixedSize(select_button_width * 2, select_button_height)
            description.setStyleSheet("""
                QLabel {
                    color: black;
                }
            """)
            self.description_layout.addWidget(description)

            self.button_mapping[btn] = index_value

        for btn, index_value in self.button_mapping.items():
            btn.clicked.connect(lambda checked, button=btn, index=index_value: self.highlighted_button(button, story_index=index))

        # Action Buttons
        self.action_buttons = ["Select", "Edit", "Delete"]
        action_button_width, action_button_height = 210, 45
        action_button_font_size = 16

        for label in self.action_buttons:
            btn = QPushButton(label, self.action_button_frame)
            btn.setFont(QFont("Arial", action_button_font_size))
            btn.setMinimumSize(action_button_width, action_button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setVisible(False)  # Hide by default
            self.action_button_layout.addWidget(btn)
            # Store reference for later
            if not hasattr(self, 'action_button_widgets'):
                self.action_button_widgets = []
            self.action_button_widgets.append(btn)

        # Back Button
        self.back_button = QPushButton("Back", self.back_button_frame)
        self.back_button.setFont(QFont("Arial", action_button_font_size))
        self.back_button.setFixedSize(action_button_width, action_button_height)
        self.back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.back_button_layout.addWidget(self.back_button)
        self.back_button.clicked.connect(lambda checked: self.back_btn_clicked.emit())

    def highlighted_button(self, button, story_index):
        if self.selected_button:
            # Reset previous button style
            self.selected_button.setStyleSheet("")
        # Highlight the selected button
        button.setStyleSheet("""
            padding: 10px;
            color: white;
            background-color: #0078d7;  /* Highlight color */
            font-weight: bold;
        """)
        self.selected_button = button
        self.selected_button_story_index = story_index
        # Show action buttons when a story is highlighted
        for btn in getattr(self, 'action_button_widgets', []):
            btn.setVisible(True)
        self.assign_button_actions()

    def assign_button_actions(self):
        if self.action_buttons[0] == "Select":
            self.action_button_widgets[0].clicked.connect(self.on_select_clicked)
        if self.action_buttons[1] == "Edit":
            try:
                self.action_button_widgets[1].clicked.disconnect(self.on_edit_clicked)
            except TypeError:
                pass
            self.action_button_widgets[1].clicked.connect(self.on_edit_clicked)
        if self.action_buttons[2] == "Delete":
            self.action_button_widgets[2].clicked.connect(self.on_delete_clicked)

    @Slot()
    def on_select_clicked(self):
        self.select_btn_clicked.emit(self.selected_button_story_index)

    @Slot()
    def on_edit_clicked(self):
        self.prompt_edit_story(self.selected_button_story_index)

    @Slot()
    def on_delete_clicked(self):
        self.delete_btn_clicked.emit(self.selected_button_story_index)

    def prompt_edit_story(self, story_index):
        # Get the current story data
        story_data = self.existing_stories_data[story_index]

        # Create a dialog for editing
        dialog = QDialog(self)
        dialog.setFixedSize(770, 380)
        dialog.setStyleSheet("""
            background-color: #444;
        """)
        dialog.setWindowTitle("Edit Story")
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 15, 30, 15)  # Wider margins for the dialog

        # --- Title / Label Input ---
        title_label_widget = QLabel("Title / Label", dialog)
        title_label_widget.setFont(QFont("Arial", 14))
        title_label_widget.setStyleSheet("color: black; font-weight: bold;")
        layout.addWidget(title_label_widget)

        title_input = QLineEdit(dialog)
        title_input.setFont(QFont("Arial", 13))
        title_input.setPlaceholderText("Enter title...")
        title_input.setText(story_data['story_name'])
        title_input.setStyleSheet("padding: 10px; font-style: italic;")
        title_input.setFixedWidth(700)
        layout.addWidget(title_input)

        # --- Error Label (Initially Hidden) ---
        title_error_label = QLabel("Title is required!", dialog)
        title_error_label.setFont(QFont("Arial", 11))
        title_error_label.setStyleSheet("color: maroon; font-weight: bold;")
        title_error_label.setVisible(False)
        layout.addWidget(title_error_label)

        # --- Description Input ---
        description_label_widget = QLabel("Description", dialog)
        description_label_widget.setFont(QFont("Arial", 14))
        description_label_widget.setStyleSheet("color: black; font-weight: bold;")
        layout.addWidget(description_label_widget)

        description_input = QTextEdit(dialog)
        description_input.setFont(QFont("Arial", 13))
        description_input.setPlaceholderText("Enter description...")
        description_input.setText(story_data['description'])
        description_input.setStyleSheet("padding: 10px; font-style: italic;")
        description_input.setFixedSize(700, 147)
        layout.addWidget(description_input)

        # --- Button Row (Update & Cancel) ---
        button_row = QHBoxLayout()
        button_row.addStretch(1)

        update_btn = QPushButton("Update", dialog)
        update_btn.setFont(QFont("Arial", 13))
        update_btn.setFixedSize(110, 36)
        button_row.addWidget(update_btn)

        cancel_btn = QPushButton("Cancel", dialog)
        cancel_btn.setFont(QFont("Arial", 13))
        cancel_btn.setFixedSize(110, 36)
        button_row.addWidget(cancel_btn)

        button_row.addStretch(1)
        layout.addLayout(button_row)

        # --- Validation and Logic ---
        def on_update():
            title_text = title_input.text().strip()
            description_text = description_input.toPlainText().strip()
            if not title_text:
                title_error_label.setVisible(True)
                return
            title_error_label.setVisible(False)
            # Update the story data
            dialog.accept()
            self.story_name_description_edited.emit(story_index, title_text, description_text)

        update_btn.clicked.connect(on_update)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.setLayout(layout)

        if dialog.exec():
            # Optionally refresh your UI here
            pass

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
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

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

    def render_fate_chart(self, nav_item, table):
        # Remove previous content
        for i in reversed(range(self.content_nav_frame.layout().count())):
            widget = self.content_nav_frame.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Create a new layout for the table
        table_layout = QGridLayout()
        table_layout.setSpacing(0)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # Main table rows
        for row_idx, row_tuple in enumerate(table):
            # First column: the string
            label = QLabel(str(row_tuple[0]).capitalize(), self.content_nav_frame)
            label.setFont(QFont("Arial", 14, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa; padding: 10px;")
            table_layout.addWidget(label, row_idx, 0)

            # Next columns: each is a tuple of 3 values
            for col_idx, cell_tuple in enumerate(row_tuple[1:], start=1):
                cell_widget = QWidget(self.content_nav_frame)
                cell_layout = QHBoxLayout(cell_widget)
                cell_layout.setContentsMargins(0, 0, 0, 0)
                cell_layout.setSpacing(0)

                left_label = QLabel(str(cell_tuple[0]), cell_widget)
                left_label.setFont(QFont("Arial", 11))
                left_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                left_label.setStyleSheet("background: transparent; color: black; border: None; padding-left: 7px; padding-right: 7px;")

                mid_label = QLabel(str(cell_tuple[1]), cell_widget)
                mid_label.setFont(QFont("Arial", 16, QFont.Bold))
                mid_label.setAlignment(Qt.AlignCenter)
                mid_label.setStyleSheet("background: transparent; color: black; border: None; padding-left: 7px; padding-right: 7px;")

                right_label = QLabel(str(cell_tuple[2]), cell_widget)
                right_label.setFont(QFont("Arial", 11))
                right_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                right_label.setStyleSheet("background: transparent; color: black; border: None; padding-left: 7px; padding-right: 7px;")

                # Add labels without any lines/separators
                cell_layout.addWidget(left_label)
                cell_layout.addWidget(mid_label)
                cell_layout.addWidget(right_label)

                # cell_widget.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa;")
                cell_widget.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa;")
                table_layout.addWidget(cell_widget, row_idx, col_idx)

        # Add Chaos Factor row below the main table
        chaos_row = len(table)
        chaos_label = QLabel("Chaos Factor", self.content_nav_frame)
        chaos_label.setFont(QFont("Arial", 13, QFont.Bold))
        chaos_label.setAlignment(Qt.AlignCenter)
        chaos_label.setStyleSheet("background-color: #eee; color: black; border: 1px solid #aaa; padding: 8px;")
        table_layout.addWidget(chaos_label, chaos_row, 0)

        for i in range(1, 10):
            cf_label = QLabel(str(i), self.content_nav_frame)
            cf_label.setFont(QFont("Arial", 13, QFont.Bold))
            cf_label.setAlignment(Qt.AlignCenter)
            cf_label.setStyleSheet("background-color: #eee; color: black; border: 1px solid #aaa; padding: 8px;")
            table_layout.addWidget(cf_label, chaos_row, i)

        # Set the new layout to the content_nav_frame
        old_layout = self.content_nav_frame.layout()
        if old_layout:
            QWidget().setLayout(old_layout)
        self.content_nav_frame.setLayout(table_layout)

    def render_random_event_focus_table(self, nav_item, table):
        """
        Renders a table with 2 columns: number (1/5 width), string (4/5 width).
        `table` should be a list of 10 (number, string) tuples.
        The table fills the content area vertically.
        """
        # Remove previous content
        layout = self.content_nav_frame.layout()
        if layout:
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 5, 0, 0)

        # Set column stretch: 1 for number, 4 for string
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 4)

        row_count = len(table)
        for row, (num_range, text) in enumerate(table):
            num_label = QLabel(str(num_range), self.content_nav_frame)
            num_label.setFont(QFont("Arial", 13, QFont.Bold))
            num_label.setAlignment(Qt.AlignCenter)
            num_label.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa; padding: 15px;")
            grid.addWidget(num_label, row, 0)

            text_label = QLabel(str(text), self.content_nav_frame)
            text_label.setFont(QFont("Arial", 13))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa; padding: 15px;")
            grid.addWidget(text_label, row, 1)

        # Make the table fill the content area vertically
        grid.setRowStretch(row_count, 1)

        # Set the new layout to the content_nav_frame
        old_layout = self.content_nav_frame.layout()
        if old_layout:
            QWidget().setLayout(old_layout)
        self.content_nav_frame.setLayout(grid)

    def render_d100_table(self, nav_item, table):
        """
        Renders a d100 table with 8 columns: (No., Word) pairs for 1-25, 26-50, 51-75, 76-100.
        `table` should be a list of (number, word) tuples.
        """
        # Remove previous content
        layout = self.content_nav_frame.layout()
        if layout:
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

        # Ensure table is sorted by number
        items = sorted(table, key=lambda x: x[0])

        # Split into 4 chunks of 25
        columns = [items[i*25:(i+1)*25] for i in range(4)]

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        # Fill rows
        for row in range(25):
            for col in range(4):
                if row < len(columns[col]):
                    num, word = columns[col][row]
                    num_label = QLabel(str(num), self.content_nav_frame)
                    num_label.setFont(QFont("Arial", 13, QFont.Bold))
                    num_label.setAlignment(Qt.AlignCenter)
                    num_label.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa; padding: 6px;")
                    word_label = QLabel(str(word), self.content_nav_frame)
                    word_label.setFont(QFont("Arial", 13))
                    word_label.setAlignment(Qt.AlignCenter)
                    word_label.setStyleSheet("background-color: white; color: black; border: 1px solid #aaa; padding: 6px;")
                    grid.addWidget(num_label, row+1, col*2)
                    grid.addWidget(word_label, row+1, col*2+1)

        # Set the new layout to the content_nav_frame
        old_layout = self.content_nav_frame.layout()
        if old_layout:
            QWidget().setLayout(old_layout)
        self.content_nav_frame.setLayout(grid)


class ArtifactsUI(QWidget):
    """UI Layout for Main Menu with buttons and styling."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Define background image path (now managed here)
        self.bg_image_path = "visuals/backgrounds/main_menu.jpg"

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
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked, v=view: self.controller.show_view(v))
            self.button_layout.addWidget(btn)
