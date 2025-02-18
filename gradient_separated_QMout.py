import sys
import matplotlib.pyplot as plt
import numpy as np
import glob
#for name in names:
names = sorted(glob.glob("*/QM.out"))
rms=np.zeros((len(names), int(sys.argv[1])+1))
geom=0
for name in names:
	fo = open(name, "r")
	lines = fo.read().splitlines()
	fo.close()
	c = 0
	grad = []
	for line in lines:
		states = int(lines[1].split()[0])
		if "Gradient Vectors" in line:
			x = int(lines[c+1].split()[0])
			y = int(lines[c+1].split()[1])
			for i in range(states):
				for j in range(x):
					u = lines[c+2+j].split()
					for k in range(y):
						grad.append(float(u[k]))
				c = c + x + 1
				grad2 = np.array(grad)
				rms[geom][i] = np.sqrt(np.mean(grad2**2))
		c = c + 1
	geom = geom + 1
count = np.arange(len(names))
for i in range(states):
	alabel="S" + str(i)
	plt.scatter(count, rms[:,i], label=alabel)
plt.title(sys.argv[1])
plt.xlabel("Number of geometry")
plt.ylabel("Gradient RMS (eV/Ang)")
plt.legend()
plt.savefig(sys.argv[1], dpi=300)
plt.show()
