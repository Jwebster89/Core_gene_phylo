from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "core_gene_phylo",
    version = "0.1",
    author = "Daniel Bogema, John Webster",
    author_email = "daniel.bogema@dpi.nsw.gov.au, john.webster@dpi.nsw.gov.au",
    description = ("Scripts to create bacterial core gene phylogenies"),
    license = "GPL-3.0",
    keywords = "genomics phylogenetics core-gene",
    url = "https://github.com/Jwebster89/Core_gene_phylo",
    py_modules=['core_gene_phylo'],
    scripts=['bin/core_gene_phylo', 'bin/Core_gene_phylogeny_runner.sh', 'bin/model_test_roary_core_gene_alignment.py', 'bin/XMFA_create.py', 'maskrc-svg/maskrc-svg.py','bin/version.py'],
    long_description=read('README.md'),
)