import pandas as pd
import time
import json
import os

from const.const import BASE_DATA_PATH,DATA



json_base=BASE_DATA_PATH



def export_constant(json_file):

    """
    -Entry point. Define a schema of the future electricity mix in an excel following the structure of the ('Create activity).
        -An example can be found in /Data/electricity.csv.

    This function:
        -Reads the csv file
        -Returns a file with a list of the existing technologies from the electricity mix


    :param json: base json file with paths and links
    :return list of existing technologies
    """
    with open(json_file) as reader:
        file=json.load(reader)

    data = file['electricity_inventory']
    #path_file=file['csv_electricity_mix']

    df = pd.read_csv(data, delimiter=';')
    current_directory = os.getcwd()

    output_filename = "constant.py"

    # Ruta completa del archivo de salida
    output_path = os.path.join(current_directory, output_filename)
    df.dropna(inplace=True,subset=['Amount'] ,axis=0)
    constant=[]
    for _,element in df.iterrows():
        instance=isinstance(element['Amount'], float)
        if instance is True:
            #print('element not equal to NA is', element['Amount'])
            technology = element['Activity name']
            constant.append(technology)
        else:
            pass
    const_to_write=repr(constant)
    with open(output_path, 'w') as file:
        file.write('constant =' + const_to_write)

    print('File of constant saved in', output_path)

    return constant



def energyMixer(json_path):
    """
    This function creates multiple csv files following the structure of the excel importer ( Create activity)
    It creates one per each scenario / spore, so each scenario has his own inventory of the future market for electricity

    :param json_path: path of the general json
    :return: Returns as much csv as spores, containing the electricity mix of each of them.

    """

    with open(json_path) as reader:
        file = json.load(reader)

    data = file['caliope_file']
    constant=export_constant(json_path)
    output_path=str(DATA / 'Outputs')
    print(output_path)
    #output_path=file["csv_electricty_mix"]


    starter_time = time.time()

    df_spores = pd.read_csv(data, delimiter=',')
    # Drop Nnn values
    df_spores = df_spores.dropna(subset=['flow_out_sum'])

    # Filter technologies --> output from Electricity_mix_filter.py
    df_spores = df_spores[df_spores['techs'].isin(constant)]
    # TODO: We're assuming electricity and waste as the only carriers for the market for electricity
    df_spores = df_spores[(df_spores['carriers'] == 'electricity') | (df_spores['carriers'] == 'waste')]

    # Group values
    df_spores = df_spores.groupby(['spores', 'techs'])['flow_out_sum'].sum().reset_index()

    # Create dictionary of technologies and values for each spore
    spore_dict = {}
    for spore in df_spores['spores'].unique():
        spore_df = df_spores[df_spores['spores'] == spore]
        spore_dict[spore] = dict(zip(spore_df['techs'], spore_df['flow_out_sum']))

    # Loop over electricity.csv (Inventory) and include the values there
    electricity_path=file['electricity_inventory']

    mix = pd.read_csv(electricity_path, delimiter=';')
    for spore, values_dict in spore_dict.items():
        mix['Amount'] = mix['Activity name'].map(values_dict)
        mix = mix.fillna('NaN')
        name_mix = f'\electricity_mix_Inventory_{spore}.csv'
        name_mix = output_path+name_mix

        mix.to_csv(name_mix, sep=';', index=False)
    final=time.time()
    print('Output generated in {:.2f} seconds'.format(final-starter_time))
    print('Multiple files saved in',output_path)


if __name__=='__main__':
    export_constant(json_base)
    energyMixer(json_base)
pass
