# encoding=utf-8
import os
import sys
sys.dont_write_bytecode = True

import json
import codecs
from os.path import join
from util import YEAR_LIST
from util import create_if_not_exist
from util import DATA_DIR


class Paper:

    __dir__ = join(DATA_DIR, 'paper')
    __selected_papers_path__ = join(DATA_DIR, 'selected_papers.txt')
    __selected_papers_auth_aff_path__ = join(DATA_DIR, 'sample_paper_author_affs_path.txt')
    create_if_not_exist(__dir__)

    @classmethod
    def get_paper_year_dict(cls, use_cache=True):

        o_paper_to_year_path = join(cls.__dir__, 'paper_year_dict.json')

        if use_cache and os.path.exists(o_paper_to_year_path):
            with open(o_paper_to_year_path) as f:
                return json.load(f)

        paper_year_dict = {}
        with codecs.open(cls.__selected_papers_path__, 'r', 'utf8') as f:
            lines = f.readlines()
        for line in lines:
            paper_id = str(line.split('\t')[0])
            paper_year = str(line.split('\t')[1])
            paper_year_dict[paper_id] = paper_year

        with open(o_paper_to_year_path, 'w') as f:
            f.write(json.dumps(paper_year_dict, indent=4))

        return paper_year_dict

    @classmethod
    def get_paper_to_conf_name_dict(cls, use_cache=True):

        o_paper_to_confname_path = join(cls.__dir__, 'paper_to_confname.json')

        if use_cache and os.path.exists(o_paper_to_confname_path):
            with open(o_paper_to_confname_path) as f:
                return json.load(f)

        paper_to_conf_name_dict = {}
        f = codecs.open(cls.__selected_papers_path__, 'r', 'utf8')
        lines = f.readlines()
        f.close()
        for line in lines:
            parts = line.replace('\n', '').replace('\r', '').split('\t')
            paper_id = str(parts[0])
            paper_conf_name = str(parts[3].upper())
            paper_to_conf_name_dict[paper_id] = paper_conf_name

        with open(o_paper_to_confname_path, 'w') as f:
            f.write(json.dumps(paper_to_conf_name_dict, indent=4))

        return paper_to_conf_name_dict

    @classmethod
    def get_year_paper_to_authors_dict(cls, use_cache=True):

        o_year_paper_to_authors_path = join(cls.__dir__, 'year_paper_to_authors.json')

        if use_cache and os.path.exists(o_year_paper_to_authors_path):
            with open(o_year_paper_to_authors_path) as f:
                return json.load(f)

        paper_year_dict = cls.get_paper_year_dict()
        print len(paper_year_dict)
        year_paper_authors_dict = {}
        # 初始化
        for year in YEAR_LIST:
            year_paper_authors_dict[year] = {}
        # 遍历所有paper，建立dict
        f = codecs.open(cls.__selected_papers_auth_aff_path__, 'r', 'utf8')
        lines = f.readlines()
        f.close()

        for line in lines:
            parts = line.split('\t')
            paper_id = parts[0]
            author_id = parts[1]

            # not selected paper, drop
            if paper_id not in paper_year_dict:
                continue

            paper_year = paper_year_dict[paper_id]

            if paper_year not in YEAR_LIST:
                continue

            if paper_id not in year_paper_authors_dict[paper_year]:
                year_paper_authors_dict[paper_year][paper_id] = []

            year_paper_authors_dict[paper_year][paper_id].append(author_id)

        with open(o_year_paper_to_authors_path, 'w') as f:
            f.write(json.dumps(year_paper_authors_dict, indent=4))

        return year_paper_authors_dict


if __name__ == '__main__':
    Paper.get_paper_year_dict()
    Paper.get_paper_to_conf_name_dict()
    Paper.get_year_paper_to_authors_dict()