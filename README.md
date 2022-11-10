## make-input.py
### Intro
Use this script to directly modify your *.dc file. 

Specify the ranks per node, unit cells (cores) per rank, buffer size, and species positions within the file. 
Note: Only works with PTO

## xyz_to_dc_config.rb
### Intro
Use this script to convert your Ovito replicated systems to the CONFIG file that fits in the lattice size that is specified in the MD cell for dcehd.

### Inputs
The program takes two command line arguments.

+ .xyz file which needs to be converted to CONFIG for dcehd
+ CONFIG file which needs to be generated

### Preferences
You may have to several xyz replicated files in the working directory such as
```
2-2-2
4-2-2
4-4-2
4-4-4
...
```
Pass each of the files as arguments to `xyz_to_dc_config.rb`.

### Previous Steps
There are two other tasks that you must complete before using this script. 

+ Change the MD cell size to the correct lattice size in the `*.dc` file that you are using
+ Develop the corresponding xyz file which is essentially a system whose lattice dimensions are the same as the MD. cell size.

### Run
use a ruby compiler to use this program. Here is an example usage `ruby xyz_to_dc_config.rb CONFIG-2-2-2.xyz CONFIG_1`
