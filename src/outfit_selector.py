from .data_handler import load_wardrobe_from_db, update_wear_count
from random import sample
from PyQt5.QtWidgets import QMessageBox

def select_outfit(temperature: int, raining: str):
    '''main function for outfit selection logic. Filters tops, bottoms, outerwears between temperature,
    rain, and also works with preventing certain color and style combinations in an effort to add stylistic 
    elements to outfit selection process. Returns outfit which is called in functions.py GetOutfit class.
    '''
    wardrobe = load_wardrobe_from_db()
    hamper = [] 

    # Temperature suitability filter
    if temperature < 55:
        temp_category = 'cold'
    elif 55 <= temperature < 75:
        temp_category = 'warm'
    else:
        temp_category = 'hot'
    
    # Filter by temperature suitability and move worn-out items to hamper
    selected_outfits = []
    for clothing in wardrobe:
        if clothing.wear_count >= clothing.wear_limit:
            hamper.append(clothing)
        elif temp_category in [temp.strip().lower() for temp in clothing.temperature_suitability]:
            selected_outfits.append(clothing)

    # Separate selected items categorically
    tops = [item for item in selected_outfits if item.category == 'top']
    bottoms = [item for item in selected_outfits if item.category == 'bottom']
    outerwears = [item for item in selected_outfits if item.category == 'outerwear']

    # if raining is selected by user then program goes through all outerwear which is rain friendly and
    #  breaks down the lists by what temperatures are selected - decided to lump warm and hot temperatures together to keep it simple as most outerwears are for cold or warm and hot 
    if raining =='yes':
        rain_outerwear = [item for item in outerwears if item.precipitation_suitability]
        if temperature >= 55: # warm and hot weathers
            outerwear = sample(rain_outerwear, 1)[0] if rain_outerwear else None
        else: # cold weather filters
            cold_rain_outerwear = [item for item in rain_outerwear if 'cold' in item.temperature_suitability]
            outerwear = sample(cold_rain_outerwear,1)[0] if rain_outerwear else None
    else: # no rain just the regular selections
        if temperature> 75: # if greater than 75 degrees no outerwear would be needed as it is too hot
            outerwear = None
        else:
            temp_suitable_outerwear = [item for item in outerwears if temp_category in item.temperature_suitability]
            outerwear = sample(temp_suitable_outerwear,1)[0] if outerwears else None
     # warm or hot tops when outerwear is suitable in cold
    if outerwear and 'cold' in outerwear.temperature_suitability:
        tops = [item for item in wardrobe if item.category == 'top']

     # laundry warning - should still be able to output 2 outfits
    if len(tops) <= 2 or len(bottoms) <=2:
        notify_laundry()

    # Ensure enough items for an outfit
    if len(tops) < 1 or len(bottoms) < 1: # checking to see if there are enough clothing at all
        print('Not enough clean outfits. Please do laundry.')
        return(None)
    else:
        # prevent clashing colors - creating better fashion sense logic rather than random selections
        banned_color_combos = {'Red': ['Green', 'Purple', 'Pink', 'Orange'],
                            'Brown': ['Black', 'Gray'],
                            'Blue': ['Black'],
                            'Purple': ['Yellow', 'Green'],
                            'Orange': ['Green', 'Pink', 'Red','Grey'],
                            'Pink': ['Red', 'Yellow'],
                            'Yellow': ['Green', 'Pink', 'Black','Grey'],
                            'Black': ['Blue', 'Brown'],
                            'Beige': ['Yellow','Grey'],
                            'Green': ['Brown','Red','Purple'],
                            'Grey': ['Yellow','Orange'],
                            'White': [] # white goes with everything
                            }
        # preventing clashing styles. Generalized categories selected - associated with options in the drop down
        banned_style_combos = {
                               'Athletic': ['Formal', 'Business Casual'],
                               'Formal': ['Athletic','Casual'],
                               'Casual':['Formal','Business Casual'], 
                               'Business Casual':['Athletic','Casual']
                            }
        loop_counter = 0
        for i in range(10): # tries 10 times to find a matching color and style otherwise gives up
            top=sample(tops,1)[0]
            bottom=sample(bottoms,1)[0]
            style = False
            for topstyle in top.style:
                for botstyle in bottom.style:
                    if botstyle not in banned_style_combos.get(topstyle): # checks if any of the styles match with eachother
                        style = True # flagging - allows for the for loop to stop and then move to color matching
                        break # if matches breaks loop and saves top and bottom items
                if style:
                    break
            if style and bottom.color not in banned_color_combos.get(top.color):
                break
            else:
               loop_counter +=1 # tracks how many times loop goes through

        if loop_counter == 10: # if the for loop runs the full amount of times then just randomly assigns top and bottom 
            top = sample(tops, 1)[0]
            bottom = sample(bottoms, 1)[0]
            no_style()

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
        else:
            outfit['outerwear'] = 'No suitable/available outerwear'
        return outfit

def notify_laundry():
    '''Alerts using QMessageBox that there are not enough outfits left based on parameters. This function is called in select_outfit for where the the len of tops and bottoms is checked'''
    alert = QMessageBox()
    alert.setIcon(QMessageBox.Information)
    alert.setText("Laundry Alert")
    alert.setInformativeText("You have two or less clean outfits left. Time to do laundry!")
    alert.exec_()

def no_style():
    '''called when style or colors does not pass this will be triggered '''
    alert = QMessageBox()
    alert.setIcon(QMessageBox.Information)
    alert.setText('Upgrade your style!')
    alert.setInformativeText('Add more colors and styles to your wardrobe! Your outfit colors/styles do not match well!')
    alert.exec_()