from data_handler import load_wardrobe_from_db, connect_db
from random import sample
from PyQt5.QtWidgets import QMessageBox

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
        selected_outfits = [item for item in selected_outfits if item.precipitation_suitability]

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
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Laundry Alert")
    msg.setText("You only have two clean outfits left. Time to do laundry!")
    msg.exec_()

def display_outfit(outfit):
    if outfit is None:
        return
    print("\n Today's Outfit:")
    print(f"Top: {outfit['top']}")
    print(f"Bottom: {outfit['bottom']}")
    if "outerwear" in outfit:
        print(f"Outerwear: {outfit['outerwear']}")


# from data_handler import load_wardrobe_from_db
# from random import sample

# def weather_input():
#     temperature = int(input("What's the temperature today? (in °F): ").strip())
#     weather = input("Is it raining today? (yes/no): ").strip().lower()
#     return temperature, weather == 'yes'

# def select_outfit(temperature, raining):
#     wardrobe = load_wardrobe_from_db()

#     if temperature < 55:
#         temp_category = 'cold'
#     elif temperature < 75:
#         temp_category = 'warm'
#     else:
#         temp_category = 'hot'
    
#     selected_outfits =[]
#     for clothing in wardrobe:
#         # if the temperature selected is in the wardrobe it will be selected - clothing 
#         if temp_category in clothing.temperature_suitability:
#             selected_outfits.append(clothing)
#     if raining:
#         rain_outfits = []
#         for clothing in wardrobe:
#             if raining == True:
#                 rain_outfits.append(clothing)
#         selected_outfits = rain_outfits

# # categorical separation
#     tops = []
#     bottoms = []
#     outerwears = []
#     for clothing in selected_outfits:
#         if clothing.category == 'top':
#             tops.append(clothing)
#         elif clothing.category == 'bottom':
#             bottoms.append(clothing)
#         else:
#             outerwears.append(clothing)

# # checking wardrobe has enough clothing items to make a pair
#     if len(tops) == 0 or len(bottoms) == 0:
#         print("Not enough clothing in Wardrobe")
#     else:
#         top = sample(tops,1)[0]
#         bottom = sample(bottoms,1)[0]
#         if temperature < 55 and len(outerwears) > 0:
#             outerwear = sample(outerwears,1)[0]
#         else:
#             outerwear = None

# # creating the outfit
#     outfit = {'top':top.clothing_name,'bottom': bottom.clothing_name}
#     if outerwear != None:
#         outfit['outerwear'] = outerwear.clothing_name

#     return outfit

# def display_outfit(outfit):
#     print("\n Today's Outfit:")
#     print(f"Top: {outfit['top']}")
#     print(f"Bottom: {outfit['bottom']}")
#     if "outerwear" in outfit:
#         print(f"Outerwear: {outfit['outerwear']}")

    





#3 random option old version - probably not needed


# def select_outfit(temperature: int, raining: bool) -> List[Dict[str, str]]:
#     wardrobe = load_wardrobe_from_db()

#     #temperature category
#     if temperature < 55:
#         temp_category = 'cold'
#     elif temperature < 75:
#         temp_category = 'warm'
#     else:
#         temp_category = 'hot'

#     # Filter by temperature suitability and precipitation
#     suitable_items = [item for item in wardrobe if temp_category in item.temperature_suitability]
#     if raining:
#         suitable_items = [item for item in suitable_items if item.precipitation_suitability]

#     # Separate by category
#     tops = [item for item in suitable_items if item.style == 'top']
#     bottoms = [item for item in suitable_items if item.style == 'bottom']
#     outerwear = [item for item in suitable_items if item.style == 'outerwear']

#     # 3 outfit options
#     outfit_suggestions = []
#     for _ in range(3):
#         if not (tops and bottoms):  # at least one top and one bottom
#             break
#         top = sample(tops, 1)[0]  # random top
#         bottom = sample(bottoms, 1)[0]  # random bottom
#         coat = sample(outerwear, 1)[0] if outerwear and temperature < 55 else None  # Outerwear when cold

#         outfit = {"top": top.clothing_name, "bottom": bottom.clothing_name}
#         if coat:
#             outfit["outerwear"] = coat.clothing_name
#         outfit_suggestions.append(outfit)
    
#     return outfit_suggestions

# def display_outfits(outfits: List[Dict[str, str]]):
#     print("\n--- Outfit Suggestions ---")
#     for idx, outfit in enumerate(outfits, 1):
#         print(f"\nOption {idx}:")
#         print(f"Top: {outfit['top']}")
#         print(f"Bottom: {outfit['bottom']}")
#         if "outerwear" in outfit:
#             print(f"Outerwear: {outfit['outerwear']}")
