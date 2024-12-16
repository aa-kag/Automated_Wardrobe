import sqlite3
from PyQt5.QtWidgets import QMessageBox

class ClothingItem:
    '''ClothingItem class is used to create an object for each of the items and assign attributes associated with the wardrobe items. Initializes all attributes from db columns so that
    they can be referenced 
    '''
    def __init__(self, clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_limit, wear_count=0,item_number=None):
        self.item_number = item_number
        self.clothing_name = clothing_name
        self.category = category
        self.color = color
        self.style = style
        self.material = material
        self.temperature_suitability = temperature_suitability  
        self.precipitation_suitability = precipitation_suitability
        self.wear_limit = wear_limit  
        self.wear_count = wear_count 

def connect_db():
    '''Creating database if not created already, and then establishing connection between program and database'''
    conn = sqlite3.connect("my_wardrobe.db") # database name
    cursor = conn.cursor() 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS my_wardrobe (
            item_number INTEGER PRIMARY KEY AUTOINCREMENT,
            clothing_name TEXT,
            category TEXT,
            color TEXT,
            style TEXT,
            material TEXT,
            temperature_suitability TEXT,
            precipitation_suitability BOOLEAN,
            wear_count INTEGER DEFAULT 0,
            wear_limit INTEGER           
        )
    """)
    conn.commit()
    return conn

def add_item_to_db(clothing):
    '''adding item to database by accepting ClothingItem object and its attributes'''
    conn = connect_db()
    cursor = conn.cursor() # adds items corresponding to clothing item attributes that the user has specified from interface
    cursor.execute("""
        INSERT INTO my_wardrobe (clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_count, wear_limit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (clothing.clothing_name, clothing.category, clothing.color, clothing.style,
         clothing.material, ",".join(clothing.temperature_suitability), int(clothing.precipitation_suitability), clothing.wear_count, clothing.wear_limit))
    conn.commit()
    conn.close()

def delete_item_from_db(item_id):
    '''Deletes item based on item_id of the clothing item'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM my_wardrobe WHERE item_number = ?", (item_id,))
    conn.commit()
    conn.close()

def load_wardrobe_from_db():
    '''loads the database when called into a list of all the ClothingItem objects'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_wardrobe")
    rows = cursor.fetchall()
    conn.close()
    wardrobe = []
    for i in rows: # iterating through every row of the database and making that into a list where each index of the list is 1 row of the database
        item_number, clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_count, wear_limit = i
        clothing = ClothingItem(
            item_number=item_number,
            clothing_name=clothing_name,
            category=category,
            color=color,
            style=style.split(","),
            material=material,
            temperature_suitability=temperature_suitability.split(","),
            precipitation_suitability=bool(precipitation_suitability),
            wear_count=wear_count,      
            wear_limit=wear_limit       
        )
        wardrobe.append(clothing)
    return wardrobe

def do_laundry():
    '''Resets the wear count for the items in the wardrobe database so that outfits can be called again'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE my_wardrobe SET wear_count = 0") # resets the counts
    conn.commit()
    conn.close()
    alert = QMessageBox()
    alert.setIcon(QMessageBox.Information)
    alert.setText("Laundry Alert")
    alert.setInformativeText("All clothing iterms are now clean!")
    alert.exec_()

def update_wear_count(item): # updates wear count referenced in the outfit selector file as items are selected 
    '''updates item wear count to the database for items in wardrobe'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE my_wardrobe SET wear_count = ? WHERE item_number = ?", (item.wear_count, item.item_number))
    conn.commit()
    conn.close()