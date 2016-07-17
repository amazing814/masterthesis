import numpy as np

import copy

from classtestify import Testify

from classcapability import Capability

from classtable import Table

from class2ndmethod import SecondMethod

from class2Randr import SecondRate

r"""
INPUT:
- ''demands'' -- [K*I] matrix: which user is asking for which file
- ''distribution'' -- [I*J] matrix: which file is stored by which sender
- ''connection'' -- [J*K] matrix: which sender is connected to which user
- ''M'' -- cache size of users
"""
M=1

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

###################################################

##demands = np.array([[0, 0, 1],
##                    [1, 0, 0],
##                    [0, 1, 0]])

##M = 1
##
##demands = np.array([[1, 0, 0],
##                    [0, 1, 0],
##                    [0, 0, 1]])
##
##distribution = np.array([[1,1,1],
##                         [1,1,1],
##                         [1,1,1]])
##
##connection = np.array([[0,1,1],
##                       [1,0,1],
##                       [1,1,0]])

######################################################
##M = 1
##
##demands = np.array([[1,0,0,0],
##                    [0,1,0,0],
##                    [0,0,1,0],
##                    [0,0,0,1]])
##
##distribution = np.array([[1,0,0],
##                         [1,0,1],
##                         [0,1,1],
##                         [0,1,0]])
##
##connection = np.array([[1,0,0,1],
##                       [0,1,1,1],
##                       [1,1,1,1]])



K = demands.shape[0]
I = demands.shape[1]
J = distribution.shape[1]
t = int(M*K/I)

a = Capability(demands, distribution, connection)
demands_sender = a.capability_matrix().tolist()

b = Table(demands_sender, K, J, M)
capability_table = b.table_list()

# for the 1st method


# for the 2nd method
c = SecondMethod(capability_table)
track = c.assignment_phase() # or track = c.track

d = SecondRate(demands_sender, track, t)
rate_pair_2 = d.required_rate() # [R, r]
print(rate_pair_2)
