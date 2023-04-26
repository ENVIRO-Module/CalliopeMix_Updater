import bw2data
import bw2io as bi
import bw2data as bd

#You only need to run this once!


#Create a new project. To do so, you need the bw2data
bd.projects.set_current('Hydrogen_SEEDS')

"""
We're going to import ecoinvent in our new project
"""
#Spold files here

spold_files = r'D:\datasets'

# Load biosphere3 and LCIA Methods
bi.bw2setup()

# Loads data from ecoinvent in our RAM. Still not written in our hard drive.
ei = bi.SingleOutputEcospold2Importer(spold_files, "CUTOFF", use_mp=False)
# Link the processes among themselves and to the biosophere
ei.apply_strategies()
ei.statistics()
# ei.statistics() (per saber si tinc tots els exchanges linked)

# Save the database in the hard drive
ei.write_database()
# bd.databases (per comprovar si la database s'ha instal·lat)

print(bd.databases) #check if database is there
print(bw2data.projects.dir)
pass