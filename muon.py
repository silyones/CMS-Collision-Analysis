import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

masses = np.load("dimuon_mass_clean.npy")

def gaussian_plus_background(x, A, mu, sigma, B):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + B

def fit_peak(name, pdg_mass, fit_range, bins, p0_sigma):
    counts, bin_edges = np.histogram(masses, bins=bins, range=fit_range)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    p0 = [counts.max(), pdg_mass, p0_sigma, np.median(counts)]
    params, pcov = curve_fit(gaussian_plus_background, bin_centers, counts, p0=p0)
    A_fit, mu_fit, sigma_fit, B_fit = params

    # sqrt of the diagonal of pcov = uncertainty on each fitted parameter
    mu_err, sigma_err = np.sqrt(pcov[1][1]), np.sqrt(pcov[2][2])

    print(f"\n--- {name} ---")
    print(f"Fitted mass:  {mu_fit:.4f} ± {mu_err:.4f} GeV   (PDG: {pdg_mass} GeV)")
    print(f"Fitted width: {sigma_fit:.4f} ± {sigma_err:.4f} GeV")
    print(f"Relative resolution (sigma/mass): {sigma_fit / mu_fit:.4f}")

    x_smooth = np.linspace(fit_range[0], fit_range[1], 500)
    plt.figure(figsize=(8, 6))
    plt.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), alpha=0.6, label="Data")
    plt.plot(x_smooth, gaussian_plus_background(x_smooth, *params), "r-", label="Fitted curve")
    plt.axvline(pdg_mass, color="black", linestyle="--", label=f"PDG value ({pdg_mass} GeV)")
    plt.xlabel("Dimuon invariant mass (GeV)")
    plt.ylabel("Number of muon pairs")
    plt.title(f"{name} peak — fitted mass")
    plt.legend()
    plt.savefig(f"fig/result/{name.lower().replace('/', '')}_fit.png", dpi=150)
    plt.close()

    return mu_fit, sigma_fit

results = {}
results["J/psi"]   = fit_peak("J/psi", 3.097, (2.7, 3.4), 60, p0_sigma=0.05)
results["Upsilon"] = fit_peak("Upsilon", 9.46, (8.8, 10.2), 40, p0_sigma=0.3)
results["Z"]       = fit_peak("Z", 91.19, (75, 110), 70, p0_sigma=3.0)

# Compare relative resolution across all three
names = list(results.keys())
masses_fit = [results[n][0] for n in names]
sigmas_fit = [results[n][1] for n in names]
rel_res = [s / m for s, m in zip(sigmas_fit, masses_fit)]

plt.figure(figsize=(7, 5))
plt.plot(masses_fit, rel_res, "o-")
for n, x, y in zip(names, masses_fit, rel_res):
    plt.annotate(n, (x, y), textcoords="offset points", xytext=(5, 5))
plt.xscale("log")
plt.xlabel("Particle mass (GeV)")
plt.ylabel("Relative mass resolution (σ / mass)")
plt.title("Detector resolution across particle masses")
plt.savefig("fig/result/resolution_comparison.png", dpi=150)
plt.close()

print("\nAll fits done. Plots saved to fig/result/")