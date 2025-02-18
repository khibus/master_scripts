import sys
import matplotlib.pyplot as plt
import numpy as np
import glob
#for name in names:
states = int(sys.argv[1])
names = sorted(glob.glob("*/ORCA.out"))
x=np.zeros((len(names), states+1))
geom=0
for name in names:
	fo = open(name, "r")
	lines = fo.read().splitlines()
	fo.close()
	c = 0
	grad = []
	for line in lines:
		if "Total Energy       :" in line:
			x[geom][0] = float(lines[c].split()[5])
		if "ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS" in line:
			for i in range(states):
				x[geom][i+1] = x[geom][0] + float(lines[c+5+i].split()[3])
		c = c + 1
	geom = geom + 1
count = np.arange(len(names))
x = x - np.min(x)
for i in range(states+1):
	alabel = "S" + str(i)
	plt.plot(count, x[:,i], label=alabel)
plt.legend()
plt.xlabel("Number of geometry")
plt.ylabel("Energy (eV)")
plt.show()
