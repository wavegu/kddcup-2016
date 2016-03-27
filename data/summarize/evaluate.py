import json
from util import get_conf_name_id_dict
from util import create_if_not_exist
from util import CONF_NAME_LIST
from os.path import join

RESULT_FILENAME = 'results.tsv'


def log_factor(i):
    import math
    return math.log(float(i + 1), 2)


def get_true_conf_year_to_aff_rank():
    with open(join('affiliation', 'conf_year_to_aff_rank_100.json')) as f:
        true_conf_year_to_aff_rank = json.load(f)
    return true_conf_year_to_aff_rank


def get_guess_confid_to_aff_rank():
    with open(join('rank', RESULT_FILENAME)) as f:
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


def get_conf_to_ndcg_dict(year):

    conf_to_ndcg_dict = {}

    conf_name_to_id_dict = get_conf_name_id_dict()
    guess_confid_to_aff_rank = get_guess_confid_to_aff_rank()
    true_conf_year_to_aff_rank = get_true_conf_year_to_aff_rank()

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
            idcg += float(true_relevance) / log_factor(true_rank)

        dcg = 0.0
        for looper in range(20):
            i = looper + 1
            guess_aff_id = guess_aff_rank[looper]
            dcg += true_affid_dict[guess_aff_id]['relevance'] / log_factor(i)

        conf_to_ndcg_dict[conf_name] = float(dcg) / float(idcg)

    return conf_to_ndcg_dict


def evaluate():
    year_dict = {}
    for year in range(2011, 2016):
        year_dict[year] = get_conf_to_ndcg_dict(year)
    create_if_not_exist('evaluate')
    with open(join('evaluate', 'evaluation_' + RESULT_FILENAME.replace('.tsv', '') + '.json'), 'w') as f:
        content = json.dumps(year_dict, indent=4)
        print RESULT_FILENAME
        print content
        f.write(content)

evaluate()
# print get_conf_to_ndcg_dict(2014)['SIGIR']