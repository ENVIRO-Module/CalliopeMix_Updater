import csv
from pathlib import Path
from Utils_seeds.const.const import BASE_DATA_PATH
import numpy as np
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
        'amount': amount,
        'name': flow.get('name'),
        'unit': flow.get('unit'),
        'categories': str(flow.get('categories')),
        'ref_product': activity['reference product'],
        'act_name':activity['name']
    } for flow, row, amount in data])
    if out_path:
        df.to_excel(out_path)
    return df




def generate_docs(name: str):
    columns = [
        'amount',
        'name',
        'unit',
        'categories',
        'Interface',
        'Processor',
        'method',
        'ref_product',
        'act_name'
    ]
    nis=pd.DataFrame(columns=columns)

    return nis


def generate_colum_names():
    "copy the bare processor sheet from the original NIS file"
    columns=[
        "ProcessorGroup",
        "Processor",
        "ParentProcessor",
        "SubsystemType",
        "System",
        "FunctionalOrStructural",
        "Accounted Stock",
        "Description",
        "GeolocationRef",
        "GeolocationCode",
        "GeolocationLatLong",
        "Attributes",
        "@EcoinventName",
        "@EcoinventFilename",
        "@EcoinventCarrierName",
        "@region"]
    bare_processor=pd.DataFrame(columns=columns)
    return bare_processor


def generate_bare_processor(path: str)->pd.DataFrame:

    """
    This function creates an excel with one sheet, following the bareProcessor structure of the nis file.
    It runs only one simulation
    :param path:
    :return:
    """
    with open(path) as path_reference:
        dict_path = json.load(path_reference)
        print(dict_path)

    #load the bare processor simulation sheet
    base = pd.read_excel(dict_path['basefile'], sheet_name='BareProcessors simulation')

    # Extract and create columns.
    # Fist, focus on the columns that can directly be copied from the base file
    bare_processor=generate_colum_names()
    # Include the generated columns
    bare_processor['ProcessorGroup']=base.get('ProcessorGroup')
    bare_processor['FunctionalOrStructural']=base.get('FunctionalOrStructural')
    bare_processor['Accounted']=base.get('Accounted')
    bare_processor['@EcoinventFilename']=base.get('@EcoinventFilename')
    bare_processor['@EcoinventCarrierName']=base.get('@EcoinventCarrierName')

    # Get the names from the inventories
    # Since we're not able to read the lci spodls, we will read the data from the electricity mix inventories using bw.

    #Open the folder containing the cas files and select the first

    object_path=Path(dict_path['csv_electricty_mix'])
    files = list(object_path.glob('*.csv'))[0] # get the first. We're only interested on generating an example
    example=pd.read_csv(files, delimiter=';')
    names_codes={name:code for name,code in zip(example['Activity name'],example['Activity_code'])}

    # Iterate over the activities in the base file. If the activity is in the dicitonary, extract the name of the spold
    # Store them in a dictionary
    activities=base.get('Processor')
    name_inventory={}
    for act in activities:
        for name in names_codes:
            if act==name:
                code=names_codes[name]
                code=ei.get(code)
                inventory_name=code['name']
                name_inventory[act]=inventory_name

    bare_processor['@EcoinventName']=list(name_inventory.values())
    #Modify it to generate the processor names

    processors=[element.replace(' ','_').replace(',', '_') for element in list(name_inventory.values())]
    bare_processor['Processor']=processors
    bare_processor.to_csv(r'C:\Users\altz7\PycharmProjects\p3\Utils_seeds\general_nis.csv', sep=';', index=False)

    return bare_processor
pass



def Nis_generator(path: str) -> csv:

    """
    This function reads the json file and extracts the path to the multiple electricity mix generated

    :param path: path to the general json file (str)
    :return: Folder containing the X nis files
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

        print(base.head())

        #create an excel sheet for the spore
        sheet_name = f"Spore_{num_spore}"
        nis = generate_docs(sheet_name)

        for _, row in base.iterrows():
            # In the LCI we just comput the results for an amount of 1
            activity = ei.get(code=row['@EcoinventFilename'])
            method=methods[0]
            method=eval(method)
            inventory=export_solved_inventory(activity,method)
            #Assign columns
            inventory['Processor'] = row['Processor']
            inventory['method'] = method[-1]
            has_float_values = inventory['categories'].dtype == float and nis['categories'].apply(
                lambda x: isinstance(x, float)).any()
            print(has_float_values)
            list_types=[type(element) for element in inventory['categories']]
            list_types=set(list_types)
            print(inventory['categories'][0], list_types)

            nis=pd.concat([nis,inventory],axis=0)
            print(nis.head())

        # Adjust the Interface values to the expected input of enbios


        nis['categories'] = [ast.literal_eval(element) for element in nis['categories']]
        nis['categories'] = ['_'.join(element).replace(' ', '_').replace('-', '_') for element in nis['categories']]

        # Create an "Unspecified"
        interfaces=[]
        for name,category in zip(nis['name'],nis['categories']):
            count=category.count('_')
            
            name_check=name[0]

            if name_check.isnumeric():
                # If starts with a number, add a "_" in front of the sting
                name='_'+name

            if count <1:
                category=str(category)+'_unspecified'
                category=name+'_'+category
                interfaces.append(category)
            else:
                cat=name+'_'+category
                interfaces.append(cat)

        nis['Interface']=interfaces
        nis['Interface'] = [element.replace(' ', '_').replace(',', '_').replace('>', '_').replace('<', '_').replace('-', '_').replace('+','_') for element in nis['Interface']]


        previous=None
        for index,row  in nis.iterrows():

            if row['ref_product'] != previous:
                new_row=pd.Series('',index=nis.columns)
                new_row['amount']= 1
                nis = nis.iloc[:index].append(new_row, ignore_index=True).append(nis.iloc[index:], ignore_index=True)
            break
            previous = row['ref_product']


        final_path = path +'/'+'Nis_'+sheet_name+'.xlsx'

        # Create an excel file containing 2 sheets:
        writer=pd.ExcelWriter(final_path,engine='xlsxwriter', options={'strings_to_numbers':True})
        bare_processor = generate_bare_processor(BASE_DATA_PATH)
        bare_processor.to_excel(writer,sheet_name='BareProcessors',index=False)
        nis.to_excel(writer,sheet_name='Interfaces', index=False)
        writer.save()
        writer.close()
        final_path_csv=path +'/'+'Nis_'+sheet_name+'.csv'


        nis.to_csv(final_path_csv, sep=',', index=False)





########################################################Supplemetary


if __name__=='__main__':
    Nis_generator(BASE_DATA_PATH)

