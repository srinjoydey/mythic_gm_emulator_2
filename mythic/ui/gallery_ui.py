from PySide6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QScrollArea, QSizePolicy, QLineEdit, QFileDialog, QTextEdit, QToolBar, QColorDialog, QFontComboBox, QComboBox, QCheckBox, QRadioButton, QButtonGroup, QApplication, QSpacerItem, QDialog)
from PySide6.QtGui import QFont, QIcon, QPixmap, QTextCharFormat, QTextListFormat, QAction
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QEvent
import os
import shutil


CHARACTERS_FIELDS = ['name', 'race', 'age', 'role_profession', 'social_status', 'economic_status', 'image_path', 'notes']
PLACES_FIELDS = ['name', 'weather', 'smell', 'image_path', 'notes']
ITEMS_FIELDS = ['name', 'material', 'rarity', 'image_path', 'notes']


class GalleryUI(QWidget):
    """A modal dialog with a left-hand vertical navigation pane and a close button row."""
    label_clicked = Signal()
    search_options_changed = Signal(str, str, list, object, str)
    details_data_ready = Signal(dict)
    notes_edited = Signal(str)
    close_gallery = Signal(str)
    image_uploaded = Signal(str)
    list_action_nav_item = Signal(str, object)

    def __init__(self, parent, controller, nav_items, existing_stories, first_nav_type, first_nav_id, prev_view, search_with):
        super().__init__(parent)
        self.parent_view = parent
        self.controller = controller
        self.existing_stories = existing_stories
        existing_stories_indexes = [idx for idx, name in self.existing_stories.items() if name]
        self.prev_view = prev_view
        self.nav_buttons = []
        self.details_values = []
        self.details_fields = None
        self.selected_nav_btn = None
        self.nav_item_edited_data = {}  # Will hold [nav_type, nav_id, {field: value, ...}] entries
        self.current_nav_type = None
        self.current_nav_id = None
        self.nav_id_to_label = {}
        self.nav_btn_map = {}
        self.current_saved_image_path = None
        self.current_notes = None
        if prev_view in ('game dashboard', 'characters list', 'threads list'):
            self.modal = True
            self.last_search_options = ["Ascending", "Active", ["Characters", "Places", "Items"], None]
        else:
            self.modal = False
            self.last_search_options = ["Ascending", "Active", ["Characters", "Places", "Items"], existing_stories_indexes]

        if self.modal:
            self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_DeleteOnClose, True)

        # Main grid layout
        self.layout = QGridLayout(self)
        if self.modal:
            self.layout.setContentsMargins(50, 40, 50, 30)
        else:
            self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # --- Top Row: Title and Close Button ---
        close_row_container = QFrame(self)
        if self.modal:
            close_row_container.setStyleSheet("background-color: transparent;")
        else:
            close_row_container.setStyleSheet("""
                background-color: #222;
            """)

        self.search_box = QLineEdit(close_row_container)
        self.search_box.setPlaceholderText("Search")
        self.search_box.setFont(QFont("Arial", 12))
        self.search_box.setStyleSheet("""
            padding: 10px;
            color: white;
            background-color: #444;
            border: 1px solid #555;
        """)
        if self.modal:
            self.search_box.setFixedSize(281, 41)
        else:
            self.search_box.setFixedSize(300, 42)

        # Create a QAction for the dialog button
        dialog_action = QAction(QIcon("assets/icons/close_icon.png"), "Search Options", self.search_box)
        dialog_action.setToolTip("Search options")
        self.search_box.addAction(dialog_action, QLineEdit.TrailingPosition)  # Add to the right

        self.popup = SearchOptionsPopup(self, modal=self.modal, existing_stories=self.existing_stories, view="Characters")
        self.popup.values_changed.connect(self.selected_search_options)

        # Connect the action to your dialog-opening function
        dialog_action.triggered.connect(self.open_search_menu)        
        self.search_box.textEdited.connect(self.emit_current_search_options)

        if not search_with:
            self.title_or_button_label = ClickableLabel("Gallery : Characters", close_row_container)
            self.title_or_button_label.setFont(QFont("Arial", 28))
            self.title_or_button_label.setStyleSheet("""
                background-color: transparent;
                padding: 10px;                                  
                color: maroon;
                font-weight: bold;
                font-style: italic;
            """)
            self.title_or_button_label.clicked.connect(self.label_clicked)
        else:
            self.title_or_button_label = QPushButton(search_with['action'].capitalize(), close_row_container)
            self.title_or_button_label.setFixedSize(240, 38)
            self.title_or_button_label.setStyleSheet("""
                background-color: maroon;
                padding: 10px;                                  
                color: white;
                font-size: 20px;
                margin-left: 34px;
            """)
            self.title_or_button_label.clicked.connect(self.emit_list_action_nav_item_and_close)

        close_button = QPushButton(close_row_container)
        if self.modal:
            close_button.setIcon(QIcon("assets/icons/close_icon.png"))
            close_button.setIconSize(QSize(25, 25))
            close_button.setFont(QFont("Arial", 14, QFont.Bold))
            close_button.setStyleSheet("padding: 0px; background-color: white; color: maroon;")
        else:
            close_button.setText("Main Menu")
            close_button.setFont(QFont("Arial", 14, QFont.Bold))
            close_button.setStyleSheet("padding: 10px; color: white;")
        close_button.clicked.connect(self.emit_details_data_and_close)

        close_row_layout = QHBoxLayout(close_row_container)
            
        close_row_layout.addWidget(self.search_box, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        close_row_layout.addStretch(1)
        if not search_with:
            close_row_layout.addWidget(self.title_or_button_label, alignment=Qt.AlignCenter)
        else:
            close_row_layout.addWidget(self.title_or_button_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        close_row_layout.addStretch(1)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(6, 5, 40, 5)

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
            self.nav_item_type = nav_item[0]
            if self.modal:
                nav_item_id = nav_item[1]
                nav_item_name = nav_item[2]
            else:
                nav_item_story_index = nav_item[1]
                nav_item_id = nav_item[2]
                nav_item_name = nav_item[3]
            btn = QPushButton(nav_item_name, self.nav_frame)
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("padding: 10px; color: white;")
            btn.clicked.connect(lambda checked, b=btn, type=self.nav_item_type, id=nav_item_id: self.handle_nav_click(b, type, id))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.nav_id_to_label[(self.nav_item_type, nav_item_id)] = nav_item_name
            self.nav_btn_map[(self.nav_item_type, nav_item_id)] = btn

        self.nav_layout.addStretch()
        self.nav_scroll_area.setWidget(self.nav_frame)
        self.layout.addWidget(self.nav_scroll_area, 1, 0, 10, 3)

        # --- Right Content Area ---
        content_frame = QFrame(self)
        content_layout = QGridLayout(content_frame)
        if self.modal:
            content_layout.setContentsMargins(10, 0, 0, 0)
        else:
            content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # --- Image ---
        self.image_section = QFrame(content_frame)
        self.image_section.setStyleSheet("""
            background-color: #333;
        """)

        self.image_label = QLabel(self.image_section)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter) 
        image_section_layout = QVBoxLayout(self.image_section)
        image_section_layout.setContentsMargins(0, 0, 0, 0)
        image_section_layout.setSpacing(0)
        image_section_layout.addWidget(self.image_label)
        self.image_label.mouseDoubleClickEvent = self.show_fullscreen_image

        # --- Details ---
        self.details_section = QFrame(content_frame)
        self.details_layout = QVBoxLayout(self.details_section)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        self.details_layout.setSpacing(0)
        self.details_section.setStyleSheet("""
            background-color: #333;
        """)

        # Determine initial nav_type and nav_id
        if first_nav_type:
            # Ensure plural form for nav_type
            if not first_nav_type.endswith('s'):
                initial_nav_type = first_nav_type + 's'
            else:
                initial_nav_type = first_nav_type
        else:
            initial_nav_type = nav_items[0][0] if nav_items else "characters"
        if first_nav_id:
            initial_nav_id = first_nav_id
        else:
            # For multi-story mode, nav_items[0][2] is id, for single-story nav_items[0][1] is id
            if len(nav_items[0]) == 4:
                initial_nav_id = nav_items[0][2]
            else:
                initial_nav_id = nav_items[0][1]

        self._place_sections(content_layout, initial_nav_type)

        # Simulate a click on the correct nav button
        first_btn = self.nav_btn_map.get((initial_nav_type, initial_nav_id))
        QTimer.singleShot(0, lambda: self.handle_nav_click(first_btn, initial_nav_type, initial_nav_id))

        for i in range(7):
            details_row = QLineEdit(self.details_section)
            details_row.setAlignment(Qt.AlignCenter)
            if i == 0:
                font = QFont("Arial", 13, QFont.Bold)
                font.setItalic(True)
                details_row.setFont(font)
                details_row.setStyleSheet("padding: 14px; color: yellow;")
                self.details_layout.addWidget(details_row, 3)
            elif i == 1:
                details_row.setFont(QFont("Arial", 15, QFont.Bold))
                details_row.setStyleSheet("padding: 13px; color: lightblue; background-color: maroon;")
                self.details_layout.addWidget(details_row, 2)
            else:
                details_row.setFont(QFont("Arial", 12))
                details_row.setStyleSheet("padding: 11px; color: white;")
                self.details_layout.addWidget(details_row, 2)
            details_row.textChanged.connect(self.set_details_placeholders_tooltips)
            details_row.editingFinished.connect(self.details_editing_finished)
            self.details_values.append(details_row)

        # Image upload button
        self.image_upload_button = QPushButton("Upload Image", self.details_section)
        self.image_upload_button.setFont(QFont("Arial", 12))
        self.image_upload_button.setStyleSheet("""
            padding: 10px;
            color: white;
            background-color: #444;
            border-radius: 6px;
        """)
        self.image_upload_button.clicked.connect(self.open_image_file_dialog)
        self.details_layout.addWidget(self.image_upload_button)

        # --- Notes ---
        self.notes_frame = QFrame(content_frame)
        self.notes_frame.setFrameShape(QFrame.StyledPanel)
        self.notes_frame.setStyleSheet("background: #444; border: None;")
        notes_layout = QVBoxLayout(self.notes_frame)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(0)

        # Notes Toolbar
        self.notes_toolbar = QToolBar("Notes Toolbar", self.notes_frame)
        self.notes_toolbar.setStyleSheet("""
            QToolBar { background: #222; color: #222; border: none; }
            QToolButton { 
                font-size: 13px; min-width: 20px; min-height: 20px; 
                border: none; padding: 5px; margin-right: 2px; margin-left: 2px;}
            QComboBox, QFontComboBox {
                font-size: 13px;
                min-width: 65px;
                min-height: 20px;
                background: #fffbe6;
                color: #222;
                border: 1px solid #aaa;
                padding: 5px;
            }
        """)      
        
        self.toolbar_buttons()

        # Notes Edit Area
        self.notes_edit = QTextEdit(self.notes_frame)
        self.notes_edit.setPlaceholderText("Enter your notes here...")
        self.notes_edit.setFont(QFont("Arial", 14))
        self.notes_edit.setStyleSheet("background: #777; color: black; border: none;")
        self.notes_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.notes_edit.textChanged.connect(self.notes_text_changed)
        self.current_notes = self.notes_edit
        notes_layout.addWidget(self.notes_toolbar, 2)
        notes_layout.addWidget(self.notes_edit, 3)

        self.notes_scroll = QScrollArea(content_frame)
        self.notes_scroll.setWidgetResizable(True)
        self.notes_scroll.setWidget(self.notes_frame)
        self.notes_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.notes_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.notes_scroll.setStyleSheet("background: transparent; border: none;")

        content_layout.addWidget(self.notes_scroll, 4, 0, 2, 9)
        self.layout.addWidget(content_frame, 1, 3, 10, 10)

        # Simulate a search if search_with is provided
        if search_with is not None:
            search_category = [search_with['type'].capitalize() + "s"]  # e.g., "Characters", "Places", "Items"
            search_text = search_with['name']
            self.search_box.setText(search_text)
            self.last_search_options[1] = "All"
            self.last_search_options[2] = search_category
            QTimer.singleShot(0, self.emit_current_search_options)

        # Simulate a click on the first nav button
        if self.nav_buttons:
            if not first_nav_type:
                first_nav_type = nav_items[0][0]
            else:
                first_nav_type = first_nav_type + "s"
            if not first_nav_id:
                first_nav_id = nav_items[0][1]
            first_btn = self.nav_btn_map.get((first_nav_type, first_nav_id))
            QTimer.singleShot(0, lambda: self.handle_nav_click(first_btn, first_nav_type, first_nav_id))


    def _place_sections(self, content_layout, nav_type):
        # Hide and detach widgets before removing
        self.image_section.hide()
        self.details_section.hide()
        self.image_section.setParent(None)
        self.details_section.setParent(None)

        print("Before remove/add:")
        print("image_section geometry:", self.image_section.geometry())
        print("details_section geometry:", self.details_section.geometry())
        print("image_section parent:", self.image_section.parent())
        print("details_section parent:", self.details_section.parent())

        # Remove if already present (safe even if not present)
        content_layout.removeWidget(self.image_section)
        content_layout.removeWidget(self.details_section)

        # Add image_section and details_section in the correct positions
        if nav_type == "characters":
            content_layout.addWidget(self.image_section, 0, 0, 3, 3)
            content_layout.addWidget(self.details_section, 0, 3, 3, 6)
        elif nav_type == "places":
            content_layout.addWidget(self.image_section, 0, 0, 3, 5)
            content_layout.addWidget(self.details_section, 0, 5, 3, 4)
        else:
            content_layout.addWidget(self.image_section, 0, 0, 3, 4)
            content_layout.addWidget(self.details_section, 0, 4, 3, 5)

        # Show widgets again
        self.image_section.show()
        self.details_section.show()

        print("After add/show:")
        print("image_section geometry:", self.image_section.geometry())
        print("details_section geometry:", self.details_section.geometry())
        print("image_section parent:", self.image_section.parent())
        print("details_section parent:", self.details_section.parent())

        # Force layout recalculation
        content_layout.invalidate()
        content_layout.activate()
        self.image_section.updateGeometry()
        self.details_section.updateGeometry()
        self.updateGeometry()

        # --- ADD THESE LINES ---
        parent_frame = self.image_section.parentWidget()
        if parent_frame:
            parent_frame.updateGeometry()
            parent_frame.adjustSize()
            parent_frame.repaint()
        self.layout.activate()
        self.layout.update()
        self.adjustSize()
        self.repaint()
        # --- END ADDITION ---

    def handle_nav_click(self, btn, nav_type, nav_id):
        # Highlight the selected button
        # If btn is None, select the first available button
        if btn is None:
            if self.nav_buttons:
                btn = self.nav_buttons[0]
                # Try to get nav_type and nav_id from the button mapping
                for (type_, id_), b in self.nav_btn_map.items():
                    if b == btn:
                        nav_type = type_
                        nav_id = id_
                        break
            else:
                return  # No buttons to select, exit gracefully

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
        if nav_type == 'characters':
            self.details_fields = CHARACTERS_FIELDS
        elif nav_type == 'places':
            self.details_fields = PLACES_FIELDS
        elif nav_type == 'items':
            self.details_fields = ITEMS_FIELDS

        self.current_nav_type = nav_type
        self.current_nav_id = nav_id
        self.emit_nav_item_edited_data() 

        # Update content area (details/image/text) as needed
        self.update_content_for_nav(nav_type, nav_id)

    def open_search_menu(self):
        sort, show, categories, stories = self.last_search_options
        # Set radio buttons
        if sort == "Ascending":
            self.popup.radio1_a.setChecked(True)
        else:
            self.popup.radio1_b.setChecked(True)
        if show == "Active":
            self.popup.radio2_a.setChecked(True)
        elif show == "Inactive":
            self.popup.radio2_b.setChecked(True)
        else:
            self.popup.radio2_c.setChecked(True)
        # Set checkboxes
        self.popup.checkbox1.setChecked("Characters" in categories)
        self.popup.checkbox2.setChecked("Places" in categories)
        self.popup.checkbox3.setChecked("Items" in categories)
        # Set story checkboxes if present
        if hasattr(self.popup, "story_checkboxes") and stories is not None:
            for story_index, cb in self.popup.story_checkboxes:
                cb.setChecked(story_index in stories)
                
        self.popup.adjustSize()
        line_edit_rect = self.search_box.rect()
        global_pos = self.search_box.mapToGlobal(line_edit_rect.bottomRight())
        icon_width = 32  # Adjust as needed for your icon size
        global_pos.setX(global_pos.x() - icon_width)
        self.popup.move(global_pos)
        self.popup.show()
        self.popup.setFocus()

    def selected_search_options(self, *args):
        radio1_val, radio2_val, checkboxes, story_checkboxes = args
        self.last_search_options = (radio1_val, radio2_val, checkboxes, story_checkboxes)
        self.emit_current_search_options()

    def emit_current_search_options(self, *args):
        # Always emit the current filter state (including search text)
        sort, show, categories, stories = self.last_search_options
        search_text = self.search_box.text()
        self.search_options_changed.emit(sort, show, categories, stories, search_text)

    def update_content_for_nav(self, nav_type, nav_id):
        # Fetch current data from the view/db
        details_data = self.parent_view.get_nav_item_data(nav_type, nav_id)

        self.current_saved_image_path = details_data.pop('image_path', None)
        self.details_values[0].setText(nav_type.upper()[:-1])
        self.notes_edit.setHtml(details_data.pop('notes', ''))

        # Remove the image_section and details_section from the layout before re-adding with updated grid positions
        parent_layout = self.image_section.parentWidget().layout()
        self.nav_item_type = nav_type
        self._place_sections(parent_layout, nav_type)

        if self.current_saved_image_path:
            self.set_image(self.current_saved_image_path)
        else:
            self.image_label.clear()
            self._original_pixmap = None
            self.image_upload_button.setText("Upload Image")

        for i in range(1, len(self.details_values)):
            if self.details_fields and i-1 < len(self.details_fields) - 2:
                field_name = self.details_fields[i-1]
                label = field_name.capitalize()
                if field_name == "name":
                    nav_label = self.nav_id_to_label.get((nav_type, nav_id), "")
                    self.details_values[i].setText(nav_label)
                    self.details_values[i].setReadOnly(True)
                else:
                    # Set value from db if present, else blank
                    self.details_values[i].setText(details_data.get(field_name, ""))
                    self.details_values[i].setReadOnly(False)
            else:
                self.details_values[i].setText("")
                self.details_values[i].setReadOnly(False)
                self.details_values[i].setPlaceholderText("")
                self.details_values[i].setToolTip("")

    def open_image_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.set_image(file_path)  # You can implement set_image as shown in a previous answer

    def set_image(self, image_path):
        """Load, save, and display the image, scaled to fit the label."""
        nav_type = self.current_nav_type
        nav_id = self.current_nav_id
        label = self.nav_id_to_label.get((nav_type, nav_id), "image")
        ext = os.path.splitext(image_path)[1] or ".png"
        save_dir = os.path.join("visuals", nav_type)
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{nav_id}_{label}{ext}"
        filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
        save_path = os.path.join(save_dir, filename)
        # Only copy if source and destination are different
        if os.path.abspath(image_path) != os.path.abspath(save_path):
            shutil.copy(image_path, save_path)
        self._current_image_path = save_path
        self.image_uploaded.emit(save_path)
        pixmap = QPixmap(save_path)
        if not pixmap.isNull():
            self._original_pixmap = pixmap
            self._update_image_pixmap()
            self.image_upload_button.setText("Change Image")
        else:
            self.image_label.clear()
            self._original_pixmap = None
            self.image_upload_button.setText("Upload Image")  

    def set_details_placeholders_tooltips(self, text):
        # For handling change of placeholder to tooltip and viceversa based on presence or absence of text
        if not self.details_fields:
            return
        for idx in range(len(self.details_fields) - 2):
            # Skip the first row if your logic requires (e.g., nav_type)
            if idx >= len(self.details_values):
                break
            line_edit = self.details_values[idx + 1]
            label = self.details_fields[idx]
            if label == "role_profession":
                label = label.replace("_", " / ").title()
            else:
                label = label.replace("_", " ").title()
            value = line_edit.text()
            if value:
                line_edit.setPlaceholderText("")
                line_edit.setToolTip(label)
            else:
                line_edit.setPlaceholderText(label)
                line_edit.setToolTip("")

    def details_editing_finished(self):
        sender = self.sender()
        idx = self.details_values.index(sender)
        if idx == 0 or not self.details_fields or idx-1 >= len(self.details_fields):
            return  # Skip first row (nav_type) or out of bounds
        nav_type = self.current_nav_type
        nav_id = self.current_nav_id
        field = self.details_fields[idx-1]
        value = sender.text()
        # Find or create the entry for this nav_type/nav_id
        for key in self.nav_item_edited_data.keys():
            if key == nav_type + "-" + str(nav_id):
                self.nav_item_edited_data[key][field] = value
                break
            else:
                # Not found, create new
                entry_dict = {field: value}
                self.nav_item_edited_data[nav_type + "-" + str(nav_id)] = entry_dict

    def notes_text_changed(self):
        sender = self.sender()
        key = self.current_nav_type + "-" + str(self.current_nav_id)
        text = self.notes_edit.toHtml()
        for key in self.nav_item_edited_data.keys():
            if key == self.current_nav_type + "-" + str(self.current_nav_id):
                self.nav_item_edited_data[key]["notes"] = text
                break
        else:
            # Not found, create new
            entry_dict = {"notes": text}
            self.nav_item_edited_data[self.current_nav_type + "-" + str(self.current_nav_id)] = entry_dict      

    def emit_nav_item_edited_data(self):
        self.details_data_ready.emit(self.nav_item_edited_data)

    def emit_details_data_and_close(self):
        self.emit_nav_item_edited_data()
        self.close_gallery.emit(self.prev_view)  # Emit close signal

    def emit_list_action_nav_item_and_close(self):
        self.emit_details_data_and_close()
        self.list_action_nav_item.emit(self.current_nav_type, self.current_nav_id)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_image_pixmap()

    def _update_image_pixmap(self):
        if hasattr(self, '_original_pixmap') and self._original_pixmap:
            scaled = self._original_pixmap.scaled(
                self.image_label.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    def show_fullscreen_image(self, event):
        if hasattr(self, '_original_pixmap') and self._original_pixmap:
            dlg = FullScreenImageDialog(self._original_pixmap, self)
            dlg.showFullScreen()

    def toolbar_buttons(self):
        # Bold
        bold_action = QAction("B", self.notes_toolbar)
        bold_action.setCheckable(True)
        bold_action.setToolTip("Bold")
        bold_action.triggered.connect(lambda: self.notes_edit.setFontWeight(QFont.Bold if bold_action.isChecked() else QFont.Normal))
        self.notes_toolbar.addAction(bold_action)
        # self.notes_toolbar.setIconSize(QSize(32, 32))

        # Italic
        italic_action = QAction("I", self.notes_toolbar)
        italic_action.setCheckable(True)
        italic_action.setToolTip("Italic")
        italic_action.triggered.connect(lambda: self.notes_edit.setFontItalic(italic_action.isChecked()))
        self.notes_toolbar.addAction(italic_action)

        # Underline
        underline_action = QAction("U", self.notes_toolbar)
        underline_action.setCheckable(True)
        underline_action.setToolTip("Underline")
        underline_action.triggered.connect(lambda: self.notes_edit.setFontUnderline(underline_action.isChecked()))
        self.notes_toolbar.addAction(underline_action)

        # Font family
        font_box = QFontComboBox(self.notes_toolbar)
        font_box.setToolTip("Select Font")
        font_box.currentFontChanged.connect(lambda font: self.notes_edit.setCurrentFont(font))
        self.notes_toolbar.addWidget(font_box)

        # Font size
        size_box = QComboBox(self.notes_toolbar)
        size_box.setToolTip("Font Size")
        for size in range(8, 30, 2):
            size_box.addItem(str(size))
        size_box.setCurrentText("14")
        size_box.currentTextChanged.connect(lambda s: self.notes_edit.setFontPointSize(int(s)))
        self.notes_toolbar.addWidget(size_box)

        # Font color
        color_action = QAction("A", self.notes_toolbar)
        color_action.setToolTip("Font Color")
        def set_font_color():
            color = QColorDialog.getColor()
            if color.isValid():
                fmt = QTextCharFormat()
                fmt.setForeground(color)
                self.notes_edit.mergeCurrentCharFormat(fmt)
        color_action.triggered.connect(set_font_color)
        self.notes_toolbar.addAction(color_action)

        # Highlight
        highlight_action = QAction("HL", self.notes_toolbar)
        highlight_action.setToolTip("Highlight")
        def set_highlight_color():
            color = QColorDialog.getColor()
            if color.isValid():
                fmt = QTextCharFormat()
                fmt.setBackground(color)
                self.notes_edit.mergeCurrentCharFormat(fmt)
        highlight_action.triggered.connect(set_highlight_color)
        self.notes_toolbar.addAction(highlight_action)

        # Bullets
        bullets_action = QAction("•", self.notes_toolbar)
        bullets_action.setToolTip("Bulleted List")
        def insert_bullets():
            cursor = self.notes_edit.textCursor()
            cursor.insertList(QTextListFormat.ListDisc)
        bullets_action.triggered.connect(insert_bullets)
        self.notes_toolbar.addAction(bullets_action)

        # Numbering
        numbering_action = QAction("1.", self.notes_toolbar)
        numbering_action.setToolTip("Numbered List")
        def insert_numbering():
            cursor = self.notes_edit.textCursor()
            cursor.insertList(QTextListFormat.ListDecimal)
        numbering_action.triggered.connect(insert_numbering)
        self.notes_toolbar.addAction(numbering_action)

        # Fullscreen Notes button
        fullscreen_notes_action = QAction("🗖", self.notes_toolbar)
        fullscreen_notes_action.setToolTip("Fullscreen Notes")
        def show_fullscreen_notes():
            dlg = FullScreenNotesDialog(self.notes_edit, self.notes_toolbar, self)
            dlg.showFullScreen()
            dlg.exec()
        fullscreen_notes_action.triggered.connect(show_fullscreen_notes)
        self.notes_toolbar.addAction(fullscreen_notes_action)

    def update_nav_bar(self, nav_bar_list):
        # Remove all existing nav buttons from the layout and clear lists/maps
        for btn in self.nav_buttons:
            self.nav_layout.removeWidget(btn)
            btn.deleteLater()
        self.nav_buttons.clear()
        self.nav_id_to_label.clear()
        self.nav_btn_map.clear()

        # Remove any previous stretch
        count = self.nav_layout.count()
        if count > 0 and isinstance(self.nav_layout.itemAt(count - 1), QSpacerItem):
            item = self.nav_layout.takeAt(count - 1)
            del item

        # Add new buttons from nav_bar_list
        for nav_item in nav_bar_list:
            nav_item_type = nav_item[0]
            if self.modal:
                nav_item_id = nav_item[1]
                nav_item_name = nav_item[2]
            else:
                nav_item_story_index = nav_item[1]
                nav_item_id = nav_item[2]
                nav_item_name = nav_item[3]
            btn = QPushButton(nav_item_name, self.nav_frame)
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                padding: 10px;
                color: white;
            """)
            btn.clicked.connect(lambda checked, b=btn, type=nav_item_type, id=nav_item_id: self.handle_nav_click(b, type, id))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.nav_id_to_label[(nav_item_type, nav_item_id)] = nav_item_name
            self.nav_btn_map[(nav_item_type, nav_item_id)] = btn

        self.nav_layout.addStretch()


class ThreadsGalleryUI(QWidget):
    """A modal dialog with a left-hand vertical navigation pane and a close button row."""
    label_clicked = Signal()
    search_options_changed = Signal(str, str, object, object, str)
    details_data_ready = Signal(dict)
    notes_edited = Signal(str)
    close_gallery = Signal(str)
    image_uploaded = Signal(str)
    list_action_nav_item = Signal(str, object)

    def __init__(self, parent, controller, nav_items, existing_stories, first_nav_id, prev_view, search_with):
        super().__init__(parent)
        self.parent_view = parent
        self.controller = controller
        self.existing_stories = existing_stories
        existing_stories_indexes = [idx for idx, name in self.existing_stories.items() if name]
        self.prev_view = prev_view
        self.nav_buttons = []
        self.details_values = []
        self.selected_nav_btn = None
        self.nav_item_edited_data = {}  # Will hold [nav_type, nav_id, {field: value, ...}] entries
        self.current_nav_type = None
        self.current_nav_id = None
        self.nav_id_to_label = {}
        self.nav_btn_map = {}
        self.current_saved_image_path = None
        self.current_notes = None
        if prev_view in ('game dashboard', 'characters list', 'threads list'):
            self.modal = True
            self.last_search_options = ["Ascending", "Active", None]
        else:
            self.modal = False
            self.last_search_options = ["Ascending", "Active", existing_stories_indexes]

        if self.modal:
            self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_DeleteOnClose, True)

        # Main grid layout
        self.layout = QGridLayout(self)
        if self.modal:
            self.layout.setContentsMargins(50, 40, 50, 30)
        else:
            self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # --- Top Row: Title and Close Button ---
        close_row_container = QFrame(self)
        if self.modal:
            close_row_container.setStyleSheet("background-color: transparent;")
        else:
            close_row_container.setStyleSheet("""
                background-color: #222;
            """)

        self.search_box = QLineEdit(close_row_container)
        self.search_box.setPlaceholderText("Search")
        self.search_box.setFont(QFont("Arial", 12))
        self.search_box.setStyleSheet("""
            padding: 10px;
            color: white;
            background-color: #444;
            border: 1px solid #555;
        """)
        if self.modal:
            self.search_box.setFixedSize(571, 41)
        else:
            self.search_box.setFixedSize(617, 42)

        # Create a QAction for the dialog button
        dialog_action = QAction(QIcon("assets/icons/close_icon.png"), "Search Options", self.search_box)
        dialog_action.setToolTip("Search options")
        self.search_box.addAction(dialog_action, QLineEdit.TrailingPosition)  # Add to the right

        self.popup = SearchOptionsPopup(self, modal=self.modal, existing_stories=self.existing_stories, view="Threads")
        self.popup.values_changed.connect(self.selected_search_options)

        # Connect the action to your dialog-opening function
        dialog_action.triggered.connect(self.open_search_menu)        
        self.search_box.textEdited.connect(self.emit_current_search_options)

        if not search_with:
            self.title_or_button_label = ClickableLabel("Gallery : Threads", close_row_container)
            self.title_or_button_label.setFont(QFont("Arial", 28))
            self.title_or_button_label.setStyleSheet("""
                background-color: transparent;
                padding: 10px;                                  
                color: maroon;
                font-weight: bold;
                font-style: italic;
            """)
            self.title_or_button_label.clicked.connect(self.label_clicked)
        else:
            self.title_or_button_label = QPushButton(search_with['action'].capitalize(), close_row_container)
            self.title_or_button_label.setFixedSize(240, 38)
            self.title_or_button_label.setStyleSheet("""
                background-color: maroon;
                padding: 10px;                                  
                color: white;
                font-size: 20px;
                margin-left: 34px;
            """)
            self.title_or_button_label.clicked.connect(self.emit_list_action_nav_item_and_close)

        close_button = QPushButton(close_row_container)
        if self.modal:
            close_button.setIcon(QIcon("assets/icons/close_icon.png"))
            close_button.setIconSize(QSize(25, 25))
            close_button.setFont(QFont("Arial", 14, QFont.Bold))
            close_button.setStyleSheet("padding: 0px; background-color: white; color: maroon;")
        else:
            close_button.setText("Main Menu")
            close_button.setFont(QFont("Arial", 14, QFont.Bold))
            close_button.setStyleSheet("padding: 10px; color: white;")
        close_button.clicked.connect(self.emit_details_data_and_close)

        close_row_layout = QHBoxLayout(close_row_container)
            
        close_row_layout.addWidget(self.search_box, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        close_row_layout.addStretch(1)
        if not search_with:
            close_row_layout.addWidget(self.title_or_button_label, alignment=Qt.AlignCenter)
        else:
            close_row_layout.addWidget(self.title_or_button_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        close_row_layout.addStretch(1)
        close_row_layout.addWidget(close_button, alignment=Qt.AlignRight)
        close_row_layout.setContentsMargins(6, 5, 40, 5)

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
            self.nav_item_type = nav_item[0]
            if self.modal:
                nav_item_id = nav_item[0]
                nav_item_name = nav_item[1]
            else:
                nav_item_story_index = nav_item[0]
                nav_item_id = nav_item[1]
                nav_item_name = nav_item[2]
            btn = QPushButton(nav_item_name, self.nav_frame)
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("padding: 10px; color: white;")

            btn.clicked.connect(lambda checked, b=btn, id=nav_item_id: self.handle_nav_click(b, id))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.nav_id_to_label[nav_item_id] = nav_item_name
            self.nav_btn_map[nav_item_id] = btn

        self.nav_layout.addStretch()
        self.nav_scroll_area.setWidget(self.nav_frame)
        self.layout.addWidget(self.nav_scroll_area, 1, 0, 10, 6)

        # --- Right Content Area ---
        content_frame = QFrame(self)
        content_layout = QGridLayout(content_frame)
        if self.modal:
            content_layout.setContentsMargins(10, 0, 0, 0)
        else:
            content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # --- Image ---
        self.image_section = QFrame(content_frame)
        self.image_section.setStyleSheet("""
            background-color: #333;
        """)

        content_layout.addWidget(self.image_section, 0, 0, 7, 9)

        self.image_label = QLabel(self.image_section)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter) 
        self.image_section_layout = QVBoxLayout(self.image_section)
        self.image_section_layout.setContentsMargins(0, 0, 0, 0)
        self.image_section_layout.setSpacing(0)
        self.image_section_layout.addWidget(self.image_label)
        self.image_label.mouseDoubleClickEvent = self.show_fullscreen_image

        # Image buttons toolbar
        self.image_toolbar_frame = QFrame(content_frame)
        self.image_toolbar_frame.setStyleSheet("""
            QFrame {
                background: #333;
                border: 1px solid #444;
                border-radius: 6px;
            }
        """)
        self.image_toolbar_layout = QHBoxLayout(self.image_toolbar_frame)
        self.image_toolbar_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.addWidget(self.image_toolbar_frame, 7, 0, 1, 9)

        # Image upload button
        self.image_upload_button = QPushButton("Upload Image", self.image_toolbar_frame)
        self.image_toolbar_layout.addWidget(self.image_upload_button)

        self.image_upload_button.setFont(QFont("Arial", 12))
        self.image_upload_button.setStyleSheet("""
            padding: 10px;
            color: white;
            background-color: #444;
            border-radius: 6px;
        """)
        self.image_upload_button.clicked.connect(self.open_image_file_dialog)

        # --- Notes ---
        self.notes_frame = QFrame(content_frame)
        self.notes_frame.setFrameShape(QFrame.StyledPanel)
        self.notes_frame.setStyleSheet("background: #444; border: None;")
        notes_layout = QVBoxLayout(self.notes_frame)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(0)

        # Notes Toolbar
        self.notes_toolbar = QToolBar("Notes Toolbar", self.notes_frame)
        self.notes_toolbar.setStyleSheet("""
            QToolBar { background: #222; color: #222; border: none; }
            QToolButton { 
                font-size: 13px; min-width: 20px; min-height: 20px; 
                border: none; padding: 5px; margin-right: 2px; margin-left: 2px;}
            QComboBox, QFontComboBox {
                font-size: 13px;
                min-width: 65px;
                min-height: 20px;
                background: #fffbe6;
                color: #222;
                border: 1px solid #aaa;
                padding: 5px;
            }
        """)      
        
        self.toolbar_buttons()

        # Notes Edit Area
        self.notes_edit = QTextEdit(self.notes_frame)
        self.notes_edit.setPlaceholderText("Enter your notes here...")
        self.notes_edit.setFont(QFont("Arial", 14))
        self.notes_edit.setStyleSheet("background: #777; color: black; border: none;")
        self.notes_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.notes_edit.textChanged.connect(self.notes_text_changed)
        self.current_notes = self.notes_edit
        notes_layout.addWidget(self.notes_toolbar, 2)
        notes_layout.addWidget(self.notes_edit, 3)

        self.notes_scroll = QScrollArea(content_frame)
        self.notes_scroll.setWidgetResizable(True)
        self.notes_scroll.setWidget(self.notes_frame)
        self.notes_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.notes_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.notes_scroll.setStyleSheet("background: transparent; border: none;")

        content_layout.addWidget(self.notes_scroll, 8, 0, 5, 9)
        self.layout.addWidget(content_frame, 1, 6, 10, 7)

        # Simulate a search if search_with is provided
        if search_with is not None:
            search_text = search_with['thread']
            self.search_box.setText(search_text)
            self.last_search_options[1] = "All"
            QTimer.singleShot(0, self.emit_current_search_options)

        # Simulate a click on the first nav button
        if self.nav_buttons:
            if not first_nav_id:
                first_nav_id = nav_items[0][0]
            first_btn = self.nav_btn_map.get((first_nav_id))
            QTimer.singleShot(0, lambda: self.handle_nav_click(first_btn, first_nav_id))


    def handle_nav_click(self, btn, nav_id):
        # Highlight the selected button
        # If btn is None, select the first available button
        if btn is None:
            if self.nav_buttons:
                btn = self.nav_buttons[0]
                # Try to get nav_id from the button mapping
                for id_, b in self.nav_btn_map.items():
                    if b == btn:
                        nav_id = id_
                        break
            else:
                return  # No buttons to select, exit gracefully

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

        self.current_nav_id = nav_id
        self.emit_nav_item_edited_data() 
        # Update content area (details/image/text) as needed
        self.update_content_for_nav(nav_id)

    def open_search_menu(self):
        sort, show, stories = self.last_search_options
        # Set radio buttons
        if sort == "Ascending":
            self.popup.radio1_a.setChecked(True)
        else:
            self.popup.radio1_b.setChecked(True)
        if show == "Active":
            self.popup.radio2_a.setChecked(True)
        elif show == "Inactive":
            self.popup.radio2_b.setChecked(True)
        else:
            self.popup.radio2_c.setChecked(True)
        # Set story checkboxes if present
        if hasattr(self.popup, "story_checkboxes") and stories is not None:
            for story_index, cb in self.popup.story_checkboxes:
                cb.setChecked(story_index in stories)
                
        self.popup.adjustSize()
        line_edit_rect = self.search_box.rect()
        global_pos = self.search_box.mapToGlobal(line_edit_rect.bottomRight())
        icon_width = 32  # Adjust as needed for your icon size
        global_pos.setX(global_pos.x() - icon_width)
        self.popup.move(global_pos)
        self.popup.show()
        self.popup.setFocus()

    def selected_search_options(self, *args):
        radio1_val, radio2_val, _, story_checkboxes = args
        self.last_search_options = (radio1_val, radio2_val, story_checkboxes)
            
        self.emit_current_search_options()

    def emit_current_search_options(self, *args):
        # Always emit the current filter state (including search text)
        sort, show, stories = self.last_search_options
        search_text = self.search_box.text()
        self.search_options_changed.emit(sort, show, None, stories, search_text)

    def update_content_for_nav(self, nav_id):
        # Fetch current data from the view/db
        details_data = self.parent_view.get_nav_item_data(None, nav_id)

        self.current_saved_image_path = details_data.pop('image_path', None)
        self.notes_edit.setHtml(details_data.pop('notes', ''))

        if self.current_saved_image_path:
            self.set_image(self.current_saved_image_path)
        else:
            self.image_label.clear()
            self._original_pixmap = None
            self.image_upload_button.setText("Upload Image")

    def open_image_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.set_image(file_path)  # You can implement set_image as shown in a previous answer

    def set_image(self, image_path):
        """Load, save, and display the image, scaled to fit the label."""
        nav_type = self.current_nav_type
        nav_id = self.current_nav_id
        label = self.nav_id_to_label.get(nav_id, "image")
        ext = os.path.splitext(image_path)[1] or ".png"
        save_dir = os.path.join("visuals", "threads")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{nav_id}_{label}{ext}"
        filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
        save_path = os.path.join(save_dir, filename)
        # Only copy if source and destination are different
        if os.path.abspath(image_path) != os.path.abspath(save_path):
            shutil.copy(image_path, save_path)
        self._current_image_path = save_path
        self.image_uploaded.emit(save_path)
        pixmap = QPixmap(save_path)
        if not pixmap.isNull():
            self._original_pixmap = pixmap
            self._update_image_pixmap()
            self.image_upload_button.setText("Change Image")
        else:
            self.image_label.clear()
            self._original_pixmap = None
            self.image_upload_button.setText("Upload Image")  

    def notes_text_changed(self):
        sender = self.sender()
        text = self.notes_edit.toHtml()

        for key in self.nav_item_edited_data.keys():
            if key == self.current_nav_id:
                self.nav_item_edited_data[key]["notes"] = text
                break
        else:
            # Not found, create new
            entry_dict = {"notes": text}
            self.nav_item_edited_data[self.current_nav_id] = entry_dict      

    def emit_nav_item_edited_data(self):
        self.details_data_ready.emit(self.nav_item_edited_data)

    def emit_details_data_and_close(self):
        self.emit_nav_item_edited_data()
        self.close_gallery.emit(self.prev_view)  # Emit close signal

    def emit_list_action_nav_item_and_close(self):
        self.emit_details_data_and_close()
        self.list_action_nav_item.emit(self.current_nav_type, self.current_nav_id)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_image_pixmap()

    def _update_image_pixmap(self):
        if hasattr(self, '_original_pixmap') and self._original_pixmap:
            scaled = self._original_pixmap.scaled(
                self.image_label.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    def show_fullscreen_image(self, event):
        if hasattr(self, '_original_pixmap') and self._original_pixmap:
            dlg = FullScreenImageDialog(self._original_pixmap, self)
            dlg.showFullScreen()

    def toolbar_buttons(self):
        # Bold
        bold_action = QAction("B", self.notes_toolbar)
        bold_action.setCheckable(True)
        bold_action.setToolTip("Bold")
        bold_action.triggered.connect(lambda: self.notes_edit.setFontWeight(QFont.Bold if bold_action.isChecked() else QFont.Normal))
        self.notes_toolbar.addAction(bold_action)
        # self.notes_toolbar.setIconSize(QSize(32, 32))

        # Italic
        italic_action = QAction("I", self.notes_toolbar)
        italic_action.setCheckable(True)
        italic_action.setToolTip("Italic")
        italic_action.triggered.connect(lambda: self.notes_edit.setFontItalic(italic_action.isChecked()))
        self.notes_toolbar.addAction(italic_action)

        # Underline
        underline_action = QAction("U", self.notes_toolbar)
        underline_action.setCheckable(True)
        underline_action.setToolTip("Underline")
        underline_action.triggered.connect(lambda: self.notes_edit.setFontUnderline(underline_action.isChecked()))
        self.notes_toolbar.addAction(underline_action)

        # Font family
        font_box = QFontComboBox(self.notes_toolbar)
        font_box.setToolTip("Select Font")
        font_box.currentFontChanged.connect(lambda font: self.notes_edit.setCurrentFont(font))
        self.notes_toolbar.addWidget(font_box)

        # Font size
        size_box = QComboBox(self.notes_toolbar)
        size_box.setToolTip("Font Size")
        for size in range(8, 30, 2):
            size_box.addItem(str(size))
        size_box.setCurrentText("14")
        size_box.currentTextChanged.connect(lambda s: self.notes_edit.setFontPointSize(int(s)))
        self.notes_toolbar.addWidget(size_box)

        # Font color
        color_action = QAction("A", self.notes_toolbar)
        color_action.setToolTip("Font Color")
        def set_font_color():
            color = QColorDialog.getColor()
            if color.isValid():
                fmt = QTextCharFormat()
                fmt.setForeground(color)
                self.notes_edit.mergeCurrentCharFormat(fmt)
        color_action.triggered.connect(set_font_color)
        self.notes_toolbar.addAction(color_action)

        # Highlight
        highlight_action = QAction("HL", self.notes_toolbar)
        highlight_action.setToolTip("Highlight")
        def set_highlight_color():
            color = QColorDialog.getColor()
            if color.isValid():
                fmt = QTextCharFormat()
                fmt.setBackground(color)
                self.notes_edit.mergeCurrentCharFormat(fmt)
        highlight_action.triggered.connect(set_highlight_color)
        self.notes_toolbar.addAction(highlight_action)

        # Bullets
        bullets_action = QAction("•", self.notes_toolbar)
        bullets_action.setToolTip("Bulleted List")
        def insert_bullets():
            cursor = self.notes_edit.textCursor()
            cursor.insertList(QTextListFormat.ListDisc)
        bullets_action.triggered.connect(insert_bullets)
        self.notes_toolbar.addAction(bullets_action)

        # Numbering
        numbering_action = QAction("1.", self.notes_toolbar)
        numbering_action.setToolTip("Numbered List")
        def insert_numbering():
            cursor = self.notes_edit.textCursor()
            cursor.insertList(QTextListFormat.ListDecimal)
        numbering_action.triggered.connect(insert_numbering)
        self.notes_toolbar.addAction(numbering_action)

        # Fullscreen Notes button
        fullscreen_notes_action = QAction("🗖", self.notes_toolbar)
        fullscreen_notes_action.setToolTip("Fullscreen Notes")
        def show_fullscreen_notes():
            dlg = FullScreenNotesDialog(self.notes_edit, self.notes_toolbar, self)
            dlg.showFullScreen()
            dlg.exec()
        fullscreen_notes_action.triggered.connect(show_fullscreen_notes)
        self.notes_toolbar.addAction(fullscreen_notes_action)

    def update_nav_bar(self, nav_bar_list):
        # Remove all existing nav buttons from the layout and clear lists/maps
        for btn in self.nav_buttons:
            self.nav_layout.removeWidget(btn)
            btn.deleteLater()
        self.nav_buttons.clear()
        self.nav_id_to_label.clear()
        self.nav_btn_map.clear()

        # Remove any previous stretch
        count = self.nav_layout.count()
        if count > 0 and isinstance(self.nav_layout.itemAt(count - 1), QSpacerItem):
            item = self.nav_layout.takeAt(count - 1)
            del item

        # Add new buttons from nav_bar_list
        for nav_item in nav_bar_list:
            if self.modal:
                nav_item_id = nav_item[0]
                nav_item_name = nav_item[1]
            else:
                nav_item_story_index = nav_item[0]
                nav_item_id = nav_item[1]
                nav_item_name = nav_item[2]
            btn = QPushButton(nav_item_name, self.nav_frame)
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                padding: 10px;
                color: white;
            """)
            btn.clicked.connect(lambda checked, b=btn, id=nav_item_id: self.handle_nav_click(b, id))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.nav_id_to_label[nav_item_id] = nav_item_name
            self.nav_btn_map[nav_item_id] = btn

        self.nav_layout.addStretch()
        

class ClickableLabel(QLabel):
    clicked = Signal()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class SearchOptionsPopup(QWidget):
    values_changed = Signal(str, str, object, object)

    def __init__(popup_self, parent, modal, existing_stories, view):
        super().__init__(parent, Qt.Popup)
        popup_self.view = view
        popup_self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        # popup_self.setAttribute(Qt.WA_TranslucentBackground, True)
        popup_self.setStyleSheet("""
            QWidget {
                background: #444;
                border-radius: 10px;
            }
            QLabel {
                color: #fffbe6;
                font-weight: bold;
                font-size: 15px;
                padding: 4px 0 2px 0;
            }
            QRadioButton, QCheckBox {
                color: white;
                font-size: 14px;
                padding: 2px 8px;
            }
        """)
        layout = QVBoxLayout(popup_self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(3)

        # 1st row: Heading
        label_row1 = QLabel("Sort", popup_self)
        label_row1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(label_row1)

        # 2nd row: 2 radio buttons (grouped)
        radio_row1 = QHBoxLayout()
        popup_self.radio_group1 = QButtonGroup(popup_self)
        popup_self.radio1_a = QRadioButton("Ascending", popup_self)
        popup_self.radio1_b = QRadioButton("Descending", popup_self)
        popup_self.radio1_a.setChecked(True)
        popup_self.radio_group1.addButton(popup_self.radio1_a, 0)
        popup_self.radio_group1.addButton(popup_self.radio1_b, 1)
        radio_row1.addWidget(popup_self.radio1_a)
        radio_row1.addWidget(popup_self.radio1_b)
        layout.addLayout(radio_row1)

        # 3rd row: Heading
        label_row3 = QLabel("Show", popup_self)
        label_row3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(label_row3)

        # 4th row: 3 radio buttons (grouped)
        radio_row2 = QHBoxLayout()
        popup_self.radio_group2 = QButtonGroup(popup_self)
        popup_self.radio2_a = QRadioButton("Active", popup_self)
        popup_self.radio2_b = QRadioButton("Inactive", popup_self)
        popup_self.radio2_c = QRadioButton("All", popup_self)
        popup_self.radio2_a.setChecked(True)
        popup_self.radio_group2.addButton(popup_self.radio2_a, 0)
        popup_self.radio_group2.addButton(popup_self.radio2_b, 1)
        popup_self.radio_group2.addButton(popup_self.radio2_c, 2)
        radio_row2.addWidget(popup_self.radio2_a)
        radio_row2.addWidget(popup_self.radio2_b)
        radio_row2.addWidget(popup_self.radio2_c)
        layout.addLayout(radio_row2)

        if popup_self.view == "Characters":
            # 5th row: Heading
            label_row5 = QLabel("Categories", popup_self)
            label_row5.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            layout.addWidget(label_row5)

            # 6th row: 3 checkboxes (all checked by default)
            popup_self.checkbox_row = QHBoxLayout()
            popup_self.checkbox1 = QCheckBox("Characters", popup_self)
            popup_self.checkbox2 = QCheckBox("Places", popup_self)
            popup_self.checkbox3 = QCheckBox("Items", popup_self)
            popup_self.checkbox1.setChecked(True)
            popup_self.checkbox2.setChecked(True)
            popup_self.checkbox3.setChecked(True)
            popup_self.checkbox_row.addWidget(popup_self.checkbox1)
            popup_self.checkbox_row.addWidget(popup_self.checkbox2)
            popup_self.checkbox_row.addWidget(popup_self.checkbox3)
            layout.addLayout(popup_self.checkbox_row)

        if not modal:
            if existing_stories:
                label_row7 = QLabel("Stories", popup_self)
                label_row7.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                layout.addWidget(label_row7)
                popup_self.story_checkboxes = []
                story_indices = list(existing_stories.items())
                if len(story_indices) > 3:
                    # First row: first 3 stories
                    story_row1 = QHBoxLayout()
                    any_story1 = False
                    for story_index, story_name in story_indices[:3]:
                        if story_name:
                            cb = QCheckBox(story_name, popup_self)
                            cb.setChecked(True)
                            story_row1.addWidget(cb)
                            popup_self.story_checkboxes.append((story_index, cb))
                            any_story1 = True
                    if not any_story1:
                        label_row7.setVisible(False)
                    layout.addLayout(story_row1)
                    # Second row: the rest
                    story_row2 = QHBoxLayout()
                    any_story2 = False
                    for story_index, story_name in story_indices[3:]:
                        if story_name:
                            cb = QCheckBox(story_name, popup_self)
                            cb.setChecked(True)
                            story_row2.addWidget(cb)
                            popup_self.story_checkboxes.append((story_index, cb))
                            any_story2 = True
                    if not any_story1 and not any_story2:
                        label_row7.setVisible(False)
                    layout.addLayout(story_row2)
                else:
                    # All in one row
                    story_row = QHBoxLayout()
                    for story_index, story_name in story_indices:
                        if story_name:
                            cb = QCheckBox(story_name, popup_self)
                            cb.setChecked(True)
                            story_row.addWidget(cb)
                            popup_self.story_checkboxes.append((story_index, cb))
                    layout.addLayout(story_row)
            if popup_self.view == "Characters":
                popup_self.setFixedSize(480, 510)
            else:
                popup_self.setFixedSize(480, 350)
        else:
            # Modal popup size
            if popup_self.view == "Characters":
                popup_self.setFixedSize(400, 335)
            else:
                popup_self.setFixedSize(400, 290)

        # Connect signals to emit current values
        popup_self.radio1_a.toggled.connect(popup_self.emit_current_values)
        popup_self.radio1_b.toggled.connect(popup_self.emit_current_values)
        popup_self.radio2_a.toggled.connect(popup_self.emit_current_values)
        popup_self.radio2_b.toggled.connect(popup_self.emit_current_values)
        popup_self.radio2_c.toggled.connect(popup_self.emit_current_values)
        if popup_self.view == "Characters":
            popup_self.checkbox1.stateChanged.connect(popup_self.emit_current_values)
            popup_self.checkbox2.stateChanged.connect(popup_self.emit_current_values)
            popup_self.checkbox3.stateChanged.connect(popup_self.emit_current_values)

        if not modal:
            for story_index, cb in popup_self.story_checkboxes:
                cb.stateChanged.connect(popup_self.emit_current_values)

    def eventFilter(popup_self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
            popup_self.return_values_and_close()
            return True
        return super().eventFilter(obj, event)

    def focusOutEvent(popup_self, event):
        # Only close if focus is not moving to a child widget
        if not popup_self.isAncestorOf(QApplication.focusWidget()):
            popup_self.return_values_and_close()
        super().focusOutEvent(event)

    def emit_current_values(popup_self):
        # Get the text of the selected radio button in group 1
        radio1_btn = popup_self.radio_group1.checkedButton()
        radio1_val = radio1_btn.text() if radio1_btn else ""

        # Get the text of the selected radio button in group 2
        radio2_btn = popup_self.radio_group2.checkedButton()
        radio2_val = radio2_btn.text() if radio2_btn else ""

        # Get the text of all checked checkboxes
        if popup_self.view == "Characters":
            checked_boxes = []
            for cb in [popup_self.checkbox1, popup_self.checkbox2, popup_self.checkbox3]:
                if cb.isChecked():
                    checked_boxes.append(cb.text())
        if hasattr(popup_self, "story_checkboxes"):
            checked_stories = []
            for story_index, cb in popup_self.story_checkboxes:
                if cb.isChecked():
                    checked_stories.append(story_index)
            if hasattr(popup_self, "checkbox_row"):
                popup_self.values_changed.emit(radio1_val, radio2_val, checked_boxes, checked_stories)
            else:
                popup_self.values_changed.emit(radio1_val, radio2_val, None, checked_stories)
        else:
            if hasattr(popup_self, "checkbox_row"):
                popup_self.values_changed.emit(radio1_val, radio2_val, checked_boxes, None)
            else:
                popup_self.values_changed.emit(radio1_val, radio2_val, None, None)

    def return_values_and_close(popup_self):
        # Gather values
        popup_self.emit_current_values()
        popup_self.close()


class FullScreenImageDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet("background-color: black;")
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.set_pixmap(pixmap)

    def set_pixmap(self, pixmap):
        if pixmap:
            screen_rect = self.screen().geometry()
            scaled = pixmap.scaled(
                screen_rect.width(), screen_rect.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


class FullScreenNotesDialog(QDialog):
    def __init__(self, notes_edit, toolbar, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet("background-color: #222;")
        self.notes_edit = notes_edit
        self.toolbar = toolbar

        # Save parent and layout to restore later
        self._original_parent = notes_edit.parent()
        self._original_toolbar_parent = toolbar.parent()
        self._original_notes_layout = notes_edit.parent().layout()
        self._original_toolbar_layout = toolbar.parent().layout()

        # Remove widgets from their parents and add to dialog
        self.notes_edit.setParent(self)
        self.toolbar.setParent(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.notes_edit)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Restore widgets to original parents and layouts
            self.toolbar.setParent(self._original_toolbar_parent)
            self.notes_edit.setParent(self._original_parent)
            if self._original_toolbar_layout is not None:
                self._original_toolbar_layout.addWidget(self.toolbar)
            if self._original_notes_layout is not None:
                self._original_notes_layout.addWidget(self.notes_edit)
            self.close()
        else:
            super().keyPressEvent(event)