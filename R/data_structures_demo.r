# --- R Data Structures Demonstration ---
# This program demonstrates Vectors, Matrices, Lists, and Data Frames.

# 1. Vectors (Atomic Vectors)
# Vectors are the simplest data structures in R. They hold elements of the same type.
print("--- 1. VECTORS ---")
numeric_vector <- c(10, 20, 30, 40, 50)
char_vector <- c("Apple", "Banana", "Cherry")
print("Numeric Vector:")
print(numeric_vector)
print("Character Vector:")
print(char_vector)
cat("\n")

# 2. Matrix
# A matrix is a 2-dimensional collection of elements of the same type.
print("--- 2. MATRIX ---")
# Creating a 3x3 matrix from 1:9
my_matrix <- matrix(1:9, nrow = 3, ncol = 3, byrow = TRUE)
colnames(my_matrix) <- c("Col1", "Col2", "Col3")
rownames(my_matrix) <- c("Row1", "Row2", "Row3")
print("3x3 Matrix:")
print(my_matrix)
cat("\n")

# 3. List
# A list is a generic vector that can contain different types of elements (including other lists).
print("--- 3. LIST ---")
my_list <- list(
  ID = 101,
  Name = "John Doe",
  Scores = c(85, 90, 78),
  Active = TRUE
)
print("A List containing multiple data types:")
print(my_list)
cat("\n")

# 4. Data Frame
# Data frames are tabular data structures. Each column can have a different data type.
print("--- 4. DATA FRAME ---")
my_dataframe <- data.frame(
  EmployeeID = c(1, 2, 3),
  Name = c("Alice", "Bob", "Charlie"),
  Salary = c(50000, 60000, 55000),
  StringsAsFactors = FALSE
)
print("A Data Frame (Tabular Data):")
print(my_dataframe)
cat("\n")

# --- Summary Comparison ---
print("--- DATA TYPE CHECK ---")
print(paste("Type of vector:", typeof(numeric_vector)))
print(paste("Type of matrix:", typeof(my_matrix)))
print(paste("Type of list:", typeof(my_list)))
print(paste("Type of dataframe:", typeof(my_dataframe)))
