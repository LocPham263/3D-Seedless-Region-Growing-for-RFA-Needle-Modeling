import numpy as np
a = np.array(([1, 1, 1],
              [1, 0, 0],
              [1, 0, 1]))
b = np.array(([1, 0, 1],
              [0, 1, 0],
              [1, 1, 1]))

fn = a.sum() - (a * b).sum()
union = (a.astype(int) | b.astype(int)).sum()

print(round(fn / union, 2))