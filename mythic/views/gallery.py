from PySide6.QtWidgets import QWidget
from sqlalchemy import func
from ui.gallery_ui import GalleryUI, ThreadsGalleryUI
from models.db_config import session
from models.master_tables import StoriesIndex, Characters, Places, Items, Notes, Threads, ThreadsNotes


MODEL_MAP = {"characters": Characters, "places": Places, "items": Items}

class GalleryView(QWidget):
    """Handles main menu logic & navigation."""

    def __init__(self, parent, controller, story_index=None, first_nav_type=None, first_nav_id=None, prev_view=None, search_data=None, include_inactive=False, view="Characters"):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index
        existing_stories = {}
        self.multi_story_mode = self.story_index is None
        self.view = view

        if self.story_index is None:
            existing_stories = {story.index: story.name for story in session.query(StoriesIndex).all()}
            if view == "Characters":
                self.characters_base_queryset = session.query(Characters).with_entities(Characters.story_index, Characters.id, Characters.name)
                self.places_base_queryset = session.query(Places).with_entities(Places.story_index, Places.id, Places.name) 
                self.items_base_queryset = session.query(Items).with_entities(Items.story_index, Items.id, Items.name)

                self.characters_queryset = self.characters_base_queryset
                self.places_queryset = self.places_base_queryset
                self.items_queryset = self.items_base_queryset
            else:
                self.threads_base_queryset = session.query(Threads).with_entities(Threads.story_index, Threads.id, Threads.thread)
                self.threads_queryset = self.threads_base_queryset

            if not include_inactive: # Only toggle active/inactive on the first call
                self.toggle_active_inactive("Active")

            self.get_list_from_queryset(multi_story_mode=self.multi_story_mode)
        else:
            if view == "Characters":
                self.characters_base_queryset = session.query(Characters).with_entities(Characters.id, Characters.name).filter(Characters.story_index == self.story_index)
                self.places_base_queryset = session.query(Places).with_entities(Places.id, Places.name).filter(Places.story_index == self.story_index)
                self.items_base_queryset = session.query(Items).with_entities(Items.id, Items.name).filter(Items.story_index == self.story_index)

                self.characters_queryset = self.characters_base_queryset
                self.places_queryset = self.places_base_queryset
                self.items_queryset = self.items_base_queryset
            else:
                self.threads_base_queryset = session.query(Threads).with_entities(Threads.id, Threads.thread).filter(Threads.story_index == self.story_index)
                self.threads_queryset = self.threads_base_queryset

            if not include_inactive: # Only toggle active/inactive on the first call
                self.toggle_active_inactive("Active")

            self.get_list_from_queryset(multi_story_mode=self.multi_story_mode)

        if view == "Characters":
            self.nav_bar_list = self.characters_list + self.places_list + self.items_list
            self.ui = GalleryUI(self, controller, self.nav_bar_list, existing_stories, first_nav_type=first_nav_type, first_nav_id=first_nav_id, prev_view=prev_view, search_with=search_data)
        else:
            self.nav_bar_list = self.threads_list
            self.ui = ThreadsGalleryUI(self, controller, self.nav_bar_list, existing_stories, first_nav_id=first_nav_id, prev_view=prev_view, search_with=search_data)

        # Attach UI with navigation logic
        self.ui.search_options_changed.connect(self.search_nav_items)
        self.ui.details_data_ready.connect(self.post_edited_nav_items_data)
        self.ui.close_gallery.connect(self.navigate_to_previous_view)
        self.ui.image_uploaded.connect(self.save_uploaded_image)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def get_list_from_queryset(self, multi_story_mode):
        if self.view == "Characters":
            if multi_story_mode:
                if self.characters_queryset is not None:
                    self.characters_list = [('characters', story_index, id, name) for story_index, id, name in self.characters_queryset.all()]
                else:
                    self.characters_list = []
                if self.places_queryset is not None:
                    self.places_list = [('places', story_index, id, name) for story_index, id, name in self.places_queryset.all()]
                else:
                    self.places_list = []
                if self.items_queryset is not None:
                    self.items_list = [('items', story_index, id, name) for story_index, id, name in self.items_queryset.all()]
                else:
                    self.items_list = []
            else:
                if self.characters_queryset is not None:
                    self.characters_list = [('characters', id, name) for id, name in self.characters_queryset.all()]
                else:
                    self.characters_list = []
                if self.places_queryset is not None:
                    self.places_list = [('places', id, name) for id, name in self.places_queryset.all()]
                else:
                    self.places_list = []
                if self.items_queryset is not None:
                    self.items_list = [('items', id, name) for id, name in self.items_queryset.all()]
                else:
                    self.items_list = []
        else:
            if multi_story_mode:
                if self.threads_queryset is not None:
                    self.threads_list = [(story_index, id, thread) for story_index, id, thread in self.threads_queryset.all()]
                else:
                    self.threads_list = []
            else:
                if self.threads_queryset is not None:
                    self.threads_list = [(id, thread) for id, thread in self.threads_queryset.all()]
                else:
                    self.threads_list = []

    def toggle_active_inactive(self, active_inactive_flag):
        if self.view == "Characters":
            if active_inactive_flag == "Active" :
                self.characters_queryset = self.characters_queryset.filter(Characters.active == True) if self.characters_queryset else None
                self.places_queryset = self.places_queryset.filter(Places.active == True) if self.places_queryset else None
                self.items_queryset = self.items_queryset.filter(Items.active == True) if self.items_queryset else None
            if active_inactive_flag == "Inactive":
                self.characters_queryset = self.characters_queryset.filter(Characters.active == False) if self.characters_queryset else None
                self.places_queryset = self.places_queryset.filter(Places.active == False) if self.places_queryset else None
                self.items_queryset = self.items_queryset.filter(Items.active == False) if self.items_queryset else None
        else:
            if active_inactive_flag == "Active":
                self.threads_queryset = self.threads_queryset.filter(Threads.active == True) if self.threads_queryset else None
            if active_inactive_flag == "Inactive":
                self.threads_queryset = self.threads_queryset.filter(Threads.active == False) if self.threads_queryset else None

    def sort_nav_items(self, sort_position, sort_order):
        if sort_order == "Ascending":
            self.nav_bar_list.sort(key=lambda x: x[sort_position])
        elif sort_order == "Descending":
            self.nav_bar_list.sort(key=lambda x: x[sort_position], reverse=True)

    def navigate_to_previous_view(self, prev_view):
        if prev_view == 'main menu':
            from views.main_menu import MainMenu
            self.controller.show_view(MainMenu)
        elif prev_view == 'game dashboard':
            from views.game_dashboard import GameDashboardView
            self.controller.show_view(GameDashboardView, story_index=self.story_index)
        elif prev_view == 'characters list':
            from views.game_dashboard import CharactersList
            self.controller.show_view(CharactersList, story_index=self.story_index)
        elif prev_view == 'threads list':
            from views.game_dashboard import ThreadsList
            self.controller.show_view(ThreadsList, story_index=self.story_index)

    def post_edited_nav_items_data(self, details_data_dict):
        if details_data_dict:
            for key, value in details_data_dict.items():
                model_type, model_id = key.split("-")
                model = MODEL_MAP[model_type]
                data = session.query(model).filter(model.id == model_id).first()
                notes_edited_data = value.pop("notes", None)
                if data:
                    for data_field, data_value in value.items():
                        setattr(data, data_field, data_value)

                    if notes_edited_data:
                        model_type = model_type[:-1]
                        notes_data = session.query(Notes).filter(Notes.type == model_type, Notes.type_id == model_id).first()
                        notes_data.notes = notes_edited_data
                        
                    session.commit()

    def get_nav_item_data(self, nav_type, nav_id):
        if self.view == "Characters":
            model = MODEL_MAP[nav_type]
            data = session.query(model).filter(model.id == nav_id).first()
            nav_type = nav_type[:-1]
            related_notes = session.query(Notes).filter(Notes.type == nav_type, Notes.type_id == nav_id).first()
            if data:
                # Return a dict of all fields
                data = {field: getattr(data, field, "") for field in self.ui.details_fields or []}
                if related_notes:
                    data["notes"] = related_notes.notes
                return data
            return {}
        else:
            data = session.query(Threads).filter(Threads.id == nav_id).first()
            related_notes = session.query(ThreadsNotes).filter(ThreadsNotes.thread_id == nav_id).first()
            if data:
                data = {"id": data.id, "thread": data.thread, "image_path": data.image_path}
                if related_notes:
                    data["notes"] = related_notes.notes
                return data
            return {}

    def search_nav_items(self, sort, show, categories, stories, search_data=None):
        sort_position = None
        # only have selected categories
        if self.view == "Characters":
            if 'Characters' not in categories:
                self.characters_queryset = None
            else:
                self.characters_queryset = self.characters_base_queryset
            if 'Places' not in categories:
                self.places_queryset = None
            else:
                self.places_queryset = self.places_base_queryset
            if 'Items' not in categories:
                self.items_queryset = None
            else:
                self.items_queryset = self.items_base_queryset
            # if the gallery view can host multiple stories, filter by selected stories
            if self.multi_story_mode:
                if self.characters_queryset:
                    self.characters_queryset = self.characters_queryset.filter(Characters.story_index.in_(stories))
                if self.places_queryset:
                    self.places_queryset = self.places_queryset.filter(Places.story_index.in_(stories))
                if self.items_queryset:
                    self.items_queryset = self.items_queryset.filter(Items.story_index.in_(stories))

                sort_position = 3
            else:
                sort_position = 2

            if search_data:
                # If search text is present, filter the querysets based on the search text
                if self.characters_queryset:
                    self.characters_queryset = self.characters_queryset.filter(func.lower(Characters.name).like(f"%{search_data.lower()}%"))
                if self.places_queryset:
                    self.places_queryset = self.places_queryset.filter(func.lower(Places.name).like(f"%{search_data.lower()}%"))
                if self.items_queryset:
                    self.items_queryset = self.items_queryset.filter(func.lower(Items.name).like(f"%{search_data.lower()}%"))
            
            # filter querysets based on whether active or inactive
            if show == "Inactive":
                self.toggle_active_inactive("Inactive")
            elif show == "Active":
                self.toggle_active_inactive("Active")

            if self.multi_story_mode:
                self.get_list_from_queryset(multi_story_mode=True)
            else:
                self.get_list_from_queryset(multi_story_mode=False)
            # Rebuild the nav_bar_list
            self.nav_bar_list = self.characters_list + self.places_list + self.items_list
        
        else:
            # if the gallery view can host multiple stories, filter by selected stories
            if self.multi_story_mode and self.threads_queryset:
                self.threads_queryset = self.threads_queryset.filter(Threads.story_index.in_(stories))
                sort_position = 2
            else:
                sort_position = 1

            if search_data:
                # If search text is present, filter the queryset based on the search text
                if self.threads_queryset:
                    self.threads_queryset = self.threads_queryset.filter(func.lower(Threads.thread).like(f"%{search_data.lower()}%"))

            # filter querysets based on whether active or inactive
            if show == "Inactive":
                self.toggle_active_inactive("Inactive")
            elif show == "Active":
                self.toggle_active_inactive("Active")

            if self.multi_story_mode:
                self.get_list_from_queryset(multi_story_mode=True)
            else:
                self.get_list_from_queryset(multi_story_mode=False)
            # Rebuild the nav_bar_list
            self.nav_bar_list = self.threads_list

        # Sort
        if sort == "Descending":
            self.sort_nav_items(sort_position, "Descending")
        elif sort == "Ascending":
            self.sort_nav_items(sort_position, "Ascending")
        self.ui.update_nav_bar(self.nav_bar_list)

    def save_uploaded_image(self, image_path):
        """Saves the uploaded image path to the database."""
        if self.ui.current_nav_type and self.ui.current_nav_id:
            model = MODEL_MAP[self.ui.current_nav_type]
            data = session.query(model).filter(model.id == self.ui.current_nav_id).first()
            if data:
                data.image_path = image_path
                session.commit()

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass
