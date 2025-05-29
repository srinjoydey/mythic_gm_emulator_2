from PySide6.QtWidgets import QWidget, QVBoxLayout, QLayout
from ui.game_dashboard_ui import GameDashboardUI  # Assuming MainMenuUI is adapted for PySide6
from models.db_config import session
 

class GameDashboardView(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller, story_index=None):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index

        # Attach UI with navigation logic
        self.ui = GameDashboardUI(self, controller, self.story_index)
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
    def __init__(self, parent, controller, story_index=None):
        from ui.game_dashboard_ui import CharactersThreadsTablesUI
        from models.story_tables import create_dynamic_model, CharactersList as CharactersListModel

        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        self.table_name = str(self.story_index) + "_characters_list"

        self.characters_list_model = create_dynamic_model(CharactersListModel, self.table_name)

        records = session.query(self.characters_list_model).all()
        records = {}
        for record in records:
            records[record.row] = {
                "name": record.name,
                "type": record.type
            }

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "characters", self.story_index)
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        
    def receive_edited_rows_data(self, data):
        """Receives edited data from UI when closing."""
        for row, name_type_data in data.items():
            session.query(self.characters_list_model).filter(self.characters_list_model.row == row).update({"name": name_type_data["name"], "type": name_type_data["type"]})
            session.commit()

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
    def __init__(self, parent, controller, story_index=None):
        from ui.game_dashboard_ui import CharactersThreadsTablesUI
        from models.story_tables import create_dynamic_model, ThreadsList as ThreadsListModel

        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        self.table_name = str(self.story_index) + "_threads_list"

        self.threads_list_model = create_dynamic_model(ThreadsListModel, self.table_name)

        records = session.query(self.threads_list_model).all()
        records = {}
        for record in records:
            records[record.row] = {
                "thread": record.thread
            }

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "threads", self.story_index)
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        
    def receive_edited_rows_data(self, data):
        """Receives edited data from UI when closing."""
        for row, thread_data in data.items():
            session.query(self.threads_list_model).filter(self.threads_list_model.row == row).update({"thread": thread_data["thread"]})
            session.commit()

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass
