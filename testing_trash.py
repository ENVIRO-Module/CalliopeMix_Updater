

import bw2data as bd
import pandas as pd
import time

#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
ei = bd.Database("CUTOFF")
# create a copy of the database, just in case.
try:                #it'll take a few minutes
    ei.copy('CUTOFF')
    ei_copy=bd.Database('this_is_a_test')
except AssertionError:
    ei_copy=bd.Database('this_is_a_test')
    pass


code='hy_2'
act=ei_copy.get(code=code)
activty_ex=list(act.upstream())


for ex in activty_ex:
    print(ex)
code2='hy_1'
second=ei_copy.get(code=code2)

for element in act.upstream():
    element.delete()
    element.new_exchange(input=second,amount=1)
    element.save()

second_upstream=list(act.upstream())
print('########Modified')

for b in second_upstream:
    print(b)



pass