from fenpei import HopcroftKarp
import copy

capability_table=[[[{0}], [], [{1, 2, 3}]],
                    [[], [{0, 1}, {0, 2}, {1, 2}], []],
                    [[], [{0, 1}, {0, 3}, {1, 2}], []],
                    [[], [{0, 2}, {0, 3}, {1, 2}], []],
                    [[], [{0, 1}, {0, 2}, {1, 3}], []],
                    [[], [{0, 1}, {0, 3}, {1, 3}], []],
                    [[], [{0, 2}, {0, 3}, {1, 3}], []],
                    [[{1}], [], [{0, 2, 3}]],
                    [[], [{0, 2}, {1, 2}, {1, 3}], []],
                    [[], [{0, 3}, {1, 2}, {1, 3}], []],
                    [[], [{0, 1}, {0, 2}, {2, 3}], []],
                    [[], [{0, 1}, {0, 3}, {2, 3}], []],
                    [[], [{0, 2}, {0, 3}, {2, 3}], []],
                    [[], [{0, 1}, {1, 2}, {2, 3}], []],
                    [[{2}], [], [{0, 1, 3}]],
                    [[], [{0, 3}, {1, 2}, {2, 3}], []],
                    [[], [{0, 1}, {1, 3}, {2, 3}], []],
                    [[], [{0, 2}, {1, 3}, {2, 3}], []],
                    [[{3}], [], [{0, 1, 2}]],
                    [[], [{1, 2}, {1, 3}, {2, 3}], []]]


#尝试 抽取 single_sender, double_sender, triple_sender......
layer = [None] * len(capability_table[0])

for i in range(len(capability_table[0])):
    layer[i]=[]
    for delivery_task in capability_table:
        layer[i].append(delivery_task[i])
        if delivery_task[i] != []:
            # since the delivery task can be assigned to sender-union of smaller size,
            # it won't be assigned to sender-union of bigger size now.
            for j in range(i+1,len(capability_table[0])):
                delivery_task[j] = []

# now we make the capable sender union list [{1,3}, ..., {3,4}]
# where {1, 3} means sender_1 and sender_3 cooperate together can finish this task
# to be {13, ..., 34}, for maximum-matching class
new_layer = [None]* len(capability_table[0])

for k in range(len(capability_table[0])):
    new_layer[k] = []
    for sender_union_for_task in layer[k]: #锁定一层
        if sender_union_for_task == []:
            new_layer[k].append({})
        else:
            digit_value = len(sender_union_for_task[0])
            new_set = []
            for one_sender_union in sender_union_for_task: #锁定一层中的一个
                new_value = 0
                for i, j in enumerate(one_sender_union):
                    new_value = new_value + (j+1)*(10**(digit_value-i-1))
                new_set.append(new_value) #完成一层的统计
            new_layer[k].append(set(new_set))

# now we make the  new_layer[k] = [{13, ..., 34}, ...] , whose index means which task
# to be dict as {delivery_task: {13, ...., 34}}
# 现在，要生成不同的layer_dict, 用来向下兼容 HopcroftKarp-class

layer_dict = [None] * len(capability_table[0])

for different_layer in range(len(capability_table[0])):
    d = dict()
    for i, j in enumerate(new_layer[different_layer]):
        if j != {}:
            d['DS_'+str(i)] = j
    # str(i) indicates delivery_task, j indicates sender_union set
    layer_dict[different_layer] = d

# now we import HopcroftKarp from fenpei, to do the maximum_matching for each layer,
# i.e., first for the sinlge_sender layer / layer_dict[0]
# then for the double_sender layer / layer_dict[1] and so on

track = [None] * len(capability_table[0])

for i in range(len(capability_table[0])):
    track[i] = HopcroftKarp(copy.deepcopy(layer_dict[i])).maximum_matching()
    # important: HopcroftKarp will change the input dict! so we use copy.deepcopy
    print(track[i])

            

##number = 1
##
##现在 要把所有的元素变成 list 而不是 set
##
##capability_table_list = [None] * len(capability_table[0])
##
##for i, sender_union in enumerate(capability_table[number]):
##    capability_table_list[i]=[]
##    for j, one_union in enumerate(sender_union):
##        capability_table_list[i].append(list(one_union))


##for sender_union in capability_table[number]:
##    print ("first loop: ", sender_union)
##    for one_union in sender_union:
##        one_union = list(one_union)
##        print ("second loop: ", one_union)
##
##print(capability_table[number])

##layers = [None]*len(capability_table[0])
##
##for task in range(len(capability_table)):
##    layers[0] = []
##    if capability_table[task][0]
