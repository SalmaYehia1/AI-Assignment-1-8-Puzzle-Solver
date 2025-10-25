#!/usr/bin/env python
# coding: utf-8

# # **Assignmnet 1 overview**
# 
# The 8-puzzle is a sliding puzzle with 8 numbered tiles and one blank (0), where you can move the blank up, down, left, or right to swap positions.
# • The goal is to find a sequence of moves that transforms a given initial board into the goal state 0 1 2 3 4 5 6 7 8.
# • Each move has a cost of 1, so the total solution cost equals the number of moves taken from start to goal.

# In[27]:


import numpy as np
from queue import PriorityQueue
import time
GOAL_STATE_STR = "012345678"


# In[28]:


def to_str(num):
  if len(str(num))<9:
    return "0"+str(num)
  else :
    return str(num)


# # **BFS**

# In[29]:


from collections import deque


# In[30]:


#output
# path_to_goal: [‘Up’, ‘Left’, ‘Left’]
# cost_of_path: 3
# nodes_expanded: 10
# fringe_size: 11
# max_fringe_size: 12 Fringe size = the number of nodes currently waiting to be explored.
# search_depth: 3
# max_search_depth: 4
# running_time: 0.00188088
# max_ram_usage: 0.07812500


# In[31]:


# GOAL=012345678
GOAL_STR="012345678"


# In[32]:


def bfs(state):
  frontier =deque([state])
  explored=set()
  parent = {state: None}    #to track path to goal
  nodes_expanded = 0
  while frontier:
    state=frontier.popleft()
    explored.add(state)
    nodes_expanded += 1

    if state == GOAL_STR:
      path = get_path(parent, state)
      cost = len(path) - 1
      return path, cost, nodes_expanded

    children=get_children(state)
    for child in children:
      if child not in explored and child not in frontier:
        frontier.append(child)
        parent[child] = state

  return "GOAL NOT REACHED", None, nodes_expanded


# In[33]:


def get_path(parent,state):
  path=[]
  while parent[state] is not None:
    path.append(parent[state])
    state=parent[state]
  path.reverse()
  return path


# 

# In[34]:


def move_blank(state, direction):
    z = state.index('0')

    if direction == 1: #up
        if z < 3: return None
        target = z - 3
    elif direction == 2: #down
        if z > 5: return None
        target = z + 3
    elif direction == 3: #left
        if z % 3 == 0: return None
        target = z - 1
    elif direction == 4: #right
        if z % 3 == 2: return None
        target = z + 1
    else:
        return None


    s = list(state) #to be indiced
    s[z], s[target] = s[target], s[z] #swapping the blank
    return ''.join(s)


# In[35]:


def get_children(state): #all possible moves
  children=[]
  for i in range(1,5):
    child=move_blank(state,i)

    if child is not None:
      children.append(child)
  return children




# In[36]:


print("Example 1")



path1, depth1, nodes1 = bfs("123045678")
print(get_children("123045678"))
print("Path:", " -> ".join(path1))
print("Search depth:", depth1)
print("Nodes expanded:", nodes1)



print("Example 2")

path2, depth2, nodes2 = bfs("124035876")
print( get_children("124035876"))
print("Path:", " -> ".join(path2))
print("Search depth:", depth2)
print("Nodes expanded:", nodes2)

print("Example 2")
path2, depth2, nodes2 = bfs("124035876")
print( get_children("124035876"))
print("Path:", " -> ".join(path2))
print("Search depth:", depth2)
print("Nodes expanded:", nodes2)




# In[37]:


# import time

# start_time = time.time()

# path, cost = bfs("124035876")
# print("Path to goal:", " -> ".join(path))
# print("Cost of path:", cost)

# end_time = time.time()

# total_time = end_time - start_time

# print("Time taken for BFS search:", total_time, "seconds")


# #DFS

# Store states as integers (123045678)
# 
# Convert to string inside get_children() to manipulate tiles
# 
# Follow REMOVE → CHECK → EXPAND order
# 
# Use LIFO stack for DFS
# 
# Expand children in this exact order: ['Up', 'Down', 'Left', 'Right']
# 
# Track nodes_expanded as the number of visited nodes
# 
# Track parent + move_taken to reconstruct path
# 
# Stop when goal reached

# In[38]:


def dfs(state):
  frontier = deque([state])
  explored = set()
  parent = {state: None}

  while frontier:
    state = frontier.pop()
    explored.add(state)

    if state == GOAL_STR:
      path = get_path(parent, state)
      cost = len(path)-1
      return path, cost

    children = get_children(state)
    for child in children:
      if child not in explored and child not in frontier:
        frontier.append(child)     # Push to stack
        parent[child] = state

  return "GOAL NOT REACHED"


# In[39]:


# print(dfs("123045678"))
# path, cost = dfs("123045678")

# print("Path to goal:", " -> ".join(path))
# print("Cost of path:", cost)


# # **A***

# In[40]:


#heuristic skip 0


# In[41]:


goal_state_positions = {
    '0': (0, 0),
    '1': (0, 1),
    '2': (0, 2),
    '3': (1, 0),
    '4': (1, 1),
    '5': (1, 2),
    '6': (2, 0),
    '7': (2, 1),
    '8': (2, 2)
}


# In[42]:


import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []             # list of (priority, state)
        self.entry_finder = {}         # maps state -> current priority

    def insert(self, priority, state):
        heapq.heappush(self.elements, (priority, state))
        self.entry_finder[state] = priority

    def deletemin(self):
        while self.elements:
            priority, state = heapq.heappop(self.elements)
            if self.entry_finder.get(state) == priority:  # skip outdated entries
                del self.entry_finder[state]
                return priority, state
        raise KeyError("pop from empty priority queue")

    def decreaseKey(self, state, new_priority):
        """Reinsert state with a lower priority."""
        if state in self.entry_finder and new_priority < self.entry_finder[state]:
            self.insert(new_priority, state)

    def empty(self):
        return not self.entry_finder


# In[43]:


def calcIndex(index):
  return index/3,index%3


# In[44]:


def heuristic_euclidean(state):
  cost = 0
  for i in range (9):
    if state[i]!='0':
      x,y=calcIndex(i)
      goalx,goaly=goal_state_positions[state[i]]
      cost+=np.sqrt((x-goalx)**2+(y-goaly)**2)
  return cost


# In[45]:


def heuristic_manhattan(state):
  cost = 0
  for i in range (9):
    if state[i]!='0':
      x,y=calcIndex(i)
      goalx,goaly=goal_state_positions[state[i]]
      cost+=abs(x-goalx)+abs(y-goaly)
  return cost


# In[46]:


def A_star_manhattan(initial_state):
    frontier = PriorityQueue()
    frontier.insert(0, initial_state)
    explored = set()
    parent = {to_str(initial_state): None}   # to reconstruct path later
    g_cost = {to_str(initial_state): 0}
    nodes_expanded = 0

    while not frontier.empty():
        priority, state = frontier.deletemin()
        state_str = to_str(state)
        nodes_expanded += 1

        if state_str == GOAL_STATE_STR:
            path = get_path(parent, state_str)
            return {
                "path": path,
                "cost": len(path) - 1,
                "nodes_expanded": nodes_expanded
            }

        explored.add(state_str)

        for neighbor in get_children(state):
            neighbor_str = to_str(neighbor)
            new_cost = g_cost[state_str] + 1  # step cost = 1

            if neighbor_str not in g_cost or new_cost < g_cost[neighbor_str]:
                g_cost[neighbor_str] = new_cost
                total_cost = new_cost + heuristic_manhattan(neighbor)
                parent[neighbor_str] = state_str
                frontier.insert(total_cost, neighbor)

    return {
        "path": None,
        "cost": None,
        "nodes_expanded": nodes_expanded,
        "message": "Goal not reached"
    }


# In[47]:


def A_star_euclidean(initial_state):
    frontier = PriorityQueue()
    frontier.insert(0, initial_state)
    explored = set()
    parent = {to_str(initial_state): None}   # to reconstruct path later
    g_cost = {to_str(initial_state): 0}
    nodes_expanded = 0

    while not frontier.empty():
        priority, state = frontier.deletemin()
        state_str = to_str(state)

        # Skip already explored states
        if state_str in explored:
            continue

        explored.add(state_str)
        nodes_expanded += 1

        # Check if goal reached
        if state_str == GOAL_STATE_STR:
            path = get_path(parent, state_str)
            return {
                "path": path,
                "cost": len(path) - 1,
                "nodes_expanded": nodes_expanded
            }

        # Explore neighbors
        for neighbor in get_children(state):
            neighbor_str = to_str(neighbor)
            new_cost = g_cost[state_str] + 1  # uniform move cost

            # If not visited or found a cheaper path
            if neighbor_str not in g_cost or new_cost < g_cost[neighbor_str]:
                g_cost[neighbor_str] = new_cost
                total_cost = new_cost + heuristic_euclidean(neighbor)
                parent[neighbor_str] = state_str
                frontier.insert(total_cost, neighbor)

    # Goal not found
    return {
        "path": None,
        "cost": None,
        "nodes_expanded": nodes_expanded,
        "message": "Goal not reached"
    }


# In[48]:


initial_state = "867254301"

start_time = time.time()
result = A_star_euclidean(initial_state)
end_time = time.time()

print("\n=== A* Euclidean Test ===")
print(f"Initial state: {initial_state}")
print(f"Goal state:    {GOAL_STATE_STR}")
print(f"Path cost:     {result['cost']}")
print(f"Nodes expanded:{result['nodes_expanded']}")
print(f"Time taken:    {end_time - start_time:.4f} seconds")
print("Solution path:")
if result["path"]:
    print("Solution path:")
    for state in result["path"]:
        print(state)   # now prints as "125340678", etc.
else:
    print(result.get("message", "Goal not reached"))


start_time = time.time()
result = A_star_manhattan(initial_state)
end_time = time.time()

print("\n=== A* Manhattan Test ===")
print(f"Initial state: {initial_state}")
print(f"Goal state:    {GOAL_STATE_STR}")
print(f"Path cost:     {result['cost']}")
print(f"Nodes expanded:{result['nodes_expanded']}")
print(f"Time taken:    {end_time - start_time:.4f} seconds")
print("Solution path:")
if result["path"]:
    print("Solution path:")
    for state in result["path"]:
        print(state)   # now prints as "125340678", etc.
else:
    print(result.get("message", "Goal not reached"))


# In[49]:


initial_state="867254301"

# Assuming both heuristics are implemented
start_time = time.time()
res_euclid = A_star_euclidean(initial_state)
end_time = time.time()
print(f"Euclidean: cost={res_euclid['cost']}, time={end_time-start_time:.3f}s, nodes={res_euclid['nodes_expanded']}")

start_time = time.time()
res_manhattan = A_star_manhattan(initial_state)
end_time = time.time()
print(f"Manhattan: cost={res_manhattan['cost']}, time={end_time-start_time:.3f}s, nodes={res_manhattan['nodes_expanded']}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# #Iterativs DFS

# In[50]:


def is_solvable(state_str):
    # The '0' is the blank tile
    tiles = [int(t) for t in state_str if t != '0']
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0 # Returns True if inversions is even


# In[51]:


from collections import deque

def dfs_limited(state, limit, parent):
    stack = [(state, 0)]   # (node, depth)
    explored = set()

    while stack:
        state, depth = stack.pop()
        explored.add(state)

        # if state == GOAL_STR:
        #     return get_path(parent, state), len(get_path(parent, state))
        # In dfs_limited:
        if state == GOAL_STR:
           final_path = get_path(parent, state)
           cost = len(final_path) - 1
           return final_path, depth
        if depth < limit:
            children = get_children(state)
            for child in reversed(children):  # DFS order
                if child not in explored:
                    parent[child] = state
                    stack.append((child, depth + 1))

    return None  # Goal not found at this limit


def iddfs(state, max_depth=30):
    if not is_solvable(state):
        return "GOAL UNREACHABLE (Unsolvable Puzzle Parity)", None
    for limit in range(max_depth + 1):
        parent = {state: None}
        print(f" Searching at depth limit {limit}...")
        result = dfs_limited(state, limit, parent)
        if result is not None:
            print(f" Goal found at depth {limit}")
            return result

    return "GOAL NOT REACHED", None


# In[52]:


print(iddfs("123540678", max_depth=10))


# In[53]:


print(iddfs("120345678", max_depth=5))


# In[54]:


print(iddfs("210345678", max_depth=10))
print(iddfs("125340678", max_depth=15))
print(iddfs("123540678", max_depth=15))
print(iddfs("132405678", max_depth=15))

print(iddfs("724506831", max_depth=31))
print(iddfs("867254301", max_depth=31))
print(iddfs("281043765", max_depth=31))

