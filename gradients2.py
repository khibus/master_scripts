import numpy as np
import sys
import glob

filenames = sorted(glob.glob("*/output.lis"))
a = 0
for file in filenames:
	input = np.loadtxt(file)
	if np.max(input[:,6]) - np.min(input[:,6]) > float(sys.argv[1]):
		print("Energy changes more than " + sys.argv[1] + " eV in " + file)
		a = a + 1

print("This is " + str(a) + " calculations out of " + str(len(filenames)) + " trajectories" )
