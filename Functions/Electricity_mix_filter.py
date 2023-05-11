import pandas as pd
from pathlib import Path

def export_constant(data,path):
    """
    This functions returns a file with a list of the existing technologies in the electricity mix

    :param data:--> Absolute path to the electricity.csv file
    :param path: --> Place where you want to save it
    :return:
    """

    df=pd.read_csv(data, delimiter=';')
    print(df)
    path= path + str('\constant.py')


    constant=[]
    for _,element in df.iterrows():
        if element['Amount'] !='NA':
            technology = element['Activity name']
            constant.append(technology)
        else:
            pass

    const_to_write=repr(constant)
    with open(path, 'w') as file:
        file.write('constant =' + const_to_write)

export_constant(r'C:\Users\altz7\PycharmProjects\p3\Inventory\Data\electricity.csv', r'C:\Users\altz7\PycharmProjects\p3\Inventory\Filters')


