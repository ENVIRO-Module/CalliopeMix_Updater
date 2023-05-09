
import bw2data as bd
import pandas as pd
import time
#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
print(bd.projects.dir)
print(bd.databases)
#Create an instance of the database of interest


ei = bd.Database("CUTOFF")
# create a copy of the database, just in case.

"""
try:                #it'll take a few minutes
    ei.copy('this_is_a_test')
    ei_copy=bd.Database('this_is_a_test')

except AssertionError:
    ei_copy=bd.Database('this_is_a_test')
    pass
#bd.Database('this_is_a_test').deregister()
#bd.Database('test2').rename('this_is_a_test')
"""
def InventoryFromExcel(data):

    """

    :param df: can either use a predefined dataframe or a path to a csv
    :return:
    """


    starter_time=time.time()
    #check
    if isinstance(data, str):
        try:
            df=pd.read_csv(data, delimiter=';')
        except:
            print('Error: no path found')
            return None
    elif isinstance(data ,pd.DataFrame):
        df=data

    else:
        print('Input error')
        return None


    df.fillna('NA',inplace=True)
    n_processes=len(df.index)
    counter = 0
    activ=[]
    for index,row in df.iterrows():
        if row['Activity_origin'] == 'NA':

            activity_name = str(row['Activity name'])
            activity_code=str(row['Activity_code'])
            activ.append(activity_code)

            try:
                new_activity = ei.new_activity(name=str(row['Activity name']), code=str(row['Activity_code']))
                new_activity.save()
            # create a df containing the rows
            except bd.errors.DuplicateNode:
                new_activity = ei.get(code=str(row['Activity_code']))
                new_activity.delete()
                new_activity = ei.new_activity(name=str(row['Activity name']), code=str(row['Activity_code']))
                new_activity.save()

            act_df = df.loc[df['Activity_origin'] == activity_name]
            for _, row2 in act_df.iterrows():
                if row2['Technosphere'] == 'Yes':
                    act = bd.Database(row2['Database']).get(code=row2['Activity_code'])

                    if row2['Reference_product'] != 'NA':
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],product=row2['Reference_product'],location=row2['Location'])
                        exchange.save()
                    else:
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],location=row2['Location'])
                        exchange.save()
                else:
                    act = bd.Database('biosphere3').get(code=row2['Activity_code'])
                    if row2['Reference_product'] != 'NA':
                        exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'], product=row2['Reference_product'])
                    else:
                        exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'])
                    exchange.save()
                    pass
                counter = counter + 1
                print('Process saved')
                print('####################')
                print('process {} out of {}'.format(counter, n_processes))
                print('activity {} to {}'.format(act,row2['Activity_origin']))

        else:
           pass

    final_time=time.time()
    final_lap=final_time-starter_time
    print('Create activity executed in {} seconds'.format(final_lap))
    return(activ)



