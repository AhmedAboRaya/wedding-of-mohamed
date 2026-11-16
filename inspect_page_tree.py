import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Let's inspect the page structure
page = data.get('page', {})

# Canva pages structure is typically minified with letter keys.
# Let's write a recursive explorer that extracts sections, text nodes, images, and styles.

def dump_structure(obj, depth=0):
    indent = "  " * depth
    if isinstance(obj, dict):
        # check if it has text or known element markers
        keys = list(obj.keys())
        summary = {}
        for k in keys:
            v = obj[k]
            if isinstance(v, (str, int, float, bool)) and len(str(v)) < 100:
                summary[k] = v
        # print if it looks like an element or page
        return summary
    return None

# Let's save a detailed analysis script
with open('explore_page.py', 'w', encoding='utf-8') as f_out:
    f_out.write('''
import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})

# Let's inspect page keys and sizes
for k, v in page.items():
    if isinstance(v, list):
        print(f"page['{k}'] is list with {len(v)} items")
    elif isinstance(v, dict):
        print(f"page['{k}'] is dict with keys: {list(v.keys())}")
    else:
        print(f"page['{k}'] = {v}")
''')

