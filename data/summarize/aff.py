# encoding=utf8

import sys
sys.dont_write_bytecode = True

import json
import codecs
from os.path import join
from util import YEAR_LIST
from util import CONF_NAME_LIST
from util import create_if_not_exist

from paper import Paper
from author import Author


class Affiliation:

    __dir__ = 'affiliation'
    create_if_not_exist(__dir__)

    @classmethod
    def get_selected_aff_id_name_dict(cls):
        aff_id_name_dict = {}
        f = codecs.open(join('..', 'sample', 'top_affs.json'), 'r', 'utf8')
        affs = json.load(f)
        f.close()
        for aff_dict in affs:
            aff_id_name_dict[list(aff_dict.keys())[0]] = list(aff_dict.values())[0]
        return aff_id_name_dict

    @classmethod
    def get_aff_tot_paper_num_dict(cls):

        aff_paper_set_dict = {}
        aff_tot_paper_num_dict = {}
        selected_aff_list = SELECTED_AFF_LIST
        f = codecs.open(join('..', 'sample', 'selected_paper_auth_aff.txt'), 'r', 'utf8')
        lines = f.readlines()
        f.close()

        for line in lines:

            aff_id = line.split('\t')[2]
            aff_name = line.split('\t')[3]
            # aff = "[%s]%s" % (aff_id, aff_name)
            aff = aff_id
            if not aff_id or aff_id not in selected_aff_list:
                continue

            if aff not in aff_tot_paper_num_dict:
                aff_tot_paper_num_dict[aff] = 0
            if aff_id not in aff_paper_set_dict:
                aff_paper_set_dict[aff_id] = []

            paper_id = line.split('\t')[0]
            if paper_id in aff_paper_set_dict[aff_id]:
                continue

            aff_paper_set_dict[aff_id].append(paper_id)
            aff_tot_paper_num_dict[aff] += 1

        return aff_tot_paper_num_dict


    @classmethod
    def get_aff_conf_year_to_kdd_score_dict(cls):

        aff_conf_year_to_kdd_score_dict = {}
        author_affids_dict = Author.get_author_affids_dict()
        year_paper_authors_dict = Paper.get_year_paper_authors_dict()
        paper_to_conf_name_dict = Paper.get_paper_to_conf_name_dict()

        # 初始化
        global SELECTED_AFF_LIST
        for aff_id in SELECTED_AFF_LIST:
            if aff_id not in aff_conf_year_to_kdd_score_dict:
                aff_conf_year_to_kdd_score_dict[aff_id] = {}
                for conf_name in CONF_NAME_LIST:
                    aff_conf_year_to_kdd_score_dict[aff_id][conf_name] = {}
                    for year in YEAR_LIST:
                        aff_conf_year_to_kdd_score_dict[aff_id][conf_name][year] = 0.0

        # 计算每一年的kdd_score
        for year in YEAR_LIST:
            paper_authors_dict = year_paper_authors_dict[year]
            for paper, authors in paper_authors_dict.items():
                author_num = len(authors)
                if paper not in paper_to_conf_name_dict:
                    continue
                conf_name = paper_to_conf_name_dict[paper]
                if conf_name not in CONF_NAME_LIST:
                    continue
                for author_id in authors:
                    if author_id not in author_affids_dict:
                        continue
                    involved_affs = author_affids_dict[author_id]
                    for aff_id in involved_affs:
                        if aff_id in SELECTED_AFF_LIST:
                            aff_conf_year_to_kdd_score_dict[aff_id][conf_name][year] += float(1) / float(author_num * len(involved_affs))

        return aff_conf_year_to_kdd_score_dict


AFF_ID_TO_NAME_DICT = Affiliation.get_selected_aff_id_name_dict()
SELECTED_AFF_LIST = list(AFF_ID_TO_NAME_DICT.keys())


if __name__ == '__main__':
    pass
