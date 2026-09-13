import numpy as np
import matplotlib.pyplot as plt

masses = np.load("dimuon_mass.npy")

# Drop the NaNs from mismeasured muons before plotting
masses = masses[~np.isnan(masses)]
print("Valid dimuon pairs after cleanup:", len(masses))

plt.figure(figsize=(9, 6))
plt.hist(masses, bins=300, range=(0.2, 200), log=True)  # log=True -> log scale on the COUNT axis
plt.xscale("log")                                        # log scale on the MASS axis too
plt.xlabel("Dimuon invariant mass (GeV)")
plt.ylabel("Number of muon pairs")
plt.title("Dimuon mass spectrum")
plt.savefig("dimuon_mass_spectrum.png", dpi=150)
plt.show()