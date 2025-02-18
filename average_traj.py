#!/usr/bin/python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import glob

filenames = glob.glob("*/output_omega.txt")
for file in filenames[0]:
        data = np.zeros((len(file), int(sys.argv[1])))
for file in filenames:
        input = np.loadtxt(file)
        data = (data + input)
data = data / len(filenames)
print("The average of {} trajectories was generated into average_traj.txt".format(len(filenames)))
np.savetxt("average_traj.txt", data)

