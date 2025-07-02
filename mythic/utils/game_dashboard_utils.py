from PySide6.QtWidgets import QPushButton
import random


## --- UI --- ##

def align_dialog_to_button(dialog, parent, button_layout_attr="center_content_button_layout", button_text="Start a Scene"):
    btn = None
    if hasattr(parent, button_layout_attr):
        layout = getattr(parent, button_layout_attr)
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() == button_text:
                btn = widget
                break
    if btn:
        btn_pos = btn.mapToGlobal(btn.rect().topLeft())
        dlg_geom = dialog.frameGeometry()
        x = btn_pos.x() + (btn.width() - dlg_geom.width()) // 2
        y = btn_pos.y()
        dialog.move(x, y)

def get_dice_roll_result(sides_of_dice, flutter=False):
    roll = []
    if not flutter:
        roll.append(random.randint(1, sides_of_dice))
    else:
        flutter_count_options = list(range(1, 6))
        flutter_count = random.choices(flutter_count_options, weights=[1, 2, 3, 2, 1], k=1)[0]
        for _ in range(flutter_count):
            roll.append(random.randint(1, sides_of_dice))

    return roll