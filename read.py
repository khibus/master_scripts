#!/usr/bin/python3
import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import glob 

# ------------------------------------------ #

# ---------------- GET DATA ---------------- #

data=np.loadtxt(sys.argv[1], comments='#', dtype=float)
time=data[:,0]

raw_states=input("Enter the number of states: ")
states=[]
states=raw_states.split()
base_state=0
for i in range(len(states)):
	if int(states[i]) != 0:
		no_of_states=input("How many states on mult %d? "%(i+1))
		for j in range(int(no_of_states)):
			which_states=input("Which states should be added to mult %d state %d? "%(i+1,j+1))
			plotted_data=np.zeros(len(data))
			plot_states=which_states.split()
			for k in range(i+1):
				for l in range(len(plot_states)):
					act_state = base_state+(int(plot_states[l])-1)+k*int(states[i])
					print(act_state)
					plotted_data= plotted_data + data[:,act_state+1]
			alabel=input("Add a label to mult %d state %d! "%(i+1,j+1))
			plt.plot(time, plotted_data, label=alabel)
		base_state = base_state + (i+1) * int(states[i])

font = {'size'   : 14}
plt.xlabel('Timestep (fs)', fontsize=14)
plt.ylabel('Population', fontsize=14)
plt.ylim(0,1)
matplotlib.rc('font', **font)
matplotlib.rc('xtick', labelsize=13) 
matplotlib.rc('ytick', labelsize=13) 
plt.legend(loc='best')
#plt.ylim(0, 1)
plt.savefig('out.svg', format='svg')
plt.savefig('out.png', format='png', dpi=300)
plt.show()

