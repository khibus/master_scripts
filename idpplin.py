from ase.build import molecule
from ase.io import read
from ase.neb import NEB
from ase.calculators.emt import EMT
from ase.optimize.fire import FIRE as QuasiNewton
import sys

init=sys.argv[1]
fin=sys.argv[2]
steps=int(sys.argv[3])
steps2=int(sys.argv[4])
# Optimise molecule.
initial = read(init)
#initial.calc = EMT()
#relax = QuasiNewton(initial)
#relax.run(fmax=0.05)
# Create final state.
# final = initial.copy()
# final.positions[2:5] = initial.positions[[3, 4, 2]]
final = read(fin)
# Generate blank images.
images = [initial]
init=[[0 for x in range(3)] for y in range(len(initial)*(steps+steps2))]
for i in range(steps):
    images.append(initial.copy())

for image in images:
    image.calc = EMT()

images.append(final)
# Run IDPP interpolation.
neb = NEB(images)
neb.interpolate()
name = initial.get_chemical_symbols()
coord2 = neb.get_positions()
coord = coord2.tolist()
l=0
for j in range(len(initial)):
	init[j][0]=coord[j][0]-(steps2/2)*(coord[len(initial)+j][0]-coord[j][0])
	init[j][1]=coord[j][1]-(steps2/2)*(coord[len(initial)+j][1]-coord[j][1])
	init[j][2]=coord[j][2]-(steps2/2)*(coord[len(initial)+j][2]-coord[j][2])
#	if abs(init[j][0]) < 0.1:
#		init[j][0] = 0
#	if abs(init[j][1]) < 0.1:
#		init[j][1] = 0
#	if abs(init[j][2]) < 0.1:
#		init[j][2] = 0
for jaj in range(steps+steps2-1):
	for lal in range(len(initial)):
		init[(jaj+1)*len(initial)+lal][0]=init[lal][0]+(jaj+1)*(coord[len(initial)+lal][0]-coord[lal][0])
		init[(jaj+1)*len(initial)+lal][1]=init[lal][1]+(jaj+1)*(coord[len(initial)+lal][1]-coord[lal][1])
		init[(jaj+1)*len(initial)+lal][2]=init[lal][2]+(jaj+1)*(coord[len(initial)+lal][2]-coord[lal][2])
#		if abs(init[(jaj+1)*len(initial)+lal][0]) < 0.1:
#			init[(jaj+1)*len(initial)+lal][0] = 0
#		if abs(init[(jaj+1)*len(initial)+lal][1]) < 0.1:
#			init[(jaj+1)*len(initial)+lal][1] =0 
#		if abs(init[(jaj+1)*len(initial)+lal][2]) < 0.1:
#			init[(jaj+1)*len(initial)+lal][2] = 0
for k in range(steps+steps2):
	init.insert(l, [len(initial), "", "", ""])
	l = l + 1
	init.insert(l, ["", "", "", ""])
	l = l + 1
	for j in range(len(initial)):
#	print(coord[i][0] + "  " + coord[i][1] + "  " + coord[i][2])
		init[l].insert(0, name[j])
		l = l + 1
# Run NEB calculation.
# qn = QuasiNewton(neb, trajectory='ethane_idpp.traj', logfile='ethane_idpp.log')
# qn.run(fmax=0.05)
with open(sys.argv[5], 'w') as File2:
        for sublist in init:
                line = "{} {} {} {}\n".format(sublist[0], sublist[1], sublist[2], sublist[3])
                File2.write(line)

