'''Main script for testing'''
import json
import datetime
from posixpath import split

import bungie
    
def main():
    manifest = bungie.get_manifest()
    # write_to("manifest.json", pp(manifest))

    bungie_names = {"Sagey#8502", "chris#5313", "AKapella#7901", "CharlOwOtte#2339"}
    current_status(manifest, bungie_names[1])


def write_to(file_path, text):
    '''Write text to output file in the output folder
    Args:
        file_path (string): path to file
        text (string): text to write to file
    '''
    with open(f"output/{file_path}", "w") as f:
        f.write(text)

def pp(jsn):
    '''Pretty print JSON text (j)'''
    return json.dumps(jsn, indent=3, sort_keys=True)

def current_status(manifest, bungie_name):
    components = {"characters", "characterActivities"}
    user = bungie.get_user(bungie_name, components)["Response"]
    character_infos = user["characters"]["data"]
    character_activities = user["characterActivities"]["data"]

    activity_manifeset = manifest["DestinyActivityDefinition"]
    destination_manifeset = manifest["DestinyDestinationDefinition"]
    class_manifest = manifest["DestinyClassDefinition"]
    for id in character_infos:
        try:
            class_hash = str(character_infos[id]["classHash"])
            class_name = class_manifest[class_hash]["displayProperties"]["name"]
        except Exception as e:
            class_name = e

        try:
            # Get current activity
            activity_hash = str(character_activities[id]["currentActivityHash"])
            activity_name = activity_manifeset[activity_hash]["displayProperties"]["name"]
        except KeyError:
            activity_name = 'No activity'
        
        try:
            # Get current destination
            destination_hash = str(activity_manifeset[activity_hash]["destinationHash"])
            destination_name = destination_manifeset[destination_hash]["displayProperties"]["name"]
        except KeyError:
            destination_name = 'No destination'

        try:
            # Get date-time
            dt_string = character_activities[id]["dateActivityStarted"]
            dt_object = datetime.datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%SZ').strftime("%m/%d/%Y, %H:%M:%S")
        except KeyError as e:
            print(e)

        # print(f'{class_name}\t\t{dt_object}\t\t{destination_name}\t\t{activity_name}')
        print(bungie_name, class_name, dt_object, destination_name, activity_name, sep="\n")
        break

if __name__ == "__main__":
    main()