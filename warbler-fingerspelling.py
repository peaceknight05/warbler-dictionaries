import re

LONGEST_KEY = 1

L_STROKES = [
	"#STKPWHR",

	"#TKPWHR", "STKPWHR",

	"#STKPH", "TKPWHR",

	"#SKWR", "STKPW", "STKPH", "SKPHR", "KPWHR",

	"#STP", "#TPH", "#THR", "#KWR", "#KHR", "STPH", "SKWR", "TKPW", "KPHR",

	"#SK", "#TP", "#TR", "#TH", "#KP", "#KW", "#PH", "#HR", "STK", "STP", "TPH",
	"KWR", "PHR",

	"#T", "#K", "#W", "SR", "TK", "TP", "KP", "KR", "KW", "KH", "PW", "PH", "HR",

	"S", "T", "K", "P", "W", "H", "R"
]

L_TRANS = [
	"ni",

	"gl", "ne",

	"ankyl", "ny",

	"e", "z", "acanth", "macr", "pyl",

	"phyt", "a", "erythr", "i", "an", "leuc", "j", "g", "micr",

	"ac", "phy", "tyr", "mni", "ex", "q", "ph", "rhyn", "pseud", "cephal", "n",
	"y", "pl",

	"tri", "cocc", "u", "v", "d", "f", "x", "c", "qu", "ch", "b", "m", "l",

	"s", "t", "k", "p", "w", "h", "r"
]

V_STROKES = [
	"AOEU",
	"AOE", "AOU", "AEU", "OEU",
	"AO", "AE", "AU", "OE", "OU", "EU",
	"A", "O", "E", "U"
]

V_TRANS = [
	"ea",
	"ee", "oo", "ei", "oi",
	"oa", "ae", "au", "oe", "ou", "i",
	"a", "o", "e", "u"
]

R_STROKES = [
	"FPLTGS",

	"*FRPB", "*FRPL", "*FRGS", "*FRDZ", "*PBLG", "*PBGS", "FLGTD",

	"*FRP", "*FPL", "*FPZ", "*FBL", "*FSZ", "*RPB", "*PBG", "*PLD", "*PLZ", "*BGT",
	"*BGS", "*BGZ", "*LGT", "*LGD", "FRPB", "FRPL", "FBGS", "FLGD", "PBLG", "PBGT",
	"LGTD",

	"*FP", "*FZ", "*RP", "*PB", "*PL", "*BG", "*BS", "*BZ", "*LS", "*GT", "*GZ",
	"*TS", "*DZ", "FRP", "FPB", "FPD", "FLT", "FGS", "FSZ", "PBG", "PBZ", "PLT",
	"BGS", "BGZ", "LGT", "LGD", "GSZ",

	"*F", "*R", "*L", "*G", "*T", "*S", "*D", "*Z", "FR", "FP", "FB", "FT", "FS",
	"FD", "FZ", "RB", "PB", "PL", "BL", "BG", "BZ", "LG", "LS", "LD", "LZ", "GT",
	"GS", "GZ", "TD", "SZ", "DZ",

	"F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"
]

R_TRANS = [
	"phthalmus",

	"nch", "mim", "virus", "vri", "j", "nnus", "stes",

	"mp", "forme", "ceps", "phyll", "ssis", "rrhen", "nc", "pillo", "pillus", "canth",
	"ces", "cys", "lta", "les", "min", "mum", "phus", "ses", "myc", "na",
	"tes",

	"forma", "phis", "re", "nae", "pyl", "c", "x", "ceae", "lis", "ta", "gis",
	"tus", "des", "pter", "chry", "chy", "phthal", "sus", "ssis", "ng", "nis", "ment",
	"cus", "cis", "la", "es", "zus",

	"v", "rr", "ll", "gea", "th", "cea", "dae", "zoa", "saur", "ch", "phy", "st", "sis",
	"sa", "phys", "sh", "n", "m", "bil", "k", "bis", "lch", "lys", "ia", "yx", "a",
	"us", "o", "um", "sys", "ii",

	"f", "r", "p", "b", "l", "g", "t", "s", "d", "z"
]

def lookup(outline):
	assert len(outline) <= LONGEST_KEY

	stroke = outline[0]

	if stroke == "*": return "=undo"
	elif stroke == "#": return "{^ ^}"
	elif stroke == "R-R": return "{^~|\n^}"
	elif stroke == "#*": return "{PLOVER:END_SOLO_DICT}"

	out = ""

	left, vowels, right = re.match("(#?[STKPWHR]*)([AO]*[-*]?[EU]*)([FRPBLGTSDZ]*)", stroke).groups()
	vowels = vowels.replace("-", "")
	if "*" in vowels:
		right = "*" + right
		vowels = vowels.replace("*", "")

	larr = []
	if left:
		for i, chord in enumerate(L_STROKES):
			if chord in left:
				larr.append((left.index(chord), L_TRANS[i]))
				left = left.replace(chord, "-"*len(chord))
	out += "".join([i[1] for i in sorted(larr)])
	if vowels:
		out += V_TRANS[V_STROKES.index(vowels)]
	rarr = []
	if right:
		for i, chord in enumerate(R_STROKES):
			if chord in right:
				rarr.append((right.index(chord), R_TRANS[i]))
				right = right.replace(chord, "-"*len(chord))
	out += "".join([i[1] for i in sorted(rarr)])

	return "{&" + out + "}"