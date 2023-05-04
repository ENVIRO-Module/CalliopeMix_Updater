from modify_background import ModifyBackground
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

electricity_2050=pd.read_csv(r'Data\electricity.csv',delimiter=';')

market_for_electricity_2020='f44aa84c22af00eb9a286714b45f50b4'

starter_time=time.time()

ModifyBackground(electricity_2050,market_for_electricity_2020)

finish_time=time.time()

print('Run time: {}'.format(finish_time-starter_time))