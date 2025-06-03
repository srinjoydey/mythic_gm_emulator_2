from PySide6.QtWidgets import QWidget
from ui.gallery_ui import GalleryModalUI


class GalleryModalView(QWidget):
    """Handles main menu logic & navigation."""

    def __init__(self, parent, controller, story_index=None):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index

        # Attach UI with navigation logic
        self.ui = GalleryModalUI(
            # self, controller, ["Section 1", "Section 2", "Section 3", "Section 4", "Section 5", "Section 6", "Section 7", "Section 8", "Section 9", "Section 10", "Section 11", "Section 12"], on_close=self.close)
            self, controller, ["Section 1", "Section 2", "Section 3", "Section 4"], on_close=self.close)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def navigate_to_main_menu(self):
        from views.main_menu import MainMenu
        self.controller.show_view(MainMenu)

    # def update_dimensions(self, width, height):
    #     """Propagate resizing logic to UI component."""
    #     self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass
