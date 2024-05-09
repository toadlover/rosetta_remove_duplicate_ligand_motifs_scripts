# rosetta_remove_duplicate_ligand_motifs_scripts
This repository serves to host scripts and tutorials as a companion for using the remove_duplicate_motifs app in Rosetta.

I have set these scripts up to break up a list of millions of motifs into sections of up to 500,000 motifs, and then run the Rosetta duplicate motif removal script to remove duplicate motifs. The smaller lists are used because the runtimes of the duplicate removal script are unreasonably long on multiple millions of motifs at once. The logic of this pipeline is to randomize the main list of motifs, and break up the list into multiple lists of 500k motifs to run duplicate removal on. The smaller lists with duplicates removed are spliced back into a single list. This order of motifs are randomly shuffled again and then the process repeats for breaking up the list, removing duplicates, and splicing.

The pipeline is currently written to be run on a slurm job scheduler, but the slurm jobs can be adapted to other job schedulers. Ideally, the runs of the duplicate motif removal are conducted in parallel.
