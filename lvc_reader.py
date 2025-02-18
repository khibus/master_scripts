#!/usr/bin/env python3

import sys, os
import numpy as np
import cclib
import scipy.constants as const
import matplotlib.pyplot as plt

with open("LVC.template", 'r') as fo:
	lines = fo.readlines()
	fo.close()
v0 = lines[0].split()
states = lines[1].split()
states_new=[]
states_new2=[]
no_mode=int(sys.argv[1])
steps=abs(int(sys.argv[2]))
print(steps)
lvc_pot=np.zeros(2*steps+1)
q=np.zeros(2*steps+1)
for i in range(len(states)):
	if states[i] != '0':
		states_new.append(i)
		states_new2.append(int(states[i]))
for i in range(len(lines)):
	if "epsilon" in lines[i]:
		nostate = int(lines[i+1])
		epsilon_matrix = [[float(digit) for digit in lines[k].split()] for k in range(i+2,i+2+nostate)]
		epsilon_matrix = np.asarray(epsilon_matrix)
	if "kappa" in lines[i]:
		kappas = int(lines[i+1])
		kappa_matrix = [[float(digit) for digit in lines[k].split()] for k in range(i+2,i+2+kappas)]
		kappa_matrix = np.asarray(kappa_matrix)
if int(sys.argv[2]) < 0:
	kappa_matrix[3] = np.negative(kappa_matrix[3])
with open(v0[0], 'r') as fo2:
	lines2 = fo2.readlines()
	fo2.close()
for i in range(len(lines2)):
	if "Frequencies" in lines2[i]:
		freq = lines2[i+1].split()
y1 = 0
y3 = 0
y5 = 0
y7 = 0
labels = []
colors = []

for i in range(nostate):
	x = 0
	for k in range(kappas):
		if int(kappa_matrix[k][0]) == int(epsilon_matrix[i][0]) and int(kappa_matrix[k][1]) == int(epsilon_matrix[i][1]) and int(kappa_matrix[k][2]) == no_mode:
			x = 1
			for l in range(2*steps+1):
				q[l]=l-steps
				lvc_pot[l]=27.212*(epsilon_matrix[i][2]+np.sign(int(sys.argv[2]))*kappa_matrix[k][3]*q[l]+0.5*float(freq[no_mode-1])*q[l]**2)
	if x==0:
		for l in range(2*steps+1):
			q[l]=l-int(steps)
			lvc_pot[l]=27.212*(epsilon_matrix[i][2]+0.5*float(freq[no_mode-1])*q[l]**2)
	if int(epsilon_matrix[i][0]) == 1:
		alabel=input("Plot Singlet %d state with label: "%(int(epsilon_matrix[i][1])))
		if alabel != "":
			colour=input("with color: ")
			plt.plot(q, lvc_pot, label=alabel, color=colour)
		else:
			plt.plot(q, lvc_pot, color=colour)
	if int(epsilon_matrix[i][0]) == 2:
		alabel=input("Plot Doublet %d state with label: "%(int(epsilon_matrix[i][1])))
		if alabel != "" and alabel not in labels:
			colour=input("with color: ")
			plt.plot(q, lvc_pot, label=alabel, color=colour)
			labels.append(alabel)
			colors.append(colour)
		elif alabel != "" and alabel in labels:
			index = labels.index(alabel)
			plt.plot(q, lvc_pot, color=colors[index])
		else:
			plt.plot(q, lvc_pot, color=colour)
	if int(epsilon_matrix[i][0]) == 3:
		alabel=input("Plot Triplet %d state with label: "%(int(epsilon_matrix[i][1])))
		if alabel != "" and alabel not in labels:
			colour=input("with color: ")
			plt.plot(q, lvc_pot, label=alabel, color=colour)
			labels.append(alabel)
			colors.append(colour)
		if alabel != "" and alabel in labels:
			index = labels.index(alabel)
			plt.plot(q, lvc_pot, color=colors[index])
		else:
			plt.plot(q, lvc_pot, color=colour)
	if int(epsilon_matrix[i][0]) == 4:
		alabel=input("Plot Quartet %d state with label: "%(int(epsilon_matrix[i][1])))
		if alabel != "" and alabel not in labels:
#			colour=input("with color: ")
			plt.plot(q, lvc_pot, label=alabel)
			labels.append(alabel)
#			colors.append(colour)
		elif alabel != "" and alabel in labels:
			index = labels.index(alabel)
			plt.plot(q, lvc_pot)
		else:
			plt.plot(q, lvc_pot)
	if int(epsilon_matrix[i][0]) == 5:
		alabel=input("Plot Quintet %d state with label: "%(int(epsilon_matrix[i][1])))
		if alabel != "" and alabel not in labels:
			colour=input("with color: ")
			plt.plot(q, lvc_pot, label=alabel, color=colour)
			labels.append(alabel)
			colors.append(colour)
		elif alabel != "" and alabel in labels:
			index = labels.index(alabel)
			plt.plot(q, lvc_pot, color=colors[index])
		else:
			plt.plot(q, lvc_pot, color=colour)
	if int(epsilon_matrix[i][0]) == 7:
		if y7 == 0:
			plt.plot(q, lvc_pot, label='7MLCT', color='gray')
			y7 = 1
		else:
			plt.plot(q, lvc_pot, color='gray')

plt.xlabel("Fe-N breathing normal mode", fontsize=14)
plt.ylabel("Energy (eV)", fontsize=14)
plt.rcParams.update({'font.size': 12})
plt.rcParams.update({'xtick.minor.size': 12})
plt.rcParams.update({'ytick.major.size': 12})
plt.legend(loc='best', ncol=2)
plt.grid()
plt.xlim(-steps,steps)
plt.ylim(None, None)
plt.savefig("lvc" + "_" + sys.argv[1] + "_" + sys.argv[2] + ".png", dpi=300)
plt.savefig("lvc" + "_" + sys.argv[1] + "_" + sys.argv[2] + ".svg")
plt.show()
