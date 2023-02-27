#!/usr/bin/env python
# Run this at first: chmod +x safe_harbor.py 
# Adapted from https://github.com/elvirakinzina/GSH

import argparse
import os
from pathlib import Path

def create_flanks(gtf,dist,folder,pattern):
    print(f"Creating flanks for {folder}")
    os.mkdir(f"tmp/{folder}")
    cur_dir = Path.cwd()/f"tmp/{folder}/"
    # Get pattern
    os.system(f'less {gtf} | grep "{pattern}" >> {cur_dir}/{folder}_annotation.gtf')
    # Get transcripts
    os.system(f'awk \'{{ if ($0 ~ "transcript_id") print $0; else print $0" transcript_id \\"\\";"; }}\' {cur_dir}/{folder}_annotation.gtf >> {cur_dir}/{folder}_transcript_id.gtf')
    # GTF to BED
    os.system(f'gtf2bed --do-not-sort < {cur_dir}/{folder}_transcript_id.gtf | awk -v OFS="\\t" \'{{print $1, $2, $3}}\' >> {cur_dir}/{folder}_annotation.bed')
    # Get regions of length dist base pairs flanking from both sides
    os.system(f'bedtools slop -b {dist} -i {cur_dir}/{folder}_annotation.bed -g {os.getcwd()}/tmp/reference/chromInfo.txt >> {cur_dir}/{folder}_annotation_w_flanks.bed')

def run(a):
    os.mkdir("tmp")
    os.mkdir("tmp/reference")
    fastq = Path(a.fastq)
    gtf = Path(a.gtf)

    cur_dir = Path.cwd()/"tmp/reference/"
    print("Creating reference files")
    # Create .fai file
    os.system(f'samtools faidx {fastq} -o {cur_dir/fastq.name}.fai')
    # Create chromInfo file
    os.system(f"awk -v OFS='\\t' '{{print $1,$2}}'   {cur_dir/fastq.name}.fai > {cur_dir}/chromInfo.txt")
    # Create BED file for reference
    os.system(f"awk 'BEGIN {{FS=\"\\t\"}}; {{print $1 FS \"0\" FS $2}}' {cur_dir/fastq.name}.fai > {cur_dir/fastq.name}.bed")

    # Folders for each annotation
    folders = ["genes", "oncogenes", "mirnas", "trnas", "lncrnas", "enhancers", "centromeres","telomeres"]
    # Patterns for each annotation escaped 
    patterns = ["\\tgene\\t", "oncogene", "miR", "tRNA", "lnc_\?RNA", "enhancer", "centromere", "telomere"]
    # Distances for each annotation
    distances = [a.dist_from_genes, a.dist_from_oncogenes, a.dist_from_mirnas, a.dist_from_trnas, a.dist_from_lncrnas, a.dist_from_enhancers, a.dist_from_centromeres, a.dist_from_gaps]

    # Iterate over folders, patterns, and distances
    for folder, pattern, dist in zip(folders, patterns, distances):
        create_flanks(gtf,dist,folder,pattern)
    
    # Iterate through flanked annotations and concatenate them
    for folder in folders:
        os.system(f'cat tmp/{folder}/{folder}_annotation_w_flanks.bed >> tmp/flanked_annotations.bed')

    
    # Sort and merge flanked annotations
    print("Sorting and merging flanked annotations")
    os.system(f'sortBed -i tmp/flanked_annotations.bed >> tmp/flanked_annotations_sorted.bed')
    os.system(f'bedtools merge -i tmp/flanked_annotations_sorted.bed >> tmp/flanked_annotations_merged.bed')

    print("Taking safe harbors")
    os.system(f'bedtools subtract -a {cur_dir/fastq.name}.bed -b tmp/flanked_annotations_merged.bed > Safe_harbors_with_alt.bed')

    # 

    # Get sequences of those regions
    os.system(f'bedtools getfasta -fi {fastq} -bed Safe_harbors_with_alt.bed > Safe_harbors.fasta')

    # Remove temporary files
    os.system(f'rm -r tmp')


def main():
    parser=argparse.ArgumentParser(description="Find Safe Harbor Sites")
    parser.add_argument("-fastq",help="Genome" ,dest="fastq", type=str, required=True)
    parser.add_argument("-gtf",help="Annotation of genome" ,dest="gtf", type=str, required=True)
    parser.add_argument("-dist_from_genes",help="Minimal distance from any safe harbor to any gene in bp (default=50000)" ,dest="dist_from_genes", type=int, default=50000)
    # Requires a list of oncogenes
    parser.add_argument("-dist_from_oncogenes",help="Minimal distance from any safe harbor to any oncogene in bp (default=300000)" ,dest="dist_from_oncogenes", type=int, default=300000)
    parser.add_argument("-dist_from_mirnas",help="Minimal distance from any safe harbor to any microRNA in bp (default=300000)" ,dest="dist_from_mirnas", type=int, default=300000)
    parser.add_argument("-dist_from_trnas",help="Minimal distance from any safe harbor to any tRNA in bp (default=150000)" ,dest="dist_from_trnas", type=int, default=150000)
    parser.add_argument("-dist_from_lncrnas",help="Minimal distance from any safe harbor to any long-non-coding RNA in bp (default=150000)" ,dest="dist_from_lncrnas", type=int, default=150000)
    parser.add_argument("-dist_from_enhancers",help="Minimal distance from any safe harbor to any enhancer in bp (default=20000)" ,dest="dist_from_enhancers", type=int, default=20000)
    parser.add_argument("-dist_from_centromeres",help="Minimal distance from any safe harbor to any centromere in bp (default=300000)" ,dest="dist_from_centromeres", type=int, default=300000)
    # Gaps in this case only includes telomeres
    parser.add_argument("-dist_from_gaps",help="Minimal distance from any safe harbor to any gaps in bp (default=300000)" ,dest="dist_from_gaps", type=int, default=300000)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()