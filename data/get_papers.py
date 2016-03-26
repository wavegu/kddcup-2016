with open('/home/share/MAG/2016KDDCupSelectedPapers.txt') as f:
    lines = f.readlines()
conf_ids = []
for line in lines:
    conf_id = line.split('\t')[-2]
    if conf_id not in conf_ids:
        conf_ids.append(conf_id)

with open('/home/share/MAG/Papers.txt') as f:
    with open('selected_papers.txt', 'w') as wf:
        line = f.readline()
        counter = 0
        while line:
            counter += 1
            if counter % 10000000 == 0:
                print(counter / 10000000, '0M')
            parts = line.split('\t')
            if parts[-2] in conf_ids:
                try:
                    wf.write(parts[0] + '\t' + parts[3] + '\t' + parts[4] + '\t' + parts[7] + '\t' + parts[8] + '\t' + parts[9] + '\n')
                except Exception:
                    line = f.readline()
                    continue
            line = f.readline()
