import sqlite3

class ClothingItem:
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
    conn = sqlite3.connect("my_wardrobe.db")
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
    conn = connect_db()
    cursor = conn.cursor() 
    cursor.execute("""
        INSERT INTO my_wardrobe (clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_count, wear_limit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (clothing.clothing_name, clothing.category, clothing.color, clothing.style,
         clothing.material, ",".join(clothing.temperature_suitability), int(clothing.precipitation_suitability), clothing.wear_count, clothing.wear_limit))
    conn.commit()
    conn.close()

def delete_item_from_db(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM my_wardrobe WHERE item_number = ?", (item_id,))
    conn.commit()
    conn.close()

def load_wardrobe_from_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_wardrobe")
    rows = cursor.fetchall()
    conn.close()
    wardrobe = []
    for i in rows: 
        item_number, clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_count, wear_limit = i
        clothing = ClothingItem(
            item_number=item_number,
            clothing_name=clothing_name,
            category=category,
            color=color,
            style=style,
            material=material,
            temperature_suitability=temperature_suitability.split(","),
            precipitation_suitability=bool(precipitation_suitability),
            wear_count=wear_count,      
            wear_limit=wear_limit       
        )
        wardrobe.append(clothing)
    return wardrobe

def do_laundry():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE my_wardrobe SET wear_count = 0")
    conn.commit()
    conn.close()
    print("All clothing items are now clean!")