# Load necessary libraries (commented out)
# library(dplyr)
# library(ggplot2)
# library(tidyr)
# library(shiny)
# library(caret)

# Create a vector X with numeric values
X <- c(007, 4, 21, 007, 89, 2)
cat("using c function to create a vector X:\n", X, "\n")
# Output: using c function to create a vector X:
#  7 4 21 7 89 2

# Create a factor Y without specifying levels (R assigns levels alphabetically)
Y <- factor(c("single", "married", "single", "married", "single", "married"))
print(Y)

# Create a factor Z with specified levels order
Z <- factor(c("single", "married", "single", "married", "single", "married"), levels = c("single", "married"))
print(Z)
# Output for Y and Z:
# [1] single  married single  married single  married
# Levels: married single
# [1] single  married single  married single  married
# Levels: single married

# Create a data frame R with columns SN, Age, and Name
R <- data.frame(SN = c(1, 2), Age = c(49, 18), Name = c("John", "Smith"))
print(R)
print(typeof(R))
print(class(R))  # Note: Changed 'r' to 'R' assuming it's a typo

LIST<- list("a"=2.5,"b"=TRUE,"c"=c(1:3))
print(LIST)