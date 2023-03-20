from PyQt6.QtWidgets import QApplication
import sys
from controllers import MainWindowController


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindowController()
    main_window.show()
    sys.exit(app.exec())
