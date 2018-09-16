
import itertools
import numpy as np
from rake_nltk import Rake

def rank(M, d, err):
    N = M.shape[1]
    v = np.random.rand(N, 1)
    v /= np.linalg.norm(v)
    last_v = np.ones((N, 1)) * 999
    M_hat = (d * M) + (((1 - d) / N) * np.ones((N, N)))

    while (np.linalg.norm(v - last_v) > err):
        last_v = v
        v = np.dot(M_hat, v)
    return v