#!/usr/bin/python
# -*-coding:utf-8-*-
# @author galaxy

import os
import glob

#######################################################################################
intersect_dir = "/data5/galaxy/project/tf_analysis/TFBS_analysis/intersect_result_each"
file_list = glob.glob("%s/*/tfbs/intersect_result.txt" % intersect_dir)
tfbs_list = [i_file.split("/")[-3] for i_file in file_list]
result_file = os.path.join(intersect_dir, "enrich_result.txt")
########################################################################################


def stat_overlap_number(in_file):
    return_s = os.popen("wc -l %s" % in_file)
    overlap_num = return_s.read().split()[0]
    overlap_num = int(overlap_num)
    return overlap_num


with open(result_file, 'w') as fw:
    print("TFBS\tIP\tControl(mean)\tEnrich ratio\n")
    fw.write("TFBS\tIP\tControl(mean)\tEnrich ratio\n")
    for tfbs in tfbs_list:
        ip_bed = "%s/%s/tfbs/intersect_result.txt" % (intersect_dir, tfbs)
        ip_num = stat_overlap_number(ip_bed)
        input_bed_list = glob.glob("%s/%s/control/*.bed" % (intersect_dir, tfbs))
        input_num_list = [stat_overlap_number(input_file) for input_file in input_bed_list]
        aver_input_num = (sum(input_num_list) * 1.0) / (len(input_num_list) * 1.0)
        enrich_ratio = float(ip_num) / aver_input_num
        print("%s\t%d\t%f\t%f\n" % (tfbs, ip_num, aver_input_num, enrich_ratio))
        fw.write("%s\t%d\t%f\t%f\n" % (tfbs, ip_num, aver_input_num, enrich_ratio))
        # fw.write("%s\t%d\t%f\n" % (tfbs, ip_num, aver_input_num))
