
""""

DO NOT PAY ATTENTION TO THIS

"""


import bw2data as bd
import bw2data as bd
import pandas as pd
#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
print(bd.projects.dir)
print(bd.databases)
#Create an instance of the database of interest
ei = bd.Database("CUTOFF")
biosphere=bd.Database('biosphere3')

#all_methods=list(bd.methods)
#results=[n for n in all_methods if 'GWP' in str(n) and 'ReCiPe' in str(n)]

#check biosphere flows
oxygen=bd.Database('biosphere3').search('Oxygen)
pass
