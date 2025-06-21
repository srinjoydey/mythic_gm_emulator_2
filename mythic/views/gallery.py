from PySide6.QtWidgets import QWidget
from ui.gallery_ui import GalleryUI
from models.db_config import session
from models.master_tables import Characters, Places, Items, Notes


MODEL_MAP = {"characters": Characters, "places": Places, "items": Items}

class GalleryView(QWidget):
    """Handles main menu logic & navigation."""

    def __init__(self, parent, controller, story_index=None, first_nav_type=None, first_nav_id=None, prev_view=None):
        super().__init__(parent)
        self.controller = controller
        self.story_index = story_index

        if self.story_index is None:
            characters_list = [('characters', id, name) for id, name in session.query(Characters).with_entities(Characters.id, Characters.name).all()]
            places_list = [('places', id, name) for id, name in session.query(Places).with_entities(Places.id, Places.name).all()]
            items_list = [('items', id, name) for id, name in session.query(Items).with_entities(Items.id, Items.name).all()]
        else:
            characters_list = [('characters', id, name) for id, name in session.query(Characters).with_entities(Characters.id, Characters.name).filter(Characters.story_index == self.story_index, Characters.active == True).all()]
            places_list = [('places', id, name) for id, name in session.query(Places).with_entities(Places.id, Places.name).filter(Places.story_index == self.story_index, Places.active == True).all()]
            items_list = [('items', id, name) for id, name in session.query(Items).with_entities(Items.id, Items.name).filter(Items.story_index == self.story_index, Items.active == True).all()]

        characters_nav_bar_list = sorted(characters_list + places_list + items_list, key=lambda x: x[2])

        # Attach UI with navigation logic
        self.ui = GalleryUI(self, controller, characters_nav_bar_list, first_nav_type=first_nav_type, first_nav_id=first_nav_id, prev_view=prev_view)
        self.ui.details_data_ready.connect(self.post_edited_nav_items_data)
        self.ui.close_gallery.connect(self.navigate_to_previous_view)
        self.ui.image_uploaded.connect(self.save_uploaded_image)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

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
