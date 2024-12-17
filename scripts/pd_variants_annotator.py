#!/usr/bin/env python3

import argparse
import os
import pandas as pd
from pandas_plink import read_plink
from pandas_plink import read_plink1_bin
from utils import xlHighlight, xlFormat

def generate_summary(inp_bed,inp_bim,inp_fam,nc_suppl_sheet,query,file_prefix,outdir):

    sporadic_ids = pd.read_csv(query, header=None)[0].tolist()
    print(f"Query IDs: {sporadic_ids}")

    (bim, fam, bed) = read_plink(inp_bed,verbose=True)

    G = read_plink1_bin(inp_bed,inp_bim,inp_fam, verbose=True)

    sporadic_IDs_in_G = [x for x in sporadic_ids if x in G.sample]
    print(f"IDs found in the genotyped dataset: {sporadic_IDs_in_G}")

    st2 = pd.read_excel(nc_suppl_sheet)
    NeuroChip_variant_names = st2.loc[map(lambda x: x.startswith("Parkinson"),st2['HGMD.Associated_disease/phenotype']),'NeuroChip_variant_name']
    print(f"Total PD associated variants found in the NeuroChip Supplementary data {len(NeuroChip_variant_names)}")

    all_snps_df = pd.DataFrame()

    for snp_id in NeuroChip_variant_names:
        snp_id_in_G = False
        try:
            G.sel(sample=sporadic_IDs_in_G).values[:,bim.loc[bim['snp'] == snp_id].index[0]]
        except IndexError:
            pass
        else:
            snp_id_in_G = True
        
        if(not(snp_id_in_G)):
            print(f"{str(snp_id)} not present in G.")
            empty_snp_df_t = pd.DataFrame([['NA']*(11+len(sporadic_IDs_in_G))], 
                                                columns=['NeuroChip_variant_location_hg19',
                                            'ANNO_Gene.refGene','ANNO_AAChange.refGene','HGMD_Ref_Allele',
                                            'HGMD_Alt_Allele',
                                            'ANNO_PopFreqMax',
                                            'num_obs_genotypes',
                                            'all_Ref',
                                            'all_Alt',
                                            'all_a0 (Plink first allele: usually minor)',
                                            'all_a1 (Plink second allele: usually major)']+sporadic_IDs_in_G).transpose()
            empty_snp_df_t.columns = [snp_id]
            empty_snp_df = empty_snp_df_t.transpose()
            all_snps_df = pd.concat([all_snps_df, empty_snp_df])
        else:
            print(f"Found: {snp_id}")
            snp_genotype_aux = list(G.sel(sample=sporadic_IDs_in_G).values[:,bim.loc[bim['snp'] == snp_id].index[0]])
            genotype_mapper = [bim.loc[bim['snp'] == snp_id]['a0'].values[0]+bim.loc[bim['snp'] == snp_id]['a0'].values[0],
                            bim.loc[bim['snp'] == snp_id]['a0'].values[0]+bim.loc[bim['snp'] == snp_id]['a1'].values[0],
                            bim.loc[bim['snp'] == snp_id]['a1'].values[0]+bim.loc[bim['snp'] == snp_id]['a1'].values[0]]
            snp_genotype = list(map(lambda x: genotype_mapper[int(x)] if not(pd.isna(x)) else "No call",snp_genotype_aux))
            snp_genotype_df = pd.DataFrame(data={snp_id:snp_genotype})
            
            st2_data_df = st2.loc[st2['NeuroChip_variant_name']==snp_id, 
                            ['NeuroChip_variant_location_hg19',
                                'ANNO_Gene.refGene','ANNO_AAChange.refGene','HGMD_Ref_Allele',
                                'HGMD_Alt_Allele','ANNO_PopFreqMax']].transpose()
            st2_data_df.columns = [snp_id]
            num_genotypes = len(set(snp_genotype))
            HGMD_Ref_Allele = list(st2.loc[st2['NeuroChip_variant_name']==snp_id, ['HGMD_Ref_Allele']]['HGMD_Ref_Allele'])[0]
            HGMD_Alt_Allele = list(st2.loc[st2['NeuroChip_variant_name']==snp_id, ['HGMD_Alt_Allele']]['HGMD_Alt_Allele'])[0]

            a0 = list(bim.loc[bim['snp'] == snp_id, 'a0'])[0]
            a1 = list(bim.loc[bim['snp'] == snp_id, 'a1'])[0]

            all_Ref = all([x==HGMD_Ref_Allele for x in list(''.join(snp_genotype))])
            all_Alt = all([x==HGMD_Alt_Allele for x in list(''.join(snp_genotype))])

            all_a0 = all([x==a0 for x in list(''.join(snp_genotype))])
            all_a1 = all([x==a1 for x in list(''.join(snp_genotype))])

            genotype_summary_df = pd.DataFrame(data={'num_obs_genotypes':[num_genotypes],
                                                    'all_Ref':[all_Ref],
                                                    'all_Alt':[all_Alt],
                                                    'all_a0 (Plink first allele: usually minor)':[all_a0],
                                                    'all_a1 (Plink second allele: usually major)':[all_a1]}).transpose()
            genotype_summary_df.columns = [snp_id]
            snp_df = pd.concat([st2_data_df, genotype_summary_df, snp_genotype_df]).transpose()
            snp_df.columns = list(snp_df.columns.values)[0:11] + sporadic_IDs_in_G
            all_snps_df = pd.concat([all_snps_df, snp_df])
            all_snps_df.columns
    all_snps_df = all_snps_df.rename_axis('NeuroChip_variant_name').reset_index()

    single_file_genes = []
    excel_filepath = os.path.join(outdir, file_prefix + '_extracted_genotyped_snps.xlsx')
    with pd.ExcelWriter(excel_filepath, engine='openpyxl') as writer:
        for gene in set(list(all_snps_df['ANNO_Gene.refGene'].values)):
            if sum(list(all_snps_df['ANNO_Gene.refGene'].values==gene)) >= 5:
                single_file_genes = single_file_genes + [gene]
                gene_snps_df = all_snps_df.loc[all_snps_df['ANNO_Gene.refGene']==gene,]
                gene_snps_df = gene_snps_df.sort_values(by=['num_obs_genotypes','NeuroChip_variant_location_hg19'], ascending=False)
                gene_snps_transposed_df = gene_snps_df.transpose()
                filepath = os.path.join(outdir, file_prefix + '_extracted_genotyped_snps_' + gene + '.csv')
                gene_snps_transposed_df.to_csv(filepath, index=True,header=False)
                gene_snps_transposed_df.to_excel(writer, sheet_name=gene, index=True, header=False)
                worksheet = writer.sheets[gene]
                xlHighlight(worksheet)
                xlFormat(worksheet)

        gene_blob_genes = [g for g in list(all_snps_df['ANNO_Gene.refGene'].values) if not(g in single_file_genes)]
        gene_blob_genes.sort()
        gene_blob_snps_df = pd.DataFrame()
        for gene in set(gene_blob_genes):
            if(gene != 'NA'):
                gene_snps_df = all_snps_df.loc[all_snps_df['ANNO_Gene.refGene']==gene,]
                gene_blob_snps_df = pd.concat([gene_blob_snps_df, gene_snps_df])

        gene_blob_snps_df = gene_blob_snps_df.sort_values(by=['num_obs_genotypes','ANNO_Gene.refGene','NeuroChip_variant_location_hg19'], ascending=False)
        gene_blob_snps_transposed_df = gene_blob_snps_df.transpose()
        filepath = os.path.join(outdir, file_prefix + '_extracted_genotyped_snps_remaining_genes.csv')
        gene_blob_snps_transposed_df.to_csv(filepath, index=True, header=False)
        gene_blob_snps_transposed_df.to_excel(writer, sheet_name="other_gene_SNPs", index=True, header=False)
        worksheet = writer.sheets['other_gene_SNPs']
        xlHighlight(worksheet)
        xlFormat(worksheet)

        notfound_snps_df = all_snps_df.loc[all_snps_df['ANNO_Gene.refGene']=='NA',]
        notfound_snps_transposed_df = notfound_snps_df.transpose()
        filepath = os.path.join(outdir, file_prefix + '_extracted_genotyped_snps_notfound.csv')
        notfound_snps_transposed_df.to_csv(filepath, index=True,header=False)
        notfound_snps_transposed_df.to_excel(writer, sheet_name="not_found_SNPs", index=True, header=False)
        worksheet = writer.sheets['not_found_SNPs']
        xlFormat(worksheet)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This script annotate samples with genotypes for the NeuroChip Parkinson related variants and generate output files in CSV and Excel formats.',
        epilog='Example usage:\npython3 pd_variants_annotator.py --bed foo.bed --bim foo.bim --fam foo.fam --neurochip neurochip_supplementary.xlsx --query list_of_samples.txt --prefix pd_variants --outdir ./results\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--bed', help='(Required) PLINK BED file containing the genotype data.', required=True)
    parser.add_argument('--bim', help='(Required) PLINK BIM file containing variant information.', required=True)
    parser.add_argument('--fam', help='(Required) PLINK FAM file containing sample information.', required=True)
    parser.add_argument('--neurochip', help='(Required) NeuroChip Supplementary spreadsheet containing the variant annotations.', required=True)
    parser.add_argument('--query', help='(Required) List query sample IDs in a plain text file. Please make sure that the file contains one sample ID per line.', required=True)
    parser.add_argument('--prefix', help='(Optional) Prefix for output files. Defaults to the name of the query file.', required=False)
    parser.add_argument('--outdir', help='(Optional) Output directory. Defaults to the current working directory.', required=False)
    args = parser.parse_args()

    if not args.prefix:
        args.prefix = os.path.splitext(os.path.basename(args.query))[0]
    if not args.outdir:
        args.outdir = os.getcwd()
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    generate_summary(args.bed,args.bim,args.fam,args.neurochip,args.query,args.prefix,args.outdir)


