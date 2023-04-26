
import bw2data as bd
import pandas as pd
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
    """
    :param df:
    Expected columns: [Amount, Activity, Activity name, Code]
    :return:
    """

    for index,row in df.iterrows():
        print(row['Product'])

        #Check if we're creating a new activity

        if row['Activity']=='Yes':
            activity_name = str(row['Activity name'])
            print(activity_name)
            try:
                new_activity=ei_copy.new_activity(name=str(row['Activity name']),code=str(row['Code']))
                new_activity.save()
            #create a df containing the rows

            except bd.errors.DuplicateNode:
                new_activity=ei_copy.get(code=str(row['Code']))
                new_activity.delete()
                new_activity = ei_copy.new_activity(name=str(row['Activity name']), code=str(row['Code']))
                new_activity.save()

            act_df=df.loc[df['Activity_origin']==activity_name]
            for ind,row2 in act_df.iterrows():
                act=bd.Database('CUTOFF').get(code=row2['Product'])
                exchange=new_activity.new_exchange(input=act,type='technosphere',amount=row2['Amount'])
                exchange.save()

            #check it worked:
            print(list(new_activity.technosphere()))
        else:
            pass

InventoryFromExcel(df)

pass
