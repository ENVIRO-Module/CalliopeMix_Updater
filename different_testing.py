
import bw2data as bd
import pandas as pd
import time

#set the current project
bd.projects.set_current("Hydrogen_SEEDS")
ei_copy = bd.Database("this_is_a_test")

activity_1=ei_copy.get(code='hy_1')
exchanges=list(activity_1.exchanges())

gas=ei_copy.get(code='ec8137188b6f9f38417b8d5a5ec95bd9')
print(gas['unit'])
pass
""""

#create a random activity

try:
    new_activity = ei_copy.new_activity(name='Testing_upstreams', code='test_test')
    new_activity.save()
    # create a df containing the rows

except bd.errors.DuplicateNode:
    new_activity = ei_copy.get(code='test_test')
    new_activity.delete()
    new_activity = ei_copy.new_activity(name='Testing_upstreams', code='test_test')
    new_activity.save()

exchange = new_activity.new_exchange(input=activity_1, type='technosphere', amount=1)
exchange.save()
upstreams=list(activity_1.upstream())
for element in upstreams:
    print(element)

#activity_2=ei_copy.get(code='hy2')
#let's substitue the upstreams of activity1 for hy_2
activity_2=ei_copy.get(code='hy_2')

print('#####Upstream from activity 1 before#####')
for el in activity_1.upstream():
    print(el)
print('######Upstream from activity 2 before#####')
for el in activity_2.upstream():
    print(el)

print('Here comes the magic')


for exchange in activity_1.upstream():
        exchange.input = activity_2
        exchange.save()
        print('an exchange has been changed', exchange)


print('#####Upstream from activity 1 AFTER#####')
for el in activity_1.upstream():
    print(el)
print('######Upstream from activity 2 AFTER#####')
for el in activity_2.upstream():
    print(el)

pass
#create a copy of activity 1
try:
    act_1_copy=activity_1.copy(name='copy_111',code='copy_111')
    act_1_copy.save()
except:
    act_1_copy=ei_copy.get(code='copy_111')

try:
    activity_2_copy=activity_2.copy(name='copy222',code='code_222')
    activity_2_copy.save()
except:
    activity_2_copy = ei_copy.get(code='code_222')


#let's try to substitue the upstream of activity 1 by activity 2


for exchange in activity_1.upstream():
        exchange.input = activity_2
        exchange.save()
        print('an exchange has been changed', exchange)


pass

"""