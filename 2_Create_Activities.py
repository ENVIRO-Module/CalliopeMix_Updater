# Copy ecoinvent 3.9 to a new database "my ecoinvent"
# Create a new activity "future grid mix", which has a single input: wind electricity
# Replace all electricity inputs in Spanish activities with the new activity
import bw2data as bd
import pandas as pd
#set the current project
bd.projects.set_current("Hydrogen_SEEDS")

print(bd.projects.dir) #aqui puedes acceder al archivo databases.db y ver las actividades
print(bd.databases)

pass
#Create an instance of the database of interest
ei = bd.Database("CUTOFF")

print(bd.projects.dir)
pass
# create a copy of the database, just in case.
try:                #If it's not copied yet, it'll take a few minutes
    ei.copy('CUTOFF')
    ei_copy=bd.Database('this_is_a_test')
except AssertionError:
    ei_copy=bd.Database('this_is_a_test')
    pass

#import the csv file containing the LCI data
df=pd.read_csv('data.csv',delimiter=';')


pass


# Create an activity. Include a code  and name






"""

try:
    electro=ei_copy.new_activity(code='THIS IS JUST A TEST',name='TEST_TEST')
    electro.save()
except bd.errors.DuplicateNode:
    pass

"""






#check in database
print(bd.projects._get_base_directories())


#create a new activity




pass
"""

ei = bd.Database("cutoff39")

ei.copy("my ecoinvent 2")
my_ecoinvent = bd.Database("my ecoinvent 2")

# create a new activity
new_act = my_ecoinvent.new_activity(name="future grid mix", code="future grid mix")
new_act.save()

electricity_es = my_ecoinvent.get(code='a6fabdc10edd02a7f2a3d8a0e9b3c0a5', name='electricity production, wind, 1-3MW turbine, onshore', location='ES')
ex = new_act.new_exchange(input=electricity_es, amount=1, type="technosphere")
ex.save()

elect_medium_voltage = my_ecoinvent.get(code='939fddb10cde1b967a39d939d3502ab8', name='market for electricity, medium voltage', location='ES')
upstream_exchanges = list(elect_medium_voltage.upstream())
for ex in upstream_exchanges:
    if ex.output["location"] == "ES":
        ex.input = new_act
        ex.save()

"""
pass



