"""
Authors Thomas Linker @tlinker123.
Edited by Taufeq Razakh @TaufeqRazakh


Example Usage:
python rep.py 2 2 2

"""

import ase
import ase.io
import numpy as np
import ase.build
from ase import Atoms
import sys
#print (sys.argv)
commands=sys.argv
if(len(sys.argv)!=4) :
    print(' User must supply nx ny nz replication')
    raise('GOOD BYE')
a=3.9690490000000000
nx=int(commands[1])
ny=int(commands[2])
nz=int(commands[3])
rep=[nx,ny,nz]
atoms_unit = Atoms('TiPbO3',
              pbc=True,
              cell=(a, a, a),
              positions=[(a/2, a/2, a/2),
                         (0, 0, 0),
                         (a/2, 0, a / 2),
                         (a / 2, a / 2, 0),
                          (0,a / 2,a / 2)])
mat=np.zeros((3,3),dtype=np.int64)
for i in range(3) :
    mat[i,i]=rep[i]
atoms=ase.build.make_supercell(atoms_unit,mat)
atoms.center()
real_pos=atoms.get_positions()
scaled_pos=atoms.get_scaled_positions()
types=atoms.get_chemical_symbols()
MD_CELL=atoms.get_cell()
print('MD CELL ')
print(MD_CELL.array)
natoms=len(types)
ids=[]
for i in range(natoms) :
    if(types[i]=='Ti') :
        ids.append(1)
    elif(types[i]=='Pb') :
        ids.append(2)
    elif(types[i]=='O') :
        ids.append(3)
outfile='IN.CONFIG_REAL'
write_file=open(outfile,'w')
print('File opened :' + outfile) 
write_file.write("%s\n" %(str(natoms)))
for i in range(natoms) :
    x=real_pos[i,0]
    y=real_pos[i,1]
    z=real_pos[i,2]
    name=str(ids[i])
    write_file.write("%2s  %12.8f %12.8f %12.8f\n" %(name,x,y,z))
write_file.close()
outfile='IN.CONFIG_SCALED'
write_file=open(outfile,'w')
print('File opened :' + outfile) 
write_file.write("%s\n" %(str(natoms)))
for i in range(natoms) :
    x=scaled_pos[i,0]
    y=scaled_pos[i,1]
    z=scaled_pos[i,2]
    name=str(ids[i])
    write_file.write("%2s  %12.8f %12.8f %12.8f\n" %(name,x,y,z))
write_file.close()
ase.io.write('out.xyz',atoms)