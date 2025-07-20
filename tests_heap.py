import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 2)
heapq.heappush(h, 8)

print(h)
print(f'pai(0) = {h[(0-1)//2]}')
print(f'filho esq(0) = {h[2*0+1]}')
print(f'filho dir(0) = {h[2*0+2]}')

topo = h[0]

print(topo)

menor = heapq.heappop(h)

print(menor)

heapq.heapify([])