with open('rank.json') as f:
    import json
    affs = []
    rank = json.load(f)[:100]
    for pair in rank:
        id = pair[0].replace('\r', '').split(' ')[0]
        name = pair[0].replace('\r', '')
        name = name[name.find(' ')+1:]
        affs.append({id: name})
with open('../../sample/top_affs.json', 'w') as f:
    f.write(json.dumps(affs, indent=4))