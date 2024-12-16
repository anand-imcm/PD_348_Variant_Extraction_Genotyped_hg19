version 1.0

workflow main {
    input {
        File query_samples
        String prefix
        File array_bed
        File array_bim
        File array_fam
        File neurochip_variants
    }
    parameter_meta {
        query_samples:"(Required) List query sample IDs in a plain text file without header. Please make sure that the file contains one sample ID per line."
        prefix:"(Required) Output file prefix"
        array_bed:"(Required) PLINK BED: containing the genotype."
        array_bim:"(Required) PLINK BIM: containing variant information."
        array_fam:"(Required) PLINK FAM: containing sample information."
        neurochip_variants:"(Required) NeuroChip Supplementary spreadsheet containing the variant annotation."
    }
}
