# encoding=utf8
import os
import sys
sys.dont_write_bytecode = True

import json
import codecs
from os.path import join
from util import YEAR_LIST
from util import CONF_NAME_LIST
from util import create_if_not_exist
from util import MAG_DIR, DATA_DIR, MAG_SAMPLE_PAPER_AUTHOR_AFFS_PATH

from paper import Paper
from author import Author


class Affiliation:

    __dir__ = join(DATA_DIR, 'affiliation')
    create_if_not_exist(__dir__)

    @classmethod
    def get_aff_id_name_dict(cls, use_cache=True):
        o_affid_to_name_path = join(cls.__dir__, 'affid_to_name.json')

        if use_cache and os.path.exists(o_affid_to_name_path):
            with open(o_affid_to_name_path) as f:
                return json.load(f)

        affid_to_name_dict = {}
        with open(join(MAG_DIR, '2016KDDCupSelectedAffiliations.txt')) as f:
            afflines = f.readlines()
        for line in afflines:
            parts = line.replace('\n', '').split('\t')
            affid_to_name_dict[parts[0]] = parts[1]

        with open(o_affid_to_name_path, 'w') as f:
            f.write(json.dumps(affid_to_name_dict, indent=4))

        return affid_to_name_dict

    @classmethod
    def get_top_100_aff_id_name_dict(cls):
        aff_id_name_dict = {}
        with open(join(DATA_DIR, 'top_affs_100.json')) as f:
            aff_id_name_list = json.load(f)
        for aff_dict in aff_id_name_list:
            aff_id = aff_dict.keys()[0]
            aff_id_name_dict[aff_id] = aff_dict[aff_id]
        return aff_id_name_dict

    @classmethod
    def get_aff_to_author_num_dict(cls, use_cache=True):
        o_aff_to_author_num_path = join(cls.__dir__, 'aff_to_author_num.json')

        if use_cache and os.path.exists(o_aff_to_author_num_path):
            with open(o_aff_to_author_num_path) as f:
                return json.load(f)

        aff_to_authors_dict = {}
        aff_to_author_num_dict = {}
        author_to_affs_dict = Author.get_author_affids_dict()
        for author, affs in author_to_affs_dict.items():
            for aff in affs:
                if not aff:
                    continue
                if aff not in aff_to_authors_dict:
                    aff_to_authors_dict[aff] = []
                aff_to_authors_dict[aff].append(author)
        for aff in aff_to_authors_dict.keys():
            aff_to_authors_dict[aff] = list(set(aff_to_authors_dict[aff]))
            aff_to_author_num_dict[aff] = len(aff_to_authors_dict[aff])

        with open(o_aff_to_author_num_path, 'w') as f:
            f.write(json.dumps(aff_to_author_num_dict, indent=4))

        return aff_to_author_num_dict


    @classmethod
    def get_aff_to_paper_num_dict(cls, use_cache=True):

        o_aff_to_paper_num_path = join(cls.__dir__, 'aff_to_paper_num.json')

        if use_cache and os.path.exists(o_aff_to_paper_num_path):
            with open(o_aff_to_paper_num_path) as f:
                return json.load(f)

        aff_paper_set_dict = {}
        aff_tot_paper_num_dict = {}
        selected_aff_list = AFFID_LIST
        with codecs.open(join(DATA_DIR, 'sample_paper_author_affs.txt'), 'r', 'utf8') as f:
            lines = f.readlines()

        for line in lines:

            aff_id = line.split('\t')[2]
            if not aff_id or aff_id not in selected_aff_list:
                continue

            if aff_id not in aff_tot_paper_num_dict:
                aff_tot_paper_num_dict[aff_id] = 0
            if aff_id not in aff_paper_set_dict:
                aff_paper_set_dict[aff_id] = []

            paper_id = line.split('\t')[0]
            if paper_id in aff_paper_set_dict[aff_id]:
                continue

            aff_paper_set_dict[aff_id].append(paper_id)
            aff_tot_paper_num_dict[aff_id] += 1

        with open(o_aff_to_paper_num_path, 'w') as f:
            f.write(json.dumps(aff_tot_paper_num_dict, indent=4))

        return aff_tot_paper_num_dict


    @classmethod
    def get_aff_conf_year_to_kdd_score_dict(cls, use_cache=True):

        o_aff_conf_year_to_kdd_score_path = join(cls.__dir__, 'aff_conf_year_to_kdd_score.json')

        if use_cache and os.path.exists(o_aff_conf_year_to_kdd_score_path):
            with open(o_aff_conf_year_to_kdd_score_path) as f:
                return json.load(f)

        aff_conf_year_to_kdd_score_dict = {}
        author_affids_dict = Author.get_author_affids_dict()
        year_paper_authors_dict = Paper.get_year_paper_to_authors_dict()
        paper_to_conf_name_dict = Paper.get_paper_to_conf_name_dict()

        # 初始化
        global AFFID_LIST
        for aff_id in AFFID_LIST:
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
                        if aff_id in AFFID_LIST:
                            aff_conf_year_to_kdd_score_dict[aff_id][conf_name][year] += float(1) / float(author_num * len(involved_affs))

        with open(o_aff_conf_year_to_kdd_score_path, 'w') as f:
            f.write(json.dumps(aff_conf_year_to_kdd_score_dict, indent=4))

        return aff_conf_year_to_kdd_score_dict

    @classmethod
    def get_conf_year_aff_to_kdd_score_dict(cls, use_cache=True):

        o_conf_year_aff_to_score_path = join(cls.__dir__, 'conf_year_aff_to_kdd_score.json')

        if use_cache and os.path.exists(o_conf_year_aff_to_score_path):
            with open(o_conf_year_aff_to_score_path) as f:
                return json.load(f)

        # 整理成每个会议每年各机构的kdd score情况
        conf_year_aff_to_score_dict = {}
        aff_conf_year_to_kdd_score_dict = cls.get_aff_conf_year_to_kdd_score_dict()
        for aff, conf_year_to_kdd_score_dict in aff_conf_year_to_kdd_score_dict.items():
            for conf, year_to_score_dict in conf_year_to_kdd_score_dict.items():
                if conf not in conf_year_aff_to_score_dict:
                    conf_year_aff_to_score_dict[conf] = {}
                for year, score in year_to_score_dict.items():
                    if year not in conf_year_aff_to_score_dict[conf]:
                        conf_year_aff_to_score_dict[conf][year] = {}
                    conf_year_aff_to_score_dict[conf][year][aff] = score

        with open(o_conf_year_aff_to_score_path, 'w') as f:
            f.write(json.dumps(conf_year_aff_to_score_dict, indent=4))

        return conf_year_aff_to_score_dict

    @classmethod
    def get_conf_year_to_aff_rank_by_kdd_score_dict(cls, use_cache=True):

        o_conf_year_to_aff_rank_by_kdd_score_path = join(cls.__dir__, 'conf_year_to_aff_rank_by_kdd_score.json')

        if use_cache and os.path.exists(o_conf_year_to_aff_rank_by_kdd_score_path):
            with open(o_conf_year_to_aff_rank_by_kdd_score_path) as f:
                return json.load(f)

        # 排序
        conf_year_to_aff_rank = {}
        conf_year_aff_to_score_dict = cls.get_conf_year_aff_to_kdd_score_dict()
        for conf, year_aff_to_score_dict in conf_year_aff_to_score_dict.items():
            if conf not in conf_year_to_aff_rank:
                conf_year_to_aff_rank[conf] = {}
            for year, aff_to_score_dict in year_aff_to_score_dict.items():
                aff_score_rank = sorted(aff_to_score_dict.items(), key=lambda x: x[1], reverse=True)
                conf_year_to_aff_rank[conf][year] = [(aff_score_pair[0], AFF_ID_TO_NAME_DICT[aff_score_pair[0]], aff_score_pair[1]) for aff_score_pair in aff_score_rank]

        with open(o_conf_year_to_aff_rank_by_kdd_score_path, 'w') as f:
            f.write(json.dumps(conf_year_to_aff_rank, indent=4))

        return conf_year_to_aff_rank


AFF_ID_TO_NAME_DICT = Affiliation.get_top_100_aff_id_name_dict()
AFFID_LIST = list(AFF_ID_TO_NAME_DICT.keys())


if __name__ == '__main__':
    # Affiliation.get_conf_year_to_aff_rank_by_kdd_score_dict()
    # Affiliation.get_aff_to_paper_num_dict()
    Affiliation.get_conf_year_aff_to_kdd_score_dict(False)
