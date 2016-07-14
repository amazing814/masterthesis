import numpy as np

from classtestify import Testify

from classcapability import Capability

from classtable import Table

r"""
INPUT:
- ''demands'' -- [K*I] matrix: which user is asking for which file
- ''distribution'' -- [I*J] matrix: which file is stored by which sender
- ''connection'' -- [J*K] matrix: which sender is connected to which user
- ''M'' -- cache size of users
"""
M=2
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
##demands = np.array([[1,0,0,0],
##                    [0,1,0,0],
##                    [0,0,1,0],
##                    [0,0,0,1]])
##
##distribution = np.array([[1,1,1],
##                         [1,1,1],
##                         [0,0,0],
##                         [0,0,0]])
##
##connection = np.array([[1,0,0,1],
##                       [0,1,1,1],
##                       [1,1,1,1]])



K = demands.shape[0]
I = demands.shape[1]
J = distribution.shape[1]

a = Capability(demands, distribution, connection)
demands_sender = a.capability_matrix().tolist()

b = Table(demands_sender, K, J, M)
capability_table = b.table_list()

i = 0
for j in capability_table:
    print (i,": ", j)
    i = i+1
