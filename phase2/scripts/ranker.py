from os.path import join
from model.util import DATA_DIR, CONF_NAME_LIST
from model.util import create_if_not_exist
from model.aff import Affiliation, AFFID_LIST


class Ranker:

    __dir__ = join(DATA_DIR, 'ranker')
    create_if_not_exist(__dir__)

    def __init__(self):
        self.aff_to_author_num_dict = Affiliation.get_aff_to_author_num_dict()
        self.aff_to_paper_num_dict = Affiliation.get_aff_to_paper_num_dict()
        self.conf_year_aff_to_score_dict = Affiliation.get_conf_year_aff_to_kdd_score_dict()
        self.conf_year_to_aff_rank_by_kdd_score_dict = Affiliation.get_conf_year_to_aff_rank_by_kdd_score_dict()

    def write_features(self):
        conf_qid_dict = {
            'KDD': 1,
            'ICML': 2
        }

        def get_feature_line(affid, conf, seq, year):

            feature_line = '%d qid=%d' % (seq, conf_qid_dict[conf] + 10 * year)
            author_num = self.aff_to_author_num_dict[affid]
            paper_num = self.aff_to_paper_num_dict[affid]
            year_aff_to_score_dict = self.conf_year_aff_to_score_dict[conf]
            kdd_score_1_1 = year_aff_to_score_dict[str(year-1)][affid]
            kdd_score_2_4 = 0
            kdd_score_5_10 = 0
            for y in range(year-4, year-1):
                kdd_score_2_4 += year_aff_to_score_dict[str(y)][affid]
            for y in range(year-10, year-4):
                kdd_score_5_10 += year_aff_to_score_dict[str(y)][affid]

            feature_list = [
                author_num,
                paper_num,
                kdd_score_1_1,
                kdd_score_2_4,
                kdd_score_5_10
            ]

            for looper in range(len(feature_list)):
                feature_line += ' %d:%s' % (looper, str(feature_list[looper]))

            return feature_line

        for year in range(2010, 2016):
            feature_path = join(self.__dir__, 'feature_' + str(year) + '.txt')
            with open(feature_path, 'w') as f:
                for conf in CONF_NAME_LIST:
                    rank = self.conf_year_to_aff_rank_by_kdd_score_dict[conf][str(year)]
                    seq = 0
                    for affid, affname, score in rank:
                        if affid not in AFFID_LIST:
                            continue
                        seq += 1
                        f.write(get_feature_line(affid, conf, seq, year) + '\n')


if __name__ == '__main__':
    ranker = Ranker()
    ranker.write_features()