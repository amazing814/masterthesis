# this is the test for matrix multiple
r"""
I decided to use numpy.array instead of numpy.mat to multiple two matrices.
In the sack for later extensions
"""

import numpy as np

file_sender_distribution = np.array([[1, 1], [1, 1]])

sender_user_connection = np.array([[1, 1], [1, 1]])

file_user_distribution = np.dot(file_sender_distribution, sender_user_connection)

print(file_user_distribution)

if file_user_distribution.min() == 0:
    print ('Wrong, plz type in new matrix.')
    else:
        print ('Now we can try to bulid the capablitiy table.')
