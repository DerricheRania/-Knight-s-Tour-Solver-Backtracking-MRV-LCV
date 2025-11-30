# 🐴 Knight’s Tour Solver — Backtracking + MRV + LCV

This project implements a complete solver for the **Knight’s Tour Problem** on an 8×8 chessboard using **Backtracking** and optimized with powerful constraint-solving heuristics: **MRV (Minimum Remaining Values)** and **LCV (Least Constraining Value)**.
The Knight’s Tour is a classic problem where a knight must visit **all 64 squares exactly once** without revisiting any square.

This repository contains:
* A base backtracking algorithm
* An optimized solver using MRV and LCV
* A clean class-based implementation
* A modular successor function for legal knight moves

## 📌 About the Knight’s Tour Problem

The knight moves in an “L” shape:
* 2 squares in one direction and 1 square perpendicular
* 8 possible moves max from any position

The challenge:
➡️ Find a sequence of moves such that the knight visits **every square exactly once**.
This is a **Constraint Satisfaction Problem (CSP)** with:
* Variables → each step in the tour
* Domain → unvisited squares
* Constraints → valid knight moves, no repeated squares
  
## 🧠 Features & Algorithms

### 🔹 **1. Successor Function**

The solver uses a dedicated function to generate all legal knight moves from a given position, filtering out:

* moves outside the board
* already visited squares
This keeps the search space clean and consistent.

### 🔹 **2. Simple Backtracking**

This is the brute-force approach:

* Start from an initial square
* Recursively explore all possible knight moves
* Backtrack whenever the knight reaches a dead end
Correct but **very slow**, since the search tree is huge.

### 🔹 **3. MRV – Minimum Remaining Values**

MRV is a heuristic that selects the next move with the **fewest onward moves**.
Benefits:

* Reduces branching
* Avoids early dead-ends
* Implements Warnsdorff’s heuristic, proven to work efficiently for Knight’s Tour

### 🔹 **4. LCV – Least Constraining Value**

LCV orders the valid moves so that the knight picks the move that **constrains future moves the least**.
This means:

* It explores moves that leave the most freedom later
* Improves overall performance and reduces failed branches

### 🔹 **5. Backtracking With MRV + LCV**

The most powerful solver in this project.
Pipeline:

1. Generate all successors
2. Apply **MRV** to restrict the options
3. Apply **LCV** to sort them
4. Explore recursively
This version dramatically improves the efficiency and makes the Knight’s Tour solvable in a reasonable time.

## 🧩 Code Architecture

```
KnightsTour/
│
├── successor_fct()          # Generates legal knight moves
├── backtracking()           # Simple backtracking solver
├── MRV()                    # Minimum Remaining Values heuristic
├── LCV()                    # Least Constraining Value heuristic
└── backtracking_with_heuristics()  # Combined MRV + LCV solver
```

All logic is encapsulated inside a clean, reusable Python class.

## 🚀 How It Works

1. Choose a starting square (e.g., (0, 0))
2. Add it to the assignment list
3. Run:
   ```python
   kt.backtracking_with_heuristics([(0, 0)])
   ```
4. The solver returns a list of **64 ordered moves**, representing a complete Knight’s Tour.

## 📝 Example of Knight Moves Definition

```python
self.moves = [
    (1, 2),     # 2 up, 1 right
    (-1, 2),    # 2 up, 1 left
    (1, -2),    # 2 down, 1 right
    (-1, -2),   # 2 down, 1 left
    (-2, 1),    # 2 left, 1 up
    (-2, -1),   # 2 left, 1 down
    (2, 1),     # 2 right, 1 up
    (2, -1)     # 2 right, 1 down
]
```
These are the standard 8 knight moves.

## 🎯 Goals of the Project

* Learn and implement a classical CSP
* Demonstrate the power of MRV + LCV heuristics
* Build a reusable solver with clean architecture
* Provide a basis for visualization using Pygame (optional extension)
