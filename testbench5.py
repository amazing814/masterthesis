import numpy as np
import itertools
import copy

from classtestify import Testify

from classcapability import Capability

r"""
INPUT:
- ''demands'' -- [K*I] matrix: which user is asking for which file
- ''distribution'' -- [I*J] matrix: which file is stored by which sender
- ''connection'' -- [J*K] matrix: which sender is connected to which user
"""
demands = np.array([[1, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 1]])

distribution = np.array([[1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1]])

connection = np.array([[1, 1, 1, 0, 0, 0],
                       [1, 0, 0, 1, 1, 0],
                       [0, 1, 0, 1, 0, 1],
                       [0, 0, 1, 0, 1, 1]])

I = 6
J = 4
K = 6
N = 6
M = 2

# 以上，除了 M 是要求输入的，I,J,K,N都是可以从输入的矩阵维度读出来的
t = int(M*K / I)



a = Capability(demands, distribution, connection)

demands_sender = a.capability_matrix().tolist()



US = itertools.combinations(range(K), t+1)
user_subsets = [us for us in US] #取出了所有 user-subsets 组合，一共20个

subset_demands_sender = [None]*len(user_subsets)

for i, one_subset in enumerate(user_subsets):
    subset_demands_sender[i] = []
    for one_user, j in enumerate(one_subset):
        subset_demands_sender[i].append(copy.deepcopy(demands_sender[j]))
# 从此 就是处理list 而不是 array了

subset_demands_sender_array = np.array(subset_demands_sender)
# 再把所有的 list 转成 array 以便后续转置操作(.T)
# 每一个 array 有 t+1行， J 列

sender_subset_demands = [None]*len(user_subsets) #用来转置

capable_sender_subset_demands = [None]*len(user_subsets)
#用来收集每个user-subset的capable senders

maximum_sender_union_size = 3


for sub in range(len(user_subsets)):
    
    # 先模拟操作一个subset[sub]/ delivery task
    capable_sender_subset_demands[sub] = []
    sender_subset_demands[sub] = subset_demands_sender_array[sub].T
    
    multi_capable_sender = [None]* maximum_sender_union_size
    # 以上，是 track list, 为了记录不同长度的 sender_union： single, double, triple...

    for union_size in range(maximum_sender_union_size):
        
        multi_capable_sender[union_size] = []
        CS = itertools.combinations(range(J), union_size +1)
        sender_unions = [cs for cs in CS]

        for one_sender_union in sender_unions:
            min_help = np.zeros(t+1, dtype=np.int)
            for sender in one_sender_union:
                min_help = min_help + sender_subset_demands[sub][sender]
            if min(min_help)>0:
                multi_capable_sender[union_size].append(set(one_sender_union))

##    for i in multi_capable_sender:
##        print ("loop sender union reslut: ", i)

    # 现在开始处理 multi_capable_sender 里面的重叠项目（不是重复项目，是重叠！）
    # 比如： {1} 表示 sender1 可以单独完成这个任务，那么它就没有必要再和其他sender组队，也就是说
    # {1,2} {1,3,4} 这样的sender-union就没有意义，需要删除。 
    # 以 single sender (mulit_capable_sender[0])开始向下删除，
    # 然后以 double senders (multi_capable_sender[1])开始向下删除.....直到最后

    for smaller_sender_union in range(maximum_sender_union_size):
        for bigger_sender_union in range(smaller_sender_union + 1, maximum_sender_union_size):
            record_list = []
            for i in multi_capable_sender[smaller_sender_union]:
                for j in multi_capable_sender[bigger_sender_union]:
                    if i.issubset(j):
                        record_list.append(j)
            # 因为record_list 里面可能会有完全重复项：i1和j1有重叠，然后i2和j1也有重叠，导致j1被记录了两次
            record_list_c = []
            [record_list_c.append(i) for i in record_list if not i in record_list_c]

            for k in record_list_c:
                multi_capable_sender[bigger_sender_union].remove(k)

    # 删除所有 重叠项目 之后， multi_capable_sender 里面就记录了针对这个user-subset所有可能的sender-union
    # 第一层 [[single_sender]，[double_sender]...] one type of sender-unions each list
    # 第二层 [double_sender] = [{1,2},{2,3}...] senders/ one sender-union each set 
    # 现在开始登记这个user-subset/delivery-task 的capable senders

    for i in multi_capable_sender:
        capable_sender_subset_demands[sub].append(i)

# check out the final result
i = 0
for cssd in capable_sender_subset_demands:
    i = i+1
    print (i,": ",cssd)
        


















