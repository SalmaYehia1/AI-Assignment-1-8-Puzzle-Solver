# AI Assignment 1: 8-Puzzle Solver Using Search Algorithms

---

## Introduction

This assignment focuses on implementing and comparing four search algorithms to solve the classic 8-puzzle problem. The objective is to reach the goal configuration by sliding tiles into the blank space. Both uninformed and informed search strategies were used to evaluate performance, memory behavior, and optimality.

Implemented search algorithms:

- Breadth-First Search (BFS)  
- Depth-First Search (DFS)  
- Iterative Deepening Depth-First Search (IDDFS)  
- A* Search  

Each method explores the state space differently and generates a path from the initial state to the goal state when a solution exists.

---

## Problem Definition

The 8-puzzle is represented as a string of 9 digits, with `'0'` representing the blank space. Tiles move by swapping with the blank, in one of four directions: up, down, left, right.  

**Key points:**

- Example puzzle state: `"123045678"`  
- Goal state: `"012345678"`  
- Each move has equal cost of 1  
- Solvability is checked using inversion count before search  
- Shared helper functions:
  - `move_blank()` – moves blank tile  
  - `get_children()` – generates valid child states  
  - `get_path()` – reconstructs the solution path  

---

## Data Structures

| Algorithm | Data Structure | Purpose |
|-----------|----------------|---------|
| BFS       | Queue (`collections.deque`) | Explore nodes level by level |
| DFS       | Stack | Explore nodes deeply first |
| IDDFS     | Stack | Depth-limited DFS with iterative depth increase |
| A*        | Priority Queue (`heapq`) | Expand nodes with lowest estimated total cost f(n) = g(n) + h(n) |

---

## Algorithms

### Breadth-First Search (BFS)
- Explores nodes by increasing depth.  
- Guarantees shortest path when all moves have equal cost.  
- Uses FIFO queue.  
- **Pros:** Always finds shortest path.  
- **Cons:** High memory usage for deep puzzles.  

### Depth-First Search (DFS)
- Explores one branch deeply before backtracking.  
- Uses stack (LIFO).  
- **Pros:** Low memory consumption.  
- **Cons:** May explore long irrelevant branches and does not guarantee optimal solution.  

### Iterative Deepening Depth-First Search (IDDFS)
- Performs depth-limited DFS with increasing depth limit.  
- Combines DFS memory efficiency and BFS optimality.  
- **Pros:** Optimal and memory-efficient.  
- **Cons:** Repeats shallow-level searches; slightly slower than BFS in practice.  

### A* Search
- Informed search using a heuristic: f(n) = g(n) + h(n)
- `g(n)` = cost from start to node n  
- `h(n)` = estimated cost to goal (Manhattan distance used)  
- Uses a priority queue to select the node with the lowest f(n)  
- **Pros:** Fast and optimal with an admissible heuristic  
- **Cons:** Higher memory usage than DFS or IDDFS  

---

## Sample Runs

The project includes multiple executions demonstrating how each algorithm solves different initial states. Output includes:

- Solution path length  
- Number of expanded nodes  
- Search depth  
- Execution time  

---

## Observations

- BFS guarantees the shortest path but uses high memory.  
- DFS consumes little memory but may return non-optimal paths.  
- IDDFS provides optimal solutions efficiently with low memory.  
- A* is fastest when a strong heuristic is used, prioritizing promising states.  

---

## Conclusion

- **BFS:** Reliable and optimal, memory-intensive.  
- **DFS:** Simple but inefficient for deep puzzles.  
- **IDDFS:** Optimal and memory-efficient; good choice for memory-limited environments.  
- **A\*:** Best trade-off between speed and optimality; most practical overall.  

BFS and IDDFS provided accurate solutions for deep puzzles, while A* offered the best performance when speed and optimality were required.

