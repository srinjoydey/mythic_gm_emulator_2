from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.artifacts_ui import ArtifactsUI  # Assuming MainMenuUI is adapted for PySide6


class ArtifactsView(QWidget):
    """Handles main menu layout & navigation."""
    def __init__(self, parent, controller):
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
