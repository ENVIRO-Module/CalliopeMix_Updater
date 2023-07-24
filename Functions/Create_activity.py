
import bw2data as bd
import pandas as pd
import time
from tqdm import tqdm
bd.projects.set_current("Hydrogen_SEEDS")
ei = bd.Database("CUTOFF")


def InventoryFromExcel(data):

    """
    This function creates bw activities reading an excel file.
    Please check the expected structure of the Excel file on ____

    :param df: can either use a predefined dataframe or a path to a csv
    :return:
    """
    starter_time=time.time()
    #check
    if isinstance(data, str):
        try:
            df=pd.read_csv(data, delimiter=';')
        except:

            raise FileNotFoundError(f"The path '{data}' does not exist.")


            return None
    elif isinstance(data ,pd.DataFrame):
        df=data

    else:
        print('Input error')
        return None

    df.fillna('NA',inplace=True)

    activ=[]
    for index,row in df.iterrows():
        if row['Activity_origin'] == 'NA': # If Act origin=NA == This is the new activity to create

            activity_name = str(row['Activity name'])
            activity_code=str(row['Activity_code'])
            activ.append(activity_code)

            try:
                new_activity = ei.new_activity(name=str(row['Activity name']), code=str(row['Activity_code']), unit=str(row['Unit']))
                new_activity.save()
            # create a df containing the rows
            except bd.errors.DuplicateNode:
                new_activity = ei.get(code=str(row['Activity_code']))
                new_activity.delete()
                new_activity = ei.new_activity(name=str(row['Activity name']), code=str(row['Activity_code']),unit=str(row['Unit']))
                new_activity.save()

            act_df = df.loc[df['Activity_origin'] == activity_name]
            # Subset all the activities that have origin in the new activity created
            for _, row2 in tqdm(act_df.iterrows()):
                if row2['Technosphere'] == 'Yes':
                    act = bd.Database(row2['Database']).get(code=row2['Activity_code'])

                    if row2['Reference_product'] != 'NA':
                        exchange = new_activity.new_exchange(input=act, type='technosphere',unit=row2['Unit'], amount=row2['Amount'],product=row2['Reference_product'],location=row2['Location'])
                        exchange.save()
                    else:
                        pass
                else:
                    act = bd.Database('biosphere3').get(code=row2['Activity_code'])
                    if row2['Reference_product'] != 'NA':
                        exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'])
                    else:
                        pass

                print('####################')
                print('activity {} to {}'.format(act,row2['Activity_origin']))

        else:
           pass

    final_time=time.time()
    final_lap=final_time-starter_time
    print('Create activity executed in {} seconds'.format(final_lap))
    return(activ)



