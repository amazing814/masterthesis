import numpy as np
import itertools
import copy

##demands_sender = np.array([[1, 1, 1, 0],
##                           [1, 1, 1, 0],
##                           [1, 1, 1, 1],
##                           [0, 1, 1, 0],
##                           [0, 1, 0, 1],
##                           [0, 0, 1, 1]])
demands_sender = np.array([[1, 1, 0, 0],
                           [1, 0, 1, 0],
                           [1, 0, 0, 1],
                           [0, 1, 1, 0],
                           [0, 1, 0, 1],
                           [0, 0, 1, 1]])

t = 2

K = demands_sender.shape[0]
J = demands_sender.shape[1]

user_subset_demands_sender = []
#to track every delivery task and its relevant capable senders

cut_value = []
#to track every delivery task will be split into how many smaller pieces

S = itertools.combinations(range(K), t+1)
user_subsets = [f for f in S]


for one_user_subset in user_subsets:
    one_user_subset_demands_sender = np.ones(np.shape(demands_sender), dtype = np.int)*2
    for one_user in one_user_subset:
        one_user_subset_demands_sender[one_user] = copy.deepcopy(demands_sender[one_user])

    
    user_subset_demands_sender.append(one_user_subset_demands_sender)
    cut_value.append(np.min(np.sum(one_user_subset_demands_sender, axis=1)))


for delivery_task in range(len(user_subset_demands_sender)):
    for one_user in user_subsets[delivery_task]:
        cut_recorder = 0
        for one_sender in range(len(user_subset_demands_sender[delivery_task][one_user])):
            cut_recorder = cut_recorder + user_subset_demands_sender[delivery_task][one_user][one_sender]
            if cut_recorder > cut_value[delivery_task]:
                user_subset_demands_sender[delivery_task][one_user][one_sender] = 0
            

real_user_subset_demands_sender = []

for delivery_task in range(len(user_subsets)):
    one_user_subset_demands_sender = np.zeros(np.shape(demands_sender), dtype = np.int)

    for one_user in user_subsets[delivery_task]:
        one_user_subset_demands_sender[one_user] = copy.deepcopy(user_subset_demands_sender[delivery_task][one_user])

    real_user_subset_demands_sender.append(one_user_subset_demands_sender)


assignment_result = [] # to track which sender participates in each delivery_task

for delivery_task in range(len(real_user_subset_demands_sender)):
    assignment_result_lang = np.zeros(J)
    
    for one_user in range(len(real_user_subset_demands_sender[delivery_task])):
        for one_sender in range(len(real_user_subset_demands_sender[delivery_task][one_user])):
            if real_user_subset_demands_sender[delivery_task][one_user][one_sender] == 1:
                assignment_result_lang[one_sender] = 1/(cut_value[delivery_task])

    assignment_result.append(assignment_result_lang)

sender_packet = np.zeros(J) # to calculate R
for rate_single_delivery_task in assignment_result:
    sender_packet = sender_packet + rate_single_delivery_task

#################################################################
R_max = sender_packet.max()
R_min = sender_packet.min()
#################################################################

user_sender_packets = np.zeros(np.shape(demands_sender), dtype = np.int) # to calculate r

for delivery_task in range(len(real_user_subset_demands_sender)):
    
    real_user_subset_demands_sender[delivery_task] = real_user_subset_demands_sender[delivery_task]/cut_value[delivery_task]
    user_sender_packets = user_sender_packets + real_user_subset_demands_sender[delivery_task]
    
######################################################################
r_max = user_sender_packets.max()

min_recorder = 10000
for i in user_sender_packets:
    for j in i:
        if j != 0:
            min_recorder = min(min_recorder, j)
r_min = min_recorder
######################################################################




