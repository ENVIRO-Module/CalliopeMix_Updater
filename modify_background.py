import bw2data as bd
import pandas as pd
import time
from Create_activity import InventoryFromExcel


#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
#print(bd.databases)
#Create an instance of the database of interest
ei = bd.Database("CUTOFF")
# create a copy of the database, just in case.
try:                #it'll take a few minutes
    ei.copy('CUTOFF')
    ei_copy=bd.Database('this_is_a_test')
except AssertionError:
    ei_copy=bd.Database('this_is_a_test')
    pass

def ModifyBackground(data, activity_code : str):
    """

    :param data: csv containing the inventory you want to create
    :param activity_code: db code of the activity that you want to change
    :return:

    """

    #Create a new activity

    # We're creating a new market for electricity in 2050
    new_activity_code=InventoryFromExcel(data)
    new_activity=ei_copy.get(code=new_activity_code)
    act_to_change=ei_copy.get(code=activity_code)

    print('upstream before this function')
    for element in new_activity.upstream():
        print(element)


    for exchange in act_to_change.upstream():
        #replace and save
        exchange.input = new_activity
        exchange.save()

        print('an exchange has been changed', exchange)

    print('upstream after the execution of this function')

    for element in new_activity.upstream():
        print(element)



