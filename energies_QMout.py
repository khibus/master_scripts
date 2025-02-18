import sys
import matplotlib.pyplot as plt
import numpy as np
import glob
#for name in names:
names = sorted(glob.glob("*/QM.out"))
geom=0
for name in names:
	fo = open(name, "r")
	lines = fo.read().splitlines()
	fo.close()
	if geom == 0:
		states = int(lines[1].split()[0])
		energies=np.zeros((len(names), states))
	for i in range(states):
		energies[geom][i] = float(lines[i+2].split()[2*i])
	geom = geom + 1
energies = (energies - np.min(energies))*27.212
count = np.arange(len(names))
for i in range(states):
	alabel="S" + str(i)
	plt.scatter(count, energies[:,i], label=alabel)
plt.title(sys.argv[1])
plt.xlabel("Number of geometry")
plt.ylabel("Energy (eV)")
plt.legend()
plt.savefig(sys.argv[1], dpi=300)
plt.show()
