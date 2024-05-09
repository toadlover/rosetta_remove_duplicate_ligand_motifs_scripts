#Ari Ginsparg
#5/9/2024
#This script is used by remove_duplicate_motifs_helper.job to automate the calling and running of Rosetta's remove_duplicate_motifs executable on a given motifs file

import os, sys

file = sys.argv[1]

#remove_duplicate_motifs executable (ideally with path leading up to it)
rdm_executable = sys.argv[2]

#maximum number of motifs to include in a smaller file (ideally 100,000-1,000,000)
chunk_size = int(sys.argv[3])

#double chunk size since motifs are 2 lines long, that way we have the right number of motifs in each file
motif_chunk_size = chunk_size * 2

#get number of motifs in the file (line count / 2)
os.system("wc -l " + file + " >> temp_line_number_holder.txt")


line_number_file = open("temp_line_number_holder.txt", "r")

for line in line_number_file.readlines():
	line_number_count = int(line.split()[0])

motif_count =  int(line_number_count / 2)

os.system("rm temp_line_number_holder.txt")
#print(motif_count, line_number_count)

#read through the main motif file, and break it into files of 1 million motifs per file
line_counter = 1
motif_file = open(file, "r")

file_prefix = file.split(".")[0]


current_out_file = open(file_prefix + "_" + str(chunk_size) + "_0.motifs", "w")
for line in motif_file.readlines():
	
	#print(line_counter, file_number)

	current_out_file.write(line)

	#output the motif to a corresponding file, get the modulus of the line counter and make new file when mod of line counter and 2 million is 0
	if line_counter % motif_chunk_size == 0:
		file_number = int(line_counter / motif_chunk_size)
		current_out_file.close()
		current_out_file = open(file_prefix + "_" + str(chunk_size) + "_" + str(file_number) + ".motifs", "w")

		#fire off a job to remove duplicate motifs from the closed motif file (and make a slurm job/arg file)
		job_file = open(file_prefix + "_" + str(file_number - 1) +  ".job", "w")
		job_file.write("#!/bin/bash\n")
		job_file.write("#SBATCH -p short # Partition to submit to\n")
		job_file.write("#SBATCH -n 1 # Number of cores requested\n")
		job_file.write("#SBATCH -N 1 # Ensure that all cores are on one machine\n")
		job_file.write("#SBATCH -t 720 # Runtime in minutes\n")
		job_file.write("#SBATCH --mem=30000 # Memory per cpu in MB (see also --mem-per-cpu)\n")
		job_file.write("#SBATCH -o " + file_prefix + "_" + str(file_number - 1) + "_remove_duplicates_hostname_%A_%a.out # Standard out goes to this file\n")
		job_file.write("#SBATCH -e " + file_prefix + "_" + str(file_number - 1) + "_remove_duplicates_hostname_%A_%a.err # Standard out goes to this file\n")
		job_file.write(rdm_executable + " @" + file_prefix + "_" + str(file_number - 1) + "_args\n")
		job_file.close()
		arg_file = open(file_prefix + "_" + str(file_number - 1) + "_args", "w")
		arg_file.write("-parser:protocol lite_enzdes.xml\n")
		arg_file.write("-out::overwrite true\n")
		arg_file.write("-motif_filename " + file_prefix + "_" + str(chunk_size) + "_" + str(file_number - 1) + ".motifs\n")
		arg_file.write("-output_file " + file_prefix + "_" + str(chunk_size) + "_duplicates_removed_" + str(file_number - 1) + ".motifs\n")
		arg_file.write("-duplicate_dist_cutoff 0.8\n")
		arg_file.write("-duplicate_angle_cutoff 0.3\n")
		arg_file.close()
		os.system("sbatch " + file_prefix + "_" + str(file_number - 1) +  ".job")

	line_counter = line_counter + 1

current_out_file.close()

#print(line_counter)

#if there are no motifs left (clean break off of previous file), don't make a new file that won'd remove duplicates off of anything
if line_counter % motif_chunk_size == 1 or line_counter % motif_chunk_size == 0:
    quit()

#fire off a job to remove duplicate motifs from the closed motif file (and make a slurm job/arg file) for final  motif file
job_file = open(file_prefix + "_" + str(file_number) +  ".job", "w")
job_file.write("#!/bin/bash\n")
job_file.write("#SBATCH -p short # Partition to submit to\n")
job_file.write("#SBATCH -n 1 # Number of cores requested\n")
job_file.write("#SBATCH -N 1 # Ensure that all cores are on one machine\n")
job_file.write("#SBATCH -t 720 # Runtime in minutes\n")
job_file.write("#SBATCH --mem=30000 # Memory per cpu in MB (see also --mem-per-cpu)\n")
job_file.write("#SBATCH -o " + file_prefix + "_" + str(file_number) + "_remove_duplicates_hostname_%A_%a.out # Standard out goes to this file\n")
job_file.write("#SBATCH -e " + file_prefix + "_" + str(file_number) + "_remove_duplicates_hostname_%A_%a.err # Standard out goes to this file\n")
job_file.write(rdm_executable + " @" + file_prefix + "_" + str(file_number) + "_args\n")
job_file.close()
arg_file = open(file_prefix + "_" + str(file_number) + "_args", "w")
arg_file.write("-parser:protocol lite_enzdes.xml\n")
arg_file.write("-out::overwrite true\n")
arg_file.write("-motif_filename " + file_prefix + "_" + str(chunk_size) + "_" + str(file_number) + ".motifs\n")
arg_file.write("-output_file " + file_prefix + "_" + str(chunk_size) + "_duplicates_removed_" + str(file_number) + ".motifs\n")
arg_file.write("-duplicate_dist_cutoff 0.8\n")
arg_file.write("-duplicate_angle_cutoff 0.3\n")
arg_file.close()
os.system("sbatch " + file_prefix + "_" + str(file_number) +  ".job")
