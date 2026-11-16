import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})
root = page.get('A', {}).get('A', [])[0]
subpages = root.get('t', [])

# Let's inspect media and graphics bindings for each element in each section
for i, sp in enumerate(subpages):
    print(f"\n================ SECTION {i+1}: {sp.get('B')} ================")
    # Section background
    bg = sp.get('D')
    print("Background config:", json.dumps(bg, indent=2))
    for j, el in enumerate(sp.get('E', [])):
        print(f"\n--- Element {j+1} [Type: {el.get('A?')}, Role: {el.get('N')}] ---")
        print("Position & Size: x={}, y={}, w={}, h={}".format(el.get('A'), el.get('B'), el.get('D'), el.get('C')))
        # Check text
        if 'a' in el and isinstance(el['a'], dict) and 'C' in el['a']:
            c = el['a']['C']
            if isinstance(c, dict):
                texts = c.get('A', [])
                styles = c.get('C', [])
                for idx, t in enumerate(texts):
                    style = styles[idx] if idx < len(styles) else {}
                    print(f"  Text: {repr(t)}")
                    print(f"  Style: font={style.get('C')}, size={style.get('G')}, color={style.get('M')}, align={style.get('c')}, weight={style.get('I')}")
        # Check if button/f text
        if 'f' in el and isinstance(el['f'], list) and el['f']:
            for f_item in el['f']:
                if isinstance(f_item, dict) and 'A' in f_item and 'C' in f_item['A']:
                    c = f_item['A']['C']
                    texts = c.get('A', [])
                    styles = c.get('C', [])
                    for idx, t in enumerate(texts):
                        style = styles[idx] if idx < len(styles) else {}
                        print(f"  Button/Inner Text: {repr(t)}")
                        print(f"  Style: font={style.get('C')}, size={style.get('G')}, color={style.get('M')}")
        # Check image/media reference
        # Where does J get its image from? Let's check keys in el
        for k in ['c', 'd', 'b', 'e', 'g', 'h', 'T', 'W', '5']:
            if k in el:
                val = el[k]
                # print if it looks like media ID
                print(f"  Key '{k}': {json.dumps(val, ensure_ascii=False)[:200]}")
