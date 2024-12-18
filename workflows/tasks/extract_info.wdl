version 1.0

task extract {
    input {
        File query
        String prefix
        File bed
        File bim
        File fam
        File nc_xlsx
        String docker
        Int memory_gb = 32
        Int cpu = 16
    }
    Int disk_size_gb = ceil(size([bed,bim,fam,nc_xlsx], "GiB")) + 2
    command <<<
        set -euo pipefail
        python /scripts/pd_variants_annotator.py \
            --bed ~{bed} \
            --bim ~{bim} \
            --fam ~{fam} \
            --neurochip ~{nc_xlsx} \
            --query ~{query} \
            --prefix ~{prefix}
        tar -czvf "~{prefix}_result.csv.tar.gz" *.csv
    >>>
    output {
        File csv = prefix + "_result.csv.tar.gz"
        File xlsx = prefix + "_extracted_genotyped_snps.xlsx"
    }
    runtime {
        docker: "~{docker}"
        cpu: "~{cpu}"
        memory: "~{memory_gb}GB"
        disks: "local-disk ~{disk_size_gb} HDD"
    }
}