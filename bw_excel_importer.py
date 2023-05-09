import bw2data as bd
import bw2io as bi
import pandas as pd
import time
#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
print(bd.projects.dir)
print(bd.databases)

ei = bd.Database("CUTOFF")
# create a copy of the database, just in case.
try:                #it'll take a few minutes
    ei.copy('this_is_a_test2')
    ei_copy=bd.Database('this_is_a_test2')

except AssertionError:
    ei_copy=bd.Database('this_is_a_test2')
    pass


act=ei.get(code='e9f251f40cfbdb5be9fdc08cc1ddae94')
act2=ei_copy.get(code='c97de36e061768ba4015b90539bbb0cb')

print(act['unit'])



gas=ei_copy.get(code='d5a031db0bd7796a8f959ce8f4b54d0f')

for exchange in list(gas.technosphere()):
    print(exchange)
º
pass


