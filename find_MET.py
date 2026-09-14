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

        # Find branches related to missing transverse momentum
        met_branches = [b for b in tree.keys() if "MET" in b]

        print("MET branches:")
        print(met_branches)

        # Look at the first 5 events
        sample = tree.arrays(
            ["MET_pt", "MET_phi"],
            entry_stop=5,
            library="ak"
        )

        print("MET pt, first 5 events:")
        print(sample["MET_pt"].tolist())

        print("MET phi, first 5 events:")
        print(sample["MET_phi"].tolist())