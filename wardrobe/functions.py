from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QDialog, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit
from data_handler import load_wardrobe_from_db, delete_item_from_db, add_item_to_db, ClothingItem
from outfit_selector import select_outfit

class AddItem(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Items to Wardrobe")
        self.setGeometry(200, 200, 700, 300)

        layout = QVBoxLayout(self)

        # each question needs to have its own line - instructions are in the pretext
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText('Clothing Name (ex. Mclaren T-Shirt)')
        layout.addWidget(self.item_name)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText('Enter the category (top, bottom, outerwear): ')
        layout.addWidget(self.category_input)

        self.color = QLineEdit()
        self.color.setPlaceholderText('Enter the color: ')
        layout.addWidget(self.color)

        self.style_ = QLineEdit()
        self.style_.setPlaceholderText('Enter the style (ex. cargo, graphics, athletic, formal, etc.): ')
        layout.addWidget(self.style_)

        self.material = QLineEdit()
        self.material.setPlaceholderText('Enter the material (ex: cotton, denim): ')
        layout.addWidget(self.material)

        self.temp = QLineEdit()
        self.temp.setPlaceholderText('Suitable temperature (comma-separated: cold, warm, hot): ')
        layout.addWidget(self.temp)

        self.precipitation = QLineEdit()
        self.precipitation.setPlaceholderText("Is this item suitable for rainy weather? (yes/no): (leave blank if not adding an outerwear)")
        layout.addWidget(self.precipitation)

        self.wearLimit = QLineEdit()
        self.wearLimit.setPlaceholderText('Enter the maximum wears before laundry as a number')
        layout.addWidget(self.wearLimit)

        self.submit = QPushButton('Submit Item')
        self.submit.clicked.connect(self.addItem) # references addItem function
        layout.addWidget(self.submit)

    def addItem(self): #grabs user input from QLineEdit text boxs and then processes them
        #input data collection - .text() grabs the user input and then stripping spaces and lowering case for consistency
        clothing_name = self.item_name.text().strip()
        category = self.category_input.text().strip().lower() 
        color = self.color.text().strip().lower() 
        style = self.style_.text().strip().lower()
        material = self.material.text().strip().lower() 
        temperature_suitability = [i.strip() for i in self.temp.text().strip().split(',')] 
        precipitation_suitability = self.precipitation.text().lower().strip() == 'yes'
        wear_limit = int(self.wearLimit.text().strip())

        item = ClothingItem(clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_limit)
        add_item_to_db(item)
        QMessageBox.information(self, "Success",f'Added item {clothing_name} to your wardrobe')
        self.close()


class RemoveItem(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remove Items from Wardrobe")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)

        self.item_ID = QLineEdit()
        self.item_ID.setPlaceholderText('Item number that you want to remove (ex. type 4 if you want to remove item in 4th index)')
        layout.addWidget(self.item_ID)

        self.submit = QPushButton('Submit Removal')
        self.submit.clicked.connect(self.removeItem)
        layout.addWidget(self.submit)
        
    def removeItem(self):
        remove = self.item_ID.text().strip()
        wardrobe = load_wardrobe_from_db()
        if remove.isdigit():
             remove = int(remove)
             delete_item_from_db(remove)
             QMessageBox.information(self, "Attention",'Item Removed')
             self.close()
        else:
            QMessageBox.information(self, "Attention",'Invalid Input')
            self.close()


class View(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Wardrobe")
        self.setGeometry(100, 100, 1200, 500)

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        wardrobe = load_wardrobe_from_db()
        self.table.setRowCount(len(wardrobe)) # number of items currently in db so lined up with rows of table widget
        self.table.setColumnCount(10) # number of  columns = to the db columns
        self.table.setHorizontalHeaderLabels(['Item Number', 'Clothing Name', 'Category', 'Color', 'Style', 'Material', 'Temperature Suitability', 'Precipitation Suitability', 'Wear Count', 'Wear Limit'])
        self.table.setColumnWidth(1,150)
        self.table.setColumnWidth(6,150)
        self.table.setColumnWidth(7,150)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.viewCloset()

    def viewCloset(self):
        wardrobe = load_wardrobe_from_db()

        if not wardrobe:
            QMessageBox.information(self, "Wardrobe Empty", "No items to display.")
            return

        count = 0
        for item in wardrobe:
            if item.wear_count < item.wear_limit:
                self.table.setItem(count, 0, QTableWidgetItem(str(item.item_number)))
                self.table.setItem(count, 1, QTableWidgetItem(item.clothing_name))
                self.table.setItem(count, 2, QTableWidgetItem(item.category))
                self.table.setItem(count, 3, QTableWidgetItem(item.color))
                self.table.setItem(count, 4, QTableWidgetItem(item.style))
                self.table.setItem(count, 5, QTableWidgetItem(item.material))
                self.table.setItem(count, 6, QTableWidgetItem(str(item.temperature_suitability).replace("'", "").replace("[","").replace("]", "")))
                self.table.setItem(count, 7, QTableWidgetItem(str(item.precipitation_suitability)))
                self.table.setItem(count, 8, QTableWidgetItem(str(item.wear_count)))
                self.table.setItem(count, 9, QTableWidgetItem(str(item.wear_limit)))
                count +=1

class GetOutfit(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Wardrobe")
        self.setGeometry(100, 100, 500, 500)
        self.layout = QVBoxLayout(self)
        
        self.temp = QLineEdit()
        self.temp.setPlaceholderText('Enter temperature (°F): ')
        self.layout.addWidget(self.temp)

        self.rain = QLineEdit()
        self.rain.setPlaceholderText('Is it raining? (yes/no):')
        self.layout.addWidget(self.rain)

        self.suggestion = QPushButton('Get an outfit!')
        self.suggestion.clicked.connect(self.select_outfit)
        self.layout.addWidget(self.suggestion)

        self.topbottom = QLabel()
        self.layout.addWidget(self.topbottom)

        self.outerwear = QLabel()
        self.layout.addWidget(self.outerwear)

    def select_outfit(self):
        temp = int(self.temp.text().strip())
        rain = self.rain.text().strip().lower()
        outfit = select_outfit(temp,rain)
        if outfit:
            self.topbottom.setText(f"Top: {outfit['top']} , Bottom: {outfit['bottom']}, Outerwear: {outfit.get('outerwear', 'None')}")
        else:
            self.topbottom.setText("Not enough clean outfits. Please do laundry.")
            self.outerwear.setText('')