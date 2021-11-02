import pickle
import time
datafile = open("substr_1e3.pkl", 'rb')
data = pickle.load(datafile)
datafile.close()
n = len(data)
maxsum = 0
current_sum = 0
start = time.time()
for p in range(0, n):
    current_sum = max(0, current_sum + data[p])
    maxsum = max(current_sum, maxsum)
t = time.time()-start
print(n, t, maxsum)
