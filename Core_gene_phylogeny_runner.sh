#!/bin/bash

gff_dir=$1
outdir=$2
threads=$3

panaroo -i $gff_dir/* -o $outdir -t $threads --clean-mode moderate -a core --core_threshold 0.9999
cd $outdir
modeltest_roary_core_gene_alignment.py core_gene_alignment.aln core_alignment_header.embl $threads core_gene_alignment
XMFA_create.py core_gene_alignment.partitions.txt $outdir/aligned_gene_sequences
iqtree -s core_gene_alignment.aln -p core_gene_alignment.partitions.txt -m GTR+I+F+R4 -T $threads
ClonalFrameML core_gene_alignment.partitions.txt.treefile core_aln.xmfa core_gene_alignment.partitions.cfml.em -em true -emsim 100 -xmfa_file true
maskrc-svg.py --aln core_gene_alignment.aln --out core_gene_alignment.rc_masked.aln --svg core_gene_alignment.rc_masked.svg core_gene_alignment.partitions.cfml.em

modeltest_roary_core_gene_alignment.py core_gene_alignment.rc_masked.aln core_alignment_header.embl $threads core_gene_alignment.rc_masked.filtered
iqtree -s core_gene_alignment.rc_masked.filtered.aln -p core_gene_alignment.rc_masked.filtered.partitions.txt -T $threads -B 1000 --prefix core_gene_alignment.rc_masked.filtered 
FastRoot.py -i core_gene_alignment.rc_masked.filtered.treefile -o core_gene_alignment.rc_masked.filtered.mvroot.treefile
