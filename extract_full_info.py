import json
import re

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})

print("Page keys:", list(page.keys()))

# Let's see what each page key represents
for k in page:
    val = page[k]
    if isinstance(val, list):
        print(f"Key {k}: List of len {len(val)}")
        if len(val) > 0:
            print(f"  First item type: {type(val[0])}")
            if isinstance(val[0], dict):
                print(f"  First item keys: {list(val[0].keys())}")
    elif isinstance(val, dict):
        print(f"Key {k}: Dict with keys {list(val.keys())[:10]}")
    else:
        print(f"Key {k}: {val}")

# Let's extract all colors (hex codes)
all_str = json.dumps(data)
hex_colors = set(re.findall(r'#[0-9a-fA-F]{3,8}', all_str))
print("\n=== All Hex Colors Found ===")
for c in sorted(hex_colors):
    print(c)

# Let's find font names or typography info
font_matches = set(re.findall(r'[A-Za-z0-9_-]+,\s*\d+', all_str))
print("\n=== Potential Font IDs ===")
for fm in font_matches:
    print(fm)

# Let's search for all text contents in document
def extract_text_blocks(obj, path=""):
    results = []
    if isinstance(obj, dict):
        # Look for text indicators
        for k, v in obj.items():
            if isinstance(v, str) and len(v.strip()) > 0:
                # Check if it looks like human text
                if not v.startswith('http') and not v.startswith('#') and not v.startswith('data:') and not v.endswith('.js') and not v.endswith('.css') and not re.match(r'^[A-Za-z0-9+/=_-]{20,}$', v):
                    # Filter out short hash IDs
                    if len(v) > 2 and not re.match(r'^[A-Z0-9_]{10,}$', v):
                        results.append((path + "." + k, v))
            elif isinstance(v, (dict, list)):
                results.extend(extract_text_blocks(v, path + "." + k))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            results.extend(extract_text_blocks(item, f"{path}[{i}]"))
    return results

texts = extract_text_blocks(page, "page")
print(f"\n=== Text Blocks Found ({len(texts)}) ===")
for p, t in texts:
    print(f"[{p}] -> {t}")
