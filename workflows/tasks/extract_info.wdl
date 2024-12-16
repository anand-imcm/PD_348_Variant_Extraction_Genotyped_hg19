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
    echo ~{disk_size_gb}
        ls -ltrh
    >>>
    runtime {
        docker: "~{docker}"
        cpu: "~{cpu}"
        memory: "~{memory_gb}GB"
        disks: "local-disk ~{disk_size_gb} HDD"
    }
}