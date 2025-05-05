import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PyQt6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)
    app_icon = QIcon("src/assets/application_icon.ico")
    app.setWindowIcon(app_icon)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 