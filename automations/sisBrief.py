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

ws = [
		line.strip(",\n").replace('"', '').split(": ")
		for line in open("warbler-base.json").readlines()
	]
ws = ws[1:-2]
s += ws

warbler = json.load(open("warbler-base.json"))

suggestions = {}

for outline, translation in s:
	if outline in warbler:
		continue
	if re.search("[^TZ]/SEUS$", outline) is not None and translation[-3:] == "sis":
		suggestion = outline.replace("/SEUS", "SZ")
		print(outline, translation, suggestion)
		suggestions[suggestion] = translation

json.dump(suggestions, open("sisBrief.json", "w+"), indent=0)