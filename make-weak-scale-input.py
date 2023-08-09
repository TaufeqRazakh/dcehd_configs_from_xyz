import numpy as np
nx_md=16
ny_md=16
nz_md=16

nx_buffer=1
ny_buffer=1
nz_buffer=1


nx_core=1
ny_core=1
nz_core=1

nx_core_buffer=nx_core+nx_buffer
ny_core_buffer=ny_core+ny_buffer
nz_core_buffer=nz_core+nz_buffer

n_Pb=1
n_Ti=1
n_O=3

unit_cell=np.array([[3.91,0.0,0.0], [0.0,3.91,0.0],[0.0,0.0,4.156]])
pos=np.array([ [   3.909999504,         3.909999504,       4.146000],
     [1.940999975  ,      1.940999975 ,      2.224681],
     [1.940999975  ,      1.940999975,       0.454640],
     [3.909999504  ,       1.940999975 ,      2.555914],
     [1.940999975  ,     3.909999504  ,     2.555914]])
natom_unit=pos.shape[0]
for i in range(natom_unit) :
	pos[i,:]=np.linalg.inv(unit_cell).dot(pos[i,:])
#print(pos)
#print(unit_cell)
#natom_unit=pos.shape[0]
print('Total Number of atoms')
print((n_Pb+n_Ti +n_O)*nx_core*ny_core*nz_core*nx_md*ny_md*nz_md)
print('MD nodes')
print((nx_md,ny_md,nz_md))

print('MD cell ')
MD_cell=unit_cell.copy()
MD_cell[0,:]=unit_cell[0,:]*nx_md*nx_core
MD_cell[1,:]=unit_cell[1,:]*ny_md*ny_core
MD_cell[2,:]=unit_cell[2,:]*nz_md*nz_core
print(MD_cell)
print('Super cell ')
MD_cell=unit_cell.copy()
MD_cell[0,:]=unit_cell[0,:]*nx_core_buffer
MD_cell[1,:]=unit_cell[1,:]*ny_core_buffer
MD_cell[2,:]=unit_cell[2,:]*nz_core_buffer
print(MD_cell)

print('Species : Pb')
print('Number of Atoms')
number_atoms_Pb=n_Pb*nx_md*ny_md*nz_md*nx_core*ny_core*nz_core
print(number_atoms_Pb)
number_repilications_Pb_x=nx_md*nx_core
number_repilications_Pb_y=ny_md*ny_core
number_repilications_Pb_z=nz_md*nz_core
print('Positions ')
print((number_repilications_Pb_x,number_repilications_Pb_y,number_repilications_Pb_z))
print(pos[0,:])

print('Species : Ti')
print('Number of Atoms')
number_atoms_Ti=n_Ti*nx_md*ny_md*nz_md*nx_core*ny_core*nz_core
print(number_atoms_Ti)
number_repilications_Ti_x=nx_md*nx_core
number_repilications_Ti_y=ny_md*ny_core
number_repilications_Ti_z=nz_md*nz_core
print('Positions ')
print((number_repilications_Ti_x,number_repilications_Ti_y,number_repilications_Ti_z))
print(pos[1,:])



print('Species : O')
print('Number of Atoms')
number_atoms_O=n_O*nx_md*ny_md*nz_md*nx_core*ny_core*nz_core
print(number_atoms_O)
number_repilications_O_x=nx_md*nx_core
number_repilications_O_y=ny_md*ny_core
number_repilications_O_z=nz_md*nz_core
print('Positions ')
print((number_repilications_O_x,number_repilications_O_y,number_repilications_O_z))
print(pos[2,:])
print(pos[3,:])
print(pos[4,:])

'''
for i in range(natom_unit) :
	pos[i,:]=np.linalg.inv(unit_cell).dot(pos[i,:])
#print(pos)
'''
