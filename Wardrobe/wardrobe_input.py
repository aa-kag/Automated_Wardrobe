from data_handler import ClothingItem, add_item_to_db

def get_clothing_input():
    clothing_name = input("Enter the name of the clothing item (ex: Mclaren T-Shirt ): ").strip()
    category = input("Enter the category (top, bottom, outerwear): ").strip().lower()
    color = input("Enter the color: ").strip().lower()
    style = input("Enter the style (e.g., cargo, graphics, athletic, formal, etc.): ").strip()  
    material = input("Enter the material (ex: cotton, denim): ").strip().lower() 
    temperature_suitability = input("Suitable temperature (comma-separated: cold, warm, hot): ").strip().lower().split(',')
    temperature_suitability = [i.strip() for i in temperature_suitability]
    if category == 'outerwear': # rain is only pertaining to outerwear clothing items
        precipitation_suitability = input("Is this item suitable for rainy weather? (yes/no): ").strip().lower() == 'yes'
    else:
        precipitation_suitability = False

    wear_limit = int(input("Enter the maximum wears before laundry: ").strip())

    return ClothingItem(clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability, wear_limit)

def add_to_wardrobe():
    print("\nAdding items to your wardrobe. Type 'no' when finished.")
    while True:
        add_item = input("Would you like to add a new clothing item? (yes/no): ").strip().lower()
        if add_item == 'no':
            break
        item = get_clothing_input()  # Get clothing details from user input
        add_item_to_db(item)  # Save item to the database
        print(f"Added {item.clothing_name} to the wardrobe.")



# create forbidden pairings - categorize between different styles (formal and atheltic shouldnt go together)