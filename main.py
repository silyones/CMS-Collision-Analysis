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

        # Just the muon-related columns
        muon_branches = [b for b in tree.keys() if b.startswith("Muon_")]
        print("Muon branches:", muon_branches)

        # sanity-check the shape of the data
        sample = tree.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_charge"], entry_stop=5)
        n_muons_sample = ak.num(sample["Muon_pt"])
        print("Muons per event (first 5):", n_muons_sample.tolist())
        print("Muon pt values, event 0:", sample["Muon_pt"][0].tolist())

        # enough muons to form a pair?
        pts = tree["Muon_pt"].array(library="ak")
        n_mu = ak.num(pts)

        print("Total events:", len(pts))
        print("Events with 0 muons:", int(ak.sum(n_mu == 0)))
        print("Events with 1 muon:", int(ak.sum(n_mu == 1)))
        print("Events with 2+ muons:", int(ak.sum(n_mu >= 2)))