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

t = int(M*K / I)



a = Capability(demands, distribution, connection)

demands_sender = a.capability_matrix().tolist()



T = itertools.combinations(range(K), t+1)
user_subsets = [us for us in T] #取出了所有 user-subsets 组合，一共20个
subset_demands_sender = [None]*len(user_subsets)

for i, one_subset in enumerate(user_subsets):
    subset_demands_sender[i] = []
    for one_user, j in enumerate(one_subset):
        subset_demands_sender[i].append(copy.deepcopy(demands_sender[j]))
# 从此 就是处理list 而不是 array了

print(subset_demands_sender[19])

subset_demands_sender_array = np.array(subset_demands_sender)

print(subset_demands_sender_array[19])





