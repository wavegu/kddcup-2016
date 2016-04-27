import os
import json
import codecs
from datetime import datetime
from os.path import join
from paper import Paper
from util import create_if_not_exist
from util import YEAR_LIST
from util import MAG_SAMPLE_PAPER_AUTHOR_AFFS_PATH, DATA_DIR

import sys
sys.dont_write_bytecode = True


class Author:

    __dir__ = join(DATA_DIR, 'author')
    create_if_not_exist(__dir__)

    @classmethod
    def get_author_affids_dict(cls):
        author_to_affs_json_path = join(DATA_DIR, 'author_to_affs.json')
        with codecs.open(author_to_affs_json_path, 'r', 'utf8') as f:
            author_to_affs_dict = json.load(f)
        return author_to_affs_dict

    @classmethod
    def get_author_to_aff_num_dict(cls):
        print(datetime.now())
        print('loading author_to_aff_num...')
        author_to_aff_num_json_path = join('author', 'author_to_aff_num.json')
        f = codecs.open(author_to_aff_num_json_path, 'r', 'utf8')
        author_to_aff_num_dict = json.load(f)
        f.close()
        print('ok')
        return author_to_aff_num_dict


    @classmethod
    def get_author_year_to_paper_num_dict(cls, use_cache=True):

        o_author_year_to_papar_num_path = join(cls.__dir__, 'author_year_to_paper_num.json')

        if use_cache and os.path.exists(o_author_year_to_papar_num_path):
            with open(o_author_year_to_papar_num_path) as f:
                return json.load(f)

        author_year_to_paper_num_dict = {}
        id_paper_year_dict = Paper.get_paper_year_dict()

        with codecs.open(MAG_SAMPLE_PAPER_AUTHOR_AFFS_PATH, 'r', 'utf-8') as f:
            paper_lines = f.readlines()

        for line in paper_lines:
            parts = line.split('\t')
            paper_id = parts[0]
            paper_author = parts[1]
            if paper_id not in id_paper_year_dict:
                print paper_id
                continue
            paper_year = id_paper_year_dict[paper_id]
            if paper_year not in YEAR_LIST:
                continue

            if paper_author not in author_year_to_paper_num_dict:
                author_year_to_paper_num_dict[paper_author] = {}
                for year in YEAR_LIST:
                    author_year_to_paper_num_dict[paper_author][year] = 0

            author_year_to_paper_num_dict[paper_author][paper_year] += 1

        with open(o_author_year_to_papar_num_path, 'w') as f:
            f.write(json.dumps(author_year_to_paper_num_dict, indent=4))

        return author_year_to_paper_num_dict


if __name__ == '__main__':
    Author.get_author_year_to_paper_num_dict()