
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
try:                #it'll take a few minutes
    ei.copy('CUTOFF')
    ei_copy=bd.Database('this_is_a_test')
except AssertionError:
    ei_copy=bd.Database('this_is_a_test')
    pass

#import the csv file containing the LCI data
df=pd.read_csv('data.csv',delimiter=';')

def InventoryFromExcel(df):
    n_processes=len(df.index)
    counter = 0

    for index,row in df.iterrows():

        #Check if we're creating a new activity
        if row['New Activity'] == 'Yes':
            activity_name = str(row['Activity name'])
            print(activity_name)
            try:
                new_activity = ei_copy.new_activity(name=str(row['Activity name']), code=str(row['Code']))
                new_activity.save()
            # create a df containing the rows
            except bd.errors.DuplicateNode:
                new_activity = ei_copy.get(code=str(row['Code']))
                new_activity.delete()
                new_activity = ei_copy.new_activity(name=str(row['Activity name']), code=str(row['Code']))
                new_activity.save()

            act_df = df.loc[df['Activity_origin'] == activity_name]
            for _, row2 in act_df.iterrows():
                if row2['Technosphere'] == 'Yes':
                    act = bd.Database(row2['Database']).get(code=row2['Activity_code'])

                    if row2['Final_Product'] != 'NA':
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],product=row2['Reference_product'],location=row2['Location'])
                        exchange.save()
                    else:
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],location=row2['Location'])
                        exchange.save()
                else:
                    act = bd.Database('biosphere3').get(code=row2['Activity_code'])
                    exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'], product=row2['Reference_product'])
                    exchange.save()
                    pass
                counter = counter + 1
                print('Process saved')
                print('####################')
                print('process {} out of {}'.format(counter, n_processes))
                print('activity {} to {}'.format(act,row2['Activity_origin']))


start_time=time.time()
InventoryFromExcel(df)
end_time=time.time()
print(f'Time to run second alternative: {end_time-start_time}')


pass



