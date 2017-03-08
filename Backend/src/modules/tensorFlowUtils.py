import numpy as np

###
# 
def computeOneHotArray(hotIndex, N):
    return np.array([int(i == hotIndex) for i in range(N)])
