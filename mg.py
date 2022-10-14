import random
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from queue import Queue

num_rows = 60#int(input("Rows: ")) # number of rows
num_cols = 60#int(input("Columns: ")) # number of columns
 
# The array M is going to hold the array information for each cell.
# The first four coordinates tell if walls exist on those sides 
# and the fifth indicates if the cell has been visited in the search.
# M(LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED)
M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)
 
# The array image is going to be the output image to display
image = np.zeros((num_rows*10,num_cols*10), dtype=np.uint8)
image1 = np.zeros((num_rows*10,num_cols*10), dtype=np.uint8)
 
# Set starting row and column
r = num_rows-1
c = num_cols-1
history = [(r,c)] # The history is the stack of visited locations
 
# Trace a path though the cells of the maze and open walls along the path.
# We do this with a while loop, repeating the loop until there is no history, 
# which would mean we backtracked to the initial start.
while history: 
	#random choose a candidata cell from the cell set histroy
	r,c = random.choice(history)
	M[r,c,4] = 1 # designate this location as visited
	history.remove((r,c))
	check = [] # 标识当前cell能通路的方向
	# If the randomly chosen cell has multiple edges 
    # that connect it to the existing maze, 
	if c > 0:
		if M[r,c-1,4] == 1:
			check.append('L')
		elif M[r,c-1,4] == 0:
			history.append((r,c-1))
			M[r,c-1,4] = 2
	if r > 0:
		if M[r-1,c,4] == 1: 
			check.append('U') 
		elif M[r-1,c,4] == 0:
			history.append((r-1,c))
			M[r-1,c,4] = 2
	if c < num_cols-1:
		if M[r,c+1,4] == 1: 
			check.append('R')
		elif M[r,c+1,4] == 0:
			history.append((r,c+1))
			M[r,c+1,4] = 2 
	if r < num_rows-1:
		if M[r+1,c,4] == 1: 
			check.append('D') 
		elif  M[r+1,c,4] == 0:
			history.append((r+1,c))
			M[r+1,c,4] = 2
 
    # select one of these edges at random.
    # and break the walls between these two cells.
	if len(check):
		if check.count('L') > 0:
			check.extend(['L']*15)
		if check.count('U') > 0:
			check.extend(['U']*16)
		move_direction = random.choice(check)
		if move_direction == 'L':
			M[r,c,0] = 1
			c = c-1
			M[r,c,2] = 1
		if move_direction == 'U':
			M[r,c,1] = 1
			r = r-1
			M[r,c,3] = 1
		if move_direction == 'R':
			M[r,c,2] = 1
			c = c+1
			M[r,c,0] = 1
		if move_direction == 'D':
			M[r,c,3] = 1
			r = r+1
			M[r,c,1] = 1
         
# Open the walls at the start and finish
M[0,0,0] = 1
M[num_rows-1,num_cols-1,2] = 1
    
# Generate the image for display
for row in range(0,num_rows):
    for col in range(0,num_cols):
        cell_data = M[row,col]
        for i in range(10*row+2,10*row+8):
            image[i,range(10*col+2,10*col+8)] = 255 # 白色通路
        if cell_data[0] == 1: 
            image[range(10*row+2,10*row+8),10*col] = 255
            image[range(10*row+2,10*row+8),10*col+1] = 255
        if cell_data[1] == 1: 
            image[10*row,range(10*col+2,10*col+8)] = 255
            image[10*row+1,range(10*col+2,10*col+8)] = 255
        if cell_data[2] == 1: 
            image[range(10*row+2,10*row+8),10*col+9] = 255
            image[range(10*row+2,10*row+8),10*col+8] = 255
        if cell_data[3] == 1: 
            image[10*row+9,range(10*col+2,10*col+8)] = 255
            image[10*row+8,range(10*col+2,10*col+8)] = 255
        
# give answer
#链式前向星
head=[-1 for n in range(num_rows*num_cols+1)]
to = [0]*100000
nex = [-1]*100000
cnt = -1
# head[u] 和 cnt 的初始值都为 -1
def add(u, v):
    global to,nex,cnt,head
    cnt = cnt + 1
    nex[cnt] = head[u] # 当前边的后继
    head[u] = cnt # 起点 u 的第一条边
    to[cnt] = v # 当前边的终点

M[0,0,0] = 0
M[num_rows-1,num_cols-1,2] = 0
rcdRepeat = []
for row in range(0,num_rows):
    for col in range(0,num_cols):
        cell_data = M[row,col]
        if cell_data[0] == 1:
            add(row*num_cols+col+1,row*num_cols+col)
        if cell_data[1] == 1: 
            add(row*num_cols+col+1,(row-1)*num_cols+col+1)
        if cell_data[2] == 1: 
            add(row*num_cols+col+1,row*num_cols+col+2)
        if cell_data[3] == 1: 
            add(row*num_cols+col+1,(row+1)*num_cols+col+1)
# print(head)
vis = [False]*(num_rows*num_cols+1)
p = [-1]*(num_rows*num_cols+1)
d = [0]*(num_rows*num_cols+1)
def bfs(u):
    global to,nex,cnt,head,vis,p,d
    Q = Queue()
    Q.put(u)
    vis[u] = True
    d[u] = 0
    p[u] = -1
    while Q.qsize() != 0:
        u = Q.get()
        i = head[u]# u点的第一条边 存储在 i 处
        while i!=-1:
            if vis[to[i]] == False: # u的第一条边的终点 尚未遍历到
                Q.put(to[i]) # 添加到待遍历的队列
                vis[to[i]] = True # 标识不需要遍历该点了
                d[to[i]] = d[u] + 1 # u第一条边的终点的 最短路径 为 u的基础上+1
                p[to[i]] = u # u第一条边的终点的 的路径为 前一步为u
                print(u,p[to[i]],i)
            i = nex[i] # 同起点的下一条边存储处

def restore(x):
    res = []
    v = x
    while v != -1:
        res.append(v)
        v = p[v]
    res.reverse()
    for i in range(0, len(res)):
        print(res[i])
        row = (res[i]-1) // num_rows
        col = (res[i]-1) % num_cols
        for s in range(2,9):
            image1[range(10*row+2,10*row+8),10*col+s] = 128 # 绘制路线

bfs(1)
restore(num_rows*num_cols)
print(p)
# 当前节点不是终结点，查找连通节点。
# Display the image
plt.axis('off')
plt.imshow(image, cmap = cm.Greys_r, interpolation='none')
plt.figure()
plt.imshow(image1, cmap = cm.Greys_r, interpolation='none')
plt.show()