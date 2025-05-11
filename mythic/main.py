from PySide6.QtWidgets import QApplication
from app import MainAppWindow


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainAppWindow()
    window.show()
    app.exec()
