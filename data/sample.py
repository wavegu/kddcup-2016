import json


# with open('MAG/2016KDDCupSelectedAffiliations.txt') as f:
#     lines = f.readlines()
#     aff_ids = [line.split('\t')[0] for line in lines]


# with open('MAG/2016KDDCupSelectedPapers.txt') as f:
#     paper_lines = f.readlines()
#     paper_ids = [paper_line.split('\t')[0] for paper_line in paper_lines]

def get_author_to_affs_dict():
    print 'sampling author to affs dict...'
    with open('/home/share/MAG/2016KDDCupSelectedAffiliations.txt') as f:
        lines = f.readlines()
        selected_aff_ids = [str(line.split('\t')[0]) for line in lines]
    author_to_affs_dict = {}
    with open('/home/share/MAG/PaperAuthorAffiliations.txt') as f:
        line = f.readline()
        counter = 0
        while line:
            counter += 1
            if counter % 1000000 == 0:
                print counter / 1000000, 'M'
            parts = line.split('\t')
            auth_id = parts[1]
            affi_id = parts[2]
            if auth_id not in author_to_affs_dict:
                author_to_affs_dict[auth_id] = []
            if affi_id and affi_id in selected_aff_ids and affi_id not in author_to_affs_dict[auth_id]:
                author_to_affs_dict[auth_id].append(affi_id)
            line = f.readline()
    with open('author_to_affs.txt', 'w') as wf:
        for author, affs in author_to_affs_dict.items():
            if not affs:
                continue
            wf.write(author + '\t')
            for aff in affs:
                wf.write(aff + '\t')
            wf.write('\n')
    with open('author_to_affs.json', 'w') as wf:
        wf.write(json.dumps(author_to_affs_dict, indent=4))

    print 'sampling author to affs dict ok'


def sample_paper_author_aff():
    print 'sampling paper author aff dict...'
    with open('/home/share/MAG/2016KDDCupSelectedAffiliations.txt') as f:
        lines = f.readlines()
        selected_aff_ids = [str(line.split('\t')[0]) for line in lines]
    with open('/home/share/MAG/PaperAuthorAffiliations.txt') as f:
        with open('sample/selected_paper_auth_aff.txt', 'w') as wf:
            raw_line = f.readline()
            counter = 0
            tot_counter = 0
            while raw_line:
                tot_counter += 1
                if tot_counter % 10000000 == 0:
                    print 'raw line:', tot_counter / 1000000, 'M'
                line = ''
                parts = raw_line.split('\t')
                aff_id = parts[2]
                if aff_id in selected_aff_ids:
                    counter += 1
                    selected_parts = parts[:3] + parts[4:]
                    for part in selected_parts:
                        line += str(part) + '\t'
                    wf.write(line[:-1])
                    if counter % 1000000 == 0:
                        print 'select line:', counter / 1000000, 'M'
                raw_line = f.readline()


def select_kddcup_paper_auth_aff():
    with open('MAG/2016KDDCupSelectedPapers.txt') as f:
        paper_lines = f.readlines()
        paper_ids = [paper_line.split('\t')[0] for paper_line in paper_lines]
    counter = 0
    tot_counter = 0
    with open('sample/PaperAuthorAffiliations.txt') as f:
        with open('sample/kdd_paper_auth_aff.txt', 'w') as wf:
            raw_line = f.readline()
            while raw_line:
                tot_counter += 1
                if tot_counter % 1000000 == 0:
                    print 'total:', tot_counter / 1000000, 'M'
                if raw_line.split('\t')[0] in paper_ids:
                    counter += 1
                    if counter % 100000 == 0:
                        print 'select:', counter
                    wf.write(raw_line)
                raw_line = f.readline()


def classify_selected_papers():
    year_dict = {}
    with open('MAG/2016KDDCupSelectedPapers.txt') as f:
        paper_lines = f.readlines()
        for paper_line in paper_lines:
            parts = paper_line.split('\t')
            parts = parts[:1] + parts[2:]
            line = ''
            for part in parts:
                line += part + '\t'
            line = line[:-1]
            year = parts[1]
            if year not in year_dict:
                year_dict[year] = []
            year_dict[year].append(line)

    for year, paper_lines in year_dict.items():
        with open('sample/' + year + '_papers.txt', 'w') as f:
            for paper_line in paper_lines:
                f.write(paper_line)


get_author_to_affs_dict()
