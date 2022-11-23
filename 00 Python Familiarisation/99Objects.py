# Simplest 99 objects:

#Set variables to known initialisation states
plural = "annoyed bears"
singular = "annoyed bear"
iterations = 99

# Consider adding some checking here to validate that iterations > 1
# The code below assumes that you will have at least one iteration, < 0 goes infinite!
try:
    iterations = int(input("Please enter a number of iterations: "))
except (ValueError, TypeError):
    print("Error - defaulting to 99")
    iterations = 99

# You may wish to add some filtering here, we wouldn't want people to be inappropriate
singular = input("Please enter the singular version of the object: ")
plural = input("Please enter the plural version of the object");

# Simple implementation - count down in steps of 1 repeating song lyrics
# Assumes 2+ iterations
for i in range(iterations, 1,-1):
    print(f"{i} {plural} on the wall")
    print(f"{i} {plural}, you take one down, pass it around")
    if (i > 2):
        print(f"{i-1} {plural} on the wall")
    else:
        print(f"{i-1} {singular} on the wall")

print(f"1 {singular} on the wall")
print(f"1 {singular} on the wall, you take it down, pass it around")
print(f"No more {plural} on the wall")

