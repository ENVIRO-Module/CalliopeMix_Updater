"""
This function read the flow_out_sum and splits the data into X csv files, one per each spore.
"""
from pathlib import Path
from const.const import BASE_DATA_PATH,PROJECT_PATH
import pandas as pd
import json


output_path: Path= PROJECT_PATH / 'Outputs/spores'


print(output_path)

def split_spores(path):
    with open(path) as file:
        data=json.load(file)

    spores=pd.read_csv(data['caliope_file'], delimiter=',')

    #get the number of the spores
    spores_num=spores['spores'].unique()
    print(spores_num)
    print(spores.head())

    # Drop the empty rows
    spores.dropna(axis=0, inplace=True)
    print(spores.head())

    # Filter each spore
    for element in spores_num:
        print(element)
        dataframe=spores.loc[spores['spores']==element]

        name='flow_outsum'+'_spore'+'_' + str(element) +'.csv'
        store_path=output_path / name

        dataframe.to_csv(store_path, sep=',', index=False)
        print(dataframe.head())
    return spores


if __name__=='__main__':
    df=split_spores(BASE_DATA_PATH)
pass