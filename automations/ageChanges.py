import json, re

s = [
		line.strip(",\n").replace('"', '').split(": ")
		for line in open("lapwing-base.json").readlines()
	]
s.append([
		line.strip(",\n").replace('"', '').split(": ")
		for line in open("lapwing-proper-nouns.json").readlines()
	])
s = s[1:-2]

warbler = json.load(open("warbler-base.json"))

for outline, translation in s:
	if re.search("/.+APBLG", outline) is not None:
		if translation in warbler.values():
			print("* ", end="")
		print(outline, translation)