'''Main script for testing'''
from sys import argv
import datetime

import bungie
from extra import deep_get
from gui import create_window
from extra import pretty_print
    
def main():
    global manifest
    manifest = bungie.get_manifest()

    bungie_names = ["Sagey#8502", "chris#5313", "AKapella#7901", "CharlOwOtte#2339", "Ben Dover#4822", "W4RCL4W#5753"]
    if len(argv) == 2:
        temp(argv[1])
    else:
        temp(bungie_names[3])

def temp(bungie_name):
    components = {"characters", "characterActivities"}
    user = bungie.get_player(bungie_name, components).get("Response")
    characters = deep_get(user, ['characters', 'data'])
    char_activities = deep_get(user, ['characterActivities', 'data'])

    for id in characters:
        class_hash = str(deep_get(characters, [id, 'classHash']))
        class_name = get_dp('DestinyClassDefinition', class_hash, 'name')

        activity_hash = str(deep_get(char_activities, [id, 'currentActivityHash']))
        activity_name = get_dp('DestinyActivityDefinition', activity_hash, 'name')

        destination_hash = str(deep_get(manifest, ['DestinyActivityDefinition', activity_hash, 'destinationHash']))
        destination_name = get_dp('DestinyDestinationDefinition', destination_hash, 'name')
        
        dt_string = deep_get(char_activities, [id, 'dateActivityStarted'])
        dt_object = datetime.datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%SZ').strftime("%m/%d/%Y, %H:%M:%S")

        print(bungie_name, class_name, dt_object, activity_name, destination_name, sep="\n")
        print("-"*10)


        place_hash = str(deep_get(manifest, ['DestinyDestinationDefinition', destination_hash, 'placeHash']))
        place_bool = get_dp('DestinyPlaceDefinition', place_hash, 'hasIcon')
        # print(pretty_print(deep_get(manifest, ['DestinyDestinationDefinition', destination_hash])))
        print("Icon: " + str(place_bool))
        if place_bool:
            img = bungie.get_image(get_dp('DestinyDestinationDefinition', destination_hash, 'icon'))
            create_window(img.read())
        # break

def get_dp(definition, hash, property):
    '''Function to get name from objects Display Properties using its definition and hash'''
    return deep_get(manifest, [definition, hash, 'displayProperties', property])

if __name__ == "__main__":
    main()