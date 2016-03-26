import sys

import json
import codecs
from os.path import join
from aff import Affiliation
from aff import SELECTED_AFF_LIST
from aff import AFF_ID_TO_NAME_DICT
from util import get_conf_name_id_dict
from util import create_if_not_exist
from MachineLearning import MachineLearning
from util import YEAR_LIST

sys.dont_write_bytecode = True


train = MachineLearning()


class Rank:

    __dir__ = 'rank'
    __result_path__ = join(__dir__, 'results.tsv')
    create_if_not_exist(__dir__)

    __aff_conf_year_to_kdd_score_dict__ = Affiliation.get_aff_conf_year_to_kdd_score_dict()

    @classmethod
    def normalized_rank(cls, rank):
        selected_aff_list = SELECTED_AFF_LIST
        tot_score = 0
        for aff, num in rank:
            tot_score += num
        n_rank = []
        for aff_id, num in rank:
            if tot_score < 0.0001:
                n_score = 0.0
            else:
                n_score = float(num) / float(tot_score)
            if n_score < 0.0001:
                n_score = 0.0
            if aff_id in selected_aff_list:
                n_rank.append((aff_id, n_score))
        return n_rank

    @classmethod
    def rank_by_tot_paper_num(cls):
        aff_tot_paper_num_dict = Affiliation.get_aff_tot_paper_num_dict()
        rank = sorted(aff_tot_paper_num_dict, key=lambda d: d[1], reverse=True)
        return cls.normalized_rank(rank)

    @classmethod
    def rank_by_kdd_score(cls, conf_name):

        print('ranking:' + conf_name)
        f = codecs.open(join(cls.__dir__, conf_name + '_kdd_score.tsv'), 'w', 'utf8')
        f.write('aff name')
        for year in YEAR_LIST:
            f.write('\t' + year)
        f.write('\n')

        aff_id_to_name_dict = Affiliation.get_selected_aff_id_name_dict()
        aff_kdd_score_dict = {}

        for aff, conf_year_to_score_dict in cls.__aff_conf_year_to_kdd_score_dict__.items():

            f.write(aff_id_to_name_dict[aff])

            year_to_score_dict = conf_year_to_score_dict[conf_name]
            kdd_score = 0.0
            for year, year_score in year_to_score_dict.items():
                f.write('\t' + str(year_score))
                kdd_score += year_score
            aff_kdd_score_dict[aff] = kdd_score

            f.write('\n')

        rank = sorted(aff_kdd_score_dict.items(), key=lambda d: d[1], reverse=True)
        f.close()
        return cls.normalized_rank(rank)

    @classmethod
    def rank_by_linear_regression(cls):
        f = codecs.open(join(cls.__dir__, 'llrank.txt'), 'r', 'utf8')
        lines = f.readlines()
        f.close()
        for line in lines:
            print(line.replace('\t', ''))
        rank = [(line.split('\t')[0], float(line.split('\t')[1])) for line in lines if line]
        return cls.normalized_rank(rank)

    @classmethod
    def write_result_tsv(cls):

        conf_dict = get_conf_name_id_dict()

        # change rank strategy here
        # rank = cls.rank_by_kdd_score()
        f = codecs.open(join(cls.__dir__, 'results.tsv'), 'w', 'utf8')
        for conf in ['SIGIR', 'SIGMOD', 'SIGCOMM']:
            conf_id = conf_dict[conf]
            rank = cls.rank_by_kdd_score(conf)
            for aff, score in rank:
                f.write(conf_id + '\t' + aff + '\t' + str(score) + '\n')

            jf = codecs.open(join(cls.__dir__, 'rank_' + conf + '.json'), 'w', 'utf8')
            aff_id_name_dict = Affiliation.get_selected_aff_id_name_dict()
            rank_shown = [(aff+' '+aff_id_name_dict[aff], score) for aff, score in rank]
            jf.write(json.dumps(rank_shown, indent=4))
            jf.close()


if __name__ == '__main__':
    Rank.write_result_tsv()