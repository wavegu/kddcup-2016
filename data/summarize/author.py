import json
import codecs
from os.path import join
from util import get_paper_line_parts
from util import create_if_not_exist
from datetime import datetime
from paper import Paper

import sys
sys.dont_write_bytecode = True


class Author:

    __dir__ = 'author'
    __selected_paper_auth_aff_path__ = join('..', 'sample', 'selected_paper_auth_aff.txt')
    create_if_not_exist(__dir__)

    @classmethod
    def get_author_affids_dict(cls):
        print(datetime.now())
        print('loading author_to_affs...')
        author_to_affs_json_path = join('author', 'author_to_affs.json')
        f = codecs.open(author_to_affs_json_path, 'r', 'utf8')
        author_to_affs_dict = json.load(f)
        f.close()
        print('ok')
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
    def get_author_year_paper_num_dict(cls):
        from util import YEAR_LIST

        author_year_paper_num_dict = {}
        id_paper_year_dict = Paper.get_paper_year_dict()
        f = codecs.open(cls.__selected_paper_auth_aff_path__, 'r', 'utf8')
        paper_lines = f.readlines()
        f.close()

        for line in paper_lines:
            parts = line.split('\t')
            paper_id = parts[0]
            paper_author = parts[1]
            paper_year = id_paper_year_dict[paper_id]

            if paper_author not in author_year_paper_num_dict:
                author_year_paper_num_dict[paper_author] = {}
                for year in YEAR_LIST:
                    author_year_paper_num_dict[paper_author][year] = 0

            author_year_paper_num_dict[paper_author][paper_year] += 1

        return author_year_paper_num_dict


if __name__ == '__main__':
    with open('author_year_paper_num_dict.json', 'w') as f:
        f.write(json.dumps(Author.get_author_year_paper_num_dict(), indent=4))
