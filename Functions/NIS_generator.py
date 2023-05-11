from pathlib import Path
import pandas as pd
from modify_background import ModifyBackground
import bw2data as bd
from Create_activity import InventoryFromExcel
import time
from Create_activity import InventoryFromExcel
bd.projects.set_current("Hydrogen_SEEDS")
ei = bd.Database("CUTOFF")


def Nis_generator(path):
    path_ob=Path(path)

    path_exist= Path.is_dir(path_ob)

    if not path_exist:
        raise ValueError(f"File {path} does not exist")
    else:
        # Bring all the files in this object
        files=list(path_ob.glob('*.csv'))

    # Start the iteration over each file
    counter=0
    print(type(files))

    for file in files:
        print(file)

        file_path=str(file)

        print('#### THE CURRENT PATH IS #####')
        df = pd.read_csv(file_path, delimiter=';')


        # Modify the background of the database
        # We still want to replace the market for electricity
        market_for_electricity='f44aa84c22af00eb9a286714b45f50b4'

        ModifyBackground(file_path,market_for_electricity)
        # Works


        #ModifyBackground(file,market_for_electricity)




Nis_generator(r'C:\Users\altz7\PycharmProjects\p3\Inventory\Outputs')