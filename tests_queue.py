from collections import deque

queue = deque([1,2,3,4,5,6,7,8], maxlen=5)

print(queue)


queue = deque([], maxlen=3)

queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)
queue.append(5)

print(queue)