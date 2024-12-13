#!/usr/bin/env python3

import argparse
import pandas as pd
from pandas_plink import read_plink
from pandas_plink import read_plink1_bin

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This script annotate samples with genotypes for the NeuroChip Parkinson related variants and writes the output to a CSV file.',
        epilog='Example usage:\npython3 pd_variants_annotator.py --bed BED --bim BIM --fam FAM --neurochip NEUROCHIP --query QUERY\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--bed', help='(Required) PLINK BED: containing the genotype.', required=True)
    parser.add_argument('--bim', help='(Required) PLINK BIM: containing variant information.', required=True)
    parser.add_argument('--fam', help='(Required) PLINK FAM: containing sample information.', required=True)
    parser.add_argument('--neurochip', help='(Required) NeuroChip Supplementary spreadsheet containting the variant annotation.', required=True)
    parser.add_argument('--query', help='(Required) List query sample IDs in a plain text file. Please make sure that the file contains one sample ID per line.', required=True)
    args = parser.parse_args()


    


