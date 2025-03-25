from ui.registerWizardNew_ui import Ui_Wizard as UI
from PySide6.QtWidgets import QApplication, QMainWindow, QWizard
import sys

class RegisterWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UI
        self.ui.setupUi(self, QWizard())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWizard()
    window.show()
    sys.exit(app.exec())