#!/bin/python3
import ase.io
import ase
import numpy as np
import schnetpack as spk
from ase.units import Bohr
import os
import sys
import glob
#import sharc
import schnarc
#print(help(schnarc))
from schnarc.utils import read_QMout
#iterating over all files
nfiles = 200
nfiles2 = 101
#define number of states
ntriplets = 0
nsinglets = 5
nstates = nsinglets + 3 * ntriplets

#define number of atoms
natoms = 10

def rms_calc(name):
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
			rms = np.sqrt(np.mean(grad2**2))
		c = c + 1
	return rms

#read geometries --> these are in Angström!
files_qmout = sorted(glob.glob("a*/*/*/QM.out"))
files_xyz = sorted(glob.glob("a*/*/*/input.xyz"))
print(files_xyz[0])
if len(files_xyz) != len(files_qmout):
	print("Warning! " + str(len(files_xyz) - len(files_qmout)) + " calculation did not finish!")
geoms = []
atoms= []
atoms2= []
for i in range(len(files_xyz)):
	geoms.append(ase.io.read(files_xyz[i]))
#transform geoms into a.u.
	if "linear" in files_xyz[i]:
		atoms.append(ase.atoms.Atoms(geoms[i].get_atomic_numbers(),geoms[i].get_positions()/Bohr))
		atoms2.append(ase.atoms.Atoms(geoms[i].get_atomic_numbers(),geoms[i].get_positions()/Bohr))
	else:
		atoms.append(ase.atoms.Atoms(geoms[i].get_atomic_numbers(),geoms[i].get_positions()))
		atoms2.append(ase.atoms.Atoms(geoms[i].get_atomic_numbers(),geoms[i].get_positions()))
print("Number of geometries: %d"%(len(geoms)))

#data dictionary for updating the data base
data = {}

#we don't have spin-orbit couplings
socs=False
n = 0
exc = 0
count = len(files_qmout) - 1
rms = rms_calc(files_qmout[0])
files_qmout.reverse()
for filename in files_qmout:
	if "linear" in filename:
		rms_old = rms
		rms = rms_calc(filename)
		if rms - rms_old < 0.002:
			data[n]={}
			data[n]=read_QMout(filename,natoms,socs,nsinglets,ntriplets,0.5)
			n = n + 1
		else:
			print("Gradient diff too high between at " + filename + ", therefore it will be excluded from the dataset!")
			exc = exc + 1
			atoms.pop(count)
	elif "wigner" in filename:
		rms2 = rms_calc(filename)
		if rms2 < 0.2:
			data[n]={}
			data[n]=read_QMout(filename,natoms,socs,nsinglets,ntriplets,0.5)
			n = n + 1
		else:
			print("Gradient too high at " + filename + ", therefore it will be excluded from the dataset!")
			exc = exc + 1
			atoms.pop(count)
	count = count - 1
print(len(data), "number of data points found.")
print(str(exc), "points were excluded!")
phasesnotfound = []
for i in range(len(data)):
	if "phases" in data[i]:
		pass
	else:
		print(files_qmout[i]," requires interpolation to get phases.")
		phasesnotfound.append(i)
print(len(phasesnotfound), "data points do not contain reliable phases.")

from schnarc.utils import correct_phases

corrected_data = correct_phases(data,nsinglets,ntriplets)
for n in range(len(corrected_data)):
	corrected_data[n]['forces']=data[n].pop('gradients')
	corrected_data[n]['has_forces']=data[n].pop('has_gradients')
print(len(corrected_data), "points could be corected from the original data.")

# get relevant geometries

corrected_atoms = []
for i in range(len(atoms)):
	if "phases" not in data[i]:
		pass
	else:
		corrected_atoms.append(atoms[i])
print(len(corrected_atoms), "points were put in the dataset!")


#from schnarc.utils import read_traj

#traj_data = {}
#traj_geoms = []

#we iterate over all files in 10 different trajectory folders,
#hence ntraj (number of trajectories) = 10
#ntraj=1000

#idata = -1
#for itraj in range((ntraj)):
    
#    path = "/home/buzsaki/schnarc_test/train2/traj/Singlet_3/TRAJ_%05d/" %(itraj+1)
#    if os.path.isdir(path):
#    	datatraj_,atomstraj_ = read_traj(path,nsinglets,ntriplets,0.5)
#    	#put data into one large dictionary
#    	for i in range(len(datatraj_)):
#                idata+=1
#                traj_data[idata] = datatraj_[i]
#                traj_data[idata]['forces']=traj_data[idata].pop('gradients')
#                traj_data[idata]['has_forces']=traj_data[idata].pop('has_gradients')
#                traj_geoms.append(ase.atoms.Atoms(atomstraj_[i].get_atomic_numbers(),atomstraj_[i].get_positions()/Bohr))
#print(len(traj_data), "number of trajectory data points found.")

from ase.db import connect

# we will only write the necessary properties into the data file

keys = ["energy", "forces", "dipoles", "has_forces", "nacs"]
newdata = {}
for i in range(len(corrected_data)):
	newdata[i]={}
	for key in keys:
		if key in corrected_data[i]:
			newdata[i][key] = corrected_data[i][key]
# define the name of the data set
#delete any DB that might be here
os.system("rm -f ./pyrazine_cas.db")
dbname = "./pyrazine_cas.db"
db = connect(dbname)
for i in range(len(corrected_data)):
    #the data are in the "data" dicitonary and the atoms saved as atoms objects in the "atoms"-array
	db.write(corrected_atoms[i],data=newdata[i])
	if i % 50 == 49:
		print(str(i+1) + "th point is written!")

#newtraj_data = {}
#for i in range(len(traj_data)):
#    newtraj_data[i]={}
#    for key in keys:
#        if key in traj_data[i]:
#            newtraj_data[i][key] = traj_data[i][key]
#for i in range(len(traj_data)):
    #the traj_data are in the "traj_data" dicitonary and the atoms saved as atoms objects in the "atoms"-array
#    db.write(traj_geoms[i],data=newtraj_data[i])
    
    
#define metadata
metadata = {}
metadata["info"]="Write down any information you wish to remember later, e.g., reference method, if phasecorrected, etc."

# this information is required
metadata["n_singlets"]=nsinglets
metadata["n_triplets"]=ntriplets
db.metadata=metadata
print("We have ", len(db), " data points.")


