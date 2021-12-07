def write_coord(coords, iteration, Au_coord):
  f = open('../test/coords_IT%s.xyz'%(str(iteration)), 'w')
  N_atoms = len(coords)+len(Au_coord)
  f.write(" %d \n"%(N_atoms))
  f.write("coordinates At:%s Au: %s \n"%(str(len(coords)), len(Au_coord)))
  for atom in coords:
    f.write(" %s   %15.9f  %15.9f  %15.9f \n"%('At',atom[0],atom[1],atom[2]))
  for atom in Au_coord:
    f.write(" %s   %15.9f  %15.9f  %15.9f \n"%('Au',atom[0],atom[1],atom[2]))
  f.close()
