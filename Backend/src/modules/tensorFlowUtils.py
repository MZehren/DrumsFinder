import numpy as np
from random import shuffle

###
# transoform hotIndex = 3, N = 6 in
# [0,0,0,1,0,0]
def computeOneHotArray(hotIndex, N):
    return np.array([int(i == hotIndex) for i in range(N)])


#return a subset of X and the associated Y to have the same number of sample per classes
def limitMultilabelSamples(samples, limit):
    result = []
    labelLookup = {}
    for sample in samples:
        if sample[0] not in labelLookup:
            labelLookup[sample[0]] = []
        labelLookup[sample[0]].append(sample)
        

    for label in labelLookup:
        shuffle(labelLookup[label])
    
    while len(result) < limit and len(result) < len(samples):    
        for label in labelLookup:
            if len(labelLookup[label]):
                result.append(labelLookup[label].pop())
    
    return result
    

# from tensorflow.python.saved_model import builder as saved_model_builder
# from tensorflow.python.saved_model import signature_constants
# from tensorflow.python.saved_model import signature_def_utils
# from tensorflow.python.saved_model import tag_constants
# from tensorflow.python.saved_model import utils
# from tensorflow.python.util import compat
# 
# def exportModel(sess, export_path):
#     print 'Exporting trained model to', export_path
#     builder = saved_model_builder.SavedModelBuilder(export_path)
#     builder.add_meta_graph_and_variables(
#           sess, [tag_constants.SERVING])
#     builder.save()