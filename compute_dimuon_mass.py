import numpy as np
import uproot
import awkward as ak

files = [
    "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root",
    "opendata/raw/04935F99-9E92-4919-89C2-38670059FBDA.root",
]

def to_four_vector(pt, eta, phi, mass):
    px = pt * np.cos(phi)
    py = pt * np.sin(phi)
    pz = pt * np.sinh(eta)
    E = np.sqrt(px**2 + py**2 + pz**2 + mass**2)
    return px, py, pz, E

all_masses = []

for path in files:
    print(f"\n=== {path} ===")
    with uproot.open(path) as f:
        tree = f["Events"]
        arrs = tree.arrays(
            ["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"],
            library="ak",
        )

        # Keep only events with at least 2 muons
        n_mu = ak.num(arrs["Muon_pt"])
        arrs = arrs[n_mu >= 2]

        # Sort muons within each event by pt, highest first
        order = ak.argsort(arrs["Muon_pt"], ascending=False)
        pt, eta, phi = arrs["Muon_pt"][order], arrs["Muon_eta"][order], arrs["Muon_phi"][order]
        mass, charge = arrs["Muon_mass"][order], arrs["Muon_charge"][order]

        # Take the two leading (highest-pt) muons per event
        pt1, pt2 = pt[:, 0], pt[:, 1]
        eta1, eta2 = eta[:, 0], eta[:, 1]
        phi1, phi2 = phi[:, 0], phi[:, 1]
        m1, m2 = mass[:, 0], mass[:, 1]
        q1, q2 = charge[:, 0], charge[:, 1]

        # Build 4-vectors and add them
        px1, py1, pz1, E1 = to_four_vector(pt1, eta1, phi1, m1)
        px2, py2, pz2, E2 = to_four_vector(pt2, eta2, phi2, m2)
        E, px, py, pz = E1 + E2, px1 + px2, py1 + py2, pz1 + pz2

        inv_mass = np.sqrt(E**2 - px**2 - py**2 - pz**2)

        # Keep only opposite-charge pairs (real decay candidates)
        opp_charge = (q1 * q2) < 0
        inv_mass = ak.to_numpy(inv_mass[opp_charge])

        print("Opposite-charge muon pairs found:", len(inv_mass))
        print("Mass range: {:.2f} to {:.2f} GeV".format(inv_mass.min(), inv_mass.max()))

        all_masses.append(inv_mass)

all_masses = np.concatenate(all_masses)
np.save("dimuon_mass.npy", all_masses)
print("\nTotal opposite-charge dimuon pairs across both files:", len(all_masses))