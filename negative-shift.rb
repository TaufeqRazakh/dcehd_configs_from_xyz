# Move all negative co-ordinates in the DC-MESH CONFIG file to 
# real space positive-coordiantes along a co-ordinate axis

# @param read file
# @param write
# @param axis - can be one of [x,y,z]

if ARGV.length != 3 
  puts "Pass in 2 file names and 1 axis [x,y,z] to shift as arguments"
  exit
end

INPUT_CONFIG_FILE = ARGV[0] # CONFIG file to read
OUTPUT_CONFIG_FILE = ARGV[1] # CONFIG file to write
SHIFT_AXIS = ARGV[2] # axis to shift [x,y,z]
SHIFT_VAL = 0.5 # some small value to go beyond zero when shifting

unless File::exist?(INPUT_CONFIG_FILE)
  puts "The input file specified does not exist"
  exit
end

INPUT_FILE = File.open(INPUT_CONFIG_FILE, File::RDONLY)
OUTPUT_FILE = File.open(OUTPUT_CONFIG_FILE, File::RDWR | File::CREAT)

axes = {'x'=> 1, 'y'=> 2, 'z'=>3}
axis_number = axes[SHIFT_AXIS]

input_coordinate_elements = Array.new
INPUT_FILE.each	do |line|
	if(INPUT_FILE.lineno > 1)
		input_coordinate_elements.append(line.split[axes[SHIFT_AXIS]].to_f)
	end
end
negative_coordinate = input_coordinate_elements.min
# puts negative_coordinate

INPUT_FILE = File.open(INPUT_CONFIG_FILE, File::RDONLY)

INPUT_FILE.each	do |line|
	output_line = line
	if(INPUT_FILE.lineno > 1)
		coordinates=line.split
		final_coordinates = coordinates

		coordinate = coordinates[axes[SHIFT_AXIS]].to_f
		updated_coordinate = coordinate + negative_coordinate.abs + SHIFT_VAL
        
    final_coordinates[axes[SHIFT_AXIS]] = updated_coordinate.to_s
    output_line = final_coordinates.join(' ')+"\n"
	end
	OUTPUT_FILE.write output_line
end

unless INPUT_FILE.closed? then INPUT_FILE.close end
unless OUTPUT_FILE.closed? then OUTPUT_FILE.close end

