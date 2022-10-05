# Have all your CONFIG-n-n-n.xyz files in the same working directory as this script.
# The script will take the original XYZ file and convert into a DCEHD readable CONFIG
# The script requires two arguments. It also shifts the co-ordinatyes in the by bix lenght when co-ordinates exceed the lattice size.

# @param .xyz file which needs to be converted to CONFIG for dcehd
# @param output file which needs to be generated

if ARGV.length != 2 
  puts "Pass in 2 file names as arguments"
  exit
end

INPUT_CONFIG_FILE = ARGV[0] # xyz file to read
OUTPUT_CONFIG_FILE = ARGV[1] # .dc file to write

unless File::exist?(INPUT_CONFIG_FILE)
  puts "The input file specified does not exist"
  exit
end

INPUT_FILE = File.open(INPUT_CONFIG_FILE, File::RDONLY)
OUTPUT_FILE = File.open(OUTPUT_CONFIG_FILE, File::RDWR | File::CREAT)

@lattice_size=[7.8047, 7.804, 8.312] # lattice dimension in x,y,z. Will be overwritten by lattice size in .xyz file

def write_line_to_file(line, file)
  file.write(line)
end

def get_lattice_constrained_coords(input_coords)
  size_coords_zip = @lattice_size.zip(input_coords)
  lattice_constrained_coords = size_coords_zip.map {|c|
    if (c[1] > 0 && c[1] < c[0]) then c[1]
    elsif(c[1] > c[0]) then (c[1] - c[0]).round(9)
    else (c[1] + c[0]).round(9)
    end
  }
  puts "#{@lattice_size}, #{input_coords}, #{lattice_constrained_coords}"
  return lattice_constrained_coords
end

INPUT_FILE.each do |line|  
  if (INPUT_FILE.lineno == 2)
    # take the lattice dimensions from the file in the second line
    lattice_matrix_scan = line.scan(/Lattice=.(\d+.*)"/)
    # puts "#{lattice_matrix_scan}"
    lattice_matrix = lattice_matrix_scan[0][0]
    lattice_matrix_elems = lattice_matrix.split(/\s+/)
    
    lx = lattice_matrix_elems[0].to_f
    ly = lattice_matrix_elems[4].to_f
    lz = lattice_matrix_elems[8].to_f
    @lattice_size = [lx, ly, lz]

  elsif (INPUT_FILE.lineno > 2)
    # limit the co-ordinates to lattice dimension and write
    patricle_type_coordinates = line.split(/\s/)
    input_coordinates = patricle_type_coordinates.drop(1)
    input_coordinates = input_coordinates.map{ |v| v.to_f }
    final_coordinates = get_lattice_constrained_coords(input_coordinates)
    write_line_to_file(final_coordinates.join(" ")+"\n", OUTPUT_FILE)
  else
    write_line_to_file(line, OUTPUT_FILE)
  end
end

unless INPUT_FILE.closed? then INPUT_FILE.close end
unless OUTPUT_FILE.closed? then OUTPUT_FILE.close end
