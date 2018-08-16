#!/usr/bin/python
# -*-coding:utf-8-*-
# @author galaxy

import os
import glob
from multiprocessing import Pool


####################################################################################################
tfbs_dir = "/data5/galaxy/project/tf_analysis/TFBS_analysis/ip"
cycle_dir = "/data5/galaxy/project/tf_analysis/TFBS_analysis/100cycle_input"
m6a_dir = "/data5/galaxy/project/tf_analysis/TFBS_analysis/DMR"
intersect_dir = "/data5/galaxy/project/tf_analysis/TFBS_analysis/intersect_result_each"
if not os.path.exists(intersect_dir):
    os.makedirs(intersect_dir)
map_dict = {"STAT1": "Lung", "ETV6": "Lung", "NRF1": "Lung", "THAP11": "Heart"}
####################################################################################################


def overlap_input(input_bed, m6a_bed, tfbs):
    result_dir = "%s/%s/control" % (intersect_dir, tfbs.upper())
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    result_file = os.path.join(result_dir, os.path.basename(input_bed))
    os.system("bedtools intersect -a %s -b %s > %s" % (m6a_bed, input_bed, result_file))


def overlap_ip(tfbs_bed, m6a_bed, tfbs):
    result_dir = "%s/%s/tfbs" % (intersect_dir, tfbs.upper())
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    result_file = os.path.join(result_dir, "intersect_result.txt")
    os.system("bedtools intersect -a %s -b %s > %s" % (m6a_bed, tfbs_bed, result_file))


def get_bed_according_tfbs(name, in_list):
    out_file = ""
    for x in in_list:
        if name in x:
            out_file = x
            break
    return out_file


def main_method():
    tfbs_list = glob.glob("%s/*.bed" % tfbs_dir)
    m6a_list = glob.glob("%s/*.bed" % m6a_dir)
    for tfbs_bed in tfbs_list:
        type_name = os.path.basename(tfbs_bed).split(".")[0].upper()
        tfbs = type_name.split("_")[0].split("-")[0].upper()
        tissue_name = map_dict[str(tfbs)]
        print(tfbs, tissue_name)
        m6a_bed = get_bed_according_tfbs(tissue_name, m6a_list)
        input_list = glob.glob("%s/control-%s_*.bed" % (cycle_dir, tissue_name.lower()))
        print(os.path.basename(tfbs_bed), os.path.basename(m6a_bed), input_list[0])
        overlap_ip(tfbs_bed, m6a_bed, type_name)
        pool = Pool()
        for input_bed in input_list:
            # overlap_input(input_bed, m6a_bed)
            pool.apply_async(overlap_input, (input_bed, m6a_bed, type_name))
        pool.close()
        pool.join()


if __name__ == "__main__":
    main_method()
