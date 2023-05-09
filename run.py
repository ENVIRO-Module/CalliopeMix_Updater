from modify_background import ModifyBackground
from Create_activity import InventoryFromExcel
import bw2data as bd
import pandas as pd
import time

"""
Before running enbios, it's necessary to include the activities in the database.

"""
#select the current project
bd.projects.set_current("Hydrogen_SEEDS")
ei = bd.Database("CUTOFF")

#Create a default electricity_default.csv first
#This has no hydrogen included, so it won't raise errors

InventoryFromExcel(r'Data\electricity_default.csv')

#Include the other activities

InventoryFromExcel(r'Data\AWE.csv')
InventoryFromExcel(r'Data\PEM.csv')
InventoryFromExcel(r'Data\Market_for_hydrogen.csv')


#Create one more activity. This one modifies the inventory of CHP electricity production, replacing natural gas and using hydrogen as an input

chp=ei.get(code='79aa2a5fabdbf29b9aa415602f4a9a59')
#Create a copy, to avoid problems in the db


try:
    chp_copy=chp.copy(name='CHP_HYDROGEN_2050',code='CHP_hydrogen_2050')
    chp_copy.save()
except:
    chp_copy=ei.get(code='CHP_hydrogen_2050')
    chp_copy.delete()
    chp_copy=chp.copy(name='CHP_HYDROGEN_2050',code='CHP_hydrogen_2050')
    chp_copy.save()
pass

#import the market for hydrogen
market_hydrogen=ei.get(code='market_hydrogen_2050_A')
pass
#Replace the exchange of intrest
for ex in chp_copy.technosphere():
    if ex.input['name'] =='market for natural gas, high pressure':
        ex.delete()
        print(ex.input['name'], 'has been deleted')
        #include market for hydrogen as a new input
        exchange=chp_copy.new_exchange(input=market_hydrogen, amount=0.036, type='technosphere')
        exchange.save()

#Now you can create the electricity.csv that includes electricity production with hydrogen technologies
#~~~~~~~~~~
"""
Here is where the loop with enbios is supposed to start
"""
#~~~~~~~~~~

#Before creating the inventory, you're supposed to modify the amount of the electricity, matching the amount of the spore

#Replace all the upstream of market for electricity with this new Inventory of electriccity

#With this function you're creating a new inventory for the elctricity production, and using it instead of the Market for electricity in Portugal
ModifyBackground(r'Data\electricity.csv','f44aa84c22af00eb9a286714b45f50b4')
#Finally, we should export the DB and use it to run enbios
