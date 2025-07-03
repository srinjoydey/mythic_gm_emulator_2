from PySide6.QtWidgets import QWidget
from ui.game_dashboard_ui import GameDashboardUI  # Assuming MainMenuUI is adapted for PySide6
from models.master_tables import StoriesIndex, Characters, Places, Items, Notes
from models.db_config import session
from utils.static_data.tables_index import TESTING_THE_EXPECTED_SCENE
 

MODEL_MAP = {"character": Characters, "place": Places, "item": Items}

class GameDashboardView(QWidget):
    """Handles main menu logic & navigation."""
    def __init__(self, parent, controller, story_index=None):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        # Fetch story data
        self.story = session.query(StoriesIndex).filter(StoriesIndex.index == self.story_index).first()
        self.story_name = self.story.name
        self.description = self.story.description
        self.chaos_factor = self.story.chaos_factor

        # If chaos_factor is None, set to 5 and save to db immediately
        if self.chaos_factor is None:
            self.chaos_factor = 5
            self.story.chaos_factor = 5
            session.flush()
            session.commit()

        # Attach UI with navigation logic
        self.ui = GameDashboardUI(self, controller, self.story_index)
        self.ui.oracles_tables_button_clicked.connect(self.navigate_to_oracles_tables)
        self.ui.characters_button_clicked.connect(lambda: self.navigate_to_characters_list(self.story_index))
        self.ui.threads_button_clicked.connect(lambda: self.navigate_to_threads_list(self.story_index))
        self.ui.gallery_modal_button_clicked.connect(lambda: self.navigate_to_gallery_modal(self.story_index))
        self.ui.main_menu_button_clicked.connect(lambda: self.navigate_to_main_menu())
        self.ui.start_scene_action_selected.connect(self.handle_start_scene_action)
        self.ui.start_scene_action_resolution.connect(self.resolve_start_scene_action)
        self.ui.chaos_factor_changed.connect(self.post_updated_chaos_factor)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def navigate_to_oracles_tables(self):
        from views.main_menu import OraclesTablesView
        self.controller.show_view(OraclesTablesView, prev_view='game dashboard', first_nav_item=None, story_index=self.story_index, chaos_factor=self.chaos_factor)

    def navigate_to_characters_list(self, story_index):
        self.controller.show_view(CharactersList, story_index=story_index)

    def navigate_to_threads_list(self, story_index):       
        self.controller.show_view(ThreadsList, story_index=story_index)

    def navigate_to_gallery_modal(self, story_index):
        from views.gallery import GalleryView     
        self.controller.show_view(GalleryView, story_index=story_index, prev_view='game dashboard')

    def navigate_to_main_menu(self):
        from views.main_menu import MainMenu
        self.controller.show_view(MainMenu)

    def handle_start_scene_action(self, action):
        if action == "expected_scene_test":
            self.ui.test_expected_scene(TESTING_THE_EXPECTED_SCENE)
        elif action == "oracles_tables":
            self.open_oracle_table_in_modal()

    def resolve_start_scene_action(self, action):
        """Handles the action selected in the start scene dialog."""
        self.open_oracle_table_in_modal(action)

    def open_oracle_table_in_modal(self, table_name=None):
        from views.main_menu import OraclesTablesView
        
        self.controller.show_view(OraclesTablesView, prev_view='game dashboard', first_nav_item=table_name, story_index=self.story_index, chaos_factor = self.chaos_factor)

    def post_updated_chaos_factor(self, new_chaos_factor):
        self.story.chaos_factor = new_chaos_factor
        session.flush()
        session.commit()
        # Update the UI or perform any necessary actions with the new chaos factor

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

        existing_data_queryset = session.query(self.characters_list_model).all()
        existing_data = {}
        for data in existing_data_queryset:
            existing_data[data.row] = {
                "name": data.name,
                "type": data.type,
                "master_id": data.master_id
            }

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "characters", self.story_index, existing_data)
        self.ui.search_for_suggestions.connect(self.send_matching_suggestions_for_row)
        self.ui.row_clicked.connect(self.receive_clicked_row_data)
        self.ui.row_data_edited.connect(self.receive_edited_row_data)
        self.ui.close_table.connect(self.navigate_to_game_dashboard)
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        
    def send_matching_suggestions_for_row(self, current_typed_data_dict):
        print(f"Current typed data in row {current_typed_data_dict['row']} is {current_typed_data_dict['data']}")

    def receive_clicked_row_data(self, data):
        from views.gallery import GalleryView
        if data['name']:
            result = session.query(self.characters_list_model).filter(
                self.characters_list_model.row == data['row_index'],
                self.characters_list_model.name == data['name'],
                self.characters_list_model.type == data['type']
            ).first()
            if result:
                master_id = result.master_id
            self.controller.show_view(GalleryView, story_index=self.story_index, first_nav_type=data['type'], first_nav_id=master_id, prev_view='characters list')

    def receive_edited_row_data(self, data):
        # Add data to respective master tables
        master_tables_model = MODEL_MAP.get(data['type'])
        if master_tables_model:
            duplicates = session.query(master_tables_model).filter(
                master_tables_model.name == data["name"],
                master_tables_model.story_index == self.story_index
            ).all()

            if duplicates:
                user_choice = self.ui.prompt_duplicate_action(data["name"])

                if user_choice == "overwrite":
                    # Dealing only with the first entry in case of multiple duplicates for now. Shall add selection pop-up to select exact duplicate later.
                    duplicates[0].name = data["name"]
                    duplicates[0].story_index = self.story_index
                    existing_master_data_id = duplicates[0].id

                    session.query(self.characters_list_model).filter(self.characters_list_model.row == data['row']).update({
                        "name": data["name"],
                        "type": data["type"],
                        "master_id": existing_master_data_id
                        })

                elif user_choice == "remove":
                    pass

            new_master_data = master_tables_model(name=data["name"], story_index=self.story_index)
            session.add(new_master_data)
            session.flush()
            new_master_data_id = new_master_data.id
            
            new_notes_add = Notes(type=data["type"], type_id=new_master_data_id, story_index=self.story_index)
            session.add(new_notes_add)

            # Update the dynamic characters list table specific to the story
            session.query(self.characters_list_model).filter(self.characters_list_model.row == data['row']).update({
                "name": data["name"],
                "type": data["type"],
                "master_id": new_master_data_id
                })
        session.commit()  # Commit once at the end

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass

    def navigate_to_game_dashboard(self):
        """Navigates back to the game dashboard."""
        self.controller.show_view(GameDashboardView, story_index=self.story_index)

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

        existing_data_queryset = session.query(self.threads_list_model).all()
        existing_data = {}
        for data in existing_data_queryset:
            existing_data[data.row] = {
                "thread": data.thread
            }

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "threads", self.story_index, existing_data)
        self.setLayout(self.ui.layout)  # Use UI's layout directly
        
    def receive_edited_rows_data(self, data):
        """Receives edited data from UI when closing."""
        for row, thread_data in data.items():
            session.query(self.threads_list_model).filter(self.threads_list_model.row == row).update({"thread": thread_data["thread"]})
            session.commit()

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass

        # At the end of scene, roll d10. If roll <= chaos_factor, chaos_factor-1. Else chaos_factor+1. Chaos factor cannot be less than 1 or greater than 9
        # roll = random.randint(1, 10)
        # if roll <= self.chaos_factor:
        #     self.chaos_factor = max(1, self.chaos_factor - 1)
        # else:
        #     self.chaos_factor = min(9, self.chaos_factor + 1)
        # self.chaos_factor_changed.emit(self.chaos_factor)