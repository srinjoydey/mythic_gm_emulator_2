from PySide6.QtWidgets import QWidget, QVBoxLayout, QLayout
from ui.new_story_ui import NewStoryUI, ScrollCheckUI  # Assuming MainMenuUI is adapted for PySide6


class NewStoryView(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = NewStoryUI(self, controller)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    
class CharactersList(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        from ui.new_story_ui import CharactersThreadsTablesUI

        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection

class ThreadsList(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        from ui.new_story_ui import CharactersThreadsTablesUI

        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller)
        # self.setLayout(self.ui.layout)  # Use UI's layout directly
        self.setLayout(self.ui.layout) if isinstance(self.ui.layout, QLayout) else self.setLayout(QVBoxLayout(self))        

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection

class ScrollCheck(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        from ui.new_story_ui import CharactersThreadsTablesUI

        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = ScrollCheckUI(self, controller)
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        # self.setLayout(self.ui.layout) if isinstance(self.ui.layout, QLayout) else self.setLayout(QVBoxLayout(self))

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
