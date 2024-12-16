from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import sys
from src.data_handler import *
from src.functions import *

class Window(QMainWindow):
    '''main window where the opening interface which contains the buttons which are connected to the functions files where all the button functions are outlined. This 
    class allows for every thing to run and is the backbone of the interface'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Your Automated Wardrobe")
        self.setGeometry(100, 100, 500, 500)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)
# each button is linked to corresponding function below which is linked to the corresponding class in the functions file.
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
        # direct reference to the do_laundry function so does not need a function or class to be associated
        self.laundry_button = QPushButton('Do laundry')
        self.laundry_button.clicked.connect(do_laundry)
        layout.addWidget(self.laundry_button)
        # closes everything
        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)
# these functions are linked to the classes and execute the interface corresponding to the classes as the button is clicked
# each of these functions are connected to a button from above on the main window
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