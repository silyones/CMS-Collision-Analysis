import uproot
import awkward as ak

files = [
    "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root",
    "opendata/raw/04935F99-9E92-4919-89C2-38670059FBDA.root",
]

for path in files:
    print(f"\n=== {path} ===")

    with uproot.open(path) as f:
        tree = f["Events"]

        arrs = tree.arrays(
            [
                "Muon_pt",
                "Muon_eta",
                "Muon_phi",
                "Muon_tightId",
                "Muon_pfRelIso04_all",
            ],
            library="ak",
        )

        # Select good, isolated muons
        good = (
            arrs["Muon_tightId"]
            & (arrs["Muon_pfRelIso04_all"] < 0.15)
        )

        good_muons = arrs["Muon_pt"][good]

        # Count good muons in each event
        n_good = ak.num(good_muons)

        print("Total events:", len(n_good))
        print("Events with 0 good muons:", int(ak.sum(n_good == 0)))
        print("Events with 1 good muon:", int(ak.sum(n_good == 1)))
        print("Events with 2+ good muons:", int(ak.sum(n_good >= 2)))