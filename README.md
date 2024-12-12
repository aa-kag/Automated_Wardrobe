# Automated Wardrobe

## Project Goals

The goal of this project is to streamline the user's daily outfit decision-making by sorting their clothing items into categories which will then be considered when suggesting outfits. The hope is to simplify the daily hassle of deciding what to wear every morning and therefore lowering the daily decision fatigue of the user by making outfit selection a thoughtless task. 

## Project Overview and Description

This respository contains 4 main files and a sample database with some clothing items already stored within it. The files work together to create a database to store the user's clothing items and then create an interface where the user can get daily outfit recommendations and laundry reminders. The user will also be able to remove items and add new items as they please. The program also allows for the user to view their entire wardrobe and their dirty clothes as they populate in the hamper table.

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

* ```AddItem(QDialog)```: Initializes the Qdialog framework from which prompts from the user for details about the clothing item being added are added to the QVBoxlayout.

```addItem()``` function within the ```AddItem()``` class pulls the user inputs from each pyqt5 widget and organizes the clothing item details (e.g., name, category, color, etc.)to create a ClothingItem object.

* ```RemoveItem(QDialog)```: This class focuses on removing items using QDialog. This class initializes the framework which contains a place to enter the item id you want to remove or to remove all the items in the wardrobe.

```removeItem()``` function within the class pulls out the user inputted id number and then calls on the ```delete_item_from_db``` function from ```data_handler``` file. 
```removeAll()``` This function  creates the logic for if the user wants to clear the entire wardrobe by iterating through the wardrobe using ```load_wardrobe_from_db()``` and then iterates through all the item_numbers and deletes them from the wardrobe.

*  ```View(QDialog)```: This class creates the framework for viewing the wardrobe and hamper tables within the QDialog and then pulls from the the wardrobe 2 times. Once it pulls using the ```viewCloset``` function which pulls all clean clothes and then ```viewHamper``` function which pulls all dirty clothes. These tables are displayed on top of each other with wardrobe above the hamper.

*  ```GetOutfit(QDialog)```: This class creates the outfit selection interface. The framework is set with pyqt5 where there is a text box for the user to insert temperature and answer if it is raining or not. The ```select_outfits()``` function runs the user input through the ```select_outfit()``` function in the ```outfit_selector``` file. Once an outfit is decided it is printed onto the dialog for the user. The select_outfits function also displays an image depending on the weather specified by the user.



### 3. outfit_selector.py
Purpose: Handles outfit suggestions and wear tracking.

Functions:

```update_wear_count()```: Updates the wear_count for a clothing item in the database.

```select_outfit()```: Suggests an outfit based on weather conditions and clothing availability. Goes into filtering of different specific logics and tries to prevent various 'unfashionable' combinations of clothing from being selected. 

```notify_laundry()```: Displays a pop-up reminder when only two clean outfits remain.

```no_style()```: Triggers a pop-up encouraging the user to buy more diverse styles and colors when the ```select_outfit``` function's fashion filtering is unable to find a suitable 'fashionable' outfit.

### 4. main.py
Purpose: Provides the main menu interface by calling from the variety of different classes from the  ```functions.py``` which execute the selected button's task.

```Window(MainWindow)```: This class sets the opening interface as the MainWindow and then has the buttons for add and remove items, view wardrobe, get suggestion, do laundry, and exitting the application. The buttons are linked to functions within the Window class which call corresponding classes from the functions.py file and then execute the class using the .exec() method.

### Program Snapshots
#### Main Menu
<img width="490" alt="MainMenu" src="https://github.com/user-attachments/assets/812ce45f-3e32-4dba-9290-cbaeb5b40f42" />

#### Adding Item Interface
<img width="693" alt="AddItem" src="https://github.com/user-attachments/assets/86ca1860-8c80-402d-a641-c1dedaaa4698" />

#### Recommendation Screen
<img width="610" alt="recommendation" src="https://github.com/user-attachments/assets/9c0110c3-8222-489d-8076-a8115b62ad1b" />

#### Viewing Wardrobe and Hamper
<img width="1187" alt="wardrobeandhamper" src="https://github.com/user-attachments/assets/6ca35c9e-c426-4cd0-9ffe-16e6ae53fc73" />

