import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt


path = "opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root"


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


  
# SELECT GOOD MUONS
  

good = (
    arrs["Muon_tightId"]
    & (arrs["Muon_pfRelIso04_all"] < 0.15)
    & (arrs["Muon_pt"] > 25)
)

good_pt = arrs["Muon_pt"][good]
good_phi = arrs["Muon_phi"][good]


  
# W CANDIDATES
#
# Exactly one good muon + MET > 25 GeV
  

selection = (
    (ak.num(good_pt) == 1)
    & (arrs["MET_pt"] > 25)
)


good_pt = good_pt[selection]
good_phi = good_phi[selection]

MET_pt = arrs["MET_pt"][selection]
MET_phi = arrs["MET_phi"][selection]


  
# CHOOSE ONE EVENT
  

event_number = 100

muon_pt = float(good_pt[event_number, 0])
muon_phi = float(good_phi[event_number])

met_pt = float(MET_pt[event_number])
met_phi = float(MET_phi[event_number])


  
# CONVERT TO x-y MOMENTUM
  

muon_px = muon_pt * np.cos(muon_phi)
muon_py = muon_pt * np.sin(muon_phi)

met_px = met_pt * np.cos(met_phi)
met_py = met_pt * np.sin(met_phi)


  
# PRINT EVENT INFORMATION
  

print("===================================")
print("W CANDIDATE EVENT")
print("===================================")

print(f"Muon pT      = {muon_pt:.2f} GeV")
print(f"Muon phi     = {muon_phi:.2f} rad")

print(f"MET          = {met_pt:.2f} GeV")
print(f"MET phi      = {met_phi:.2f} rad")

print("-----------------------------------")

print(f"Muon px      = {muon_px:.2f} GeV")
print(f"Muon py      = {muon_py:.2f} GeV")

print(f"Missing px   = {met_px:.2f} GeV")
print(f"Missing py   = {met_py:.2f} GeV")


  
# DRAW EVENT
  

plt.figure(figsize=(9, 9))

ax = plt.gca()

# Muon vector

ax.arrow(
    0,
    0,
    muon_px,
    muon_py,
    width=0.5,
    head_width=3,
    head_length=5,
    length_includes_head=True,
    label="Muon"
)


# Missing momentum / neutrino candidate

ax.arrow(
    0,
    0,
    met_px,
    met_py,
    width=0.5,
    head_width=3,
    head_length=5,
    length_includes_head=True,
    label="Missing transverse momentum"
)


# Labels

ax.text(
    muon_px * 1.05,
    muon_py * 1.05,
    "Muon μ",
    fontsize=13
)

ax.text(
    met_px * 1.05,
    met_py * 1.05,
    "ν candidate\n(MET)",
    fontsize=13
)


# Origin

ax.scatter(
    0,
    0,
    s=100
)


# Axis

ax.axhline(
    0,
    linewidth=1
)

ax.axvline(
    0,
    linewidth=1
)


# Make limits large enough for both arrows

maximum = max(
    np.sqrt(muon_px**2 + muon_py**2),
    np.sqrt(met_px**2 + met_py**2)
)

limit = maximum * 1.4

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)


ax.set_aspect("equal")

ax.set_xlabel(r"$p_x$ (GeV)")
ax.set_ylabel(r"$p_y$ (GeV)")

ax.set_title(
    r"W candidate event: $W \rightarrow \mu\nu$"
)

ax.grid(alpha=0.3)

ax.legend()

plt.tight_layout()

plt.savefig(
    "fig/result/neutrino_event_display.png",
    dpi=200
)

plt.show()