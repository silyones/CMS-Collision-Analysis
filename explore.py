import uproot

files = [
    "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root",
    "opendata/raw/04935F99-9E92-4919-89C2-38670059FBDA.root",
]

for path in files:
    print(f"\n=== {path} ===")
    f = uproot.open(path)
    print(f.keys())              # top-level objects ('Events')

    events = f["Events"]
    print(events.num_entries)    # how many collision events in this file
    print(events.keys()[:30])    # first 30 branch names (things like Muon_pt, Muon_eta, etc.)


