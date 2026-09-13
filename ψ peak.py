import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

masses = np.load("dimuon_mass_clean.npy")

def gaussian_plus_background(x, A, mu, sigma, B):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + B

# Build a histogram of the J/psi region ourselves, so we get the
# actual (x, y) points to fit a curve through
counts, bin_edges = np.histogram(masses, bins=60, range=(2.7, 3.4))
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Initial guesses: peak height ~ tallest bin, center near 3.097,
# a rough width, and background ~ typical bin count away from the peak
p0 = [counts.max(), 3.097, 0.05, np.median(counts)]

params, _ = curve_fit(gaussian_plus_background, bin_centers, counts, p0=p0)
A_fit, mu_fit, sigma_fit, B_fit = params

print(f"Fitted mass (mu):   {mu_fit:.4f} GeV   (textbook value: 3.097 GeV)")
print(f"Fitted width (sigma): {sigma_fit:.4f} GeV")

# Plot data + fitted curve together
x_smooth = np.linspace(2.7, 3.4, 500)
plt.figure(figsize=(8, 6))
plt.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), alpha=0.6, label="Data")
plt.plot(x_smooth, gaussian_plus_background(x_smooth, *params), "r-", label="Fitted curve")
plt.axvline(3.097, color="black", linestyle="--", label="PDG value (3.097 GeV)")
plt.xlabel("Dimuon invariant mass (GeV)")
plt.ylabel("Number of muon pairs")
plt.title("J/ψ peak — fitted mass")
plt.legend()
plt.savefig("fig/result/jpsi_fit.png", dpi=150)
plt.show()