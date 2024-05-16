#2021073863 박승우

import numpy as np

def solve_linear_equation(n, A, B):
    if not all(len(row) == n for row in A) or len(A) != n:  #to check whether there's invalid error
        print("Error: Invalid matrix A")  #if matrix A is invalid, print error message and return nothing
        return None

    if len(B) != n or any(len(row) != 1 for row in B):  #to check whether there's invalid error
        print("Error: Invalid matrix B")  # if matrix B is invalid, print error message and return nothing
        return None

    # Convert input lists to NumPy arrays
    A = np.array(A)
    B = np.array(B).reshape(-1, 1)

    # Solve the equation
    try:
        x = np.linalg.solve(A, B)   #solve matrix equation
        return x  # Return the solution
    except np.linalg.LinAlgError:
        print("Error: Singular matrix A")  # if matrix A is singular, print error message and return nothing
        return None

n = int(input("Enter the size of the square matrix (n): "))     #receive input value of the size of matrix from the user

print(f"Enter the elements of matrix A ({n}x{n} size, each row on a new line, separated by spaces):") #receive elements of martix A
A = []
for _ in range(n):      #to split by space. seperated numbers get in to list named 'row'
    row = list(map(float, input().split()))
    A.append(row)

print(f"Enter the elements of matrix B ({n}x1 size, values separated by spaces):")  #receive elements of martix B
B_values = list(map(float, input().split()))
B = [[value] for value in B_values]

# Solve the linear equation
solution = solve_linear_equation(n, A, B)
if solution is not None:
    print("Solution:")
    print(solution)  #if it exist, print solution
else:
    print("Error")  # if solution dosen't exist, print error message