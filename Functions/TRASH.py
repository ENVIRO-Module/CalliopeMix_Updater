
import pandas as pd
from openpyxl import Workbook
import bw2data as bd
bd.projects.set_current("Hydrogen_SEEDS")
ei = bd.Database("CUTOFF")


df=pd.read_excel("C:/Users/altz7/UAB/LIVENlab - SEEDS - _Alex/Hydrogen/base_file_simplified.xlsx", sheet_name='ScalarIndicators')

df=df['Formula'].tolist()

all_methods=list(bd.methods)
results=[n for n in all_methods if 'ReCiPe' in str(n) and "midpoint (H)" in str(n)]
#method=('EF v3.0', 'climate change', 'global warming potential (GWP100)')




my_activities=['97310bf6265a7c8101f0bb8c076b1e9f','bb29a87b21e9b8f39132ed7b75ddcc16','aab4ac6e87cbb346f9e44a340bcac248']
method=df[2]
print(method)
print(type(method))

method_modif=eval(method)

methodd=('ReCiPe 2016 v1.03, midpoint (H)', 'material resources: metals/minerals', 'surplus ore potential (SOP)')
print(type(method_modif))



pass
resultados=[]
for a in my_activities:
    b=ei.get(code=a)
    lca_loop=b.lca(method=method_modif,amount=1)
    print(lca_loop.score)
    print(b['name'])
    resultados.append(lca_loop.score)

resultado=sum(resultados)

pass