# Automated Wardrobe

## Project Goals

The goal of this project is to streamline the user's daily outfit decision-making by sorting their clothing items into categories which will then be considered when suggesting outfits. The hope is to simplify the daily hassle of deciding what to wear every morning before we step outside. The hope is that this project lowers the daily decision fatigue of the user by simplfying outfit selection. 

## Project Overview and Description

This respository contains a 4 main files and a sample database with some clothing items already stored within it. The files work together to create a database to store the user's clothing items and then create an interface where the user can get daily outfit recommendations and laundry reminders. The user will also be able to remove items and add new items as they please. The program also allows for the user to view their entire wardrobe and their dirty clothes as they populate in the hamper table.

## How To Run The Program

1. Download the Wardrobe folder from the GitHub Repository.
2. In your terminal open up the folder using the ```cd``` command. Example: cd /Users/user1/Desktop/Wardrobe
3. Run command ```python main.py```. This will prompt the program to open with the main menu. In this github is a preloaded database with some clothing items already stored, you can keep them in the database or remove and add your own clothing!

## Files included

### 1. data_handler.py
Purpose: Manages all interactions and changes with the database (my_wardrobe.db).

Functions:

```connect_db()```: Sets up the database and ensures the table my_wardrobe exists.

```add_item_to_db()```: Adds a new clothing item to the database.

```delete_item_from_db()```: Removes a clothing item from the database using its item_number.

```load_wardrobe_from_db()```: Loads all clothing items from the database into a list of ClothingItem objects.

```do_laundry()```: Resets the wear_count of all clothing items to 0.

'''ClothingItem''': Class which initializes all the database columns as objects which are referenced throughout.

### 2. functions.py
Purpose: Houses all of the classes which contain the features of every widget and button in the interface. This file sets up the design for each window that opens when a button is pushed on the main interface. Each class is related to one of the main buttons of the interface.

Classes:

```AddItem()```: Initializes the Qdialog framework from which prompts from the user for details about the clothing item being added are added to the QVBoxlayout.

```addItem()``` function within the ```AddItem()``` class pulls the user inputs from each pyqt5 widget and organizes the clothing item details (e.g., name, category, color, etc.)to create a ClothingItem object.

```RemoveItem()```: This class

### 3. outfit_selector.py
Purpose: Handles outfit suggestions and wear tracking.

Functions:

```update_wear_count()```: Updates the wear_count for a clothing item in the database.

```weather_input()```: Prompts the user for weather details (temperature and rain).

```select_outfit()```: Suggests an outfit based on weather conditions and clothing availability.

```notify_laundry()```: Displays a pop-up reminder when only two clean outfits remain.

```display_outfit()```: Prints the selected outfit to the console.

### 4. main.py
Purpose: Provides the main menu interface for interacting with the wardrobe manager.

Functions:

```display_wardrobe()```: Displays all clean clothing items in the wardrobe.

```remove_item()```: Allows the user to remove an item by its ID.

```main()```: The entry point for the program, presenting a menu to:

Add items to the wardrobe.

View wardrobe contents.

Remove items from the wardrobe.

Get outfit suggestions.

Perform laundry.

Exit the program.
