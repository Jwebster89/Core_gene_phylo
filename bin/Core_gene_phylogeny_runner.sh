#!/bin/bash

gff_dir=$1
outdir=$2
threads=$3

if [ ! -e $outdir/core_gene_alignment.aln ]; then
panaroo -i $gff_dir/* -o $outdir -t $threads --clean-mode strict -a core --core_threshold 0.9999 || exit 1
fi
cd $outdir

if [ ! -e core_gene_alignment.partitions.txt ]; then
model_test_roary_core_gene_alignment.py core_gene_alignment.aln core_alignment_header.embl $threads core_gene_alignment || exit 1
fi

if [ ! -e core_gene_alignment.partitions.txt.treefile ]; then
iqtree -s core_gene_alignment.aln -p core_gene_alignment.partitions.txt -m GTR+I+F+R4 -T $threads || exit 1
fi

if [ ! -e core_aln_headerfixed.xmfa ]; then
XMFA_create.py core_gene_alignment.partitions.txt $outdir/.tmp || exit 1
fi

if [ ! -e core_gene_alignment.partitions.cfml.em ]; then
ClonalFrameML core_gene_alignment.partitions.txt.treefile core_aln_headerfixed.xmfa core_gene_alignment.partitions.cfml.em -em true -emsim 100 -xmfa_file true || exit 1
fi

if [ ! -e core_gene_alignment.rc_masked.aln ]; then
maskrc-svg.py --aln core_gene_alignment.aln --out core_gene_alignment.rc_masked.aln --svg core_gene_alignment.rc_masked.svg core_gene_alignment.partitions.cfml.em || exit 1
fi

if [ ! -e core_gene_alignment.rc_masked.filtered.partitions.txt ]; then
model_test_roary_core_gene_alignment.py core_gene_alignment.rc_masked.aln core_alignment_header.embl $threads core_gene_alignment.rc_masked.filtered || exit 1
fi

if [ ! -e core_gene_alignment.rc_masked.filtered.treefile ]; then
iqtree -s core_gene_alignment.rc_masked.filtered.aln -p core_gene_alignment.rc_masked.filtered.partitions.txt -T $threads -B 1000 --prefix core_gene_alignment.rc_masked.filtered  || exit 1
fi

if [ ! -e core_gene_alignment.rc_masked.filtered.mvroot.treefile ]; then
FastRoot.py -i core_gene_alignment.rc_masked.filtered.treefile -o core_gene_alignment.rc_masked.filtered.mvroot.treefile || exit 1
fi
