#!/usr/bin/env python3

import sys, os
import numpy as np
import cclib
#import asyncio
import time
# initiate asyncio
#def background(f):
#	def wrapped(*args, **kwargs):
#		return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
#	return wrapped

start_time = time.time()

# Parse freq calculation
filename1=sys.argv[1]
file1 = cclib.io.ccopen(filename1)
molecule = file1.parse()

transformed_vibdisps=np.zeros((molecule.natom*3-6,molecule.natom*3))
base_coord=np.zeros(molecule.natom*3)
mass=molecule.atommasses
# Import GAUSSIAN-type Cartesian displacement coordinates, orthogonalize them, form a 3N-6*3N matrix
for i in range(molecule.natom*3-6):
	for j in range(molecule.natom):
		molecule.vibdisps[i][j][0]  = molecule.vibdisps[i][j][0] * np.sqrt(mass[j])
		molecule.vibdisps[i][j][1] = molecule.vibdisps[i][j][1] * np.sqrt(mass[j])
		molecule.vibdisps[i][j][2] = molecule.vibdisps[i][j][2] * np.sqrt(mass[j])
	ss = np.sum(molecule.vibdisps[i]**2)
	molecule.vibdisps[i] = molecule.vibdisps[i]/np.sqrt(ss)
for i in range(molecule.natom*3-6):
	if molecule.vibfreqs[i] < 0:
		molecule.vibfreqs[i] = 0
	for j in range(molecule.natom):
		transformed_vibdisps[i][3*j] = molecule.vibdisps[i][j][0] * 0.172*np.sqrt(mass[j]*molecule.vibfreqs[i])
		transformed_vibdisps[i][3*j+1] = molecule.vibdisps[i][j][1] * 0.172*np.sqrt(mass[j]*molecule.vibfreqs[i])
		transformed_vibdisps[i][3*j+2] = molecule.vibdisps[i][j][2] * 0.172*np.sqrt(mass[j]*molecule.vibfreqs[i])



# Import base geometry as 3N*1 matrix
for k in range(molecule.natom):
	base_coord[3*k] = molecule.atomcoords[0][k][0]
	base_coord[3*k+1] = molecule.atomcoords[0][k][1]
	base_coord[3*k+2] = molecule.atomcoords[0][k][2]

# Read coordinates from dynamics and transform them to a time*3N matrix
inp_coords=np.loadtxt("output.xyz", comments=('t', '        '), usecols=(1,2,3))
time_step=int(len(inp_coords)/(molecule.natom))
sim_coords=np.zeros((time_step,molecule.natom*3))
k = 0
for i in range(time_step):
	for j in range(molecule.natom):
			sim_coords[i][3*j] = inp_coords[k][0]
			sim_coords[i][3*j+1] = inp_coords[k][1]
			sim_coords[i][3*j+2] = inp_coords[k][2]
			k = k + 1

# Transform geometries from dynamics to normal coordinates 
q_matrix=np.zeros((time_step,molecule.natom*3-6))

#A=np.linalg.inv(transformed_vibdisps @ transformed_vibdisps.T) @ transformed_vibdisps

# Reading LVC.template
with open("QM/LVC.template", 'r') as fo:
	lines = fo.readlines()
	fo.close()

states = lines[1].split()
states_new=[]
states_new2=[]
for i in range(len(states)):
	if states[i] != '0':
		states_new.append(i+1)
		states_new2.append(states[i])
spin_states=[]
spin_states2=[]
for i in range(len(states)):
	if states[i] != "0":
		spin_states.extend([i+1 for j in range(int(states[i]))])
for l in range(len(spin_states)):
	spin_states2.extend([spin_states[l] for m in range(int(spin_states[l]))])
for i in range(len(lines)):
	if "epsilon" in lines[i]:
		nostate = int(lines[i+1])
		epsilon_matrix = [[float(digit) for digit in lines[k].split()] for k in range(i+2,i+2+nostate)]
		epsilon_matrix = np.asarray(epsilon_matrix)
	if "kappa" in lines[i]:
		kappas = int(lines[i+1])
		kappa_matrix = [[float(digit) for digit in lines[k].split()] for k in range(i+2,i+2+kappas)]
		kappa_matrix = np.asarray(kappa_matrix)
	if "lambda" in lines[i]:
		lambdas = int(lines[i+1])
		lambda_matrix = [[float(digit) for digit in lines[k].split()] for k in range(i+2,i+2+lambdas)]
		lambda_matrix = np.asarray(lambda_matrix)

# Reading adiabatic population matrix
mch_input = np.loadtxt("output_data/coeff_MCH.out", comments='#', dtype=float)
eigen=np.zeros((nostate,nostate))
V_diag=np.zeros((nostate,nostate))
steps = 0
if len(sys.argv) == 4:
	a = int(sys.argv[2])
	b = int(sys.argv[3])
else:
	a = 0
	b = int(sys.argv[2])
	alpha = './output_alpha2.txt'
	if os.path.exists(alpha):
		os.remove(alpha)
#@background
print("The program was running for %s seconds!" % (time.time() - start_time))
for t in range(a,b):
	U_matrix=np.zeros((len(spin_states2),len(spin_states2)))
	V_matrix=np.zeros((len(spin_states2),len(spin_states2)))
	diab_matrix=np.zeros(len(spin_states2)+1)
	mch_matrix =np.zeros(len(spin_states2))
	mch_matrix2=np.zeros((len(spin_states2),len(spin_states2)))
	for i in range(len(spin_states2)):
		mch_matrix[i]=mch_input[t][2*(i+1)]**2+mch_input[t][2*(i+1)+1]**2
	mch_matrix2=np.diag(mch_matrix)
	q_matrix=np.zeros(molecule.natom*3-6)
# linear regression for q
#	q_matrix[t]= A @ sim_coords[t]
# matrix multiplication for q
	q_matrix=np.dot(transformed_vibdisps,(sim_coords[t]-base_coord))
	with open("q_omega.txt", "a") as f:
		f.write(str(t))
		f.write("\n")
		np.savetxt(f, q_matrix)
		f.write("\n")
		f.write("\n")
# potential calculation
	m = 0
	n = 0
	V=np.zeros((nostate,nostate))
	for i in range(nostate):
		for j in range(i,nostate):
			if i == j:
				V[i][j] = epsilon_matrix[i][2] 
				for k in range(m,kappas):
					if kappa_matrix[k][0] == epsilon_matrix[i][0] and kappa_matrix[k][1] == epsilon_matrix[i][1]:
						V[i][j]  = V[i][j] + kappa_matrix[k][3]*q_matrix[int(kappa_matrix[k][2])-7]
						m = m + 1
			else:
				for l in range(n,lambdas):
					if lambda_matrix[l][0] == epsilon_matrix[i][0] and lambda_matrix[l][0] == epsilon_matrix[j][0] and lambda_matrix[l][1] == epsilon_matrix[i][1] and lambda_matrix[l][2] == epsilon_matrix[j][1]:
						V[i][j]  = V[i][j] + lambda_matrix[l][4]*q_matrix[int(lambda_matrix[l][3])-7]
						V[j][i]  = V[j][i] + lambda_matrix[l][4]*q_matrix[int(lambda_matrix[l][3])-7]
						n = n + 1
	for i in range(nostate):
		for j in range(molecule.natom*3-6):
			V[i][i] = V[i][i] + 0.5*(molecule.vibfreqs[j]/219474.63)*(q_matrix[j]**2)
#	with open("Vmatrix.txt", "a") as f:
#		f.write(str(t))
#		f.write("\n")
#		np.savetxt(f, V)
#		f.write("\n")
#		f.write("\n")
	x = 0
	for i in range(len(states_new)):
		y = x + int(states_new2[i])
		eigenvalues, eigenvectors = np.linalg.eigh(V[x:y,x:y])
		eigen[x:y,x:y] = eigenvectors
		x = y
# diagonalization
#	eigenvalues, eigenvectors = np.linalg.eig(V[t])
#	if not np.all(np.iscomplex(eigenvalues)):
#		D = np.diag(eigenvalues)
#		P_inv = np.linalg.inv(eigenvectors)
#		V_diag = np.dot(P_inv, np.dot(V[t], eigenvectors))
#	else:
#		print("Matrix is not diagonalizable.")
#	with open("eigen.txt", "a") as f:
#		f.write(str(t))
#		f.write("\n")
#		np.savetxt(f, eigen)
#		f.write("\n")
#		f.write("\n")
	x = 0
	y = 0
	curr_state=0
	curr_state2=0
# spin-free -> spin-dependent transformation
	for i in range(len(states)):
		if int(states[i])!=0:
			for j in range(int(states[i])):
				for k in range(i+1):
					for l in range(len(states)):
						if int(states[l])!=0:
							for m in range(int(states[l])):
								for n in range(l+1):
									U_matrix[curr_state2+j+int(states[i])*k][curr_state+m+int(states[l])*n] = eigen[x][y]
								y = y + 1
							curr_state = curr_state + int(states[l])*(l+1)
					curr_state=0
					y = 0
				x = x + 1
			curr_state2 = curr_state2 + int(states[i])*(i+1)
#	with open("Umatrix.txt", "a") as f:
#		f.write(str(t))
#		f.write("\n")
#		np.savetxt(f, U_matrix)
#		f.write("\n")
#		f.write("\n")
# transforming adiabatic populations to diabatic, and exporting to output
	diab_matrix = U_matrix.T @ (mch_matrix2 @ U_matrix)
	pop = np.diag(diab_matrix) 
	ss = np.sum(pop)
	pop = pop/ss
	pop = np.insert(pop,[0],str(t*0.5))
	with open("output_omega.txt", "ab") as f:
		np.savetxt(f, pop, newline=' ')
		f.write(b"\n")
	steps = steps + 1
	print("Time step {} fs finished! Step {} out of {} ".format(str(t*0.5), str(steps), str(b-a)))
	if steps == a:
		print("The program was running for %s seconds!" % (time.time() - start_time))
#results = Parallel(n_jobs=2)(delayed(transformation)(i) for i in range(100))
#print(results)


print("finish")

