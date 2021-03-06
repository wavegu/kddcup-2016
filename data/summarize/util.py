import sys
sys.dont_write_bytecode = True

import os
import codecs
from os.path import join


def get_conf_name_id_dict():
    conf_dict = {}
    f = codecs.open(join('..', 'MAG', 'Conferences.txt'), 'r', 'utf8')
    lines = f.readlines()
    f.close()
    for line in lines:
        conf_id = line.split('\t')[0]
        conf_name = line.split('\t')[1]
        conf_dict[conf_name] = conf_id
    return conf_dict


def get_paper_line_parts(line):
    parts = line.split('\t')
    paper_id = parts[0]
    author_id = parts[1]
    affiliation_id = parts[2]
    return paper_id, author_id, affiliation_id


def create_if_not_exist(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


CONF_NAME_LIST = ['SIGIR', 'SIGMOD', 'SIGCOMM']
YEAR_LIST = [str(year) for year in range(2000, 2016)]
