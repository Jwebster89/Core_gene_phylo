#!/usr/bin/env python
import sys, os, subprocess, shutil

file=sys.argv[1]
dir=sys.argv[2]

def read_partitions(file):
	passed_partitions=[]
	with open(file, 'r') as fh:
		for line in fh:
			if line.startswith("\tcharset"):
				split=line.split(" ")
				passed_partitions.append(split[1]+".aln.fas")
	return(passed_partitions)


def create_xmfa(dir,parts):
	with open("core_aln.xmfa",'w') as out_h:
		for part in parts:
			with open(os.path.join(dir,part), 'r') as in_h:
				shutil.copyfileobj(in_h,out_h)
				out_h.write("\n=\n")

def fix_header():
	with open("core_aln.xmfa",'r') as in_h:
		with open("core_aln_headerfixed.xmfa", "w") as out_h:
			lines = in_h.readlines()
			for line in lines:
				replaced=re.sub(';.*','',line)
				out_h.write(replaced)

alns=read_partitions(file)
create_xmfa(dir,alns)
fix_header()
