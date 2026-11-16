import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Base keys:", list(data.get('base', {}).keys()))
print("Page keys:", list(data.get('page', {}).keys()))
print("UI keys:", list(data.get('ui', {}).keys()))

# Recursively search for text, colors, titles, fonts, sections
def find_strings(obj, min_len=3):
    res = []
    if isinstance(obj, str):
        if len(obj.strip()) >= min_len and not obj.startswith('http') and not obj.startswith('data:'):
            res.append(obj.strip())
    elif isinstance(obj, dict):
        for k, v in obj.items():
            res.extend(find_strings(v, min_len))
    elif isinstance(obj, list):
        for item in obj:
            res.extend(find_strings(item, min_len))
    return res

strings = find_strings(data)
print(f"Total strings found: {len(strings)}")
# filter unique preserving order
seen = set()
unique_strings = []
for s in strings:
    if s not in seen and len(s) < 200:
        seen.add(s)
        unique_strings.append(s)

print("Sample strings:")
for s in unique_strings[:50]:
    print("-", s)
