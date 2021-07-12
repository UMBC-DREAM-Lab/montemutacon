import numpy as np
import dill as pickle

class Pipeline:
    def __init__(self, pipeline, categorical_vecs):
        self.pipeline = pickle.load(open(pipeline, 'rb'))

        self.vectorizers = []

        for name in categorical_vecs:
            self.vectorizers.append(pickle.load(open(name, 'rb')))
        

    def transform(self, pd, categories):
        part1 = self.pipeline.transform(pd).toarray()
        vectors = []

        for i, c in enumerate(categories):
            v = self.vectorizers[i].transform(list(pd[c])).toarray()
            vectors.append(v)
        # thing = np.concatenate(vectors, 1)
        return np.concatenate((*vectors, part1), 1)