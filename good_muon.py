import numpy as np
import uproot
import awkward as ak

files = [
    "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root",
    "opendata/raw/04935F99-9E92-4919-89C2-38670059FBDA.root",
]

for path in files:

    print(f"{path}")

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

        # 3. Take highest-pt good muon

        order = ak.argsort(good_pt, ascending=False)

        good_pt = good_pt[order]
        good_phi = good_phi[order]

        muon_pt = good_pt[:, 0]
        muon_phi = good_phi[:, 0]

        # 4. Calculate angle between muon and MET

        delta_phi = np.abs(muon_phi - MET_phi)

        # Keep Δφ between 0 and π
        delta_phi = np.where(
            delta_phi > np.pi,
            2 * np.pi - delta_phi,
            delta_phi
        )

        # 5. Calculate transverse mass

        MT = np.sqrt(
            2 * muon_pt * MET_pt * (1 - np.cos(delta_phi))
        )

        print("Selected events:", len(MT))

        print("First 20 MT values:")
        print(MT[:20].tolist())

        print(
            "MT range: {:.2f} to {:.2f} GeV".format(
                float(ak.min(MT)),
                float(ak.max(MT))
            )
        )