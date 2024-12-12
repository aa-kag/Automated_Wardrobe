from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QDialog, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox, QListWidget, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from data_handler import load_wardrobe_from_db, delete_item_from_db, add_item_to_db, ClothingItem
from outfit_selector import select_outfit
# all of these classes are then referenced in the main.py where they are connected to the button inputs which run this program
class AddItem(QDialog):
    '''Works to create the interface for user intputs from the add items button.'''
    def __init__(self):
        '''initializing all the pyqt5 lines for user input  and setting up framework'''
        super().__init__()
        self.setWindowTitle("Add Items to Wardrobe")
        self.setGeometry(200, 200, 700, 300)

        layout = QVBoxLayout(self)

        # each question needs to have its own line - instructions are in the pretext
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText('Clothing Name (ex. Mclaren T-Shirt)')
        layout.addWidget(self.item_name)

        category_label =QLabel('Select item category')
        layout.addWidget(category_label)
        self.category_input = QListWidget()
        self.category_input.addItems(['Top','Bottom','Outerwear'])
        layout.addWidget(self.category_input)

        color_label = QLabel('Color')
        layout.addWidget(color_label)
        self.color = QComboBox()
        self.color.addItems(['Red','Brown','Blue','Purple','Orange','Pink','Yellow','Black','Beige','Green','Grey','White'])
        layout.addWidget(self.color)

        style_label =QLabel('Select style (click as many as applicable)')
        layout.addWidget(style_label)
        self.style_ = QListWidget()
        self.style_.addItems(['Athletic','Formal','Casual','Business Casual'])
        self.style_.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.style_)

        self.material = QLineEdit()
        self.material.setPlaceholderText('Enter the material (ex: cotton, denim): ')
        layout.addWidget(self.material)

        temp_label = QLabel('Please select the temperature environments your clothing item fits in')
        layout.addWidget(temp_label)
        self.tempHot = QCheckBox('hot')
        self.tempCold = QCheckBox('cold')
        self.tempWarm = QCheckBox('warm')
        layout.addWidget(self.tempHot)
        layout.addWidget(self.tempCold)
        layout.addWidget(self.tempWarm)

        rain_label = QLabel('Is this item suitable for rainy weather? Please leave blank if item is not an outerwear!')
        layout.addWidget(rain_label)
        self.rain = QListWidget()
        self.rain.addItems(['yes','no'])
        self.rain.setFixedHeight(40)
        layout.addWidget(self.rain)

        self.wearLimit = QLineEdit()
        self.wearLimit.setPlaceholderText('Enter the maximum wears before laundry as a number')
        layout.addWidget(self.wearLimit)

        self.submit = QPushButton('Submit Item')
        self.submit.clicked.connect(self.addItem) # references addItem function
        layout.addWidget(self.submit)

    def addItem(self): 
        '''grabs user input from QLineEdit text boxes and then processes them
        input data collection. Also processes the texts incase for standardized formatting
        '''
        # .text() grabs the user input and then stripping spaces and lowering case for consistency
        clothing_name = self.item_name.text().strip()
        category = self.category_input.currentItem().text().strip().lower()
        color = self.color.currentText()

        self.selected_styles = self.style_.selectedItems()
        style = [i.text() for i in self.selected_styles] # going through the different styles selected and formatting it so that it can be included in the database in a way that the outfit_selector rules can take it into account
        style = str(','.join(style)) # separating different styles for formatting reasons, similar to above reasoning

        material = self.material.text().strip().lower() 

        temperature_suitability = [] # adding temp suitability based on what boxes are checked by user
        if self.tempHot.isChecked():
            temperature_suitability.append('hot')
        if self.tempCold.isChecked():
            temperature_suitability.append('cold')
        if self.tempWarm.isChecked():
            temperature_suitability.append('warm')
        
        precipitation = self.rain.currentItem().text() # grabs current selection adn then pulls that text as a string with .text()
        precipitation_suitability = precipitation.lower().strip() == 'yes' # checks if the input is 'yes' so that that it assigns True or False
        
        wear_limit = int(self.wearLimit.text().strip())

        item = ClothingItem(clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_limit)
        add_item_to_db(item)
        QMessageBox.information(self, "Success",f'Added item {clothing_name} to your wardrobe')
        self.close()


class RemoveItem(QDialog):
    '''create remove items interface using QDialog'''
    def __init__(self):
        '''initializes framework for removing items'''
        super().__init__()
        self.setWindowTitle("Remove Items from Wardrobe")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)

        self.item_ID = QLineEdit()
        self.item_ID.setPlaceholderText('Item number that you want to remove (ex. type 4 if you want to remove item number 4)')
        layout.addWidget(self.item_ID)

        self.submit = QPushButton('Submit Removal')
        self.submit.clicked.connect(self.removeItem)
        layout.addWidget(self.submit)

        self.remove_all = QPushButton('REMOVE ALL')
        self.remove_all.setStyleSheet("background-color : #D9534F")
        self.remove_all.clicked.connect(self.removeAll)
        layout.addWidget(self.remove_all)
        
    def removeItem(self):
        '''pulls integer from user input and then uses delete_item_from_db function to search the db for the item_id and removes it from the db'''
        remove = self.item_ID.text().strip()
        if remove:
            if remove.isdigit():
                remove = int(remove)
                delete_item_from_db(remove)
                QMessageBox.information(self, "Attention",'Item Removed')
                self.close()
            else:
                QMessageBox.information(self, "Attention",'Invalid Input')
                self.close()
        else:
            QMessageBox.information(self, "Attention",'Please enter a number in the box')

    def removeAll(self):
        '''purges entire database and removes everything'''
        wardrobe = load_wardrobe_from_db()
        for i in wardrobe: # iterates through each row in wardrobe and collects item numbers and removes them from the database
            delete_item_from_db(i.item_number)
        QMessageBox.information(self, "Attention",'All Items Removed')
        self.close()


class View(QDialog): 
    '''Create wardrobe view using QDialog'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Wardrobe")
        self.setGeometry(100, 100, 1200, 500)

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        wardrobe = load_wardrobe_from_db()
        self.table.setRowCount(len(wardrobe)) # number of items currently in db so lined up with rows of table widget
        self.table.setColumnCount(10) # number of  columns = to the db columns
        self.table.setHorizontalHeaderLabels(['Item Number', 'Clothing Name', 'Category', 'Color', 'Style', 'Material', 'Temperature Suitability', 'Precipitation Suitability', 'Wear Count', 'Wear Limit']) # column names
        self.table.setColumnWidth(1,150)
        self.table.setColumnWidth(6,150)
        self.table.setColumnWidth(7,150)

        self.layout.addWidget(self.table)
        self.viewCloset()

        # label for hamper in between the 2 tables
        self.hamper_label = QLabel('Your Hamper')
        self.hamper_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.hamper_label)

        self.hamper = QTableWidget()
        # in order to see how many clothes are actually in hamper counts the number of times wear count exceeds or is equal to wear limit and then uses self.hamper_count as the variable to set the row count
        self.hamper_count=0
        for item in wardrobe:
            if item.wear_count >= item.wear_limit:
                self.hamper_count +=1
        # alert to explain empty hamper would be this message box
        if self.hamper_count == 0:
            self.clean = QLabel('All Clothes are clean -- Hamper is empty')
            self.clean.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.clean)
            return
        self.hamper.setRowCount(self.hamper_count) # number of items currently in db so lined up with rows of table widget
        self.hamper.setColumnCount(10) # number of  columns = to the db columns
        self.hamper.setHorizontalHeaderLabels(['Item Number', 'Clothing Name', 'Category', 'Color', 'Style', 'Material', 'Temperature Suitability', 'Precipitation Suitability', 'Wear Count', 'Wear Limit'])
        self.hamper.setColumnWidth(1,150)
        self.hamper.setColumnWidth(6,150)
        self.hamper.setColumnWidth(7,150)

        self.layout.addWidget(self.hamper)
        self.viewHamper()

        self.setLayout(self.layout)


    def viewCloset(self):
        '''function iterating through the wardobe and populating a QTableWidget rows with wardrobe information loaded from the load_wardrobe_from_db function from the data_handler file '''
        wardrobe = load_wardrobe_from_db()

        if not wardrobe: # prompt if wardrobe is empty 
            QMessageBox.information(self, "Wardrobe Empty", "No items to display.")
            return

        count = 0
        for item in wardrobe: # iterates through the wardrobe list which is pulled through the load wardrobe from db  function and then 
            if item.wear_count < item.wear_limit: # checking to make sure item is clean
                #many objects converted to string because QTableWidgetItem takes string arguments only
                self.table.setItem(count, 0, QTableWidgetItem(str(item.item_number)))
                self.table.setItem(count, 1, QTableWidgetItem(item.clothing_name))
                self.table.setItem(count, 2, QTableWidgetItem(item.category))
                self.table.setItem(count, 3, QTableWidgetItem(item.color))
                self.table.setItem(count, 4, QTableWidgetItem(str(item.style).replace("'", "").replace("[","").replace("]", ""))) # removing brackets from the list after converting from list to string
                self.table.setItem(count, 5, QTableWidgetItem(item.material))
                self.table.setItem(count, 6, QTableWidgetItem(str(item.temperature_suitability).replace("'", "").replace("[","").replace("]", ""))) # removing brackets from the list after converting from list to string
                self.table.setItem(count, 7, QTableWidgetItem(str(item.precipitation_suitability)))
                self.table.setItem(count, 8, QTableWidgetItem(str(item.wear_count)))
                self.table.setItem(count, 9, QTableWidgetItem(str(item.wear_limit)))
                count +=1
        # ordering by category so rows are grouped together (top, bottom, outerwear)
        self.table.sortItems(2,Qt.AscendingOrder)

    def viewHamper(self):
        '''populates the hamper table by iterating through the wardrobe from a filter based on looking for items which have equaled its wear limit'''
        #same concept as viewCloset but reversed in the if statement as the for loop iterates through the wardrobe so that only dirty clothes taken in
        wardrobe = load_wardrobe_from_db()
        count = 0
        for item in wardrobe:
            if item.wear_count >= item.wear_limit:
                self.hamper.setItem(count, 0, QTableWidgetItem(str(item.item_number)))
                self.hamper.setItem(count, 1, QTableWidgetItem(item.clothing_name))
                self.hamper.setItem(count, 2, QTableWidgetItem(item.category))
                self.hamper.setItem(count, 3, QTableWidgetItem(item.color))
                self.hamper.setItem(count, 4, QTableWidgetItem(str(item.style).replace("'", "").replace("[","").replace("]", ""))) # removing brackets from the list after converting from list to string
                self.hamper.setItem(count, 5, QTableWidgetItem(item.material))
                self.hamper.setItem(count, 6, QTableWidgetItem(str(item.temperature_suitability).replace("'", "").replace("[","").replace("]", ""))) # removing brackets from the list after converting from list to string
                self.hamper.setItem(count, 7, QTableWidgetItem(str(item.precipitation_suitability)))
                self.hamper.setItem(count, 8, QTableWidgetItem(str(item.wear_count)))
                self.hamper.setItem(count, 9, QTableWidgetItem(str(item.wear_limit)))
                count +=1
        self.hamper.sortItems(2,Qt.AscendingOrder)


class GetOutfit(QDialog):
    '''Gets the outfit suggestion and its framework from pyqt5'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Wardrobe")
        self.setGeometry(100, 100, 500, 500)
        self.layout = QVBoxLayout(self)
        # setting inputs for user
        self.temp = QLineEdit()
        self.temp.setPlaceholderText('Enter temperature (°F): ')
        self.layout.addWidget(self.temp)

        self.rain = QLineEdit()
        self.rain.setPlaceholderText('Is it raining? (yes/no):')
        self.layout.addWidget(self.rain)
        # triggering the select_outfits function when button is pressed
        self.suggestion = QPushButton('Get an outfit!')
        self.suggestion.clicked.connect(self.select_outfits)
        self.layout.addWidget(self.suggestion)

        self.topbottom = QLabel()
        self.layout.addWidget(self.topbottom)

        self.outerwear = QLabel()
        self.layout.addWidget(self.outerwear)

        # adds images
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)


    def select_outfits(self):
        '''pulls user input for temperature and precipitation and then runs them through the select_outfit function from the outfit_selector file. 
        This then results in the Qlabel in the init function to be populated based on parameters set by the user inputs'''
        temp = int(self.temp.text().strip())
        rain = self.rain.text().strip().lower()
        outfit = select_outfit(temp,rain) # int and str
        # sets the qlabels for the top bottom and outerwar
        if outfit:
            self.topbottom.setText(f"Top: {outfit['top']},  Bottom: {outfit['bottom']},  Outerwear: {outfit.get('outerwear', 'None')}")
        else:
            self.topbottom.setText("Not enough clean outfits. Please do laundry.")
            self.outerwear.setText('')

        #image selection based on temperature
        if temp < 55:
            image =  'images/cold.png'
        elif 55<= temp <75:
            image = 'images/warm.png'
        else:
            image = 'images/hot.png'
        pixmap = QPixmap(image)
        self.image_label.setPixmap(pixmap)