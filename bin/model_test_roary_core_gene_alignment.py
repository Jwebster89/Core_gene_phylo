#!/usr/bin/env python

#run using output of roary
#run as python modeltest_roary_core_gene_alignment.py core_gene_alignment.aln core_alignment_header.embl threads output_partition_file

from Bio import AlignIO, SeqIO
import sys, os, subprocess, gzip, glob, shutil
from collections import defaultdict

aln = AlignIO.read(sys.argv[1], 'fasta')
partitions = SeqIO.read(sys.argv[2], 'embl')
threads = sys.argv[3]
output_prefix = sys.argv[4]
outdir = ".tmp"
if os.path.isdir(outdir):
	shutil.rmtree(outdir)

os.mkdir(outdir)

print("Identifying partitions...")
for feat in partitions.features:
	out_aln = aln[:, int(feat.location.start):int(feat.location.end)]
	AlignIO.write(out_aln, os.path.join(outdir, "{}".format(feat.qualifiers["label"][0])), 'fasta')

paths = [ os.path.join(outdir, x) for x in os.listdir(outdir) ]

print("Running model tests...")
subprocess.run(['parallel', '-j', threads, '--bar', 'iqtree', '--quiet', '-m', 'TESTONLY', '-s', '{}', ':::'] + paths)

print("Extracting best BIC model...")
model_data = defaultdict(dict)
failed_modeltest = []
for gene_aln_file in paths:
	model_data_file = gene_aln_file + '.model.gz'
	if os.path.isfile(model_data_file) == True:
		with gzip.open(model_data_file, 'rt') as model_data_handle:
			for line in model_data_handle:
				k = line.split(':')[0]
				v = line.strip().replace("{}: ".format(k), '')
				model_data[os.path.basename(gene_aln_file)][k] = v
	else:
		failed_modeltest.append(os.path.basename(gene_aln_file))

print("Output failed partitions...")
with open(output_prefix + ".failed.genes.txt", 'w') as out:
	for file in failed_modeltest:
		out.write(file + '\n')


print("Writing partition file...")
with open(output_prefix + '.partitions.txt', 'w') as out:
	out.write('#nexus\nbegin sets;\n')
	partition_models = []
	first_gene = True
	for feat in partitions.features:
		if not feat.qualifiers["label"][0] in failed_modeltest:
			if first_gene == True:
				start = 0
				end = (int(feat.location.end)-int(feat.location.start))
				out_aln = aln[:, int(feat.location.start):int(feat.location.end)]
				first_gene = False
			else:
				start = end
				end += (int(feat.location.end)-int(feat.location.start))
				out_aln += aln[:, int(feat.location.start):int(feat.location.end)]
			out.write('\tcharset {} = {}-{};\n'.format(os.path.splitext(feat.qualifiers["label"][0])[0], start+1, end))
			partition_models.append("{}:{}".format(model_data["{}".format(feat.qualifiers["label"][0])]['best_model_BIC'], os.path.splitext(feat.qualifiers["label"][0])[0]))
	out.write('\tcharpartition mine = {};\nend;\n'.format(', '.join(partition_models)))
	AlignIO.write(out_aln, output_prefix + '.aln', 'fasta')


#shutil.rmtree(outdir)
print("Done.")
