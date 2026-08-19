import uproot

file = uproot.open("C:/cern/opendata/raw/01AB9889-63BA-4171-9842-85AC4E0987DE.root")

print(file.keys())

# print branches
tree = file["Events"]
print(tree.keys())