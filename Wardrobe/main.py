from wardrobe_input import add_to_wardrobe
from outfit_selector import weather_input, select_outfit, display_outfit
from data_handler import load_wardrobe_from_db, delete_item_from_db, do_laundry
from PyQt5.QtWidgets import QApplication
import sys

def display_wardrobe():
    wardrobe = load_wardrobe_from_db()
    if not wardrobe:
        print('Your wardrobe is empty!')
        return
    
    print('\n--- Your Wardrobe:')
    for item in wardrobe:
        if item.wear_count < item.wear_limit:
            print(f'{item.item_number}: {item.clothing_name} -- {item.category}, {item.color}, {item.style}, {item.material}, '
                f"Temperature suitability: {', '.join(item.temperature_suitability)}, "
                f'Rain suitable?: {item.precipitation_suitability}')

def remove_item():
    display_wardrobe()
    while True:
        item_id = input('\nEnter the ID of the item you want to remove: ').strip()
        if item_id.isdigit():
            item_id = int(item_id)
            delete_item_from_db(item_id)
            print('Item removed successfully.')
            break
        else:
            print('Invalid item number.')

def main():
    app = QApplication(sys.argv)
    print('Welcome to the Wardrobe Manager!')
    while True:
        print('\nMain Menu:')
        print('1. Add items to wardrobe')
        print('2. View wardrobe')
        print('3. Remove an item from wardrobe')
        print('4. Get outfit suggestions')
        print('5. Do laundry')
        print('6. Exit')
        
        choice = input('Choose an option: ').strip()
        if choice == '1':
            add_to_wardrobe()
        elif choice == '2':
            display_wardrobe()
        elif choice == '3':
            remove_item()
        elif choice == '4':
            temperature, raining = weather_input()
            outfit = select_outfit(temperature, raining)
            display_outfit(outfit)
        elif choice =='5':
            do_laundry()
        elif choice == '6':
            print('See you later!')
            break
        else:
            print('Invalid choice. Select 1, 2, 3, 4, or 5.')

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()