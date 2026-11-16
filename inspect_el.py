import json

with open('bootstrap.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

page = data.get('page', {})
root_pages = page.get('A', {}).get('A', [])
subpages = root_pages[0].get('t', [])

# Let's inspect all subpage names
print("Subpage names:")
for i, sp in enumerate(subpages):
    print(f"{i}: {sp.get('B')}")

# Let's see what keys are in an element
first_el = subpages[0]['E'][0]
print("\nFirst element in Home:")
print(json.dumps(first_el, indent=2)[:1000])

first_text_el = subpages[0]['E'][1]
print("\nSecond element in Home:")
print(json.dumps(first_text_el, indent=2)[:1500])
