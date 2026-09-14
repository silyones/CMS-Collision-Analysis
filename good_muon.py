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
                "MET_pt",
                "MET_phi",
            ],
            library="ak",
        )

        # Select good, isolated muons
        good = (
            arrs["Muon_tightId"]
            & (arrs["Muon_pfRelIso04_all"] < 0.15)
            & (arrs["Muon_pt"] > 25)
        )

        good_muons = arrs["Muon_pt"][good]

        # Count good muons in each event
        n_good = ak.num(good_muons)

        event_selection = (
            n_good >= 1
            & (arrs["MET_pt"] > 25)
        )

        print("Events with good muon + MET > 25 GeV:", int(ak.sum(event_selection)))

        print("Total events:", len(n_good))
        print("Events with 0 good muons:", int(ak.sum(n_good == 0)))
        print("Events with 1 good muon:", int(ak.sum(n_good == 1)))
        print("Events with 2+ good muons:", int(ak.sum(n_good >= 2)))

        print("First 10 MET values:")
        print(arrs["MET_pt"][:10].tolist())