import re

LONGEST_KEY = 1

L_STROKES = [
	"#STKPWHR",

	"#TKPWHR",

	"#STKPH", "#STPHR", "#TKPWH", "#KPWHR", "TKPWHR",

	"#STKH", "#STPH", "#SKWR", "STKPW", "STPHR", "SKPHR", "TKPHR", "TKPWH",
	"TKWHR", "KPWHR",

	"#TPH", "#THR", "#KHR", "SKWR", "SPWR", "TKPW", "TKHR", "TPHR", "KPWH",
	"KPWR", "KPHR",

	"#TP", "#TR", "#TH", "#KW", "#KR", "#PH", "STK", "STP", "SPW", "TPW",
	"TPH", "THR", "KWH", "KWR", "PHR",

	"#S", "#T", "#K", "#W", "SR", "TK", "TP", "KP", "KR", "KW", "KH", "PW", "PH", "HR",

	"#", "S", "T", "K", "P", "W", "H", "R"
]

L_TRANS = [
	"anis",

	"gl",

	"ankyl", "arhynch", "gh", "myl", "ni",

	"acanth", "an", "vir", "z", "cephal", "macr", "dipl", "ny",
	"phyt", "pyl",

	"myc", "erythr", "leuc", "j", "enter", "g", "lact", "rhynch", "phy",
	"phi", "micr",

	"eff", "tyr", "mni", "q", "acr", "ph", "pseud", "phys", "ent", "bat",
	"n", "rhyn", "y", "i", "pl",

	"a", "tri", "cocc", "u", "v", "d", "f", "x", "c", "qu", "ch", "b", "m", "l",

	"e", "s", "t", "k", "p", "w", "h", "r"
]

V_STROKES = [
	"AOEU",
	"AOE", "AOU", "AEU", "OEU",
	"AO", "AE", "AU", "OE", "OU", "EU",
	"A", "O", "E", "U"
]

V_TRANS = [
	"ea",
	"io", "oo", "ei", "oi",
	"oa", "ae", "au", "oe", "ou", "i",
	"a", "o", "e", "u"
]

R_STROKES = [
	"*FPBLDZ",

	"*FPBTD", "*FPLTD", "*FBGSZ", "*PBGSZ", "FPLGTS",

	"*FRPB", "*FRPL", "*FRGS", "*FRDZ", "*FPBZ", "*FBGS", "*FBDZ", "*FLSZ", "*PBLG",
	"*PBGS", "*BLDZ", "*BGTD", "*BGSZ", "*LGTD", "*LGSZ", "*LGDZ", "FLGTD", "PBLGZ",
	"PBGSZ", "BLGSZ",

	"*FRP", "*FPB", "*FPL", "*FBL", "*RPB", "*PBG", "*PLD", "*PLZ", "*BGT",
	"*BGS", "*BGD", "*BGZ", "*BTD", "*LGT", "*LGD", "*LSZ", "*GTD", "*GSZ",
	"FRPB", "FRPL", "FBGS", "FLGD", "FLSZ", "PBLG", "PBGT", "PBGS", "BGSZ",
	"LGTD", "LGDZ",

	"*FP", "*FB", "*FZ", "*RP", "*PB", "*PL", "*BL", "*BG", "*BS", "*BZ", "*LT",
	"*LD", "*GT", "*GD", "*TS", "*TD", "*DZ", "FRP", "FRB", "FPB", "FPD", "FPZ",
	"FLT", "FGS", "FSZ", "PBG", "PLT", "BGT", "BGS", "BGZ", "LGT", "LGD", "LGZ",
	"LTS", "LSZ", "LDZ", "GTD", "GSZ", "GDZ",

	"*F", "*R", "*L", "*G", "*T", "*S", "*D", "*Z", "FR", "FP", "FB", "FT",
	"FD", "FZ", "RB", "PB", "PL", "BL", "BG", "BS", "BZ", "LG", "LS", "LD", "LZ",
	"GT", "GS", "GD", "GZ", "TD", "SZ", "DZ",

	"F", "R", "P", "B", "L", "G", "T", "S", "D", "Z"
]

R_TRANS = [
	"bacteriaceae",

	"bacterium", "phthalmidae", "coccaceae", "neae", "phthalmus",

	"nch", "mim", "virus", "vri", "bacteraceae", "coccus", "cocci", "phis", "j",
	"nnus", "bacilli", "cum", "cae", "dus", "gis", "deae", "stes", "ni",
	"nae", "cis",

	"mp", "bacter", "forme", "phyll", "rrhen", "nc", "pillo", "pillus", "canth",
	"ces", "cidae", "cys", "batidae", "lta", "les", "lis", "dea", "zus",
	"min", "mum", "phus", "ses", "sis", "myc", "na", "nus", "bae",
	"tes", "lchii",

	"forma", "cocc", "phis", "re", "nae", "pyl", "bacill", "c", "bs", "ceae", "ti",
	"dd", "ta", "da", "tus", "tidae", "des", "pter", "chry", "mb", "chy", "ceps",
	"phthal", "sus", "ssis", "ng", "ment", "ba", "cus", "co", "la", "es", "i",
	"tis", "is", "lii", "ea", "ae", "gii",

	"v", "rr", "ll", "gea", "th", "cea", "dae", "zoa", "saur", "ch", "phy", "st",
	"sa", "phys", "sh", "n", "m", "bil", "k", "x", "bys", "lch", "lys", "ia", "yx",
	"a", "us", "ius", "o", "um", "sys", "ii",

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
	out += "".join(["{&%s}"%i[1] for i in sorted(larr)])
	if vowels:
		out += "{&%s}"%V_TRANS[V_STROKES.index(vowels)]
	rarr = []
	if right:
		for i, chord in enumerate(R_STROKES):
			if chord in right:
				rarr.append((right.index(chord), R_TRANS[i]))
				right = right.replace(chord, "-"*len(chord))
	out += "".join(["{&%s}"%i[1] for i in sorted(rarr)])

	return out