import copy

from fenpei import HopcroftKarp
# IMPORTANT: HopcroftKarp will change the input dict! so we use copy.deepcop to
# avoid potential danmage


##capability_table=[[[{0}], [], [{1, 2, 3}]],
##                    [[], [{0, 1}, {0, 2}, {1, 2}], []],
##                    [[], [{0, 1}, {0, 3}, {1, 2}], []],
##                    [[], [{0, 2}, {0, 3}, {1, 2}], []],
##                    [[], [{0, 1}, {0, 2}, {1, 3}], []],
##                    [[], [{0, 1}, {0, 3}, {1, 3}], []],
##                    [[], [{0, 2}, {0, 3}, {1, 3}], []],
##                    [[{1}], [], [{0, 2, 3}]],
##                    [[], [{0, 2}, {1, 2}, {1, 3}], []],
##                    [[], [{0, 3}, {1, 2}, {1, 3}], []],
##                    [[], [{0, 1}, {0, 2}, {2, 3}], []],
##                    [[], [{0, 1}, {0, 3}, {2, 3}], []],
##                    [[], [{0, 2}, {0, 3}, {2, 3}], []],
##                    [[], [{0, 1}, {1, 2}, {2, 3}], []],
##                    [[{2}], [], [{0, 1, 3}]],
##                    [[], [{0, 3}, {1, 2}, {2, 3}], []],
##                    [[], [{0, 1}, {1, 3}, {2, 3}], []],
##                    [[], [{0, 2}, {1, 3}, {2, 3}], []],
##                    [[{3}], [], [{0, 1, 2}]],
##                    [[], [{1, 2}, {1, 3}, {2, 3}], []]]

##capability_table = [[[{2}], [{0, 1}]],
##                    [[{1}], [{0, 2}]],
##                    [[{0}], [{1, 2}]]]

capability_table = [[[], [{0, 2}]],
                    [[], [{0, 1}, {0, 2}]],
                    [[], [{0, 1}]],
                    [[{2}], []],
                    [[], [{1, 2}]],
                    [[{1}], []]]

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
            d['DS_'+str(i+1)] = j
            # +1 is to make (task_0 ~ task_19) become (task_1~task_20), easy reading
            # str(i+1) indicates delivery_task, j indicates sender_union set
    layer_dict[different_layer] = d

# now we import HopcroftKarp from fenpei, to do the maximum_matching for each layer,
# i.e., first for the sinlge_sender layer / layer_dict[0]
# then for the double_sender layer / layer_dict[1] and so on.


layer_dict_copy_1 = [None] * len(capability_table[0])
layer_dict_copy_2 = [None] * len(capability_table[0])

track = [None] * len(capability_table[0])

for i in range(len(capability_table[0])):
    track[i] = dict()
    layer_dict_copy_1[i] = copy.deepcopy(layer_dict[i])
    already_assigned_tasks = dict()

    while layer_dict_copy_1[i] != dict():
        layer_dict_copy_2[i] = copy.deepcopy(layer_dict_copy_1[i])
        assignment = HopcroftKarp(layer_dict_copy_2[i]).maximum_matching()
        # if layer_dict_copy[i]={'DS_1':{1}}, the HopcroftKarp will return
        # {'DS_1': 4} which indicates the first delivery task is assigned to sender four
        # However, it will also rerturn {4 : 'DS_1'}, which is useless. So we have codes
        # as belows to elimates such useless item.
        for keys in assignment:
            if type(keys) != int:
                already_assigned_tasks[keys] = assignment[keys]
                layer_dict_copy_1[i].pop(keys)
                
        #print(already_assigned_tasks)   
    
    track[i] = already_assigned_tasks
    print(track[i])
    


           











