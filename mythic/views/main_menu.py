from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.main_menu_ui import MainMenuUI
from models.db_config import session, engine
from sqlalchemy import inspect


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

    def validate_new_story_data_setup_tables(self, data):
        """Receives edited data, validates uniqueness, and updates UI accordingly."""
        from models.master_tables import StoriesIndex
        from models.story_tables import create_dynamic_model, CharactersList, ThreadsList

        # Check if the title already exists
        existing_story = session.query(StoriesIndex).filter_by(name=data['title']).first()

        if existing_story:  # If title is already present, send error message to UI
            self.ui.display_error_message("Title already exists. Choose a diffferent one.")
            return  # Stop execution

        # Get the first empty index record
        first_empty_index = session.query(StoriesIndex).filter(StoriesIndex.name.is_(None)).first()

        if first_empty_index:  # Ensure we found an empty slot
            first_empty_index.name = data['title']
            first_empty_index.description = data['description']

            inspector = inspect(engine)
            characters_list_table_name = str(first_empty_index.index) + "_characters_list"
            threads_list_table_name = str(first_empty_index.index) + "_threads_list"

            if not inspector.has_table(characters_list_table_name):
                characters_list_model = create_dynamic_model(CharactersList, characters_list_table_name)
                characters_list_model.__table__.create(engine)
                session.bulk_insert_mappings(
                    characters_list_model,
                    [{"row": i, "name": None, "type": None} for i in range(1,26)]
                )

            session.commit()                

            if not inspector.has_table(threads_list_table_name):
                threads_list_model = create_dynamic_model(ThreadsList, threads_list_table_name)
                threads_list_model.__table__.create(engine)
                session.bulk_insert_mappings(                
                    threads_list_model,
                    [{"row": i, "thread": None} for i in range(1,26)]
                )                

            session.commit()
            # Send the index value back to the UI so it can be used in navigation
            self.ui.navigate_to_game_dashboard(first_empty_index.index)

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    

class ExistingStoryView(QWidget):
    """Handles existing story loading or deletion logic & navigation."""
    def __init__(self, parent, controller):
        from ui.main_menu_ui import ExistingStoryUI
        from models.master_tables import StoriesIndex

        super().__init__(parent)
        self.controller = controller
        self.all_stories = session.query(StoriesIndex).all()
        self.existing_stories_data = {}
        for story in self.all_stories:
            self.existing_stories_data[story.index] = {
                "story_name": story.name,
                "description": story.description
            }

        # Attach UI with navigation logic
        self.ui = ExistingStoryUI(self, controller, existing_stories=self.existing_stories_data)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def update_dimensions(self, width, height):
        """Propagate resizing logic to UI component."""
        self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    

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
