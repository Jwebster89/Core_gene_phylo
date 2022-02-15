#!/usr/bin/env python
import re, sys, os, subprocess, shutil
from Bio import AlignIO
from Bio.Seq import Seq

file=sys.argv[1]
dir=sys.argv[2]

def read_partitions(file):
	passed_partitions=[]
	with open(file, 'r') as fh:
		for line in fh:
			if line.startswith("\tcharset"):
				split=line.split(" ")
				passed_partitions.append(split[1]+".aln")
	return(passed_partitions)


def create_xmfa(dir,parts):
	with open("core_aln.xmfa",'w') as out_h:
		for part in parts:
			with open(os.path.join(dir,part), 'r') as in_h:
				shutil.copyfileobj(in_h,out_h)
				out_h.write("\n=\n")

def create_aln_gapped(dir,parts):
	with open("core_gene_alignment.gappend.aln",'w') as out_h:
		i=0
		gaps='-'*1000
		gaps_seq=Seq(gaps)
		for part in parts:
			alignment = AlignIO.read(os.path.join(dir,part), "fasta")
			alignment.sort()
			for seqrecord in alignment:
				seqrecord.seq=seqrecord.seq+gaps
			if i==0:
				cat_algn = alignment
			else:
				cat_algn += alignment
			i += 1
		AlignIO.write(cat_algn, out_h, "fasta")

def fix_header():
	with open("core_aln.xmfa",'r') as in_h:
		with open("core_aln_headerfixed.xmfa", "w") as out_h:
			lines = in_h.readlines()
			for line in lines:
				replaced=re.sub(';.*','',line)
				out_h.write(replaced)

alns=read_partitions(file)
create_xmfa(dir,alns)
create_aln_gapped(dir,alns)
fix_header()
