'''Main script for testing'''
import json
import bungie

'''Write text (String) to file given at file_path (String)'''
def write_to(file_path, text):
    with open(f"output/{file_path}", "w") as f:
        f.write(text)

'''Pretty print JSON text (j)'''
def pp(jsn):
    return json.dumps(jsn, indent=3, sort_keys=True)
    
def main():
    # write_to("manifest.json", pp(bungie.get_manifest()))
    # write_to("output/dump.json", pp(bungie.get_definitions("jsonWorldContentPaths")))

    classdef = bungie.get_definitions("DestinyClassDefinition")

    bungie_name = "Sagey#8502"
    # bungie_name = "andyp472#3715"
    # write_to("player.json", pp(bungie.get_player(test_names[1])))
    # components = {"Profiles", "characters"}#, "CharacterActivities"}
    components = {"Characters", "CharacterActivities"}
    # write_to("profile.json", pp(bungie.get_user(bungie_name, components)))
    activities = bungie.get_user(bungie_name, components)["Response"]["characterActivities"]["data"]
    characters = bungie.get_user(bungie_name, components)["Response"]["characters"]["data"]
    
    for id in characters:
        class_hash = str(characters[id]["classHash"])
        class_name = classdef[class_hash]["displayProperties"]["name"]
        dt = characters[id]["dateLastPlayed"]
        # print(f"{id}: {dt} ({class_name})")
        print(f"{class_name}: {dt})")

        activity_hash = activities[id]["currentActivityHash"]
        mode_hash = activities[id]["currentActivityModeHash"]
        playlist_hash = activities[id]["currentPlaylistActivityHash"]
        print("",end="\t")
        print(activity_hash,mode_hash,playlist_hash, sep="\n\t")

    # write_to("destdef", pp(bungie.get_definitions("DestinyDestinationDefinition")))

if __name__ == "__main__":
    main()