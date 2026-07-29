import json, re

with open(r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Intermediate\01_Grouping_Aggregation_and_Pivot_Tables.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    for m in re.finditer(r'\bwo\b', src, re.IGNORECASE):
        start = max(0, m.start()-40)
        end = min(len(src), m.end()+40)
        ctx = src[start:end].replace('\n', ' ').strip()
        print(f'Cell {i} ({cell["cell_type"]}): ...{ctx}...')
