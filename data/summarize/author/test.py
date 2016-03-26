with open('author_to_affs.txt') as f:
	author_to_affs_dict = {}
	lines = f.readlines()
	for line in lines:
		parts = line.replace('\n', '').replace('\r', '').split('\t')
		author_id = parts[0]
		affs = parts[1:]
		author_to_affs_dict[author_id] = affs
with open('author_to_affs.json', 'w') as f:
	import json
	f.write(json.dumps(author_to_affs_dict, indent=4))