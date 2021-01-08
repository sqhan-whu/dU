mkdir trim-galore
mkdir fastuniq
mkdir bowtie2
mkdir mapping_results

for line in `cat name.list`
do
    mkdir trim-galore/$line
    echo "#!/bin/bash" >> $line.q.sbatch
    echo "#SBATCH -N 1 -c 16" >> $line.q.sbatch
    #echo "gunzip $line\_combined_R1.fastq.gz" >> $line.q.sbatch
    #echo "gunzip $line\_combined_R2.fastq.gz" >> $line.q.sbatch
    #echo "python split_fastq.py ./$line.fastq ./$line\_R1.fastq ./$line\_R2.fastq" >> $line.q.sbatch
    #echo "gzip $line.fastq" >> $line.q.sbatch
    echo "trim_galore --fastqc --quality 20 --phred33 --stringency 3 --length 20 -o trim-galore/$line --paired $line\_combined_R1.fastq $line\_combined_R2.fastq" >> $line.q.sbatch
    echo "gzip $line\_combined_R1.fastq" >> $line.q.sbatch
    echo "gzip $line\_combined_R2.fastq" >> $line.q.sbatch
    echo "./trim-galore/$line/$line\_combined_R1_val_1.fq" > ./fastuniq/input_$line.list
    echo "./trim-galore/$line/$line\_combined_R2_val_2.fq" >> ./fastuniq/input_$line.list
    echo "fastuniq -i ./fastuniq/input_$line.list -o ./fastuniq/$line\_R1.rd.fastq -p ./fastuniq/$line\_R2.rd.fastq" >> $line.q.sbatch
    echo "gzip ./trim-galore/$line/$line\_combined_R1_val_1.fq" >> $line.q.sbatch
    echo "gzip ./trim-galore/$line/$line\_combined_R2_val_2.fq" >> $line.q.sbatch
    echo "bowtie2 -p 16 -L 20 -N 1 -x ../human/GRCh38_p7 -1 ./fastuniq/$line\_R1.rd.fastq -2 ./fastuniq/$line\_R2.rd.fastq -S ./bowtie2/$line.sam 2> ./mapping_results/$line.out" >> $line.q.sbatch
    echo "gzip ./fastuniq/$line\_R1.rd.fastq" >> $line.q.sbatch
    echo "gzip ./fastuniq/$line\_R2.rd.fastq" >> $line.q.sbatch
    #echo "bwa mem -t 16 ../human/genome ./fastuniq/$line\_R1.rd.fastq ./fastuniq/$line\_R2.rd.fastq > ./bwa/$line.sam" >> $line.q.sbatch
    #echo "samtools flagstat ./bwa/$line.sam > ./mapping_results_bwa/$line.txt" >> $line.q.sbatch
    echo "rm $line.q.sbatch" >> $line.q.sbatch
    sed -i 's/\\//g' $line.q.sbatch
    sed -i 's/\\//g' ./fastuniq/input_$line.list
    chmod +x $line.q.sbatch
    sbatch $line.q.sbatch

done
