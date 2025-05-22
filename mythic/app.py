from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QStackedWidget, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QSize
from PIL import Image
from views.main_menu import MainMenu  # Assuming MainMenu is adapted for PySide6
from models.db_config import initialize_db


class MainAppWindow(QMainWindow):
    """Main application window hosting views and managing background images dynamically."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mythic GM Emulator")
        self.setMinimumSize(800, 600)
        self.resize(1366, 768)

        # Background label for displaying images
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)  # Ensure scaling

        # Container for dynamic views
        self.container = QStackedWidget(self)
        self.setCentralWidget(self.container)

        # Load MainMenu as the first view
        self.current_view = MainMenu(self.container, self)
        self.container.addWidget(self.current_view)
        self.container.setCurrentWidget(self.current_view)

        # Set initial background from MainMenu
        self.update_background(self.current_view.get_background_image())
        initialize_db()

    def show_view(self, view_class, **kwargs):
        """Loads the selected view dynamically and updates background."""
        if not issubclass(view_class, QWidget):  # Ensure view_class is a QWidget subclass
            print(f"Error: {view_class} is not a valid QWidget subclass.")
            return

        new_view = view_class(self.container, self, **kwargs)  # Pass only `self` as the parent
        self.container.addWidget(new_view)
        self.container.setCurrentWidget(new_view)

        if hasattr(new_view, "get_background_image"):
            self.update_background(new_view.get_background_image())

        self.current_view = new_view

    def update_background(self, image_path):
        """Loads and scales the background image dynamically without saving a temp file."""
        try:
            img = Image.open(image_path)
            new_size = (self.width(), self.height())

            # Resize only if necessary
            if img.size != new_size:
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Convert PIL image to QPixmap without saving a temp file
            qimage = QImage(img.tobytes(), img.width, img.height, img.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)

            self.bg_label.setPixmap(pixmap)
            self.bg_label.setGeometry(self.rect())  # Adjust to window size
        except AttributeError as e:
            pass

    def resizeEvent(self, event):
        """Handles window resizing and updates background dynamically."""
        if hasattr(self.current_view, "get_background_image"):
            self.update_background(self.current_view.get_background_image())

        if hasattr(self.current_view, "update_dimensions"):
            self.current_view.update_dimensions(event.size().width(), event.size().height())
