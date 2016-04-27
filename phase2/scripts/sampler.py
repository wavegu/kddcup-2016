import os
from os.path import join
from model.util import MAG_SAMPLE_PAPER_AUTHOR_AFFS_PATH, DATA_DIR


class Sampler:

    def __init__(self):
        self.paper_path = join(DATA_DIR, 'selected_papers.txt')
        self.sample_paper_author_affs_path = join(DATA_DIR, 'sample_paper_author_affs.txt')
        self.paperids = []

    def get_paperids(self):
        if self.paperids:
            return self.paperids
        with open(self.paper_path) as f:
            paper_lines = f.readlines()
            self.paperids = [line.split('\t')[0] for line in paper_lines if line]
        return self.paperids

    def sample_paper_author_aff(self):
        if os.path.exists(self.sample_paper_author_affs_path):
            return
        self.get_paperids()
        with open(self.sample_paper_author_affs_path, 'w') as wf:
            with open(MAG_SAMPLE_PAPER_AUTHOR_AFFS_PATH) as f:
                counter = 0
                lines = f.readlines()
                tot = len(lines)
                for line in lines:
                    counter += 1
                    print '[%d/%d]' % (counter, tot)
                    parts = line.split('\t')
                    if parts[0] in self.paperids:
                        sample_line = '\t'.join(parts[:3] + parts[4:])
                        wf.write(sample_line)

    def get_author_to_affs_dict(self):
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
                    print(counter / 1000000, 'M')
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


if __name__ == '__main__':
    sampler = Sampler()
    sampler.sample_paper_author_aff()