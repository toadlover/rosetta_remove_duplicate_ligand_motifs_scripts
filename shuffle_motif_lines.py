import os, sys, random

file = sys.argv[1]

read_motifs_file = open(file, "r")

file_name = file.split(".")[0]

random_order_motifs_file = open(file_name +  "_randomized.motifs", "w")

all_motifs = []

for line in read_motifs_file.readlines():
	if line.startswith("SINGLE"):
		motif_line = line
	if line.startswith("RT"):
		rt_line = line

		full_motif = [motif_line,rt_line]
		all_motifs.append(full_motif)

random.shuffle(all_motifs)

for motif in all_motifs:
	random_order_motifs_file.write(motif[0])
	random_order_motifs_file.write(motif[1])
