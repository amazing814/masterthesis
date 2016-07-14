from fenpei import HopcroftKarp
import copy

#graph = {'a': {2,3}, 'b': {1, 3}, 'c': {1, 2}}
#graph = {'a': {2,3}, 'b': {1, 2,4,5}, 'c': {2, 3}, 'd':{2,3}, 'e':{4,5}}
#print(HopcroftKarp(graph).maximum_matching())
#testi = HopcroftKarp(graph).maximum_matching()
#print(testi)

graph1 = {'y1': {1}, 'y8':{2},
          'y15':{3}, 'y19':{4}}
track1 = HopcroftKarp(graph1).maximum_matching()
print(HopcroftKarp(graph1).maximum_matching())
for number in range(1,5):
    if number in track1:
        print ('Sender_{0} is to send deliveryTask_{1}'.format(number, track1[number]))

#**************************************************
graph2 = {'y2': {12,13,23},'y3': {12,14,23},'y4': {13,14,23},
          'y5': {12,13,24},'y6': {12,14,23},'y7':{13,14,24},
          'y9': {13,23,24},'y10': {14,23,24},'y11':{12,13,34},
          'y12': {12,14,34},'y13': {13,14,34},'y14':{12,23,34},
          'y16': {14,23,34},'y17': {12,24,34},'y18':{13,24,34},
          'y20':{23,24,34}}

graph2_1 = copy.deepcopy(graph2)
while len(graph2_1) > 5:
    already = {}
    track2 = HopcroftKarp(graph2_1).maximum_matching()
    print(HopcroftKarp(graph2_1).maximum_matching())
    for number in range(50):
        if number in track2:
            print ('Sender_{0} is to send deliveryTask_{1}'.format(number, track2[number]))
            already[track2[number]]= number

    for keys in already:
        graph2.pop(keys)
    graph2_1 = copy.deepcopy(graph2)

graph2_2 =  copy.deepcopy(graph2)
lowerGraph2_1=set([12,34,13,24])
#lowerGraph2_2=set([13,24])

for keys in graph2:
    graph2_2[keys]= lowerGraph2_1 & graph2[keys]

track2_1 = HopcroftKarp(graph2_2).maximum_matching()
print(HopcroftKarp(graph2_2).maximum_matching())
for number in range(50):
    if number in track2_1:
        print ('Sender_{0} is to send deliveryTask_{1}'.format(number, track2_1[number]))
       
