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
		if any([key <= i for i in stroke if key != 10]):
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
		"SH": "RB",
		"ST": "FT",
		"KH": "FP",
		"SR": "F",
		"SKWR": "PBLG",
		"TH": "*T",
		"K": "BG",
		"TR": "RT",
		"KWR": ""
	}

for outline, translation in s: # illegal steno
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
		if "*" in right:
			right = right.replace("*", "")
			if "*" in preceding:
				suggestion = outline.replace(f"/{front}EUS/TEUBG", f"{right}/ST-BG")
			else:
				precedingIndices = convertToIndices(preceding)
				asteriskIndex = [i for i, j in enumerate(precedingIndices) if j < 10][-1]
				precedingModified = preceding[:asteriskIndex] + "*" + preceding[asteriskIndex:]
				suggestion = outline.replace(f"{preceding}/{front}EUS/TEUBG", f"{precedingModified}{right}/ST-BG")
		else:
			suggestion = outline.replace(f"/{front}EUS/TEUBG", f"{right}/ST-BG")
		if suggestion in warbler:
			print("*", outline, translation, suggestion)
			continue
		print(outline, translation, suggestion)
		suggestions[suggestion] = translation

json.dump(suggestions, open("isticBrief.json", "w+"), indent=0)