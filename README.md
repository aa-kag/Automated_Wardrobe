# Automated_Wardrobe

## Files included

### 1. data_handler.py
Purpose: Manages all interactions with the database (my_wardrobe.db).

Functions:

connect_db: Sets up the database and ensures the table my_wardrobe exists.

add_item_to_db: Adds a new clothing item to the database.

delete_item_from_db: Removes a clothing item from the database using its item_number.

load_wardrobe_from_db: Loads all clothing items from the database into a list of ClothingItem objects.

do_laundry: Resets the wear_count of all clothing items to 0.

### 2. wardrobe_input.py
Purpose: Handles user input for adding new clothing items.

Functions:

get_clothing_input: Prompts the user for details about a clothing item (e.g., name, category, color, etc.) and creates a ClothingItem object.

add_to_wardrobe: Guides the user through adding multiple items to the wardrobe and saves them to the database using data_handler.

### 3. outfit_selector.py
Purpose: Handles outfit suggestions and wear tracking.

Functions:

update_wear_count: Updates the wear_count for a clothing item in the database.

weather_input: Prompts the user for weather details (temperature and rain).

select_outfit: Suggests an outfit based on weather conditions and clothing availability.

notify_laundry: Displays a pop-up reminder when only two clean outfits remain.

display_outfit: Prints the selected outfit to the console.

### 4. main.py
Purpose: Provides the main menu interface for interacting with the wardrobe manager.

Functions:

display_wardrobe: Displays all clean clothing items in the wardrobe.

remove_item: Allows the user to remove an item by its ID.

main: The entry point for the program, presenting a menu to:

Add items to the wardrobe.

View wardrobe contents.

Remove items from the wardrobe.

Get outfit suggestions.

Perform laundry.

Exit the program.
