#! /usr/bin/env python

'''
modmap.nuc_frequencies
----------------------
calculate nucleotide frequencies at modified base sites. Reports a table
that is facetable by region size and position.
'''

import sys

from operator import itemgetter
from collections import Counter, defaultdict

from toolshed import reader
from pyfaidx import Fasta, complement

from common import load_coverage

__author__ = 'Han Shaoqing'
__contact__ = '502466541.com'


bam_filename = sys.argv[1]
fasta_filename = sys.argv[2]
revcomp_strand = False
min_counts = 10
offset_min = -15
offset_max = 15
region_size = 1



def nuc_frequencies(bam_filename, fasta_filename, 
                    revcomp_strand, min_counts, 
                    offset_min, offset_max, region_size):

    pos_signal_bedtool = load_coverage(bam_filename, strand='pos')
    neg_signal_bedtool = load_coverage(bam_filename, strand='neg') 

    total_sites, nuc_counts = calc_nuc_counts(pos_signal_bedtool, neg_signal_bedtool,
                                              fasta_filename, 
                                              revcomp_strand, min_counts, 
                                              offset_min, offset_max, region_size)
    print(total_sites)
    for offset, counts in nuc_counts.items():
        print (offset,counts)
    #print (total_sites, nuc_counts)
#    print_report(nuc_counts, background_freq_filename, 
#                region_size, total_sites, verbose)

def calc_nuc_counts(pos_signal_bedtool, neg_signal_bedtool, fasta_filename, 
                    revcomp_strand, min_counts, 
                    offset_min, offset_max, region_size):

    ''' main routine for calculating nuc_counts '''

    #if verbose:
    #    msg =  ">> analyzing sequences ...\n"
    #    msg += ">> ignore:%s only:%s\n" % \
    #        (str(ignore_chroms), str(only_chroms))
    #    msg += ">> offset range: %d to %d\n" % (offset_min, offset_max)
    #    msg += ">> region size: %d\n" % (region_size)
    #    msg += ">> revcomp strand: %s\n" % str(revcomp_strand)
    #    print >>sys.stderr, msg

    seq_fasta = Fasta(fasta_filename, as_raw = True)

    nuc_counts = defaultdict(Counter)

    bedtools = (pos_signal_bedtool, neg_signal_bedtool)
    strands = ('+', '-')

    # total number of sites examined
    total_sites = 0

    for bedtool, strand in zip(bedtools, strands):

        for row in bedtool:

            # skip data based on specified chromosomes
   #         if row.chrom in ignore_chroms:
   #             continue
   #         if only_chroms and row.chrom not in only_chroms:
   #             continue

            # skip data if counts are too low
            if row.count < min_counts: continue

            # sites in bedgraph examined - must come after all checks
            # above
            total_sites += 1

            for offset in range(offset_min, offset_max + 1):

                # upstream offsets are negative values
                if strand == '+':
                    start = row.start + offset
                elif strand == '-':
                    start = row.start - offset

                if region_size == 1:
                    # half open at the position of interest
                    end = start + region_size
                else:
                    # make sure that the 3' most position in a region
                    # is the base of interest
                    if strand == '+':
                        end = start + 1 # include position with + 1
                        start = end - region_size
                    else:
                        # negative strand
                        end = start + region_size

                nucs = seq_fasta[row.chrom][start:end]

                #  1. libs where the captured strand is sequenced
                #     are the correct polarity as-is (i.e. Excision-seq
                #     libs)
                #  2. libs where the *copy* of the captured strand
                #     is sequenced should be revcomplemented (i.e.
                #     circularization-based libs)

                if (strand == '+' and revcomp_strand) or \
                   (strand == '-' and not revcomp_strand):
                    nucs = complement(nucs[::-1])

                nuc_counts[offset][nucs] += row.count

    # remove nucs that are not len region_size
    for offset, counts in nuc_counts.items():
        for nuc, count in counts.items():
            if len(nuc) != region_size:
                counts.pop(nuc)

    return total_sites, nuc_counts


nuc_frequencies(bam_filename, fasta_filename,revcomp_strand, min_counts,offset_min, offset_max, region_size)
