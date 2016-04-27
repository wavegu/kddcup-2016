import json
from model.aff import Affiliation
from model.util import get_conf_name_id_dict
from model.util import create_if_not_exist
from model.util import CONF_NAME_LIST, DATA_DIR, RESULT_FILE_PATH
from os.path import join


class Evaluator:

    def __init__(self):
        self.dir = join(DATA_DIR, 'evaluate')
        self.aff_rank_by_kdd_score = Affiliation.get_conf_year_to_aff_rank_by_kdd_score_dict()
        create_if_not_exist(self.dir)

    @classmethod
    def log_factor(cls, i):
        import math
        return math.log(float(i + 1), 2)

    def get_guess_confid_to_aff_rank(self):
        with open(RESULT_FILE_PATH) as f:
            lines = f.readlines()
            guess_confid_to_aff_rank = {}
            for line in lines:
                parts = line.split('\t')
                confid = parts[0]
                affid = parts[1]
                if confid not in guess_confid_to_aff_rank:
                    guess_confid_to_aff_rank[confid] = []
                guess_confid_to_aff_rank[confid].append(affid)
        return guess_confid_to_aff_rank

    def get_conf_to_ndcg_dict(self, year):

        conf_to_ndcg_dict = {}

        conf_name_to_id_dict = get_conf_name_id_dict()
        guess_confid_to_aff_rank = self.get_guess_confid_to_aff_rank()
        true_conf_year_to_aff_rank = self.aff_rank_by_kdd_score

        year = str(year)

        for conf_name in CONF_NAME_LIST:

            conf_id = conf_name_to_id_dict[conf_name]
            true_aff_rank = true_conf_year_to_aff_rank[conf_name][year]
            guess_aff_rank = guess_confid_to_aff_rank[conf_id]

            true_affid_dict = {}
            for looper in range(len(true_aff_rank)):
                true_rank = looper + 1
                true_affid, true_affname, true_relevance = true_aff_rank[looper]
                true_affid_dict[true_affid] = {
                    'rank': true_rank,
                    'name': true_affname,
                    'relevance': true_relevance
                }

            idcg = 0.0
            for looper in range(20):
                true_rank = looper + 1
                true_affid, true_affname, true_relevance = true_aff_rank[looper]
                idcg += float(true_relevance) / self.log_factor(true_rank)

            dcg = 0.0
            for looper in range(20):
                i = looper + 1
                guess_aff_id = guess_aff_rank[looper]
                dcg += true_affid_dict[guess_aff_id]['relevance'] / self.log_factor(i)

            conf_to_ndcg_dict[conf_name] = float(dcg) / float(idcg)

        return conf_to_ndcg_dict

    def evaluate(self):
        year_dict = {}
        for year in range(2010, 2016):
            year_dict[year] = self.get_conf_to_ndcg_dict(year)
        create_if_not_exist('evaluate')
        with open(join(self.dir, 'evaluation_' + RESULT_FILE_PATH.replace('.tsv', '') + '.json'), 'w') as f:
            content = json.dumps(year_dict, indent=4)
            print content
            f.write(content)


if __name__ == '__main__':
    evaluator = Evaluator()
    evaluator.evaluate()