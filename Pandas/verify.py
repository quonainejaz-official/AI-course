import json, re

files = [
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Basics\Pandas_Basics.ipynb',
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Intermediate\Pandas_Intermediate.ipynb',
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Advance\Pandas_Advance.ipynb',
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Intermediate\01_Grouping_Aggregation_and_Pivot_Tables.ipynb',
]

words = ['hai','hain','karo','karein','karte','karta','kiya','aur','mein','andar','ke','ki','ka','liye','se','ko',
         'samjhao','tarika','banao','kya','ye','yeh','yah','jata','hota','hoti','hote',
         'skte','skta','sakta','sakti','rakhta','rakhti','dena','deta','lena','leta','wala','wali','wale',
         'aasan','chahiye','bahut','jese','inhein','unhein','iska','unka','kyun','dunia','sab','har','kuch',
         'bataya','batao','rakhta','ho','rakhna','rakh','duniya','jo','ne','aap','hum','bhi','lekin','magar',
         'agar','woh','wo','yahan','wahan','jahan','tab','jab','isliye','kyuki','kyonke','raha','rahi','rahe',
         'kaam','samjho','jaante','jaanta','jana','karna','hona','nikal','dal','rakh','bina','liya','diya',
         'kar','nikla','sikh','parh','likh','bol','jaan','mil','milta','mila','dekh','dikha']

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        nb = json.load(fh)
    found = False
    for cell in nb['cells']:
        src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        for w in words:
            for m in re.finditer(r'\b' + w + r'\b', src, re.IGNORECASE):
                start = max(0, m.start()-30)
                end = min(len(src), m.end()+30)
                ctx = src[start:end].replace('\n',' ').strip()
                print(f'{f.split(chr(92))[-1]}: "{w}" -> ...{ctx}...')
                found = True
    if not found:
        print(f'{f.split(chr(92))[-1]}: CLEAN (no Urdu words found)')
