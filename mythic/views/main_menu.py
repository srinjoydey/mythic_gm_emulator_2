from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.main_menu_ui import MainMenuUI
from models.db_config import session, engine
from sqlalchemy import inspect
from utils.static_data.tables_index import TABLES_INDEX
from models.master_tables import StoriesIndex, Characters, Places, Items, Notes, Threads, ThreadsNotes
from models.story_tables import create_dynamic_model, CharactersList as CharactersListModel, ThreadsList as ThreadsListModel
import os
import glob
from utils.utils_functions import get_dice_roll_result


class MainMenu(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Attach UI with navigation logic
        self.ui = MainMenuUI(self, controller)
        self.ui.new_story_btn_clicked.connect(lambda: self.controller.show_view(NewStoryView))
        self.ui.existing_story_btn_clicked.connect(self.handle_existing_story_btn)
        self.ui.oracles_tables_btn_clicked.connect(self.get_full_oracles_tables)
        self.ui.gallery_btn_clicked.connect(self.get_full_gallery)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def handle_existing_story_btn(self):
        from models.master_tables import StoriesIndex

        all_stories = session.query(StoriesIndex).all()
        if not all_stories or all(story.name is None for story in all_stories):
            self.ui.show_message_under_existing_btn("No stories found. Please create a New Story.")
        else:
            self.controller.show_view(ExistingStoryView, all_stories=all_stories)

    def get_full_oracles_tables(self):
        self.controller.show_view(OraclesTablesView, prev_view="main menu")

    def get_full_gallery(self):
        from views.gallery import GalleryView
        self.controller.show_view(GalleryView, prev_view="main menu")

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

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    

class ExistingStoryView(QWidget):
    """Handles existing story loading or deletion logic & navigation."""
    def __init__(self, parent, controller, all_stories):
        from ui.main_menu_ui import ExistingStoryUI

        super().__init__(parent)
        self.controller = controller
        self.all_stories = all_stories
        self.existing_stories_data = {}
        for story in self.all_stories:
            self.existing_stories_data[story.index] = {
                "story_name": story.name,
                "description": story.description
            }

        # Attach UI with navigation logic
        self.ui = ExistingStoryUI(self, controller)
        self.ui.select_btn_clicked.connect(self.enter_game_dashboard)
        self.ui.story_name_description_edited.connect(self.update_story_details)
        self.ui.delete_btn_clicked.connect(self.delete_story)
        self.ui.back_btn_clicked.connect(lambda: self.controller.show_view(MainMenu))
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def enter_game_dashboard(self, index):
        """Enters the game dashboard for the selected story."""
        from views.game_dashboard import GameDashboardView
        
        self.controller.show_view(GameDashboardView, story_index=index)

    def update_story_details(self, index, new_name, new_description):
        """Updates the story details in the existing stories data."""
        session.query(StoriesIndex).filter(StoriesIndex.index == index).update({
            StoriesIndex.name: new_name,
            StoriesIndex.description: new_description
        })
        session.commit()
        self.controller.show_view(ExistingStoryView, all_stories=self.all_stories)

    def delete_story(self, index):
        """Deletes the selected story."""
        characters_table_name = str(index) + "_characters_list"
        threads_table_name = str(index) + "_threads_list"

        characters_list_model = create_dynamic_model(CharactersListModel, characters_table_name)
        threads_list_model = create_dynamic_model(ThreadsListModel, threads_table_name)
        # Clear slot from stories index and remove all story records from master tables
        session.query(StoriesIndex).filter(StoriesIndex.index == index).update({
            StoriesIndex.name: None,
            StoriesIndex.description: None,
            StoriesIndex.created_date: None,
            StoriesIndex.modified_date: None
        })
        session.query(Characters).filter(Characters.story_index == index).delete()
        session.query(Places).filter(Places.story_index == index).delete()
        session.query(Items).filter(Items.story_index == index).delete()
        session.query(Threads).filter(Threads.story_index == index).delete()
        session.query(Notes).filter(Notes.story_index == index).delete()
        session.query(ThreadsNotes).filter(ThreadsNotes.story_index == index).delete()
        session.commit()
        session.close()
        # Remove all images for that story
        folders = ["visuals/characters", "visuals/items", "visuals/places", "visuals/threads"]
        for folder in folders:
            pattern = os.path.join(folder, f"{index}_*")
            for file_path in glob.glob(pattern):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")
        # Drop the story-specific tables
        characters_list_model.__table__.drop(engine)
        threads_list_model.__table__.drop(engine)

        if not self.all_stories or all(story.name is None for story in self.all_stories):
            self.controller.show_view(MainMenu)
        else:
            self.controller.show_view(ExistingStoryView, all_stories=self.all_stories)

    def get_background_image(self):
        """Returns the background image path for this view."""
        return self.ui.bg_image_path  # UI manages background image selection
    

class OraclesTablesView(QWidget):
    """Handles main menu layout & navigation."""
    def __init__(self, parent, controller, prev_view, story_index=None, chaos_factor=None, first_nav_item=None):
        # from ui.main_menu_ui import OraclesTablesUI
        from ui.main_menu_ui import OraclesTablesUI

        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        self.chaos_factor = chaos_factor

        # Define background image path (handled by MainAppWindow)
        self.bg_image_path = "assets/page1_bg.jpg"

        # Attach UI with navigation logic
        self.ui = OraclesTablesUI(self, controller, list(TABLES_INDEX.keys()), first_nav_item, prev_view, chaos_factor)
        self.ui.nav_item_selected.connect(self.get_table_data)
        self.ui.nav_item_double_clicked.connect(self.roll_on_double_clicked_table)
        self.ui.fate_intersection_cell.connect(self.roll_on_fate_chart)
        self.ui.close_oracles_tables_window.connect(self.navigate_to_previous_view)
        self.ui.fate_roll_identical_digits.connect(self.navigate_to_random_events_table)
        # Layout to ensure proper expansion
        self.setLayout(self.ui.layout)

    def get_table_data(self, nav_item):
        table = TABLES_INDEX.get(nav_item)
        if nav_item == "Fate Chart":
            self.ui.render_fate_chart(nav_item, table)
        elif nav_item in ["Scene Adjustment Table", "Random Event Focus Table"]:
            self.ui.render_non_meaning_tables(nav_item, table)
        else:
            self.ui.render_d100_table(nav_item, table)

    def navigate_to_previous_view(self, prev_view):
        from views.game_dashboard import GameDashboardView

        if prev_view == 'main menu':
            self.controller.show_view(MainMenu)
        elif prev_view == 'game dashboard':
            self.controller.show_view(GameDashboardView, story_index=self.story_index)

    def roll_on_double_clicked_table(self, table_name):
        if table_name != "Fate Chart":
            if table_name == "Scene Adjustment Table":
                result = get_dice_roll_result(10, flutter=False)
                # self.ui.display_roll_result(table_name, result)
                print("Dice:", *result)
                self.ui.highlight_roll_result(result, table_name)
            elif table_name == "Random Event Focus Table":
                result = get_dice_roll_result(100, flutter=False)
                # self.ui.display_roll_result(table_name, result)
                print("Dice:", *result)
                self.ui.highlight_roll_result(result, table_name)
            else:
                result = get_dice_roll_result(100, flutter=True)
                # self.ui.display_roll_result(table_name, result)
                print("Dice:", *result)
                self.ui.highlight_roll_result(result)

    def roll_on_fate_chart(self, row_idx, col_idx, cell_content_tuple):
        """Rolls on the Fate Chart and updates the UI."""
        dice_result = get_dice_roll_result(100)[0]
        if dice_result <= cell_content_tuple[0]:
            fate_result = "Exceptional Yes"
            colour = "green"
        elif dice_result <= cell_content_tuple[1]:
            fate_result = "Yes"
            colour = "lightgreen"
        elif dice_result < cell_content_tuple[2]:
            fate_result = "No"
            colour = "orange"
        else:
            fate_result = "Exceptional No"
            colour = "red"
        self.ui.show_fate_roll_result(row_idx, col_idx, dice_result, fate_result, colour)

    def navigate_to_random_events_table(self):
        """Navigates to the Random Events Table."""
        self.controller.show_view(OraclesTablesView, prev_view="oracles tables", story_index=self.story_index, chaos_factor=self.chaos_factor, first_nav_item="Random Event Focus Table")