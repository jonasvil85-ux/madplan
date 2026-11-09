"""Skriver de engelske billedbeskrivelser fra bibliotek_4.py og bibliotek_5.py ind i billedprompts.json (kun for retter, der mangler).
Kør: python -I scripts/byg_bibliotek4.py   – derefter billeder.py og byg_opskrifter.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bibliotek_4 import EN as EN4
from bibliotek_5 import EN as EN5
EN = {**EN4, **EN5}

STI = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'billedprompts.json')
d = json.load(open(STI, encoding='utf-8'))
nye = {n: t for n, t in EN.items() if n not in d}
d.update(nye)
json.dump(d, open(STI, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(nye), 'nye billedbeskrivelser,', len(d), 'i alt')
