# PD_348_Variant_Extraction_Genotyped_hg19

> [!WARNING]
> This project is still under development.

[![Open](https://img.shields.io/badge/Open-Dockstore-blue)](https://dockstore.org/workflows/github.com/anand-imcm/pd_348_variant_extraction_genotyped_hg19:main?tab=info)&nbsp;&nbsp;
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/anand-imcm/pd_348_variant_extraction_genotyped_hg19/build.yml)&nbsp;&nbsp;
![GitHub release (with filter)](https://img.shields.io/github/v/release/anand-imcm/pd_348_variant_extraction_genotyped_hg19)&nbsp;&nbsp;

## Introdution

This repository contains a Workflow Description Language (WDL) workflow for extracting information about genotyped SNPs from Neurochip array data for a list of sample IDs.

## Workflow Steps

- The script reads the input files (`.bed`,`.bim`,`.fam`) and extracts relevant SNPs using the `pandas_plink` library.
- For each variant, the script extracts genotype information for the given list of samples and annotates them with relevant details from the NeuroChip supplementary data.

## Inputs

The workflow requires the following inputs:

- `query_samples`: List query sample IDs in a plain text file without header. Please make sure that the file contains one sample ID per line. (required)
- `prefix`: Output file prefix. (required)
- `array_bed`: PLINK BED: containing the genotype. (required)
- `array_bim`: PLINK BIM: containing variant information. (required)
- `array_fam`: PLINK FAM: containing sample information. (required)
- `neurochip_variants`: NeuroChip Supplementary spreadsheet containing the variant annotation. (required)

## Outputs

The workflow generates the following outputs:

- `report`
  - `pd_extracted_genotyped_snps.xlsx`: Contains all the extracted and genotyped SNPs with annotations in a spreasheet format.
- csv_results: `*results.csv.tar.gz`
  - `pd_extracted_genotyped_snps_<GENE NAME>.csv`: Contains SNPs for genes with at least 5 variants.
  - `pd_extracted_genotyped_snps_remaining_genes.csv`: Contains SNPs for genes with fewer than 5 variants.
  - `pd_extracted_genotyped_snps_notfound.csv`: Contains SNPs that were not found in the dataset.

Each file includes the detailed annotations and genotype information for the specified variants in the following format:

- **NeuroChip_variant_name**: Name of the NeuroChip variant.
- **NeuroChip_variant_location_hg19**: Location of the NeuroChip variant based on hg19 genome.
- **ANNO_Gene.refGene**: Gene-name based on the annotated transcripts in RefSeq Gene from ANNOVAR database .
- **HGMD_Ref_Allele**: Reference allele obtained from HGMD database.
- **HGMD_Alt_Allele**: Alternative allele obtained from HGMD database.
- **ANNO_PopFreqMax**: A database containing the maximum allele frequency from 1000G, ESP6500, ExAC and CG46 from ANNOVAR.
- **num_obs_genotypes**: Number of genotypes observed in the subset of samples annotated in this set of spreadsheets.
- **all_Ref**: `TRUE` or `FALSE`? Indicates if all samples in the subset of samples annotated here are homozygous for HGMD_Ref_Allele.
- **all_Alt**: `TRUE` or `FALSE`? Indicates if all samples in the subset of samples annotated here are homozygous for HGMD_Alt_Allele.
- **all_a0 (Plink first allele: usually minor)**: `TRUE` or `FALSE`? Indicates if all samples in the subset of samples annotated here are homozygous for the PLINK-identified minor allele amongst the OPDC cohort (from which the subset of samples are drawn).
- **all_a1 (Plink second allele: usually major)**: `TRUE` or `FALSE`? Indicates if all samples in the subset of samples annotated here are homozygous for the PLINK-identified major allele amongst the OPDC cohort (from which the subset of samples are drawn).
- **Sample ID**: Genotype reported in the given sample.

## Components

- **Python packages**
  - pandas<=2.2.3
  - pandas-plink<=2.3.1
  - openpyxl<=3.1.5

- **Container**
  - mambaorg/micromamba:1.5.5
