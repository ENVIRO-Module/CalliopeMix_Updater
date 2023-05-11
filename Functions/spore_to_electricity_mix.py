import pandas as pd
import time
from Filters.constant import 


def EnergyMixer(data):

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
    mix = pd.read_csv(r'Data\electricity.csv', delimiter=';')
    for spore, values_dict in spore_dict.items():
        mix['Amount'] = mix['Activity name'].map(values_dict)
        mix = mix.fillna('NaN')
        #Output Name --> TODO: variable
        name_mix = f'Outputs\electricity_mix_Inventory_{spore}.csv'

        mix.to_csv(name_mix, sep=';', index=False)
    final=time.time()
    print('Output generated in {:.2f} seconds'.format(final-starter_time))

EnergyMixer(r'Data\flow_out_sum.csv')
