from data_handler import load_wardrobe_from_db, connect_db
from random import sample
from PyQt5.QtWidgets import QMessageBox

# create forbidden pairings - categorize between different styles (formal and atheltic shouldnt go together)
# also create something so that when wardrobe is being viewed it is sorted by clothing type not just the order in which things were added

def update_wear_count(item):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE my_wardrobe SET wear_count = ? WHERE item_number = ?", (item.wear_count, item.item_number))
    conn.commit()
    conn.close()

def weather_input():
    temperature = int(input("What's the temperature today? (in °F): ").strip())
    weather = input("Is it raining today? (yes/no): ").strip().lower()
    return temperature, weather == 'yes'

def select_outfit(temperature, raining):
    wardrobe = load_wardrobe_from_db()
    hamper = [] 

    # Temperature suitability filter
    if temperature < 55:
        temp_category = 'cold'
    elif temperature < 75:
        temp_category = 'warm'
    else:
        temp_category = 'hot'
    
    # Filter by temperature suitability and move worn-out items to hamper
    selected_outfits = []
    for clothing in wardrobe:
        if clothing.wear_count >= clothing.wear_limit:
            hamper.append(clothing)
        elif temp_category in clothing.temperature_suitability:
            selected_outfits.append(clothing)
    if raining:
        selected_outfits = [item for item in selected_outfits if item.precipitation_suitability == True]

    # Separate items categorically
    tops = [item for item in selected_outfits if item.category == 'top' and item.wear_count < item.wear_limit]
    bottoms = [item for item in selected_outfits if item.category == 'bottom' and item.wear_count < item.wear_limit]

    # Filtering for outerwear based on temperature and rain suitability
    if temperature < 55:  # If it's cold
        if raining:
            outerwears = [item for item in selected_outfits if item.category == 'outerwear' and 'cold' in item.temperature_suitability and item.precipitation_suitability and item.wear_count < item.wear_limit]
        else:
            outerwears = [item for item in selected_outfits if item.category == 'outerwear' and 'cold' in item.temperature_suitability and item.wear_count < item.wear_limit]
        outerwear = sample(outerwears, 1)[0] if outerwears else None
    else:
        if raining:
            outerwears = [item for item in selected_outfits if item.category == 'outerwear' and item.precipitation_suitability and item.wear_count < item.wear_limit]
        else:
            outerwears = [item for item in selected_outfits if item.category == 'outerwear' and item.wear_count < item.wear_limit]
        outerwear = sample(outerwears, 1)[0] if outerwears else None

     # warm or hot tops when outerwear is suitable in cold
    if outerwear and 'cold' in outerwear.temperature_suitability:
        tops = [item for item in wardrobe if item.category == 'top' and item.wear_count < item.wear_limit]

     # laundry warning - should still be able to output 2 outfits
    if len(tops) <= 2 or len(bottoms) <=2:
        notify_laundry()

    # Ensure enough items for an outfit
    if len(tops) < 1 or len(bottoms) < 1: # checking to see if there are enough clothing at all
        print("Not enough clean outfits. Please do laundry.")
        return(None)
    else:
        top = sample(tops, 1)[0]
        bottom = sample(bottoms, 1)[0]

        # Update wear count
        top.wear_count += 1
        bottom.wear_count += 1
        update_wear_count(top)
        update_wear_count(bottom)
        if outerwear:
            outerwear.wear_count += 1
            update_wear_count(outerwear)

        # Return selected outfit
        outfit = {'top': top.clothing_name, 'bottom': bottom.clothing_name}
        if outerwear:
            outfit['outerwear'] = outerwear.clothing_name
        return outfit

def notify_laundry():
    alert = QMessageBox()
    alert.setIcon(QMessageBox.Information)
    alert.setWindowTitle("Laundry Alert")
    alert.setText("You only have two clean outfits left or do not have appropriate clothing for the weather. Time to do laundry!")
    alert.exec_()
