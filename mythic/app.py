from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QStackedWidget, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QSize
from PIL import Image
from views.main_menu import MainMenu  # Assuming MainMenu is adapted for PySide6


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

    def show_view(self, view_class):
        """Loads the selected view dynamically and updates background."""
        # Instantiate new view
        new_view = view_class(self.container, self)
        self.container.addWidget(new_view)
        self.container.setCurrentWidget(new_view)

        # Update background dynamically based on the new view
        if hasattr(new_view, "get_background_image"):
            self.update_background(new_view.get_background_image())

        # Update reference to current view
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
        except Exception as e:
            print(f"Error loading background image: {e}")

    def resizeEvent(self, event):
        """Handles window resizing and updates background dynamically."""
        if hasattr(self.current_view, "get_background_image"):
            self.update_background(self.current_view.get_background_image())

        if hasattr(self.current_view, "update_dimensions"):
            self.current_view.update_dimensions(event.size().width(), event.size().height())
