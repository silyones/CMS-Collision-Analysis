import os
import numpy as np
import matplotlib.pyplot as plt

masses = np.load("dimuon_mass_clean.npy")
masses = masses[~np.isnan(masses)]

out_dir = "fig/result"
os.makedirs(out_dir, exist_ok=True)

# --- J/psi region (known mass ~3.097 GeV) ---
plt.figure(figsize=(8, 6))
plt.hist(masses, bins=200, range=(2.5, 3.5))
plt.axvline(3.097, color="red", linestyle="--", label="J/ψ (3.097 GeV)")
plt.xlabel("Dimuon invariant mass (GeV)")
plt.ylabel("Number of muon pairs")
plt.title("J/ψ region")
plt.legend()
plt.savefig(os.path.join(out_dir, "jpsi_peak_clean.png"), dpi=150)
plt.close()

# --- Upsilon region (known mass ~9.46 GeV) ---
plt.figure(figsize=(8, 6))
plt.hist(masses, bins=40, range=(8.5, 10.5))
plt.axvline(9.46, color="red", linestyle="--", label="Upsilon (9.46 GeV)")
plt.xlabel("Dimuon invariant mass (GeV)")
plt.ylabel("Number of muon pairs")
plt.title("Upsilon region")
plt.legend()
plt.savefig(os.path.join(out_dir, "upsilon_peak_clean.png"), dpi=150)
plt.close()

print("Saved plots to", out_dir)