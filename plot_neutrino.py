import os
import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt

files = [
    "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root",
    "opendata/raw/04935F99-9E92-4919-89C2-38670059FBDA.root",
]

all_MT = []

for path in files:

    print(f"\n=== {path} ===")

    with uproot.open(path) as f:

        tree = f["Events"]

        arrs = tree.arrays(
            [
                "Muon_pt",
                "Muon_phi",
                "Muon_tightId",
                "Muon_pfRelIso04_all",
                "MET_pt",
                "MET_phi",
            ],
            library="ak",
        )

        # 1. Select good, isolated, high-pt muons
        good = (
            arrs["Muon_tightId"]
            & (arrs["Muon_pfRelIso04_all"] < 0.15)
            & (arrs["Muon_pt"] > 25)
        )

        good_pt = arrs["Muon_pt"][good]
        good_phi = arrs["Muon_phi"][good]

        # 2. Keep events with at least one good muon
        keep = ak.num(good_pt) >= 1

        good_pt = good_pt[keep]
        good_phi = good_phi[keep]

        MET_pt = arrs["MET_pt"][keep]
        MET_phi = arrs["MET_phi"][keep]

        # 3. Take the highest-pt good muon
        order = ak.argsort(good_pt, ascending=False)

        good_pt = good_pt[order]
        good_phi = good_phi[order]

        muon_pt = good_pt[:, 0]
        muon_phi = good_phi[:, 0]

        # 4. Calculate Δφ between muon and MET
        delta_phi = np.abs(muon_phi - MET_phi)

        delta_phi = np.where(
            delta_phi > np.pi,
            2 * np.pi - delta_phi,
            delta_phi
        )

        # 5. Calculate transverse mass
        MT = np.sqrt(
            2 * muon_pt * MET_pt * (1 - np.cos(delta_phi))
        )

        # Convert to normal NumPy array
        MT = ak.to_numpy(MT)

        # Remove invalid values
        MT = MT[np.isfinite(MT)]

        print("Selected events:", len(MT))
        print(
            "MT range: {:.2f} to {:.2f} GeV".format(
                MT.min(),
                MT.max()
            )
        )

        # Save this file's MT values
        all_MT.append(MT)


# Combine both ROOT files
all_MT = np.concatenate(all_MT)

print("\n==============================")
print("TOTAL EVENTS:", len(all_MT))
print(
    "Overall MT range: {:.2f} to {:.2f} GeV".format(
        all_MT.min(),
        all_MT.max()
    )
)

# Save the values
np.save("transverse_mass.npy", all_MT)


# --------------------------------
# Make histogram
# --------------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    all_MT,
    bins=100,
    range=(0, 200)
)
out_dir = "fig/result"
os.makedirs(out_dir, exist_ok=True)

plt.xlabel("Transverse mass MT (GeV)")
plt.ylabel("Number of events")
plt.title("Muon + Missing Transverse Momentum: Transverse Mass")
plt.legend()
plt.savefig(os.path.join(out_dir, "upsilon_peak_clean.png"), dpi=150)
plt.close()