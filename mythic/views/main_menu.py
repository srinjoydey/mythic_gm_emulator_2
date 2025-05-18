from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.main_menu_ui import MainMenuUI


class MainMenu(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = MainMenuUI(self, controller)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    
    
class NewStoryView(QWidget):
    """Handles new story creation logic & navigation."""
    def __init__(self, parent, controller):
        from ui.main_menu_ui import NewStoryUI

        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = NewStoryUI(self, controller)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def receive_edited_rows_data(self, data):
        """Receives edited data from UI when closing."""
        print("Final Edited Data:", data)        

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    

class ExistingStoryView(QWidget):
    """Handles main menu layout & navigation."""
    def __init__(self, parent, controller):
        from ui.main_menu_ui import ExistingStoryUI

        super().__init__(parent)
        self.controller = controller

        # Define background image path (handled by MainAppWindow)
        self.bg_image_path = "assets/page1_bg.jpg"

        # Attach UI with navigation logic
        self.ui = ExistingStoryUI(self, controller)

        # Layout to ensure proper expansion
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for full expansion

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)


class OraclesTablesView(QWidget):
    """Handles main menu layout & navigation."""
    def __init__(self, parent, controller):
        from ui.main_menu_ui import OraclesTablesUI

        super().__init__(parent)
        self.controller = controller

        # Define background image path (handled by MainAppWindow)
        self.bg_image_path = "assets/page1_bg.jpg"

        # Attach UI with navigation logic
        self.ui = OraclesTablesUI(self, controller)

        # Layout to ensure proper expansion
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for full expansion

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)


class GalleryView(QWidget):
    """Handles main menu layout & navigation."""
    def __init__(self, parent, controller):
        from ui.main_menu_ui import GalleryUI

        super().__init__(parent)
        self.controller = controller

        # Define background image path (handled by MainAppWindow)
        self.bg_image_path = "assets/page1_bg.jpg"

        # Attach UI with navigation logic
        self.ui = GalleryUI(self, controller)

        # Layout to ensure proper expansion
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for full expansion

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)


class ArtifactsView(QWidget):
    """Handles main menu layout & navigation."""
    def __init__(self, parent, controller):
        from ui.main_menu_ui import ArtifactsUI

        super().__init__(parent)
        self.controller = controller

        # Define background image path (handled by MainAppWindow)
        self.bg_image_path = "assets/page1_bg.jpg"

        # Attach UI with navigation logic
        self.ui = ArtifactsUI(self, controller)

        # Layout to ensure proper expansion
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for full expansion

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)
