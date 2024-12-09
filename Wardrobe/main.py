from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import sys
from data_handler import *
from functions import *

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Your Automated Wardrobe")
        self.setGeometry(100, 100, 500, 500)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)

        self.add_button = QPushButton('Add item to your wardrobe')
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton('Remove item from your wardrobe')
        self.remove_button.clicked.connect(self.remove_item)
        layout.addWidget(self.remove_button)

        self.view_button = QPushButton('View your wardrobe')
        self.view_button.clicked.connect(self.view_wardrobe)
        layout.addWidget(self.view_button)

        self.outfit_button = QPushButton('Get outfit suggestion')
        self.outfit_button.clicked.connect(self.outfit)
        layout.addWidget(self.outfit_button)

        self.laundry_button = QPushButton('Do laundry')
        self.laundry_button.clicked.connect(do_laundry)
        layout.addWidget(self.laundry_button)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

    def add_item(self):
        input = AddItem()
        input.exec()
    
    def remove_item(self):
        input = RemoveItem()
        input.exec()

    def view_wardrobe(self):
        input = View()
        input.exec()

    def outfit(self):
        input = GetOutfit()
        input.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())