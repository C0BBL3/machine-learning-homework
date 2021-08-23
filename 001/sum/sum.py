import time

avg = []
for i in range(10):
    temp = time.time()
    sum_ = sum([j for j in range(1,1000001)])
    avg.append(time.time() - temp)

print('Python:', sum(avg) / 10)