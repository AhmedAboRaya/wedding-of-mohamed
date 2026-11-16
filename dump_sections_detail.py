import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})
root = page.get('A', {}).get('A', [])[0]
subpages = root.get('t', [])

# Map font IDs to names
font_map = {}
for f in page.get('B', []):
    font_map[f.get('A')] = f.get('C')

def get_font_name(f_id):
    if not f_id:
        return ""
    clean_id = f_id.split(',')[0].strip()
    return font_map.get(clean_id, f_id)

def extract_element_info(el):
    info = {
        'id': el.get('_'),
        'role': el.get('N', ''),
        'type': el.get('A?'),
        'x': el.get('A'),
        'y': el.get('B'),
        'w': el.get('D'),
        'h': el.get('C'),
        'texts': [],
        'colors': [],
        'fonts': [],
        'font_sizes': [],
        'links': [],
        'button_fill': None
    }
    
    # check button/shape background fill
    if 'b' in el and isinstance(el['b'], list):
        for shape in el['b']:
            if isinstance(shape, dict):
                fill = shape.get('C', {}).get('B')
                if fill:
                    info['colors'].append(fill)
                    info['button_fill'] = fill

    # check link in element
    def find_links(sub):
        found = []
        if isinstance(sub, dict):
            for k, v in sub.items():
                if k in ['link', 'url', 'href'] and isinstance(v, str):
                    found.append(v)
                elif isinstance(v, str) and (v.startswith('http') or v.startswith('mailto:')):
                    found.append(v)
                elif isinstance(v, (dict, list)):
                    found.extend(find_links(v))
        elif isinstance(sub, list):
            for item in sub:
                found.extend(find_links(item))
        return found
    
    info['links'] = find_links(el)

    # find text in 'a' -> 'C'
    if 'a' in el and isinstance(el['a'], dict):
        c = el['a'].get('C')
        if isinstance(c, dict):
            if 'A' in c and isinstance(c['A'], list):
                for t in c['A']:
                    if isinstance(t, str):
                        info['texts'].append(t.strip())
            if 'C' in c and isinstance(c['C'], list):
                for style in c['C']:
                    if isinstance(style, dict):
                        if style.get('M'):
                            info['colors'].append(style.get('M'))
                        if style.get('G'):
                            info['font_sizes'].append(style.get('G'))
                        if style.get('C'):
                            info['fonts'].append(get_font_name(style.get('C')))

    # find text in 'f' (e.g. inside button/shape)
    if 'f' in el and isinstance(el['f'], list):
        for f_item in el['f']:
            if isinstance(f_item, dict):
                c = f_item.get('A', {}).get('C')
                if isinstance(c, dict):
                    if 'A' in c and isinstance(c['A'], list):
                        for t in c['A']:
                            if isinstance(t, str):
                                info['texts'].append(t.strip())
                    if 'C' in c and isinstance(c['C'], list):
                        for style in c['C']:
                            if isinstance(style, dict):
                                if style.get('M'):
                                    info['colors'].append(style.get('M'))
                                if style.get('G'):
                                    info['font_sizes'].append(style.get('G'))
                                if style.get('C'):
                                    info['fonts'].append(get_font_name(style.get('C')))

    # deduplicate colors and fonts
    info['colors'] = list(dict.fromkeys(info['colors']))
    info['fonts'] = list(dict.fromkeys(info['fonts']))
    info['font_sizes'] = list(dict.fromkeys(info['font_sizes']))

    return info

output_lines = []

for i, sp in enumerate(subpages):
    sec_name = sp.get('B') or f"Section {i+1}"
    output_lines.append(f"\n==================================================")
    output_lines.append(f"SECTION {i+1}: {sec_name}")
    output_lines.append(f"==================================================")
    
    # Background
    bg_info = sp.get('D')
    output_lines.append(f"Background: {json.dumps(bg_info)}")
    
    elements = sp.get('E', [])
    output_lines.append(f"Total elements: {len(elements)}")
    
    for el_idx, el in enumerate(elements):
        info = extract_element_info(el)
        if info['texts'] or info['button_fill'] or info['links']:
            output_lines.append(f"\n  [Element {el_idx+1}] (Role: {info['role']}, Type: {info['type']})")
            if info['texts']:
                output_lines.append(f"    Texts: {' | '.join(info['texts'])}")
            if info['fonts']:
                output_lines.append(f"    Fonts: {', '.join(info['fonts'])}")
            if info['font_sizes']:
                output_lines.append(f"    Sizes: {', '.join(info['font_sizes'])}")
            if info['colors']:
                output_lines.append(f"    Colors: {', '.join(info['colors'])}")
            if info['button_fill']:
                output_lines.append(f"    Button/Shape Fill: {info['button_fill']}")
            if info['links']:
                output_lines.append(f"    Links: {', '.join(info['links'])}")

report = "\n".join(output_lines)
with open('report_sections.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("Saved report_sections.txt")
