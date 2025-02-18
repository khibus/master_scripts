# BAGEL.sh
Submission bash script for BAGEL called via subbagel

# ORCA.sh
Submission bash script for ORCA5 called via suborca

# ORCA5_freq.py
Generates a MOLDEN file from ORCA 5 frequency output.
Utilization: python2.7 ORCA5_freq.py freq.out

# ORCA6.sh
Submission bash script for ORCA6 called via suborca6

# average_traj.py
Averages the populations after diabatization with the diabatizer.py script. 
Utilization: 
``python /scripts/average_traj.py nstates ``
(where nstates are the total amount of spin-states)
Generates an average_traj.txt, which can be plotted with a read.py script.

# caspt2_energy.py
Gathers MS-CASPT2 energies from all filename*out files in the current directory, and plots them.
Utilization: 
``python /scripts/caspt2_energy.py filename nstates`` 
(where states are the spin-free states)

# db_gen.py
Generates a database from SHARC QM.out files and XYZ coordinates. It excludes outliers, specifically in case of Wigner sampling and linear interpolations.

# diabatizer.py
Transforms SHARC generated MCH adiabatic populations to diabatic, using LVC potentials.
Utilization: 
``python /scripts/diabatizer.py freq_output nsteps``
Necessary files: QM/LVC.template, output_data/coeff_MCH.out

# dyn_init
Adds the necessary environment variables to enable the submission of SHARC trajectories.

# energies_QMout.py
Plots the energies of QM.out files for all subdirectories. Mainly used to determine outliers for machine learning or to show potentials for linear interpolations. Argument for the title of the plot must be given.

# energy_plotter_orca.py
Plots the energies of ORCA5 TD-DFT output files in all subdirectories. Files should be named as ORCA.out. 
Utilization: 
``python /scripts/energy_plotter_orca.py nstates``

# gradient_all_QMout.py
Plots the sum of the root mean squares of all gradients of QM.out files for all subdirectories. Mainly used to determine outliers for machine learning or to show potentials for linear interpolations. Argument for the title of the plot must be given.

# gradient_separated_QMout.py
Plots the root mean squares of the gradients of QM.out files for all subdirectories separated for all states. Mainly used to determine outliers for machine learning or to show potentials for linear interpolations. Argument for the title of the plot must be given.
Utilization: 
``python /scripts/gradient_separated_QMout.py nstates``

# gradients.py
Writes if the gradient_RMS changes more than a given value (in eV) between two steps in SHARC output.lis files in all subdirectories. 

# gradients2.py
Writes if the gradient_RMS changes more than a given value (in eV) during the whole trajectory in SHARC output.lis files in all subdirectories.

# idpplin.py
Inter-, and extrapolates between two geometries. 
Utilization: 
``python /scripts/idpplin.py init.xyz final.xyz interpolation_steps extrapolation_steps output.xyz``
Extrapolation_steps=2, if no extrapolation is performed.
output.xyz is a concatenated XYZ file containing all geometries.

# lvc_reader.py
Plots the LVC potential along the given mode and the given displacement. LVC.template should be present in the current directory
Utilization: 
``python /scripts/lvc_reader.py no_of_mode no_of_steps``

# molcas.sh
Submission bash script for MOLCAS 24.06 called via submolcas

# molcas_init
Adds the necessary environment variables to enable the submission of SHARC calculation with MOLCAS.

# molcas_wigner_init
This script is an auxiliary script for the ultimate script for ML calculations, which can be found in /calcs/ultimate_ml_data directory

# orca_init
Adds the necessary environment variables to enable the submission of SHARC calculation with ORCA 5.

# orca6_init
Adds the necessary environment variables to enable the submission of SHARC calculation with ORCA 6.

# read.py
Interactive script for plotting SHARC-formatted populations.

