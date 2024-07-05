import json

# lapwing = json.load(open("lapwing-base.json"))
# pnouns = json.load(open("lapwing-proper-nouns.json"))

# lapwing.update(pnouns)

lapwing = json.load(open("sisBrief.json"))

warbler = iter(sorted(json.load(open("warbler-base.json")).items()))

i = 0
cur = next(warbler)

overriden = []
duplicate = []

for outline, translation in sorted(lapwing.items()):
	if cur is None: break
	if outline < cur[0]: continue
	while outline > cur[0]:
		cur = next(warbler, None)
		if cur is None: break
	if cur is None: break
	if outline == cur[0]:
		if translation == cur[1]:
			duplicate.append((outline, translation))
		else:
			overriden.append([outline, cur[1], translation])

print("--- DUPLICATES ---")
for outline, translation in duplicate:
	print(f"{outline:<30}{translation}")

print("\n--- OVERRIDES ---")
for outline, warbler, lapwing in overriden:
	print(f"{outline:<25}{warbler:<25}{lapwing}")