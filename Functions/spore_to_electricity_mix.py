import pandas as pd
import time
import json
import os

def export_constant(json_file):
    """
    This functions returns a file with a list of the existing technologies in the electricity mix
    It reads the electricity.csv file, a "default file" that the user has to create to include the new activities there


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
            print('element not equal to NA is', element['Amount'])
            technology = element['Activity name']
            constant.append(technology)
        else:
            pass
    const_to_write=repr(constant)
    with open(output_path, 'w') as file:
        file.write('constant =' + const_to_write)

    return constant



def energyMixer(json_path):
    """

    :param json_path: path of the general json
    :return: Returns as much csv as spores, containing the electricity mix of each of them.
    These csv follow the general structure of the inventory form excel function

    """

    with open(json_path) as reader:
        file = json.load(reader)

    data = file['caliope_file']
    constant=export_constant(json_path)
    output_path=file["csv_electricty_mix"]


    starter_time = time.time()
    df_spores = pd.read_csv(data, delimiter=',')
    # Drop Nnn values
    df_spores = df_spores.dropna(subset=['flow_out_sum'])

    # Filter technologies --> output from Electricity_mix_filter.py
    df_spores = df_spores[df_spores['techs'].isin(constant)]
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


if __name__=='__main__':
    export_constant(r'C:\Users\altz7\PycharmProjects\p3\Utils_seeds\general.json')
    energyMixer(r'C:\Users\altz7\PycharmProjects\p3\Utils_seeds\general.json')
