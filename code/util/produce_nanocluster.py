import numpy as np

lat_param = 4.08
R = 50
bas = [[0.0, 0.0, 0.0], [0.0, lat_param/2, lat_param/2], [-lat_param/2, 0.0, lat_param/2], [-lat_param/2, lat_param/2, 0.0]]
origin = [0.0, 0.0, 0.0]
N = int(R/lat_param) + 5
atoms = []
for x in range(-N,N):
    for y in range(-N,N):
        for z in range(-N,N):
            for bas_element in bas:
                atomcoord = lat_param*np.array([x,y,z])+bas_element
                atoms.append(atomcoord)

print(len(atoms))
atoms_filtered = []
for atom in atoms:
  r_atom = np.sqrt(atom[0]**2.0 + atom[1]**2.0 + atom[2]**2.0)
  if r_atom < R:
    atoms_filtered.append(atom)
print(len(atoms_filtered))

f = open('./coords_r%s.xyz'%(str(R/10)), 'w')
N_atoms = len(atoms_filtered)
f.write(" %d \n"%(N_atoms))
f.write(" nanocluster %.1f nm \n"%(R/10))
for atom in atoms_filtered:
  f.write(" %s   %15.9f  %15.9f  %15.9f \n"%('Au',atom[0],atom[1],atom[2]))
f.close()
