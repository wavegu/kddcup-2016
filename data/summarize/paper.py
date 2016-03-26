# encoding=utf-8
import sys
sys.dont_write_bytecode = True
import json
import codecs
from os.path import join
from util import YEAR_LIST
from util import create_if_not_exist


class Paper:

    __dir__ = 'paper'
    # __selected_papers_phase1_path__ = join('..', 'sample', 'selected_papers_phase1.txt')
    __selected_papers_phase1_path__ = join('..', 'sample', 'selected_papers_phase1.txt')
    __selected_papers_auth_aff_path__ = join('..', 'sample', 'selected_paper_auth_aff.txt')
    create_if_not_exist(__dir__)

    @classmethod
    def get_paper_year_dict(cls):
        paper_year_dict = {}
        f = codecs.open(cls.__selected_papers_phase1_path__, 'r', 'utf8')
        lines = f.readlines()
        f.close()
        for line in lines:
            paper_id = str(line.split('\t')[0])
            paper_year = str(line.split('\t')[1])
            paper_year_dict[paper_id] = paper_year

        with open(join('paper', 'paper_year_dict.json'), 'w') as f:
            f.write(json.dumps(sorted(paper_year_dict.items(), key=lambda x: int(x[1]))))

        return paper_year_dict

    @classmethod
    def get_paper_to_conf_name_dict(cls):
        paper_to_conf_name_dict = {}
        f = codecs.open(cls.__selected_papers_phase1_path__, 'r', 'utf8')
        lines = f.readlines()
        f.close()
        for line in lines:
            parts = line.replace('\n', '').replace('\r', '').split('\t')
            paper_id = str(parts[0])
            paper_conf_name = str(parts[3].upper())
            paper_to_conf_name_dict[paper_id] = paper_conf_name
        return paper_to_conf_name_dict

    @classmethod
    def get_year_paper_authors_dict(cls):
        paper_year_dict = cls.get_paper_year_dict()
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
        return year_paper_authors_dict