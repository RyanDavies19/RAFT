# example script for running RAFT from a YAML input file

import numpy as np
import matplotlib.pyplot as plt
import yaml
import raft

def plotRAs(ax, w, y, color, label, rot_ra = True):
    if rot_ra:
        y = y * (180/np.pi)
    '''Plots magnitude, real and image components'''
    ax.plot(w,  np.abs(y), color=color,               label=label+" magnitude")
    ax.plot(w, np.real(y), color=color, dashes=[3,1], label=label+" real")
    ax.plot(w, np.imag(y), color=color, dashes=[1,1], label=label+" imaginary")
    ax.set_xticks(np.arange(min(w), max(w), max(w)/20))
    ax.grid()
    ax.set_xlabel('frequency (Hz)')
    if rot_ra:
        ax.set_ylabel('RAO (deg/m)')
    else:
        ax.set_ylabel('RAO (m/m)')
    ax.legend()

# open the design YAML file and parse it into a dictionary for passing to raft
with open('spar_vertical.yaml') as file:
    design = yaml.load(file, Loader=yaml.FullLoader)

# Create the RAFT model (will set up all model objects based on the design dict)
model = raft.Model(design)  

# Evaluate the system properties and equilibrium position before loads are applied
model.analyzeUnloaded()

# Compute natural frequencie
model.solveEigen()

# Simule the different load cases
model.analyzeCases(display=1)

# # Plot the power spectral densities from the load cases
# model.plotResponses()

# Visualize the system in its most recently evaluated mean offset position
model.plot(hideGrid=False)

frequencies = model.fowtList[0].w
rao = model.fowtList[0].Xi[0,:,:] # 0: surge, 1: sway, 2: heave, 3: roll, 4: pitch, 5: yaw
fig, ax = plt.subplots(6,1, sharex=True)
color = 'blue'
plotRAs(ax[0], frequencies, rao[0,:], color, 'Surge_RA', rot_ra=False)
plotRAs(ax[1], frequencies, rao[1,:], color, 'Sway_RA', rot_ra=False)
plotRAs(ax[2], frequencies, rao[2,:], color, 'Heave_RA', rot_ra=False)
plotRAs(ax[3], frequencies, rao[3,:], color, 'Roll_RA', rot_ra=True)
plotRAs(ax[4], frequencies, rao[4,:], color, 'Pitch_RA', rot_ra=True)
plotRAs(ax[5], frequencies, rao[5,:], color, 'Yaw_RA', rot_ra=True)
plt.show()
