import os, json, re
from pathlib import Path

_dir = Path("../scans")

ptrn = re.compile(r"scan-(\d+-\d+-\d+)-(.*)\.log")
loads = {}

for i in os.listdir(_dir):
	file = _dir / i
	with open(file, encoding="utf8") as f:
		_r = f.read()
		_t = json.loads(_r)
		
		date = ptrn.match(i).group(1)

		loads[date] = _t

with open("out.json", "w", encoding="utf8") as f:
	json.dump(loads, f)