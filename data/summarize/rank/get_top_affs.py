with open('rank.json') as f:
    import json
    affs = []
    rank = json.load(f)[:100]
    for pair in rank:
        affs.append(pair[0].replace('\r', ''))
with open('../../sample/top_affs.json', 'w') as f:
    f.write(json.dumps(affs, indent=4))