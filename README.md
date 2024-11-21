# Automated_Wardrobe

## Description

This respository contains a 4 main files and a sample database with some clothing items already stored within it. The files work together to create a database to store the user's clothing items and then create an interface where the user can get daily outfit recommendations and laundry reminders. The hope is that this project lowers the daily decision fatigue of the user by simplfying outfit selection. 

## How To Run The Program

1. First download the Wardrobe folder from the GitHub Repository.
2. In your terminal open up the folder using the cd command. Example: cd /Users/user1/Desktop/Wardrobe
3. Run command python main.py. This will prompt the program to open with the main menu. In this github is a preloaded database with some pieces of clothing already stored, you can keep them in the database or remove and add your own clothing!

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
