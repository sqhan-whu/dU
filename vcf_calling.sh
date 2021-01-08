## samtools mpileup
## Varscan2 version 2.4.4 

mkdir bam
mkdir vcf_results

for line in `cat name.list`
do
    mkdir bam/$line
    echo "#!/bin/bash" >> $line.q.sbatch
    echo "#SBATCH -N 1 -c 16" >> $line.q.sbatch
    echo "samtools view -@ 16 -bS ./bowtie2/$line.sam > ./bam/$line.sort.bam"
    echo "samtools index -@ 16 ./bam/$line.sort.bam"
    echo "samtools mpileup -B -f ~/Genome/hg38.fa ./bam/$line.input1.sort.bam ./bam/$line.output1.sort.bam | java -jar ~/BIN/VarScan.v2.4.4.jar mpileup2snp -output-vcf 1 > rep_1.vcf"
    echo "samtools mpileup -B -f ~/Genome/hg38.fa ./bam/$line.input2.sort.bam ./bam/$line.output2.sort.bam | java -jar ~/BIN/VarScan.v2.4.4.jar mpileup2snp -output-vcf 1 > rep_2.vcf"
    sed -i 's/\\//g' $line.q.sbatch
    sed -i 's/\\//g' ./fastuniq/input_$line.list
    chmod +x $line.q.sbatch
    sbatch $line.q.sbatch
    
done
