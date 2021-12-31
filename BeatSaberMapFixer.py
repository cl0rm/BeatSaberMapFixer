import os
import re
import json

# constants

BS_DIR = "E:\\Steam Games\\steamapps\\common\\Beat Saber\\"
LEVEL_DIR = "Beat Saber_Data\\CustomLevels\\"

# functions

def fix_beatsaber_info_file(file_name):
    file_path = os.fsencode(file_name)

    with open(file_path, "r+") as info_file:
        info_string = info_file.read()

        result = re.search("\"_beatmapCharacteristicName\":\\s\"Lightshow\",", info_string)
        if result:
            print("info file affected: "+ file_name)

            #json manipulation
            json_object = json.loads(info_string)
            
            for i in range((len(json_object["_difficultyBeatmapSets"]))):
                if json_object["_difficultyBeatmapSets"][i]["_beatmapCharacteristicName"] == "Lightshow":
                    json_object["_difficultyBeatmapSets"].pop(i)
                    break

            fixed_str = json.dumps(json_object, indent=4)

            info_file.seek(0)
            info_file.write(fixed_str)
            info_file.truncate()


def fix_beatsaber_level_file(file_name):
    file_path = os.fsencode(file_name)
    
    with open(file_path, "r+") as map_file:
        map_string = map_file.read()
        result = re.search("\"_time\":-[0-9]*\.[0-9]*", map_string)
        if result:
            fixed_str = re.sub("\"_time\":-[0-9]*\.[0-9]*", "\"_time\":0", map_string)
            
            map_file.seek(0)
            map_file.write(fixed_str)
            map_file.truncate()

            print("File affected and fixed: "+ file_name)
            

def fix_beatsaber_map(map_dir):

    for file in os.listdir(map_dir):
        file_str = os.fsdecode(file)

        #only search for dat files
        if file_str.endswith(".dat"):
            file_path_str = os.fsdecode(map_dir) + "\\" + file_str

            if (file_str == "info.dat") or (file_str == "Info.dat"):
                fix_beatsaber_info_file(file_path_str)
                continue
            else:
                fix_beatsaber_level_file(file_path_str)

   

# assemble directory

level_dir_str = BS_DIR + LEVEL_DIR

print("Searching for Broken Levels in " + level_dir_str)

level_dir = os.fsencode(level_dir_str)

for dir in os.listdir(level_dir):
    map_dir_str = level_dir_str + os.fsdecode(dir)
    map_dir = os.fsencode(map_dir_str)

    fix_beatsaber_map(map_dir)

