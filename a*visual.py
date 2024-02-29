import tkinter as tk
import heapq
import time
import random

# Grid settings
ROW, COL = 15, 15
CELL_SIZE = 40

# Directions for adjacent cells
directions = [(0, -1), (0, 1), (-1, 0), (1, 0),
              (-1, -1), (-1, 1), (1, -1), (1, 1)]

class Cell:
    def __init__(self, parent_i, parent_j):
        self.parent_i = parent_i
        self.parent_j = parent_j
        self.f = self.g = self.h = 0

def generate_random_grid(ROW, COL):
    # Generate a random grid of 0s and 1s, where 1 indicates walkable and 0 indicates blocked
    grid = [[random.randint(0, 1) for _ in range(ROW)] for _ in range(COL)]
    
    # Ensure the start and end locations are walkable by setting them to 1
    src = (random.randint(0, ROW-1), random.randint(0, COL-1))
    dest = (random.randint(0, ROW-1), random.randint(0, COL-1))
    
    # To avoid having the start and end positions being the same
    while dest == src:
        end = (random.randint(0, ROW-1), random.randint(0, COL-1))
    
    grid[src[0]][src[1]] = 1  # Ensure start is walkable
    grid[dest[0]][dest[1]] = 1  # Ensure end is walkable

    return grid, src, dest

# Function to check if position is valid 
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if destination is reached
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate h value, estimated cost from cell to destination. This is the heuristic part of the cost function, so it is like a guess
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Return the path found
def trace_path(cell_details, dest):
    print("\nThe path is ")
    row, col = dest
    path = []
    
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col
        
    path.append((row, col))
    return path[::-1]

# Perform A* algorithm search
def a_star_search(grid, src, dest, canvas, root):
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return
    
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return
    
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return
    
    closed_list = [[False] * COL for _ in range(ROW)]
    cell_details = [[Cell(-1, -1) for _ in range(COL)] for _ in range(ROW)]
    
    i, j = src
    cell_details[i][j].f = cell_details[i][j].g = cell_details[i][j].h = 0
    
    open_list = []
    heapq.heappush(open_list, (0, i, j))
    
    while open_list:
        current = heapq.heappop(open_list)
        i, j = current[1], current[2]
        closed_list[i][j] = True
        
        for direction in directions:
            row = i + direction[0]
            col = j + direction[1]
            if is_valid(row, col):
                if is_destination(row, col, dest):
                    cell_details[row][col].parent_i = i
                    cell_details[row][col].parent_j = j
                    print("The destination cell is found")
                    return trace_path(cell_details, dest)
                
                elif not closed_list[row][col] and is_unblocked(grid, row, col):
                    g_new = cell_details[i][j].g + 1.414 if direction in directions[4:] else cell_details[i][j].g + 1
                    h_new = calculate_h_value(row, col, dest)
                    f_new = g_new + h_new
                    
                    if cell_details[row][col].f == 0 or cell_details[row][col].f > f_new:
                        heapq.heappush(open_list, (f_new, row, col))
                        cell_details[row][col].f = f_new
                        cell_details[row][col].g = g_new
                        cell_details[row][col].h = h_new
                        cell_details[row][col].parent_i = i
                        cell_details[row][col].parent_j = j
                        
        draw_grid(canvas, grid, [], src, dest, open_list)
        root.update()
        time.sleep(0.1)

# Draw Grid
def draw_grid(canvas, grid, path, src, dest, open_list=[]):
    for i in range(ROW):
        for j in range(COL):
            color = "white"
            if grid[i][j] == 0:
                color = "black"
            elif (i, j) == src:
                color = "blue"
            elif (i, j) == dest:
                color = "red"
            elif (i, j) in path:
                color = "green"
            elif (i, j) in [(cell[1], cell[2]) for cell in open_list]:
                color = "orange"
            
            canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE, (j+1) * CELL_SIZE, (i+1) * CELL_SIZE, fill=color, outline="gray")


def close_current_window(root):
    # Assuming 'current_window' is a reference to the Tkinter window you want to close
    root.destroy()


def main():
    root = tk.Tk()
    root.title("A* Path Finding")
    
    canvas = tk.Canvas(root, width=COL*CELL_SIZE, height=ROW*CELL_SIZE)
    canvas.pack()


    grid, src, dest = generate_random_grid(ROW, COL)
    
    path = a_star_search(grid, src, dest, canvas, root)
    
    start_button = tk.Button(root, text="Replay", command=lambda: [a_star_search(grid, src, dest, canvas, root), draw_grid(canvas, grid, path, src, dest)])
    start_button.pack()

    reset_grid_button = tk.Button(root, text="Generate New Maze", command=lambda: [close_current_window(root), generate_random_grid(ROW, COL), main(), draw_grid(canvas, grid, path, src, dest)])
    reset_grid_button.pack()

    if path:
        draw_grid(canvas, grid, path, src, dest)
        root.update()

    root.mainloop()


if __name__ == "__main__":
    main()
