import json, re

STENO_ORDER = ["#", "S1", "T1", "K", "P1", "W", "H", "R1", "A", "O", "*",
				"E", "U", "F", "R2", "P2", "B", "L", "G", "T2", "S2", "D", "Z"]
LEFT_RIGHT_DUPL = ["S", "T", "P", "R"]

def convertToIndices(stroke, force_right=False):
	indices = []
	middle = 100
	for i, key in enumerate(stroke):
		if key in "AO*-EU":
			middle = i
		if key == "-":
			indices.append(10)
		elif key not in LEFT_RIGHT_DUPL:
			indices.append(STENO_ORDER.index(key))
		elif force_right or i > middle:
			indices.append(STENO_ORDER.index(key+"2"))
		else:
			indices.append(STENO_ORDER.index(key+"1"))
	return indices

def hasOverlap(stroke, insert):
	stroke = convertToIndices(stroke)
	insert = convertToIndices(insert, force_right=True)
	for key in insert:
		if any([key <= i for i in stroke]):
			return True
	return False

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

left_to_right = {
		"TP": "F",
		"TKPW": "G",
		"PH": "PL",
		"TP*": "F",
		"TPH": "PB",
		"TK": "D",
		"PW": "B",
		"HR": "L",
		"S*": "Z",
		"SR": "F",
		"SKWR": "PBLG",
		"KWR": ""
	}

for outline, translation in s:
	if outline in warbler:
		continue
	if re.search("/[^/]*EUS/TEUBG(/.*)?", outline) is not None:
		front = re.search("/([^/]*)EUS/TEUBG(/.*)?", outline).groups(1)[0]
		right = front
		if right in left_to_right: right = left_to_right[right]
		preceding = re.search("(.*)/[^/]*EUS/TEUBG(/.*)?", outline).groups(1)[0]
		preceding = preceding.split("/")[-1]
		if front == "KW" or hasOverlap(preceding, right):
			print("(x)", outline, translation)
			continue
		suggestion = outline.replace(f"/{front}EUS/TEUBG", f"{right}/ST-BG")
		print(outline, translation, suggestion)
		suggestions[suggestion] = translation

json.dump(suggestions, open("isticBrief.json", "w+"), indent=0)
