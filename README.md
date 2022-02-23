# Core_gene_phylo
Repository for code to create bacterial core gene phylogenies

Core_gene_phylo uses Panaroo to identify core genes in all isolates and performs model testing on all partitions with IQtree.
ClonalFrameML is then used to filter recombination in passed partitions and a bootstrap replicate tree is inferred with IQtree and minVar rooted with FastRoot.


## Installation and dependancies

Install dependancies with conda and pip:

```
conda create -n core_gene_phylo_env python=3 biopython=1.79 panaroo=1.2.9 iqtree=2.1.2 clonalframeml=1.12 ete3 bcbio-gff svgwrite dos2unix
```
Or
```
conda env create -f environment.yml
```
Once environment has been created.
```
conda activate core_gene_phylo_env
pip install FastRoot
dos2unix $(which FastRoot.py)
git clone --recurse-submodules https://github.com/Jwebster89/Core_gene_phylo.git
cd Core_gene_phylo
python setup.py install
```
## Output
Final output from Core_gene_phylo is `core_gene_alignment.rc_masked.filtered.mvroot.treefile` a minvar rooted, bootstrap replicate tree. 
This tree is composed of core genes from panaroo that have  passed model testing in IQ tree and have been through recombination filtering.

Other files of interest include:
* core_gene_alignment.rc_masked.filtered.aln:
	* The filtered alignment used for tree building
* core_gene_alignment.aln
	* The core gene alignment output from Panaroo
* gene_presence_absence.csv
	* Pangenome results from Panaroo


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
