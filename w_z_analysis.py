import os

import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt

files = [
    "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root",
    "opendata/raw/04935F99-9E92-4919-89C2-38670059FBDA.root",
]


all_z_mass = []
all_w_MT = []


for path in files:

    print(f"\nProcessing: {path}")

    with uproot.open(path) as f:

        tree = f["Events"]

        arrs = tree.arrays(
            [
                "Muon_pt",
                "Muon_eta",
                "Muon_phi",
                "Muon_mass",
                "Muon_charge",
                "Muon_tightId",
                "Muon_pfRelIso04_all",
                "MET_pt",
                "MET_phi",
            ],
            library="ak",
        )

        # GOOD MUONS

        good = (
            arrs["Muon_tightId"]
            & (arrs["Muon_pfRelIso04_all"] < 0.15)
            & (arrs["Muon_pt"] > 25)
        )


        good_pt = arrs["Muon_pt"][good]
        good_eta = arrs["Muon_eta"][good]
        good_phi = arrs["Muon_phi"][good]
        good_mass = arrs["Muon_mass"][good]
        good_charge = arrs["Muon_charge"][good]
         
        # Z BOSON
        #
        # Require at least 2 good muons
        
        has_two_muons = ak.num(good_pt) >= 2

        z_pt = good_pt[has_two_muons]
        z_eta = good_eta[has_two_muons]
        z_phi = good_phi[has_two_muons]
        z_mass = good_mass[has_two_muons]
        z_charge = good_charge[has_two_muons]


        # Sort by pT

        order = ak.argsort(z_pt, ascending=False)

        z_pt = z_pt[order]
        z_eta = z_eta[order]
        z_phi = z_phi[order]
        z_mass = z_mass[order]
        z_charge = z_charge[order]


        # Take two leading muons

        pt1 = z_pt[:, 0]
        pt2 = z_pt[:, 1]

        eta1 = z_eta[:, 0]
        eta2 = z_eta[:, 1]

        phi1 = z_phi[:, 0]
        phi2 = z_phi[:, 1]

        mass1 = z_mass[:, 0]
        mass2 = z_mass[:, 1]

        charge1 = z_charge[:, 0]
        charge2 = z_charge[:, 1]


        # Require opposite charge

        opposite_charge = charge1 * charge2 < 0

        pt1 = pt1[opposite_charge]
        pt2 = pt2[opposite_charge]

        eta1 = eta1[opposite_charge]
        eta2 = eta2[opposite_charge]

        phi1 = phi1[opposite_charge]
        phi2 = phi2[opposite_charge]

        mass1 = mass1[opposite_charge]
        mass2 = mass2[opposite_charge]


         
        # CONVERT MUONS TO FOUR-VECTORS
         

        px1 = pt1 * np.cos(phi1)
        py1 = pt1 * np.sin(phi1)
        pz1 = pt1 * np.sinh(eta1)

        E1 = np.sqrt(
            px1**2 +
            py1**2 +
            pz1**2 +
            mass1**2
        )


        px2 = pt2 * np.cos(phi2)
        py2 = pt2 * np.sin(phi2)
        pz2 = pt2 * np.sinh(eta2)

        E2 = np.sqrt(
            px2**2 +
            py2**2 +
            pz2**2 +
            mass2**2
        )


         
        # DIMUON INVARIANT MASS
         

        E = E1 + E2
        px = px1 + px2
        py = py1 + py2
        pz = pz1 + pz2

        mass_Z = np.sqrt(
            np.maximum(
                E**2 - px**2 - py**2 - pz**2,
                0
            )
        )

        mass_Z = ak.to_numpy(mass_Z)
        mass_Z = mass_Z[np.isfinite(mass_Z)]

        all_z_mass.append(mass_Z)


         
        # W BOSON
        #
        # Exactly ONE good muon
        # MET > 25 GeV
         

        n_good = ak.num(good_pt)

        w_selection = (
            (n_good == 1)
            & (arrs["MET_pt"] > 25)
        )


        w_pt = good_pt[w_selection]
        w_phi = good_phi[w_selection]

        MET_pt = arrs["MET_pt"][w_selection]
        MET_phi = arrs["MET_phi"][w_selection]


        # Take the only good muon

        muon_pt = w_pt[:, 0]
        muon_phi = w_phi[:, 0]


         
        # DELTA PHI
         

        delta_phi = np.abs(muon_phi - MET_phi)

        delta_phi = np.where(
            delta_phi > np.pi,
            2 * np.pi - delta_phi,
            delta_phi
        )


         
        # TRANSVERSE MASS
         

        MT = np.sqrt(
            2 *
            muon_pt *
            MET_pt *
            (1 - np.cos(delta_phi))
        )


        MT = ak.to_numpy(MT)
        MT = MT[np.isfinite(MT)]

        all_w_MT.append(MT)


all_z_mass = np.concatenate(all_z_mass)
all_w_MT = np.concatenate(all_w_MT)


print("\n==============================")
print("Z → μμ events:", len(all_z_mass))
print("W → μν candidates:", len(all_w_MT))

print(
    "Z mass range:",
    f"{all_z_mass.min():.2f} - {all_z_mass.max():.2f} GeV"
)

print(
    "W MT range:",
    f"{all_w_MT.min():.2f} - {all_w_MT.max():.2f} GeV"
)


out_dir = "fig/result"

os.makedirs(out_dir, exist_ok=True)


fig, axes = plt.subplots(
    1,
    2,
    figsize=(14, 6)
)


# LEFT: Z → μμ


axes[0].hist(
    all_z_mass,
    bins=120,
    range=(0, 120),
    color="royalblue",
    alpha=0.85
)

axes[0].axvline(
    91.19,
    linestyle="--",
    linewidth=2,
    color="black",
    label="Z mass ≈ 91.2 GeV"
)

axes[0].set_xlabel(
    "Dimuon invariant mass (GeV)"
)

axes[0].set_ylabel(
    "Number of events"
)

axes[0].set_title(
    r"$Z \rightarrow \mu^+\mu^-$"
)

axes[0].legend()

axes[0].grid(
    alpha=0.25
)



# RIGHT: W → μν


axes[1].hist(
    all_w_MT,
    bins=100,
    range=(0, 150),
    color="limegreen",
    alpha=0.85
)

axes[1].axvline(
    80.4,
    linestyle="--",
    linewidth=2,
    color="black",
    label="W mass ≈ 80.4 GeV"
)

axes[1].set_xlabel(
    "Transverse mass $M_T$ (GeV)"
)

axes[1].set_ylabel(
    "Number of events"
)

axes[1].set_title(
    r"$W \rightarrow \mu\nu$"
)

axes[1].legend()

axes[1].grid(
    alpha=0.25
)



# OVERALL TITLE

fig.suptitle(
    "CMS Open Data: W and Z Boson Signatures",
    fontsize=16
)

plt.tight_layout()


output_file = os.path.join(
    out_dir,
    "w_z_analysis.png"
)

plt.savefig(
    output_file,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nSaved:")
print(output_file)