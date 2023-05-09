

"""
We're creating a new inventory for hydrogen combustion using CHP.

We're assuming a wide development of hydrogen in 2050, we're a 400MW CHP power plant can be operated using hydrogen

"""
from Create_activity import InventoryFromExcel

import bw2data as bd
import pandas as pd
import time
#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
print(bd.projects.dir)

#create an instance for the database

ei_copy = bd.Database("this_is_a_test")

"""
We're going to use the CHP plant 400MW in Portugal as a Proxy where we're going to change the input of natural gas for hydrogen
"""



chp=ei_copy.get(code='79aa2a5fabdbf29b9aa415602f4a9a59')
for a in list(chp.technosphere()):
    print(a)

#we want to replace the following exhcange: Exchange: 0.11608779637830263 cubic meter 'market for natural gas, high pressure

#First, we copy the activity with a differnt name
chp_copy=chp.copy(name='CHP_HYDROGEN_2050',code='CHP_hydrogen_2050')
chp_copy.save()

#check
print('######IS THIS WORKING?#######')
for a in list(chp_copy.technosphere()):
    print(a)



#import the market for hydrogen
market_hydrogen=ei_copy.get(code='market_hydrogen_2050_A')


#Replace the exchange of intrest
for ex in chp_copy.technosphere():
    if ex.input['name'] =='market for natural gas, high pressure':
        ex.delete()
        print('!!!!!!!!!!!!')
        print(ex.input['name'], 'has been deleted')
        #include market for hydrogen as a new input
        exchange=chp_copy.new_exchange(input=market_hydrogen, amount=0.036, type='technosphere')
        exchange.save()
#finally, let's check if it worked


print('#####################################')
for exchange in list(chp_copy.technosphere()):
    print(exchange)



pass