import numpy as np
import sys
import glob

filenames = sorted(glob.glob("*/output.lis"))
a = 0
for file in filenames:
	input = np.loadtxt(file)
	for i in range(len(input)-1):
		if input[i+1][6] - input[i][6] > float(sys.argv[1]):
			print("Energy changes more than " + sys.argv[1] + " eV at " + str(input[i+1][1]) + " fs in " + file)
			a = a + 1
print("This is " + str(a) + " calculations out of " + str(len(filenames)) + " trajectories" )
