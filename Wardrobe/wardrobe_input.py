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








# from data_handler import ClothingItem, add_item_to_db

# def get_clothing_input():
#     clothing_name = input("Enter the name of the clothing item (ex: Mclaren T-Shirt ): ").strip()
#     category = input("Enter the category (top, bottom, outerwear): ").strip().lower()
#     color = input("Enter the color: ").strip().lower()
#     style = input("Enter the style (e.g., cargo, graphics, athletic, formal, etc.): ").strip()  # how to make this relevant in matching process
#     material = input("Enter the material (ex: cotton, denim): ").strip().lower() # same as above
#     temperature_suitability = input("Suitable temperature (comma-separated: cold, warm, hot): ").strip().lower().split(',')
#     temperature_suitability = [t.strip() for t in temperature_suitability]
#     precipitation_suitability = input("Is this item suitable for rainy weather? (yes/no): ").strip().lower() == 'yes'
    
#     return ClothingItem(clothing_name, category, color, style, material, temperature_suitability, precipitation_suitability)

# # need to make it so that style options are based on category and is limited to certain options only. Same with materials

# # how can I get a counter for how many times each piece of clothing has been used - then throw certain items into the "hamper"
# # when the time comes and trigger a wash - example jeans used 5 times then wash but t-shirts 1 time 1 wash. 
# # pop-up is the best way to have like an alert "You need to do the laundry! you have 2 outfits left!"
# # need to get a way to match styles and colors

# def add_to_wardrobe():
#     print("\nAdding items to your wardrobe. Type 'no' when finished.")
#     while True:
#         add_item = input("Would you like to add a new clothing item? (yes/no): ").strip().lower()
#         if add_item == 'no':
#             break
#         item = get_clothing_input()  # Get clothing details from user input
#         add_item_to_db(item)  # Save item to the database
#         print(f"Added {item.clothing_name} to the wardrobe.")