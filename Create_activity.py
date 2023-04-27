
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
print('we ran this')


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
                    act = bd.Database(row2['Database']).get(code=row2['Product'])
                    if row2['Final_Product'] == 'Yes':
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],product=row2['Activity name'])
                        exchange.save()
                    else:
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'])
                        exchange.save()
                else:
                    act = bd.Database('biosphere3').get(code=row2['Product'])
                    #exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'],product=' 1kg of Hydrogen, 20 bars')
                    #exchange.save()
                    pass
                counter = counter + 1
                print('Process saved')
                print('####################')
                print('process{} out of {}'.format(counter, n_processes))


start_time=time.time()
InventoryFromExcel(df)
end_time=time.time()
print(f'Time to run second alternative: {end_time-start_time}')


act_to_study=bd.Database('this_is_a_test').get(code='hy_1')
ac2=list(act_to_study.technosphere())
ac3=list(act_to_study.exchanges())

pass

#faster alternative
"""
def InventoryFromExcel2(df):

    n_processes=len(df.index)
    def iterrow(row): #avoid using pd.iterrows()
        counter = 0
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
                if row2['Technosphere']=='Yes':
                    act = bd.Database('CUTOFF').get(code=row2['Product'])
                    if row2['Final_Product']=='Yes':
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],product=row2['Activity name'])
                        exchange.save()
                    else:
                        exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'])
                        exchange.save()
                else:
                    act = bd.Database('biosphere3').get(code=row2['Product'])
                    exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'],product=' 1kg of Hydrogen, 20 bars')
                    exchange.save()
                counter= counter+ 1
                print('Process saved')
                print('####################')
                print('process{} out of {}'.format(counter,n_processes))



            # check it worked:
            print(list(new_activity.technosphere()))
        else:
            print('Going to the next process')
    df.apply(lambda row: iterrow(row),axis=1)


start_time=time.time()
InventoryFromExcel2(df)
end_time=time.time()
print(f'Time to run second alternative: {end_time-start_time}')
"""



"""


#third alternative
def InventoryFromExcel3(df): #Use dictionary instead of df

    n_processes = len(df.index)
    counter = 0
    data = df.to_dict(orient='records')
    for row in data:
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
                act = bd.Database('CUTOFF').get(code=row2['Product'])
                if row2['Final_Product'] == 'Yes':
                    exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'],
                                                         product=row2['Activity name'])
                    exchange.save()
                else:
                    exchange = new_activity.new_exchange(input=act, type='technosphere', amount=row2['Amount'])
                    exchange.save()
            else:
                act = bd.Database('biosphere3').get(code=row2['Product'])
                exchange = new_activity.new_exchange(input=act, type='biosphere', amount=row2['Amount'],
                                                     product=' 1kg of Hydrogen, 20 bars')
                exchange.save()
            counter = counter + 1
            print('Process saved')
            print('####################')
            print('process{} out of {}'.format(counter, n_processes))
"""
"""
start_time=time.time()
InventoryFromExcel3(df)
end_time=time.time()
print(f'Time to run the third alternative: {end_time-start_time}')

"""

