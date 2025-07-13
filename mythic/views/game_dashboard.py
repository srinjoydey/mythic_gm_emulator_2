from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import QTimer
from ui.game_dashboard_ui import GameDashboardUI
from models.master_tables import StoriesIndex, Characters, Places, Items, Notes, Threads, ThreadsNotes
from views.gallery import GalleryView 
from models.db_config import session
from utils.static_data.tables_index import TESTING_THE_EXPECTED_SCENE
from utils.utils_functions import get_dice_roll_result 

MODEL_MAP = {"character": Characters, "place": Places, "item": Items}
LIST_DICE_ROLL_MAP = {
    1: "1 - 2",
    2: "1 - 2",
    3: "3 - 4",
    4: "3 - 4",
    5: "5 - 6",
    6: "5 - 6",
    7: "7 - 8",
    8: "7 - 8",
    9: "9 - 10",
    10: "9 - 10"
}

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
        self.ui.main_menu_button_clicked.connect(self.navigate_to_main_menu)
        self.ui.existing_stories_button_clicked.connect(self.navigate_to_existing_stories)
        self.ui.start_scene_action_selected.connect(self.handle_start_scene_action)
        self.ui.start_scene_action_resolution.connect(self.resolve_start_scene_action)
        self.ui.chaos_factor_changed.connect(self.post_updated_chaos_factor)
        self.ui.roll_for_chaos_factor.connect(self.roll_and_update_chaos_factor)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def navigate_to_oracles_tables(self):
        from views.main_menu import OraclesTablesView
        self.controller.show_view(OraclesTablesView, prev_view='game dashboard', first_nav_item=None, story_index=self.story_index, chaos_factor=self.chaos_factor)

    def navigate_to_characters_list(self, story_index):
        self.controller.show_view(CharactersList, story_index=story_index)

    def navigate_to_threads_list(self, story_index):       
        self.controller.show_view(ThreadsList, story_index=story_index)

    def navigate_to_gallery_modal(self, story_index):
        self.controller.show_view(GalleryView, story_index=story_index, prev_view='game dashboard')

    def navigate_to_main_menu(self):
        from views.main_menu import MainMenu
        self.controller.show_view(MainMenu)

    def handle_start_scene_action(self, action):
        if action == "Test the Expected Scene":
            self.ui.test_expected_scene(TESTING_THE_EXPECTED_SCENE)
        elif action == "Go to Fate Chart / Oracle":
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

    def navigate_to_main_menu(self):
        from views.main_menu import MainMenu

        self.controller.show_view(MainMenu)

    def navigate_to_existing_stories(self):
        from views.main_menu import ExistingStoryView

        all_stories = session.query(StoriesIndex).all()
        if not all_stories or all(story.name is None for story in all_stories):
            self.ui.show_message_under_existing_btn("No stories found. Please create a New Story.")
        else:
            self.controller.show_view(ExistingStoryView, all_stories=all_stories)

    def roll_and_update_chaos_factor(self):
        roll = get_dice_roll_result(10)[0]
        if roll <= self.chaos_factor:
            new_chaos_factor = max(1, self.chaos_factor - 1)
            colour = "green"
        else:
            new_chaos_factor = min(9, self.chaos_factor + 1)
            colour = "red"
        self.chaos_factor = new_chaos_factor
        self.post_updated_chaos_factor(self.chaos_factor)
        QTimer.singleShot(3000, lambda: self.ui.counter_label.setText(str(self.chaos_factor)))
        self.ui.show_chaos_factor_roll_result(colour)

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

        self.characters_master_queryset = session.query(Characters).filter(Characters.story_index == self.story_index)
        self.places_master_queryset = session.query(Places).filter(Places.story_index == self.story_index)
        self.items_master_queryset = session.query(Items).filter(Items.story_index == self.story_index)

        self.characters_list_model = create_dynamic_model(CharactersListModel, self.table_name)

        existing_data_queryset = session.query(self.characters_list_model).all()
        self.existing_data = {}
        for data in existing_data_queryset:
            self.existing_data[data.row] = {
                "name": data.name,
                "type": data.type,
                "master_id": data.master_id
            }

        self.duplicate_resolution_pending = False

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "characters", self.story_index, self.existing_data)
        self.ui.search_for_suggestions.connect(self.send_matching_suggestions_for_row)
        self.ui.row_clicked.connect(self.receive_clicked_row_data)
        self.ui.section_label_double_clicked.connect(self.roll_on_characters_list)
        self.ui.row_data_edited.connect(self.receive_edited_row_data)
        self.ui.request_close_table.connect(self.handle_request_close_table)
        self.ui.close_table.connect(self.navigate_to_game_dashboard)
        self.ui.clear_all_rows.connect(self.clear_all_rows_data)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def receive_clicked_row_data(self, data):
        if data['name']:
            result = session.query(self.characters_list_model).filter(
                self.characters_list_model.row == data['row_index'],
                self.characters_list_model.name == data['name'],
                self.characters_list_model.type == data['type']
            ).first()
            if result:
                master_id = result.master_id
                self.controller.show_view(
                    GalleryView,
                    story_index=self.story_index,
                    first_nav_type=data['type'],
                    first_nav_id=master_id,
                    prev_view='characters list'
                )
        
    def send_matching_suggestions_for_row(self, current_typed_data_dict):
        if current_typed_data_dict['data']:
            matching_characters_queryset = self.characters_master_queryset.filter(
                Characters.active==False, Characters.name.like(f"%{current_typed_data_dict['data']}%")
            ).with_entities(Characters.id, Characters.name)
            matching_places_queryset = self.places_master_queryset.filter(
                Places.active==False, Places.name.like(f"%{current_typed_data_dict['data']}%")
            ).with_entities(Places.id, Places.name)
            matching_items_queryset = self.items_master_queryset.filter(Items.active == False).filter(
                Items.name.like(f"%{current_typed_data_dict['data']}%")
            ).with_entities(Items.id, Items.name)

            suggestions = {}

            for char_id, char_name in matching_characters_queryset:
                suggestions[f"characters"] = {"id": char_id, "name": char_name}
            for place_id, place_name in matching_places_queryset:
                suggestions[f"places"] = {"id": place_id, "name": place_name}
            for item_id, item_name in matching_items_queryset:
                suggestions[f"items"] = {"id": item_id, "name": item_name}

            all_names = [(v["id"], v['name']) for k, v in suggestions.items()]
            if all_names:
                all_names.sort(key=lambda x: (x[1].lower(), x[0]))  # Sort by name (case-insensitive), then id

            # Find the QLineEdit for this row
            row_index = current_typed_data_dict['row']
            table_cell = None
            for le in self.ui.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break

            if table_cell is not None:
                self.ui.show_suggestions_popup(table_cell, all_names)

    def receive_edited_row_data(self, data):
        master_tables_model = MODEL_MAP.get(data['type'])
        data_action = data.get("action")

        duplicates = session.query(master_tables_model).filter(
            master_tables_model.story_index == self.story_index, 
            master_tables_model.name == data["name"]
        ).all()

        if data_action == "delete":
            # Remove from story-specific list
            self.delete_row_data(data, master_tables_model)
            if getattr(self, "close_requested", False):
                self.navigate_to_game_dashboard()

        elif duplicates:
            user_choice = self.ui.prompt_duplicate_action(data["name"])

            if user_choice == "Create New":
                self.create_row_data(data, master_tables_model)
                if getattr(self, "close_requested", False):
                    self.navigate_to_game_dashboard()
            elif user_choice in ("Select Existing", "Overwrite Existing"):
                self.duplicate_resolution_pending = True  # Prevent closing the table until resolution is handled
                data['action'] = "select" if user_choice == "Select Existing" else "overwrite"
                self.controller.show_view(
                    GalleryView,
                    story_index=self.story_index,
                    first_nav_type=data['type'],
                    first_nav_id=duplicates[0].id,
                    prev_view='characters list',
                    search_data=data, include_inactive=True
                )
                self.controller.current_view.ui.list_action_nav_item.connect(
                    lambda nav_type, nav_id: self.handle_gallery_selection(nav_type, nav_id, data, master_tables_model)
                )

            elif user_choice == "Remove Entry":
                self.controller.show_view(CharactersList, story_index=self.story_index)
                if getattr(self, "close_requested", False):
                    self.navigate_to_game_dashboard()

        else:
            # No duplicates, create new entry
            self.create_row_data(data, master_tables_model)
            if getattr(self, "close_requested", False):
                self.navigate_to_game_dashboard()

    def handle_gallery_selection(self, nav_type, nav_id, data, master_tables_model):
        self.select_or_overwrite_existing_item(nav_type, nav_id, data, master_tables_model)
        self.duplicate_resolution_pending = False
        if getattr(self, "close_requested", False):
            self.navigate_to_game_dashboard()

    def create_row_data(self, data, master_tables_model):
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
        session.flush()
        session.commit()  # Commit once at the end
        self.controller.show_view(CharactersList, story_index=self.story_index)

    def delete_row_data(self, data, master_tables_model):
        session.query(self.characters_list_model).filter(self.characters_list_model.row == data['row']).update({
                    "name": None,
                    "type": None,
                    "master_id": None
                })
        # Handle deletion of the row
        session.flush
        session.commit()
        deletion_type = self.ui.prompt_deletion_type()
        if deletion_type is not None:
            self.controller.show_view(CharactersList, story_index=self.story_index)

            if deletion_type == "Delete from Story":
                # Also mark the master data as inactive
                session.query(master_tables_model).filter(master_tables_model.id == data["master_id"]).update({"active": False})
                # Mark related notes as inactive
                session.query(Notes).filter(Notes.type == data['type'], Notes.type_id == data["master_id"]).update({"active": False})

            elif deletion_type == "Delete from Game":
                # Also delete from the master data
                session.query(master_tables_model).filter(master_tables_model.id == data["master_id"]).delete()
                # Delete related notes
                session.query(Notes).filter(Notes.type == data['type'], Notes.type_id == data["master_id"]).delete()

        session.commit()
        return

    def select_or_overwrite_existing_item(self, existing_nav_type, existing_nav_id, new_record_data, master_tables_model):
        """Handles the selection or overwriting of an existing navigation item."""
        list_row = new_record_data.get('row')
        list_row_to_update = session.query(self.characters_list_model).filter(self.characters_list_model.row == list_row).first()
        existing_nav_type = existing_nav_type[:-1]
        selected_master_data = session.query(master_tables_model).filter(master_tables_model.id == existing_nav_id).first()
        related_notes = session.query(Notes).filter(Notes.type == existing_nav_type, Notes.type_id == existing_nav_id).first()
        
        list_row_to_update.name = selected_master_data.name
        list_row_to_update.type = existing_nav_type
        list_row_to_update.master_id = existing_nav_id

        if new_record_data['action'] == "overwrite":
            if existing_nav_type == "character":
                selected_master_data.race = None
                selected_master_data.age = None
                selected_master_data.role_profession = None
                selected_master_data.social_status = None
                selected_master_data.economic_status = None
            elif existing_nav_type == "place":
                selected_master_data.weather = None
                selected_master_data.smell = None
            elif existing_nav_type == "item":
                selected_master_data.material = None
                selected_master_data.rarity = None
            related_notes.notes = None

        if selected_master_data.active is False:
            selected_master_data.active = True
        if related_notes.active is False:
            related_notes.active = True

        session.flush()
        session.commit()
        self.controller.show_view(CharactersList, story_index=self.story_index)

    def handle_request_close_table(self):
        self.close_requested = True
        if not self.duplicate_resolution_pending:
            self.navigate_to_game_dashboard()

    def roll_on_characters_list(self, row_index, section_label_text):
        """Rolls on the characters list based on the section label."""
        section_label_result = ["1 - 2"]
        row_label_result = []
        if section_label_text != "1 - 2":
            section_label_dice_result = get_dice_roll_result(int(section_label_text.split(" - ")[1]))
            section_label_result = [LIST_DICE_ROLL_MAP.get(section_label_dice_result[0])]
        row_label_dice_result = get_dice_roll_result(10, flutter=True)
        for roll in row_label_dice_result:
            row_label_result.append(LIST_DICE_ROLL_MAP.get(roll))

        self.ui.highlight_rolled_row(section_label_result, row_label_result)

    def clear_all_rows_data(self):
        character_master_ids = []
        place_master_ids = []
        item_master_ids = []
        for k, v in self.existing_data.items():
            if v['name'] is not None:
                if v['type'] == "character":
                    character_master_ids.append(v['master_id'])
                elif v['type'] == "place":
                    place_master_ids.append(v['master_id'])
                elif v['type'] == "item":
                    item_master_ids.append(v['master_id'])
        if character_master_ids:
            session.query(Characters).filter(Characters.id.in_(character_master_ids)).update({"active": False}, synchronize_session=False)
        if place_master_ids:
            session.query(Places).filter(Places.id.in_(place_master_ids)).update({"active": False}, synchronize_session=False)
        if item_master_ids:
            session.query(Items).filter(Items.id.in_(item_master_ids)).update({"active": False}, synchronize_session=False)

        session.query(self.characters_list_model).update({
            "name": None,
            "type": None,
            "master_id": None
        }, synchronize_session=False)

        session.commit()
        self.controller.show_view(CharactersList, story_index=self.story_index)

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

        self.threads_master_queryset = session.query(Threads).filter(Threads.story_index == self.story_index)

        self.threads_list_model = create_dynamic_model(ThreadsListModel, self.table_name)

        existing_data_queryset = session.query(self.threads_list_model).all()
        existing_data = {}
        for data in existing_data_queryset:
            existing_data[data.row] = {
                "thread": data.thread,
                "master_id": data.master_id
            }

        self.duplicate_resolution_pending = False

        # Attach UI with navigation logic
        self.ui = CharactersThreadsTablesUI(self, controller, "threads", self.story_index, existing_data)
        self.ui.search_for_suggestions.connect(self.send_matching_suggestions_for_row)
        self.ui.row_clicked.connect(self.receive_clicked_row_data)
        self.ui.section_label_double_clicked.connect(self.roll_on_threads_list)
        self.ui.row_data_edited.connect(self.receive_edited_row_data)
        self.ui.request_close_table.connect(self.handle_request_close_table)
        self.ui.close_table.connect(self.navigate_to_game_dashboard)
        self.ui.clear_all_rows.connect(self.clear_all_rows_data)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def receive_clicked_row_data(self, data):
        if data['thread']:
            result = session.query(self.threads_list_model).filter(
                self.threads_list_model.row == data['row_index'],
                self.threads_list_model.thread == data['thread'],
            ).first()
            if result:
                master_id = result.master_id
            self.controller.show_view(GalleryView, story_index=self.story_index, first_nav_id=master_id, prev_view='threads list', view='Threads')

    def send_matching_suggestions_for_row(self, current_typed_data_dict):
        # from ui.game_dashboard_ui import ThreadLineEdit

        if current_typed_data_dict['data']:
            matching_threads_queryset = self.threads_master_queryset.filter(
                Threads.active == False,
                Threads.thread.like(f"%{current_typed_data_dict['data']}%"),
                Threads.story_index == self.story_index
            ).with_entities(Threads.id, Threads.thread)

            suggestions = {}

            for thread_id, thread_name in matching_threads_queryset:
                suggestions[f"threads"] = {"id": thread_id, "name": thread_name}

            all_names = [(v["id"], v['name']) for k, v in suggestions.items()]
            if all_names:
                all_names.sort(key=lambda x: (x[1].lower(), x[0]))  # Sort by name (case-insensitive), then id

            # Find the QLineEdit for this row
            row_index = current_typed_data_dict['row']
            table_cell = None
            for le in self.ui.scroll_widget.findChildren(QLineEdit):
                if le.property("row_index") == row_index:
                    table_cell = le
                    break

            if table_cell is not None:
                self.ui.show_suggestions_popup(table_cell, all_names)

    def receive_edited_row_data(self, data):
        data_action = data.get("action")

        duplicates = session.query(Threads).filter(
            Threads.story_index == self.story_index, 
            Threads.thread == data["thread"]
        ).all()

        if data_action == "delete":
            # Remove from story-specific list
            self.delete_row_data(data)
            if getattr(self, "close_requested", False):
                self.navigate_to_game_dashboard()

        elif duplicates:
            user_choice = self.ui.prompt_duplicate_action(data["thread"])

            if user_choice == "Create New":
                self.create_row_data(data)
                if getattr(self, "close_requested", False):
                    self.navigate_to_game_dashboard()
            elif user_choice in ("Select Existing", "Overwrite Existing"):
                self.duplicate_resolution_pending = True  # Prevent closing the table until resolution is handled
                data['action'] = "select" if user_choice == "Select Existing" else "overwrite"
                self.controller.show_view(
                    GalleryView,
                    story_index=self.story_index,
                    first_nav_id=duplicates[0].id,
                    prev_view='threads list',
                    search_data=data, include_inactive=True, view='Threads'
                )
                self.controller.current_view.ui.list_action_nav_item.connect(
                    lambda nav_type, nav_id: self.handle_gallery_selection(nav_id, data)
                )
            elif user_choice == "Remove Entry":
                self.controller.show_view(ThreadsList, story_index=self.story_index)
                if getattr(self, "close_requested", False):
                    self.navigate_to_game_dashboard()

        else:
            # No duplicates, create new entry
            self.create_row_data(data)
            if getattr(self, "close_requested", False):
                self.navigate_to_game_dashboard()

    def handle_gallery_selection(self, nav_id, data):
        self.select_or_overwrite_existing_item(nav_id, data)
        self.duplicate_resolution_pending = False
        if getattr(self, "close_requested", False):
            self.navigate_to_game_dashboard()

    def create_row_data(self, data):
        new_master_data = Threads(thread=data["thread"], story_index=self.story_index)
        session.add(new_master_data)
        session.commit()
        new_master_data_id = new_master_data.id
        new_notes_add = ThreadsNotes(thread_id=new_master_data_id, story_index=self.story_index)
        session.add(new_notes_add)
        session.commit()

        # Update the dynamic characters list table specific to the story
        session.query(self.threads_list_model).filter(self.threads_list_model.row == data['row']).update({
            "thread": data["thread"],
            "master_id": new_master_data_id
        })
        session.flush()
        session.commit()  # Commit once at the end
        self.controller.show_view(ThreadsList, story_index=self.story_index)

    def delete_row_data(self, data):
        session.query(self.threads_list_model).filter(self.threads_list_model.row == data['row']).update({
            "thread": None,
            "master_id": None
        })
        # Handle deletion of the row
        session.flush()
        session.commit()
        deletion_type = self.ui.prompt_deletion_type()
        if deletion_type is not None:
            self.controller.show_view(ThreadsList, story_index=self.story_index)

            if deletion_type == "Delete from Story":
                # Also mark the master data as inactive
                session.query(Threads).filter(Threads.id == data["master_id"]).update({"active": False})
                # Mark related notes as inactive
                session.query(ThreadsNotes).filter(ThreadsNotes.thread_id == data["master_id"]).update({"active": False})

            elif deletion_type == "Delete from Game":
                # Also delete from the master data
                session.query(Threads).filter(Threads.id == data["master_id"]).delete()
                # Delete related notes
                session.query(ThreadsNotes).filter(ThreadsNotes.thread_id == data["master_id"]).delete()

        session.commit()
        return
    
    def select_or_overwrite_existing_item(self, existing_nav_id, new_record_data):
        """Handles the selection or overwriting of an existing navigation item."""
        list_row = new_record_data.get('row')
        list_row_to_update = session.query(self.threads_list_model).filter(self.threads_list_model.row == list_row).first()
        selected_master_data = session.query(Threads).filter(Threads.id == existing_nav_id).first()
        related_notes = session.query(ThreadsNotes).filter(ThreadsNotes.thread_id == existing_nav_id).first()

        list_row_to_update.thread = selected_master_data.thread
        list_row_to_update.master_id = existing_nav_id

        if new_record_data['action'] == "overwrite":
            selected_master_data.thread = None

        if selected_master_data.active is False:
            selected_master_data.active = True
        if related_notes.active is False:
            related_notes.active = True

        session.flush()
        session.commit()
        self.controller.show_view(ThreadsList, story_index=self.story_index)

    def handle_request_close_table(self):
        self.close_requested = True
        # If a duplicate popup is currently being handled, do not close yet.
        if not self.duplicate_resolution_pending:
            self.navigate_to_game_dashboard()
    
    def roll_on_threads_list(self, row_index, section_label_text):
        """Rolls on the threads list based on the section label."""
        section_label_result = ["1 - 2"]
        row_label_result = []
        if section_label_text != "1 - 2":
            section_label_dice_result = get_dice_roll_result(int(section_label_text.split(" - ")[1]))
            section_label_result = [LIST_DICE_ROLL_MAP.get(section_label_dice_result[0])]
        row_label_dice_result = get_dice_roll_result(10, flutter=True)
        for roll in row_label_dice_result:
            row_label_result.append(LIST_DICE_ROLL_MAP.get(roll))

        self.ui.highlight_rolled_row(section_label_result, row_label_result)

    def clear_all_rows_data(self):
        for k, v in self.ui.existing_data.items():
            if v['thread'] is not None:
                session.query(Threads).filter(Threads.id == v['master_id']).update({"active": False}, synchronize_session=False)

        session.query(self.threads_list_model).update({
            "thread": None,
            "master_id": None
        }, synchronize_session=False)

        session.commit()
        self.controller.show_view(ThreadsList, story_index=self.story_index)
    
    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass

    def navigate_to_game_dashboard(self):
        """Navigates back to the game dashboard."""
        self.controller.show_view(GameDashboardView, story_index=self.story_index)
