import re
import json

with open('site.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Locate window['bootstrap']
idx = content.find("window['bootstrap'] = JSON.parse('")
if idx != -1:
    start = idx + len("window['bootstrap'] = JSON.parse('")
    # find where the JSON string ends
    # The JSON string ends with ');
    end = content.find("');", start)
    raw = content[start:end]
    print(f"Extracted raw length: {len(raw)}")
    # Canva json is string-escaped
    # Let's decode JSON string or unescape
    # In JS: JSON.parse('...') where ... has escaped quotes \' or \\
    # Let's use json.loads directly by wrapping in quotes or replacing \'
    # Actually python's codecs or json can handle it:
    try:
        data = json.loads(f'"{raw}"')
        data = json.loads(data) # second parse if double encoded
    except Exception as e:
        # let's try raw unicode_escape or custom replace
        import codecs
        try:
            un = codecs.decode(raw, 'unicode_escape')
            data = json.loads(un)
        except Exception as e2:
            print(f"Error decoding: {e2}")
            # Try manual replace
            cleaned = raw.replace(r"\'", "'").replace(r'\"', '"')
            data = json.loads(cleaned)

    print("Success! Keys:", list(data.keys()))
    with open('bootstrap.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
    print("Dumped bootstrap.json")
else:
    print("Not found")
