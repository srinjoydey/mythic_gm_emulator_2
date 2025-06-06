from PySide6.QtWidgets import QWidget
from ui.gallery_ui import GalleryModalUI
from models.db_config import session
from models.master_tables import Characters, Places, Items


MODEL_MAP = {"characters": Characters, "places": Places, "items": Items}

class GalleryModalView(QWidget):
    """Handles main menu logic & navigation."""

    def __init__(self, parent, controller, story_index=None):
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
        self.ui = GalleryModalUI(self, controller, characters_nav_bar_list)
        self.ui.details_data_ready.connect(self.receive_details_data)
        self.ui.close_modal.connect(self.navigate_to_game_dashboard)
        self.setLayout(self.ui.layout)  # Use UI's layout directly

    def navigate_to_game_dashboard(self):
        from views.game_dashboard import GameDashboardView
        self.controller.show_view(GameDashboardView, story_index=self.story_index)

    def receive_details_data(self, details_data_list):
        if details_data_list:
            model = MODEL_MAP[details_data_list[0][0]]
            data = session.query(model).filter(model.id == details_data_list[0][1]).first()
            if data:
                for field, value in details_data_list[0][2].items():
                    setattr(data, field, value)
                session.commit()

    def get_details_data(self, nav_type, nav_id):
        model = MODEL_MAP[nav_type]
        data = session.query(model).filter(model.id == nav_id).first()
        if data:
            # Return a dict of all fields (or just the ones you want)
            return {field: getattr(data, field, "") for field in self.ui.details_fields or []}
        return {}


    # def update_dimensions(self, width, height):
    #     """Propagate resizing logic to UI component."""
    #     self.ui.update_dimensions(width, height)

    def get_background_image(self):
        """Returns the background image path for this view."""
        try:
            return self.ui.bg_image_path  # UI manages background image selection
        except AttributeError:
            pass
