from PySide6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QScrollArea, QSizePolicy, QLineEdit, QFileDialog, QTextEdit, QToolBar, QColorDialog, QFontComboBox, QComboBox)
from PySide6.QtGui import QFont, QIcon, QPixmap, QTextCharFormat, QTextCursor, QColor, QTextListFormat, QAction
from PySide6.QtCore import Qt, QSize, Signal, QTimer
import os
import shutil


CHARACTERS_FIELDS = ['name', 'race', 'age', 'role_profession', 'social_status', 'economic_status', 'image_path', 'notes']
PLACES_FIELDS = ['name', 'weather', 'smell', 'image_path', 'notes']
ITEMS_FIELDS = ['name', 'material', 'rarity', 'image_path', 'notes']


class GalleryModalUI(QWidget):
    """A modal dialog with a left-hand vertical navigation pane and a close button row."""
    details_data_ready = Signal(dict)
    notes_edited = Signal(str)
    close_modal = Signal()
    image_uploaded = Signal(str)

    def __init__(self, parent, controller, nav_items, first_nav_type=None, first_nav_id=None):
        super().__init__(parent)
        self.parent_view = parent
        self.controller = controller
        self.nav_buttons = []
        self.details_rows = []
        self.details_fields = None
        self.selected_nav_btn = None
        self.nav_item_edited_data = {}  # Will hold [nav_type, nav_id, {field: value, ...}] entries
        self.current_nav_type = None
        self.current_nav_id = None
        self.nav_id_to_label = {}
        self.nav_btn_map = {}
        self.current_saved_image_path = None
        self.current_notes = None

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
        close_button.clicked.connect(self.emit_details_data_and_close)

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
            btn = QPushButton(nav_item[2], self.nav_frame)
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                padding: 10px;
                color: white;
            """)
            btn.clicked.connect(lambda checked, b=btn, type=nav_item[0], id=nav_item[1]: self.handle_nav_click(b, type, id))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.nav_id_to_label[(nav_item[0], nav_item[1])] = nav_item[2]
            self.nav_btn_map[(nav_item[0], nav_item[1])] = btn

        self.nav_layout.addStretch()
        self.nav_scroll_area.setWidget(self.nav_frame)
        self.layout.addWidget(self.nav_scroll_area, 1, 0, 10, 3)

        # --- Right Content Area ---
        content_frame = QFrame(self)
        content_layout = QGridLayout(content_frame)
        content_layout.setContentsMargins(10, 0, 0, 0)
        content_layout.setSpacing(0)

        # --- Image ---
        self.image_section = QFrame(content_frame)
        self.image_section.setStyleSheet("""
            background-color: #333;
        """) 
        content_layout.addWidget(self.image_section, 0, 0, 3, 3)

        self.image_label = QLabel(self.image_section)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter) 
        image_section_layout = QVBoxLayout(self.image_section)
        image_section_layout.setContentsMargins(0, 0, 0, 0)
        image_section_layout.setSpacing(0)
        image_section_layout.addWidget(self.image_label) 

        # --- Details ---
        self.details_section = QFrame(content_frame)
        self.details_layout = QVBoxLayout(self.details_section)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        self.details_layout.setSpacing(0)
        self.details_section.setStyleSheet("""
            background-color: #333;
        """) 
        content_layout.addWidget(self.details_section, 0, 3, 3, 2)

        for i in range(7):
            details_row = QLineEdit(self.details_section)          
            details_row.setAlignment(Qt.AlignCenter)
            if i == 0:
                font = QFont("Arial", 13, QFont.Bold)
                font.setItalic(True)
                details_row.setFont(font)           
                details_row.setStyleSheet("""
                    padding: 14px;
                    color: yellow;                                       
                """)
                self.details_layout.addWidget(details_row, 3)
            elif i == 1:
                details_row.setFont(QFont("Arial", 15, QFont.Bold))
                details_row.setStyleSheet("""
                    padding: 13px;
                    color: lightblue;
                    background-color: maroon;
                """)
                self.details_layout.addWidget(details_row, 2)
            else:
                details_row.setFont(QFont("Arial", 12))              
                details_row.setStyleSheet("""
                    padding: 11px;
                    color: white;
                """)
                self.details_layout.addWidget(details_row, 2)
            details_row.textChanged.connect(self.details_text_changed)    
            details_row.editingFinished.connect(self.details_editing_finished)
            self.details_rows.append(details_row)

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
                font-size: 12px; min-width: 20px; min-height: 20px; 
                border: none; padding: 5px; margin-right: 2px; margin-left: 2px;}
            QComboBox, QFontComboBox {
                font-size: 12px;
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
        content_layout.addWidget(self.notes_scroll, 3, 0, 2, 5)

        self.layout.addWidget(content_frame, 1, 3, 10, 10)

        if self.nav_buttons:
            # Simulate a click on the first nav button
            if not first_nav_type:
                first_nav_type = nav_items[0][0]
            else:
                first_nav_type = first_nav_type + "s"
            if not first_nav_id:
                first_nav_id = nav_items[0][1]
            first_btn = self.nav_btn_map.get((first_nav_type, first_nav_id))
            QTimer.singleShot(0, lambda: self.handle_nav_click(first_btn, first_nav_type, first_nav_id))


    def handle_nav_click(self, btn, nav_type, nav_id):
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

    def update_content_for_nav(self, nav_type, nav_id):
        # Fetch current data from the view/db
        details_data = self.parent_view.get_nav_item_data(nav_type, nav_id)

        self.current_saved_image_path = details_data.pop('image_path', None)
        self.details_rows[0].setText(nav_type.upper()[:-1])
        self.notes_edit.setHtml(details_data.pop('notes', ''))

        if self.current_saved_image_path:
            self.set_image(self.current_saved_image_path)
        else:
            self.image_label.clear()
            self._original_pixmap = None
            self.image_upload_button.setText("Upload Image")

        for i in range(1, len(self.details_rows)):
            if self.details_fields and i-1 < len(self.details_fields) - 2:
                field_name = self.details_fields[i-1]
                label = field_name.capitalize()
                self.details_rows[i].setPlaceholderText(label)
                self.details_rows[i].setToolTip(label)
                if field_name == "name":
                    nav_label = self.nav_id_to_label.get((nav_type, nav_id), "")
                    self.details_rows[i].setText(nav_label)
                    self.details_rows[i].setReadOnly(True)
                else:
                    # Set value from db if present, else blank
                    self.details_rows[i].setText(details_data.get(field_name, ""))
                    self.details_rows[i].setReadOnly(False)
            else:
                self.details_rows[i].setPlaceholderText("")
                self.details_rows[i].setToolTip("")
                self.details_rows[i].setText("")
                self.details_rows[i].setReadOnly(False)

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

    def details_text_changed(self, text):
        # For handling change of placeholder to tooltip and viceversa based on presence or absence of text
        sender = self.sender()
        idx = self.details_rows.index(sender)
        if idx == 0 or not self.details_fields or idx-1 >= len(self.details_fields):
            return
        field_name = self.details_fields[idx-1]
        label = field_name.capitalize()
        if text:
            sender.setPlaceholderText("")
            sender.setToolTip(label)
        else:
            sender.setPlaceholderText(label)
            sender.setToolTip("")

    def details_editing_finished(self):
        sender = self.sender()
        idx = self.details_rows.index(sender)
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
        self.close_modal.emit()  # Emit close signal

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

    # def update_dimensions(self, width, height):
    #     """Updates font sizes and button sizes dynamically when the main window resizes."""
    #     title_font_size = max(20, width // 50)
    #     self.title_label.setFont(QFont("Arial", title_font_size))

    #     btn_height = max(40, min(150, int(height / 11)))
    #     button_font_size = max(8, width // 90)

    #     for btn in self.nav_buttons:
    #         btn.setFont(QFont("Arial", button_font_size))
    #         btn.setFixedHeight(btn_height)