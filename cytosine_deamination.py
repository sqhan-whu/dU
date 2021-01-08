from sys import argv

def get_list(file_name,min_T_ratio,T_dev,min_C_ratio,pval,r=False):
	n = 0
	inp = []
	oup = []
	out_list = []
	pos = []
	with open(file_name) as f1:
		for line in f1:
			if not line.strip().startswith("#"):
				line1 = line
				line = line.strip().replace('%','').split('\t')
				if line[3] == "C" and line[4] == "T" and not line[9].startswith(".") and not line[10].startswith(".") or line[3] == "G" and line[4] == "A" and not line[9].startswith(".") and not line[10].startswith("."):
					inp = line[9].split(':')
					oup = line[10].split(':')
					inp_t = float(inp[6])
					oup_t = float(oup[6])
					inp_pval = float(inp[7])
					oup_pval = float(oup[7])
					inp_gq = float(inp[1])
					oup_gq = float(oup[1])
					inp_cov = int(inp[3])
					out_cov = int(oup[3])
					inp_ref_cov = int(inp[4])
					inp_alt_cov = int(inp[5])
					oup_ref_cov = int(oup[4])
					oup_alt_cov = int(oup[5])
					inp_c = inp_ref_cov/inp_cov
					oup_c = oup_ref_cov/out_cov

					if r == False and line1.split('\t')[9].startswith("0/1"):
						if inp_pval < pval and inp_t > min_T_ratio and inp_t<50 and oup_t/inp_t < T_dev and inp_ref_cov + inp_alt_cov >=20 and oup_ref_cov + oup_alt_cov >=20 and oup_c/inp_c > min_C_ratio and inp_c >0.5 and oup_c >0.5:

							n +=1
							out_list.append([line[0],line[1],line[3],line[4],inp_cov,inp_ref_cov,inp_alt_cov,inp_t,out_cov,oup_ref_cov,oup_alt_cov,oup_t,oup_t/inp_t,oup_c/inp_c])
							pos.append(str(line[0])+"\t"+str(line[1]))

					elif r == True and line1.split('\t')[10].startswith("0/1"):
						if oup_pval < pval and oup_t > min_T_ratio and oup_t<50 and inp_t/(oup_t+0.0001) < T_dev and inp_ref_cov + inp_alt_cov >=20 and oup_ref_cov + oup_alt_cov >=20 and inp_c/(oup_c+0.0001) > min_C_ratio and inp_c>0.5 and oup_c >0.5:
							n +=1
							out_list.append([line[0],line[1],line[3],line[4],inp_cov,inp_ref_cov,inp_alt_cov,inp_t,out_cov,oup_ref_cov,oup_alt_cov,oup_t,inp_t/(oup_t+0.0001),inp_c/(oup_c+0.0001)])
							pos.append(str(line[0])+"\t"+str(line[1]))
	f1.close()			
	return n,out_list,pos

file_name_1 = argv[1]
file_name_2 = argv[2]
file_name_3 = argv[3]

def get_interval(list1,list2):
	centro_num = 0
	centro_content = []
	for i in list2:
		i=i.split('\t')
		list2_id = i[0]
		min_num = int(i[1])
		max_num = int(i[2])
		for j in list1:
			j=j.split('\t')
			if j[0] == list2_id and int(j[1]) >= min_num and int(j[1]) <= max_num:
				centro_num +=1
				centro_content.append('\t'.join(list1))
	return centro_num,centro_content

def get_centro_list(file_name):
	centro_list = []
	with open (file_name) as f:
		for line in f:
			line = line.strip().split('\t')
			centro_list.append(str(line[0])+"\t"+str(line[1])+"\t"+str(line[2]))
	f.close()
	return centro_list

centro = []
centro = get_centro_list(file_name_3)

final_out_list = []
for T_ratio in [10]:
	for T_dev in [0.8]:
		for min_C_ratio in [1.05]:
			for pval in [0.000001]:
				file_line_1,file_content_1,file_pos_1 = get_list(file_name_1,T_ratio,T_dev,min_C_ratio,pval)
				file_line_2,file_content_2,file_pos_2 = get_list(file_name_2,T_ratio,T_dev,min_C_ratio,pval)
				rev_file_line_1,rev_file_content_1,rev_file_pos_1 = get_list(file_name_1,T_ratio,T_dev,min_C_ratio,pval,r=True)
				rev_file_line_2,rev_file_content_2,rev_file_pos_2 = get_list(file_name_2,T_ratio,T_dev,min_C_ratio,pval,r=True)
				comm = [x for x in file_pos_1 if x in file_pos_2]
				rev_comm = [x for x in rev_file_pos_1 if x in rev_file_pos_2]
				cen_n, cen_l = get_interval(comm,centro)
				rev_cen_n, rev_cen_l = get_interval(rev_comm,centro)
				#for i in comm:
				#	print(i)
				print(str(T_ratio)+'\t'+str(T_dev)+'\t'+str(min_C_ratio)+'\t'+str(pval)+'\t'+str(file_line_1)+"\t"+str(file_line_2)+"\t"+str(len(comm))+'\t'+str(cen_n)+'\t'+str(rev_file_line_1)+"\t"+str(rev_file_line_2)+"\t"+str(len(rev_comm))+'\t'+str(rev_cen_n))
