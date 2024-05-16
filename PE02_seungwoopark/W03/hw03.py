#2021073863 박승우
import numpy as np

N = int(input('Enter N, A, X, Y ='))  # receive number of fields from user
A = list(map(int, input().split()))  # split by space. And make a list students per field
X, Y = map(int, input().split())

total_teachers = 0

# Calculate minimum number of teachers required
A2 = np.array(A)  # Convert list of students per field into a numpy array
total_teachers_numpy = np.zeros(N)  # Initialize an array to store the total teachers required for each field

# Calculate additional teachers needed if students exceed the maximum per teacher
total_teachers_numpy += np.maximum(0, (A2 - X) // Y)
# Add one teacher if there are remaining students after dividing by Y
total_teachers_numpy += np.where((A2 - X) % Y != 0, 1, 0)
# Add one teacher for the initial X students
total_teachers_numpy += 1

# Sum up the total teachers required across all fields
print("Total teachers :", int(np.sum(total_teachers_numpy)))
