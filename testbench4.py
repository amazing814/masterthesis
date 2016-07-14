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

maximum_sender_union_size = 4

# 先模拟操作一个subset[0]
r"""
开始生成 capable sender
"""
capable_sender_subset_demands[0] = []
sender_subset_demands[0] = subset_demands_sender_array[1].T
# 以上，转置获得 [J* (t+1)] 矩阵, 针对每一个deliverytask/user-subset, 各个sender的情况

    
single_capable_sender = []
SS = itertools.combinations(range(J), 1)
single_sender = [ss for ss in SS]

for i, one_single_sender in enumerate(single_sender):
    min_help = np.zeros(t+1, dtype=np.int)
    for j, sender in enumerate(one_single_sender):
        min_help = min_help + sender_subset_demands[0][sender]
    if min(min_help)>0:
        single_capable_sender.append(set(one_single_sender))
    
##    if sum(sender_subset_demands[0][one_single_sender]) == 3:
##        single_capable_sender.append(set([one_single_sender]))

#以上，检测单个sender是否可能是capable_sender
#使用set 的原因，是因为 后面要用到 i.issubset(j) 来消去无用项

double_capable_senders = []
DS = itertools.combinations(range(J), 2)
double_senders = [ds for ds in DS]

for i, one_double_sender in enumerate(double_senders):
    min_help = np.zeros(t+1, dtype=np.int)
    for j, sender in enumerate(one_double_sender):
        min_help = min_help + sender_subset_demands[0][sender]
    if min(min_help)>0:
        double_capable_senders.append(set(one_double_sender))
#以上， 检测 两个sender 是否可能是 capable_sender
        

triple_capable_senders = []
TS = itertools.combinations(range(J), 3)
triple_senders = [ts for ts in TS]

for i, one_triple_sender in enumerate(triple_senders):
    min_help = np.zeros(t+1, dtype=np.int)
    for j, sender in enumerate(one_triple_sender):
        min_help = min_help + sender_subset_demands[0][sender]
    if min(min_help)>0:
        triple_capable_senders.append(set(one_triple_sender))
#以上， 检测 三个sender 是否可能是 capable_sender

print("single sender", single_capable_sender)
print("double sender", double_capable_senders)
print("triple sender", triple_capable_senders)

r"""
开始删减无用capable sender
"""

record_list = []
for i in single_capable_sender:
    for j in double_capable_senders:
        if i.issubset(j):
            record_list.append(j)

record_list_c = []
[record_list_c.append(i) for i in record_list if not i in record_list_c]

for k in record_list_c:
    double_capable_senders.remove(k)

# 删除 两个sender 中 的无用项 与 一个sender对比

record_list = []
for i in single_capable_sender:
    for j in triple_capable_senders:
        if i.issubset(j):
            record_list.append(j)
# 因为record_list 里面可能会有完全重复项
record_list_c = []
[record_list_c.append(i) for i in record_list if not i in record_list_c]

for k in record_list_c:
    triple_capable_senders.remove(k)

# 删除 三个sender 中 的无用项 与 一个sender对比


record_list = []
for i in double_capable_senders:
    for j in triple_capable_senders:
        if i.issubset(j):
            record_list.append(j)

record_list_c = []
[record_list_c.append(i) for i in record_list if not i in record_list_c]

for k in record_list_c:
    triple_capable_senders.remove(k)
# 删除 三个sender 中 的无用项 与 两个sender对比

print("new single sender", single_capable_sender)
print("new double sender", double_capable_senders)
print("new triple sender", triple_capable_senders)

# 现在开始收集"针对这一个user subset/ delivery task"所有可选的 capable sender

for i in single_capable_sender:
    capable_sender_subset_demands[0].append(list(i))

for i in double_capable_senders:
    capable_sender_subset_demands[0].append(list(i))

for i in triple_capable_senders:
    capable_sender_subset_demands[0].append(list(i))

print(capable_sender_subset_demands)

# 以上，又把所有 set 格式转变为 list， 是为了以后方便读取每个set里面的元素，
# 每个元素代表了不同的 sender


r"""
全新loop 更高效
"""

multi_capable_sender = [None]* maximum_sender_union_size
# 以上，是 track list, 为了记录不同长度的 sender_union： single, double, triple...

for union_size in range(maximum_sender_union_size):
    
    multi_capable_sender[union_size] = []
    CS = itertools.combinations(range(J), union_size +1)
    sender_unions = [cs for cs in CS]

    for one_sender_union in sender_unions:
        min_help = np.zeros(t+1, dtype=np.int)
        for sender in one_sender_union:
            min_help = min_help + sender_subset_demands[0][sender]
        if min(min_help)>0:
            multi_capable_sender[union_size].append(set(one_sender_union))

for i in multi_capable_sender:
    print ("loop sender union reslut: ", i)

# 现在开始处理 multi_capable_sender 里面的重叠项目（不是重复项目，是重叠！）
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

# 删除 两个sender 中 的无用项 与 一个sender对比

for i in multi_capable_sender:
    print ("new loop sender union reslut: ", i)

a = []
for i in multi_capable_sender:
    a.append(i)

print(a)


















