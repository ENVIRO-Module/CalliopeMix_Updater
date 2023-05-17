import json

paths={
    'basefile': 'C:/Users/altz7/UAB/LIVENlab - SEEDS - _Alex/Hydrogen/base_file_simplified.xlsx'
}
with open('general.json', mode='w') as file:
    json.dump(paths, file, indent=3)


