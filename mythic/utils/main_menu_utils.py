def scroll_to_widget(nav_scroll_area, widget):
    # Ensure the highlighted widget is visible in the scroll area
    if widget:
        area = nav_scroll_area
        widget_rect = widget.geometry()
        # Map widget's rect to the scroll area's coordinate system
        target = widget.mapTo(area.viewport(), widget_rect.topLeft())
        area.ensureVisible(target.x(), target.y(), widget_rect.width(), widget_rect.height())