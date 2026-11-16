import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})
root_pages = page.get('A', {}).get('A', [])

print(f"Total root page sets: {len(root_pages)}")
if root_pages:
    subpages = root_pages[0].get('t', [])
    print(f"Total sub-sections/pages (t): {len(subpages)}")
    for i, sp in enumerate(subpages):
        sec_name = sp.get('B', f'Section_{i}')
        sec_id = sp.get('a', '')
        elements = sp.get('E', [])
        print(f"\n==========================================")
        print(f"SECTION {i+1}: {sec_name} (id: {sec_id}) - Elements: {len(elements)}")
        print(f"==========================================")
        
        # Check background of this section
        # Look for background color or fill in sp
        for k in ['D', 'C', 'F', 'G']:
            if k in sp:
                print(f"  Prop {k}: {sp[k]}")

        for el_idx, el in enumerate(elements):
            # Inspect element
            el_type = el.get('N', 'unknown')
            # Extract text if any
            # In Canva text is often stored in 'a' -> 'C' -> 'C' or similar, or let's search recursively
            def find_text_and_styles(sub):
                texts = []
                styles = []
                if isinstance(sub, dict):
                    # Check text content
                    # Canva text runs often have text or font
                    for k, v in sub.items():
                        if isinstance(v, str) and len(v.strip()) > 0:
                            if any(c in v for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') and not v.startswith('LB') and not v.startswith('PB') and not v.startswith('EAG') and not v.startswith('MAG'):
                                texts.append(f"{k}:{v}")
                        elif isinstance(v, (dict, list)):
                            t, s = find_text_and_styles(v)
                            texts.extend(t)
                            styles.extend(s)
                elif isinstance(sub, list):
                    for item in sub:
                        t, s = find_text_and_styles(item)
                        texts.extend(t)
                        styles.extend(s)
                return texts, styles

            # Print element summary
            print(f"  Element {el_idx+1} [Type: {el_type}] keys: {list(el.keys())}")
            # Let's inspect el structure
