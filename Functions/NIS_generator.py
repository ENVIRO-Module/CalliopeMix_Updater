import csv
from pathlib import Path
import pandas as pd
from modify_background import ModifyBackground
import bw2data as bd
import json
from typing import Optional
from bw2data.backends import Activity
import ast
import typing


bd.projects.set_current("Hydrogen_SEEDS")
ei = bd.Database("CUTOFF")


def export_solved_inventory(activity: Activity, method: tuple[str, ...],
                            out_path: Optional[str] = None) -> pd.DataFrame:
    """
    All credits to Ben Portner.
    :param activity:
    :param method:
    :param out_path:
    :return:
    """
    # print("calculating lci")
    lca = activity.lca(method, 1)
    lca.lci()
    array = lca.inventory.sum(axis=1)
    if hasattr(lca, 'dicts'):
        mapping = lca.dicts.biosphere
    else:
        mapping = lca.biosphere_dict
    data = []
    for key, row in mapping.items():
        amount = array[row, 0]
        data.append((bd.get_activity(key), row, amount))
    data.sort(key=lambda x: abs(x[2]))
    df = pd.DataFrame([{
        'row_index': row,
        'amount': amount,
        'name': flow.get('name'),
        'unit': flow.get('unit'),
        'categories': str(flow.get('categories'))
    } for flow, row, amount in data])
    if out_path:
        df.to_excel(out_path)
    return df



def generate_docs(name: str):
    columns = [
        'row_index',
        'amount',
        'name',
        'unit',
        'categories',
        'Interface',
        'Processor',
        'method',
    ]
    nis=pd.DataFrame(columns=columns)

    return nis

def Nis_generator(path: str) -> csv:

    """
    This function reads the json file and extracts the path to the multiple electricity mix generated

    :param path: path to the general json file (str)
    :return: Foder containing the X nis files
    """

    with open(path) as path_reference:
        dict_path = json.load(path_reference)
        print(dict_path)

    base = pd.read_excel(dict_path['basefile'], sheet_name='BareProcessors simulation')
    methods_df=pd.read_excel(dict_path['basefile'],sheet_name='ScalarIndicators')


    path=dict_path['nis_path']
    mix_path=dict_path['csv_electricty_mix']
    market_for_electricity=dict_path['old_market_FElectricity']


    path_ob=Path(mix_path)

    path_exist= Path.is_dir(path_ob)

    if not path_exist:
        raise ValueError(f"File {mix_path} does not exist. Run spore to electricity_mix first")
    else:
        pass

    # Bring all the files in this object
    files=list(path_ob.glob('*.csv'))

    # Create an excel for the nis file
    # The nis file is going to be structured as the export solved inventory function

    # Generate a list of methods
    methods=methods_df['Formula'].tolist()


    for file in files:
        file_path=str(file)
        num_spore=file_path.split('_')[-1].split('.')[0]
        print(num_spore)

        # Modify the background of the database
        # We still want to replace the market for electricity
        ModifyBackground(file_path,market_for_electricity)
        #Read the Excel file
        # TODO: a general yaml with the path of different files and folders
        # TODO: revisar on posar-ho
        # load the path file (json)

        print(base.head())

        #create an excel sheet for the spore
        sheet_name = f"Spore_{num_spore}"
        nis = generate_docs(sheet_name)

        for _, row in base.iterrows():
            # In the LCI we just comput the results for an amount of 1
            activity = ei.get(code=row['@EcoinventFilename'])

            for method in methods:
                inventory=export_solved_inventory(activity, method)
                print(inventory.columns)

                inventory['Processor'] = row['Processor']
                inventory['method'] = method[-1]


                nis=pd.concat([nis,inventory],axis=0)


        # Adjust the Interface values to the expected input of enbios
        nis['categories'] = [ast.literal_eval(element) for element in nis['categories']]
        nis['categories'] = ['_'.join(element).replace(' ','_').replace('-','_') for element in nis['categories']]
        nis['Interface'] = nis['name']+'_'+nis['categories']
        nis['Interface'] = [element.replace(' ', '_').replace(',','_').replace('<','_').replace('<','_').replace('-','_') for element in nis['Interface']]


        final_path = path +'/'+'Nis_'+sheet_name + ".csv"

        nis.to_csv(final_path, sep=';', index_label=False)


def csv_to_json(nis_file_folder: Path) -> None:

    """
    Function to adapt the output to the requirements of update_nis_table from enbios

    :param nis_file_folder: folder containing the nis files
    :return: same files in json to use them in enbios' functions
    """
    docs=nis_file_folder.glob('*csv')
    for nis in docs:
        with open(nis,'r') as csv_file:
            csv_data=csv.DictReader(csv_file, delimiter=';')
            data=[row for row in csv_data]
            # Write it in json

        nis_to_json_name=str(nis).split('.')[0]
        nis_to_json_name=f"{nis_to_json_name}.json"
        with open(nis_to_json_name, "w") as json_file:
            json.dump(data,json_file,indent=4)






if __name__=='__main__':
    Nis_generator(r'C:\Users\altz7\PycharmProjects\p3\Inventory\general.json')