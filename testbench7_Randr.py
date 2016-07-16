import itertools
import numpy as np
import copy

track = [{'DS_15': 3, 'DS_19': 4, 'DS_1': 1, 'DS_8': 2},
         {'DS_6': 12, 'DS_14': 34, 'DS_7': 13, 'DS_9': 23,
          'DS_4': 14, 'DS_11': 34, 'DS_18': 13, 'DS_10': 24,
          'DS_13': 13, 'DS_5': 12, 'DS_16': 14, 'DS_20': 24,
          'DS_12': 14, 'DS_3': 23, 'DS_2': 12, 'DS_17': 34},
         {}]

t = 2

demands_sender = [[1, 1, 0, 0],
                  [1, 0, 1, 0],
                  [1, 0, 0, 1],
                  [0, 1, 1, 0],
                  [0, 1, 0, 1],
                  [0, 0, 1, 1]]

K = len(demands_sender)
J = len(demands_sender[0])

##track = [{'DS_6': 2, 'DS_4': 3},
##         {'DS_3': 12, 'DS_1': 13, 'DS_2': 12, 'DS_5': 23}]

US = itertools.combinations(range(K), t+1)
user_subset = [list(us) for us in US]

# 首先 建立每一个 user_subset 的索引
delivery_task_relevant_user_subset = dict()
for delivery_task, relevant_user_subset in enumerate(user_subset):
    delivery_task_relevant_user_subset['DS_'+str(delivery_task+1)] = relevant_user_subset

# 填充 user_subset 的索引为 user_subset 对应 sender
dict_user_subset_demands_sender = dict()   

for keys in delivery_task_relevant_user_subset:
    # 再建立一个和 demands_sender 等大小的全0 矩阵， 用来辅助填充生成 user_subset 对应的 矩阵
    user_subset_demands_sender = np.zeros(np.shape(demands_sender), dtype = np.int)
    
    for user in delivery_task_relevant_user_subset[keys]:
        user_subset_demands_sender[user] = copy.deepcopy(demands_sender[user])

    dict_user_subset_demands_sender[keys] = user_subset_demands_sender

r"""
In dict_user_subset_demands_sender: its key is 'DS_XXX'; value is the relevant
matrix of 'DS_XXX', e.g., DS_1 is the first delivery task aims for user-subset
[0,1,2] (user_one, user_two and user_three). then
  dict_user_subset_demands_sender['DS_1'] = array([[1, 1, 0, 0],
                                                   [1, 0, 1, 0],
                                                   [1, 0, 0, 1],
                                                   [0, 0, 0, 0],
                                                   [0, 0, 0, 0],
                                                   [0, 0, 0, 0]])
where the rows for rest users (user_four, user_five and user_six) are set zero.
"""

# 现在开始回溯 track， 得到 assignment_result_lang, where {'DS_XXX': [0, 1, 0, 1]} 这样的结果

assignment_result = dict() # used to calculate R and for assignment_result_lang

for i in range(len(track)):
    for keys in track[i]:
        recorder = []
        # recorder is to change {DS_1 : 14} to be {DS_1 : [1,4]}
        # then to be {DS_1 : [0,3]}
        for j in range(i+1)[::-1]:
            recorder_help = int(track[i][keys]/(10**(j)))
            recorder.append(recorder_help-1)
            track[i][keys] = track[i][keys]-(recorder_help*(10**j))
        assignment_result[keys] = recorder

    

assignment_result_lang = dict() # used to calculate r

for keys in assignment_result:
    lang_list = np.zeros(J, dtype = np.int)
    for i in assignment_result[keys]:
        lang_list[i] = 1
    assignment_result_lang[keys] = lang_list

r"""
give assignment_result_lang, e.g., assignment_result_lang['DS_7'] = array([1, 0, 1, 0]),
which indicates that the 7the delivery_task is taken by sender_one and sender_three
"""
sender_packets = np.zeros(J, dtype = np.int)
for keys in assignment_result_lang:
    sender_packets = sender_packets+assignment_result_lang[keys]

####################################################################
R = sender_packets.max()
###################################################################

        
r"""
given dict_user_subset_demands_sender and assignment_result_lang, e.g.,
dict_user_subset_demands_sender['DS_3']  =  array([[1, 1, 0, 0],
                                                   [1, 0, 1, 0],
                                                   [0, 0, 0, 0],
                                                   [0, 0, 0, 0],
                                                   [0, 1, 0, 1],
                                                   [0, 0, 0, 0]])
while assignment_result_lang['DS_3'] = array([0, 1, 1, 0]).
We should get the reult as: array([[0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 0, 0]])
                                                
which indicates that, sender_two sends file-pieces for user_one and user_five,
and sender_three sends file-piece for user_two. (in the third delivery task)
"""
single_delivery_task_relevant_sender = dict() # matrix for every delivery_task and its relevant senders
user_sender_packets = np.zeros(np.shape(dict_user_subset_demands_sender[keys]), dtype=np.int)

for keys in dict_user_subset_demands_sender:
    matrix_recorder_help = np.zeros(np.shape(dict_user_subset_demands_sender[keys]), dtype=np.int)
    for i in range(len(dict_user_subset_demands_sender[keys])):
        matrix_recorder_help[i] = dict_user_subset_demands_sender[keys][i]*assignment_result_lang[keys]
    single_delivery_task_relevant_sender[keys] = matrix_recorder_help
    user_sender_packets = user_sender_packets + matrix_recorder_help

#######################################################################            
r = user_sender_packets.max()
#######################################################################

print("The maximum required transmission rate of senders is: R={0} packets.".format(R))
print("The maximum required transmission rate through each link is: r={0} packets.".format(r))






