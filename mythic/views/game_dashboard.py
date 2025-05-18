from PySide6.QtWidgets import QWidget, QVBoxLayout, QLayout
from ui.game_dashboard_ui import GameDashboardUI  # Assuming MainMenuUI is adapted for PySide6


class GameDashboardView(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = GameDashboardUI(self, controller)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass
    
class CharactersList(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        from ui.game_dashboard_ui import CharactersThreadsTablesUI

        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "Characters")
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        
    def receive_edited_rows_data(self, data):
        """Receives edited data from UI when closing."""
        print("Final Edited Data:", data)  # Handle DB or logic operations here

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass

class ThreadsList(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        from ui.game_dashboard_ui import CharactersThreadsTablesUI

        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "Threads")
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        
    def receive_edited_rows_data(self, data):
        """Receives edited data from UI when closing."""
        print("Final Edited Data:", data)  # Handle DB or logic operations here

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass
