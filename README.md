# Core_gene_phylo
Repository for code to create bacterial core gene phylogenies

## Installation and dependancies

Install dependancies with conda and pip:

```
conda create -n core_gene_phylo_env python=3 biopython=1.79 panaroo=1.2.9 iqtree=2.1.2 clonalframeml=1.12 ete3 bcbio-gff svgwrite dos2unix
conda activate core_gene_phylo_env
pip install FastRoot
dos2unix $(which FastRoot.py)
git clone https://github.com/Jwebster89/Core_gene_phylo.git
cd Core_gene_phylo
python setup.py install
```

## Quick Usage
Core_gene_phylogeny_runner.sh requires a folder with gff files, an output directory and the number of threads.

```
usage: core_gene_phylo [-h] -g GFF_DIR -o OUTDIR [-t THREADS]

core_gene_phylo - Scripts to create bacterial core gene phylogenies.

optional arguments:
  -h, --help            show this help message and exit
  -g GFF_DIR, --gff-dir GFF_DIR
                        Path to a directory with your sample gff files.
  -o OUTDIR, --output-dir OUTDIR
                        Path to the output directory. A directory will be created if one does not exist.
  -t THREADS, --threads THREADS
                        Number of threads.
```
