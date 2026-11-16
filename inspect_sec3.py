import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})
root = page.get('A', {}).get('A', [])[0]
subpages = root.get('t', [])

# Inspect all elements in all sections
for i, sp in enumerate(subpages):
    print(f"\n--- Section {i+1}: {sp.get('B')} (Elements: {len(sp.get('E', []))}) ---")
    for j, el in enumerate(sp.get('E', [])):
        print(f"El {j+1}: type={el.get('A?')}, role={el.get('N')}, keys={list(el.keys())}")
        # print full json of element
        el_str = json.dumps(el, ensure_ascii=False)
        # find arabic or english strings
        import re
        strs = re.findall(r'[\u0600-\u06FF\w\s.,!?:;\'"’♡🤍🕊️-]+', el_str)
        meaningful = [s.strip() for s in strs if len(s.strip()) > 3 and not s.strip().startswith('LB') and not s.strip().startswith('MAG') and not s.strip().startswith('PB') and not s.strip().startswith('EAG')]
        if meaningful:
            print(f"   Texts/Tokens: {meaningful[:8]}")
        # check if it has media or video or embed
        if 'B' in el and isinstance(el['B'], dict):
            print(f"   B: {el['B']}")
        for k in ['f', 'b', 'c', 'd', 'e', 'h', 'G', 'I']:
            if k in el:
                val = str(el[k])
                if len(val) < 200:
                    print(f"   {k}: {val}")
