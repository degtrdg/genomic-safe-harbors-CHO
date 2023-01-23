# Genomic Safe Harbors for CHO

## Index

- [Genomic Safe Harbors for CHO](#genomic-safe-harbors-for-cho)
	- [Index](#index)
	- [Description](#description)
	- [Prerequisites](#prerequisites)
	- [Data](#data)
	- [Usage](#usage)
	- [Reference](#reference)

## Description

Python implementation of https://github.com/elvirakinzina/GSH extended to the Chinese Hamster Ovary genome. Can easily be extended to other genomes through changing files in data folder. Note: this is a WIP and only takes into account the annotations in the annotation file. If the annotation file is incomplete, the safe harbors will be incomplete. I have not finished confirming that the annotations contain all known instances of each feature.

Pipeline that takes in genome (FASTA) and annotation (GTF) files and outputs genomic safe harbors with FASTA and BED files.

The default parameters are set to the following:

- 50kb away from known genes
- 300kb away from known oncogenes
- 300kb away from microRNAs, centromeres, telomeres, genomic gaps
- 150kb away from lncRNAs, tRNAs
- 20kb away from enhancers

## Prerequisites

- gtf2bed from BEDOPS https://bedops.readthedocs.io/en/latest/content/installation.html#installation
- bedtools https://bedtools.readthedocs.io/en/latest/content/installation.html

## Data

- Genome and annotation files in FASTA and GTF format
  - data was downloaded from https://www.ncbi.nlm.nih.gov/data-hub/genome/GCF_000223135.1/ for the chinese hamster ovary cell line (CHO). The zip file can be found in the `data` folder.

## Usage

Run this at first:

```bash
chmod +x safe_harbor.py
```

Usage:

```bash
  ./safe_harbor.py [-dist_from_genes] [-dist_from_oncogenes] [-dist_from_micrornas] [-dist_from_trnas] [-dist_from_lncrnas] [-dist_from_enhancers] [-dist_from_centromeres] [-dist_from_gaps] [-h|--help]
```

Options:

```bash
    -fastq: FASTA file of genome
    -gtf: GTF file of genome

	-dist_from_genes: Minimal distance from any safe harbor to any gene in bp (default=50000)
	-dist_from_oncogenes: Minimal distance from any safe harbor to any oncogene in bp (default=300000)
	-dist_from_micrornas: Minimal distance from any safe harbor to any microRNA in bp (default=300000)
	-dist_from_trnas: Minimal distance from any safe harbor to any tRNA in bp (default=150000)
	-dist_from_lncrnas: Minimal distance from any safe harbor to any long-non-coding RNA in bp (default=150000)
	-dist_from_enhancers: Minimal distance from any safe harbor to any enhancer in bp (default=20000)
	-dist_from_centromeres: Minimal distance from any safe harbor to any centromere in bp (default=300000)
	-dist_from_gaps: Minimal distance from any safe harbor to any gaps in bp (default=300000)
	-h, --help: Prints help
```

Running with the default parameters:

```bash
chmod +x safe_harbor.py
./safe_harbor.py -fastq data/GCF_000223135.1_ChoWGS_1.0_genomic.fna -gtf data/GCF_000223135.1_ChoWGS_1.0_genomic.gtf
```

Output:

```bash

Creating reference files
Creating flanks for genes
Creating flanks for oncogenes
Creating flanks for mirnas
Creating flanks for trnas
Creating flanks for lncrnas
Creating flanks for enhancers
Creating flanks for centromeres
Creating flanks for telomeres
Sorting and merging flanked annotations
Taking safe harbors

```

The output is two files: Safe_harbors.bed that has genomic coordinates of all regions potentially containing safe harbors and Safe_harbors.fasta contains sequences of these regions.

## Reference

Aznauryan et al. (2022), Discovery and validation of novel human genomic safe harbor sites for gene and cell therapies. Cell Genomics

```

```
