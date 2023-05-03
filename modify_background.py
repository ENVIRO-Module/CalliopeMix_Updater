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



def ModifyBackground(data,activity_code : str,location : str):
    #Create a new activity
    # We're creating a new market for electricity in 2050
    new_activity_code=InventoryFromExcel(data)

    new_activity=ei_copy.get(code=new_activity_code)
    act_to_change=ei_copy.get(code=activity_code)

    upstream_exchanges=list(act_to_change.upstream())
    """
    
    for exchange in upstream_exchanges:
        if exchange.output['location']==location:
            exchange.input=new_activity
            exchange.save()
            #check
            print('an exchange has been changed',exchange)
"""
    return upstream_exchanges

electricity_2050=pd.read_csv('electricity.csv',delimiter=';')

market_for_electricity_2020='f44aa84c22af00eb9a286714b45f50b4'

starter_time=time.time()
a=ModifyBackground(electricity_2050,market_for_electricity_2020,'PT')
finish_time=time.time()

print('Run time: {}'.format(finish_time-starter_time))
pass


