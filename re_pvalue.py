from scipy.stats import binom
from statsmodels.stats.multitest import multipletests
import numpy as np
import pandas as pd
import sys
#pval = binom.sf(k=3, n=12, p=0.016)
#reject, pvals_corrected, alphacSidak, alphacBonf = multipletests(pval,alpha=0.05,method="bonferroni",is_sorted=False)
#print(pval,pvals_corrected)
def calculate_p_value(ex_bg, ex_mut, in_bg, in_mut, p_bg=0.016):
	pval = 1
	if in_bg >= 10 and ex_bg >= 10 and ex_mut >= 0:
		p = np.divide(in_mut, in_bg)
		p = max(p, p_bg)
		pval = 1-binom.sf(k=ex_mut, n=ex_bg, p=p)
	return pval

#pvals = [0.005,0.006]
#reject, pvals_corrected, alphacSidak, alphacBonf = multipletests(pvals,alpha=0.05,method="bonferroni",is_sorted=False)
#print(calculate_p_value(185, 13, 111, 0, p_bg=0.016),pvals_corrected)

#rawdata = pd.read_table(sys.argv[1])

#rawdata = list(rawdata.as_matrix())
#input_cov = list(rawdata.iloc[:,1])
#input_alt = list(rawdata.iloc[:,2])

#print(rawdata.iloc[:,1])
#print(input_cov)

with open(sys.argv[1]) as f:
	pvalue_1 = []
	pvalue_2 = []
	k = []
	for line in f:
		line = line.strip().split('\t')
		k.append(line)
		line = line[4:]
		input_cov = int(line[0])
		input_alt = int(line[1])
		output1_cov = int(line[2])
		output1_alt = int(line[3])
		output2_cov = int(line[4])
		output2_alt = int(line[5])
		pvalue1 = calculate_p_value(output1_cov, output1_alt, input_cov, input_alt)
		pvalue2 = calculate_p_value(output2_cov, output2_alt, input_cov, input_alt)
		pvalue_1.append(pvalue1)
		pvalue_2.append(pvalue2)
	reject, pvals_corrected1, alphacSidak, alphacBonf = multipletests(pvalue_1,alpha=0.05,method="bonferroni",is_sorted=False)
	reject, pvals_corrected2, alphacSidak, alphacBonf = multipletests(pvalue_2,alpha=0.05,method="bonferroni",is_sorted=False)
	for i in range(len(pvalue_1)):
		if (pvalue_1[i] <0.05 and pvalue_2[i]<0.05):
			print(str(k[i][0])+"\t"+str(k[i][1])+"\t"+str(pvalue_1[i])+"\t"+str(pvals_corrected1[i])+"\t"+str(pvalue_2[i])+"\t"+str(pvals_corrected2[i]))
