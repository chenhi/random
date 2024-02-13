import math

################################################### OPTIONS ###################################################

# Can tweak the symbols
mark = '×'
empty = '0'
special = '*'

# For turning on debug messages
debug = False

################################################### CODE ###################################################


print("This is a tool for drawing circles in Minecraft (i.e. on a grid).\n\n")

print("Typically, in Minecraft we center circles on the middle of a block or on the corner, leading to the following properties. \n\nMiddle: odd diameter, integer radius like 10.0 \nCorner: even diameter, half integer radius like 10.5\n\nThis can have implications for symmetry, e.g. whether you want to put single or double doors at the center of your structure, so decide beforehand.\n\n")

# Center must be either middle or corner
# If middle, then (0, 0) corresponds to the center block
# If corner, then the center is adjacent to (0, 0) and (-1, -1)
s = input("Type 'x' to middle-center the circle, and 'c' to corner-center it: ")
corner = False
if s == 'x':
	corner = False
elif s == 'c':
	corner = True
else:
	print("Unexpected choice.  Exiting.")
	exit()
print("You have chosen to", ("CORNER" if corner else "MIDDLE") + "-center your circle!\n")

# Allow any radius
r = float(input("Input radius: "))

# Create grid
n = 2 * math.ceil(r) + 10			#Grid size, with some leeway
grid = [[empty for i in range(n)] for j in range(n)]

x, y = 0,0
# Symmetric in quadrants, so only do first quadrant
if corner:
	x, y = math.ceil(r-1), 0
else:
	x, y = math.ceil(r - 0.5), 0

while x >= 0:
	print(x,y) if debug else None
	# First, check if the circle enters the interior this box
	lower, upper = 0, 0		# Initialize
	if corner:
		lower = math.sqrt(x**2 + y**2)
		upper = math.sqrt((x+1.)**2 + (y+1)**2)
	else:
		lower = math.sqrt((x-.5)**2 + (y-.5)**2)
		upper = math.sqrt((x + .5)**2 + (y + .5)**2)
	
	if r <= lower:		# Too far, so move left and down
		x -= 1
		y -= 1
		continue
	if r >= upper:		# Too close, so move up
		y += 1
		continue
	# Otherwise, mark the grid and its reflections, and move up
	grid[x][y] = mark
	if corner:
		grid[-x-1][y], grid[x][-y-1], grid[-x-1][-y-1] = mark, mark, mark
	else:
		grid[-x][y], grid[x][-y], grid[-x][-y] = mark, mark, mark
	print(x, y,"OK") if debug else None
	y += 1

# Mark the center
if corner:
	grid[0][0], grid[0][-1], grid[-1][0], grid[-1][-1] = special, special, special, special
else:
	grid[0][0] = special


# Draw the grid
text = ""
for i in range(int(n/2), -int(n/2), -1):
	line = ""
	for j in range(-int(n/2), int(n/2)):
		line += grid[j][i]
	text += line + "\n"

print("\n" + text + "\n")


# Option to write to output

fname = "mc_circle_output.txt"
dowrite = input("Write to " + fname + "? (y/n) ")

if dowrite == "y":
	f = open(fname, "w")
	f.write(text)
	f.close()
	print("\nOutput written to", fname + ".")
else:
	print("\nNo file written.")

