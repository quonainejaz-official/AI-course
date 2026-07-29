import json
import re
import os

MULTI_WORD = [
    (r'\bkar sakte hain\b', 'can'),
    (r'\bkar sakta hai\b', 'can'),
    (r'\bkar sakti hai\b', 'can'),
    (r'\bde sakte hain\b', 'can'),
    (r'\bho sakta hai\b', 'can be'),
    (r'\bho sakti hai\b', 'can be'),
    (r'\bho sakte hain\b', 'can be'),
    (r'\bhoti hain\b', 'are'),
    (r'\bhota hai\b', 'is'),
    (r'\bhote hain\b', 'are'),
    (r'\bhai yeh\b', 'is this'),
    (r'\bhai ye\b', 'is this'),
    (r'\bka istemal\b', 'usage'),
    (r'\bke saath\b', 'with'),
    (r'\bke liye\b', 'for'),
    (r'\bka matlab\b', 'means'),
    (r'\bka fayda\b', 'benefit of'),
    (r'\bki tarah\b', 'like'),
    (r'\bke upar\b', 'on'),
    (r'\bke baad\b', 'after'),
    (r'\bke andar\b', 'inside'),
    (r'\brakh kar\b', 'by keeping'),
    (r'\bkar rahe\b', 'doing'),
    (r'\bkar raha\b', 'doing'),
    (r'\bkar rahi\b', 'doing'),
    (r'\bho raha\b', 'is being'),
    (r'\bho rahi\b', 'is being'),
    (r'\bho rahe\b', 'are being'),
    (r'\buse karte\b', 'use'),
    (r'\buse karta\b', 'uses'),
    (r'\buse kiya\b', 'used'),
    (r'\bka use\b', 'use of'),
    (r'\bmein convert\b', 'convert to'),
    (r'\bse select\b', 'select by'),
    (r'\bse access\b', 'access by'),
    (r'\bse filter\b', 'filter by'),
    (r'\bse grouping\b', 'group by'),
    (r'\bse create\b', 'create from'),
    (r'\bse load\b', 'load from'),
    (r'\bse read\b', 'read from'),
    (r'\bse save\b', 'save to'),
]

REPLACEMENTS = [
    (r'\bhai\b', 'is'),
    (r'\bhain\b', 'are'),
    (r'\bkaro\b', 'do'),
    (r'\bkarein\b', 'do'),
    (r'\bkarte\b', 'do'),
    (r'\bkarta\b', 'does'),
    (r'\bkarti\b', 'does'),
    (r'\bkiya\b', 'done'),
    (r'\bkiye\b', 'done'),
    (r'\baur\b', 'and'),
    (r'\bmein\b', 'in'),
    (r'\bandar\b', 'inside'),
    (r'\bke\b', 'of'),
    (r'\bki\b', 'of'),
    (r'\bka\b', 'of'),
    (r'\bliye\b', 'for'),
    (r'\bse\b', 'with'),
    (r'\bko\b', 'to'),
    (r'\bsamjhao\b', 'explain'),
    (r'\bsamjhaya\b', 'explained'),
    (r'\btarika\b', 'method'),
    (r'\btareeqay\b', 'methods'),
    (r'\btareeqa\b', 'method'),
    (r'\bbanao\b', 'create'),
    (r'\bbanayein\b', 'create'),
    (r'\bbana\b', 'make'),
    (r'\bbanaye\b', 'create'),
    (r'\bkya\b', 'what'),
    (r'\bye\b', 'this'),
    (r'\byeh\b', 'this'),
    (r'\byah\b', 'this'),
    (r'\busay\b', 'it'),
    (r'\bise\b', 'it'),
    (r'\bjata\b', 'goes'),
    (r'\bhota\b', 'is'),
    (r'\bhoti\b', 'is'),
    (r'\bhote\b', 'are'),
    (r'\bskte\b', 'can'),
    (r'\bskta\b', 'can'),
    (r'\bsakta\b', 'can'),
    (r'\bsakti\b', 'can'),
    (r'\brakhta\b', 'contains'),
    (r'\brakhti\b', 'holds'),
    (r'\bdena\b', 'give'),
    (r'\bdeta\b', 'gives'),
    (r'\bdeti\b', 'gives'),
    (r'\blena\b', 'take'),
    (r'\bleta\b', 'takes'),
    (r'\bleti\b', 'takes'),
    (r'\bwala\b', 'which'),
    (r'\bwali\b', 'which'),
    (r'\bwale\b', 'which'),
    (r'\baasan\b', 'easy'),
    (r'\bchahiye\b', 'needed'),
    (r'\bbahut\b', 'very'),
    (r'\bjese\b', 'like'),
    (r'\binhein\b', 'them'),
    (r'\bunhein\b', 'them'),
    (r'\biska\b', 'its'),
    (r'\bunka\b', 'their'),
    (r'\bkyun\b', 'why'),
    (r'\bdunia\b', 'world'),
    (r'\bsab\b', 'all'),
    (r'\bhar\b', 'every'),
    (r'\bkuch\b', 'some'),
    (r'\bbataya\b', 'explained'),
    (r'\bbatao\b', 'tell'),
    (r'\bho\b', 'be'),
    (r'\brakhna\b', 'to keep'),
    (r'\bhona\b', 'to be'),
    (r'\bkarna\b', 'to do'),
    (r'\bjo\b', 'that'),
    (r'\bne\b', ''),
    (r'\bna\b', 'not'),
    (r'\baap\b', 'you'),
    (r'\bhum\b', 'we'),
    (r'\bbhi\b', 'also'),
    (r'\blekin\b', 'but'),
    (r'\bmagar\b', 'but'),
    (r'\bagar\b', 'if'),
    (r'\bwoh\b', 'that'),
    (r'\bvo\b', 'that'),
    (r'\baata\b', 'comes'),
    (r'\baati\b', 'comes'),
    (r'\baate\b', 'come'),
    (r'\brakha\b', 'kept'),
    (r'\bge\b', ''),
    (r'\bga\b', ''),
    (r'\bgi\b', ''),
    (r'\braha\b', ''),
    (r'\brahi\b', ''),
    (r'\brahe\b', ''),
    (r'\byahan\b', 'here'),
    (r'\bwahan\b', 'there'),
    (r'\bjahan\b', 'where'),
    (r'\btab\b', 'then'),
    (r'\bjab\b', 'when'),
    (r'\bisliye\b', 'therefore'),
    (r'\bkyuki\b', 'because'),
    (r'\bkyonke\b', 'because'),
    (r'\bchahiye\b', 'needed'),
    (r'\bnikalna\b', 'to find'),
    (r'\bnikalte\b', 'find'),
    (r'\bnikala\b', 'found'),
    (r'\bdalna\b', 'to put'),
    (r'\bdal kar\b', 'by putting'),
    (r'\bdaal\b', 'put'),
    (r'\bdaalein\b', 'put'),
    (r'\brakhte\b', 'keep'),
    (r'\bdekhna\b', 'to see'),
    (r'\bdekh\b', 'see'),
    (r'\bdikha\b', 'show'),
    (r'\bdikhao\b', 'show'),
    (r'\bdikhta\b', 'appears'),
    (r'\bmaan\b', 'assume'),
    (r'\bmaani\b', 'meaning'),
    (r'\bnikal\b', 'extract'),
    (r'\bdal\b', 'put'),
    (r'\brakh\b', 'keep'),
    (r'\bde\b', 'give'),
    (r'\ble\b', 'take'),
    (r'\bbina\b', 'without'),
    (r'\bliya\b', 'taken'),
    (r'\bdiya\b', 'given'),
    (r'\bkaam\b', 'work'),
    (r'\bsamajho\b', 'understand'),
    (r'\bsamajh\b', 'understanding'),
    (r'\baana\b', 'to come'),
    (r'\bjaana\b', 'to go'),
    (r'\bkar\b', 'do'),
    (r'\brakh\b', 'keep'),
    (r'\bnikal\b', 'extract'),
    (r'\bdal\b', 'put'),
    (r'\bdekh\b', 'see'),
    (r'\bnikla\b', 'result'),
    (r'\bnikalna\b', 'to extract'),
    (r'\bdaalna\b', 'to put'),
    (r'\brakhna\b', 'to keep'),
    (r'\bsikhna\b', 'to learn'),
    (r'\bsikhte\b', 'learn'),
    (r'\bsikha\b', 'teach'),
    (r'\bparho\b', 'read'),
    (r'\bparh\b', 'read'),
    (r'\bparha\b', 'read'),
    (r'\blikh\b', 'write'),
    (r'\blikha\b', 'written'),
    (r'\bbol\b', 'speak'),
    (r'\bbola\b', 'spoken'),
    (r'\bjaan\b', 'know'),
    (r'\bjaante\b', 'know'),
    (r'\bjaanta\b', 'knows'),
    (r'\bmil\b', 'get'),
    (r'\bmila\b', 'got'),
    (r'\bmilta\b', 'gets'),
    (r'\bdekhna\b', 'to see'),
    (r'\bdikhai\b', 'visible'),
    (r'\bdikha\b', 'show'),
    (r'\bnikal kar\b', 'after extracting'),
    (r'\bdaal kar\b', 'after putting'),
]


def apply_replacements(text):
    for pattern, replacement in MULTI_WORD:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def process_code_line(line):
    stripped = line.strip()
    # Apply replacements to all code cell text (comments AND string literals)
    # No Python keywords/identifiers use Urdu words, so this is safe
    if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
        return apply_replacements(line)
    # For lines with print(), etc - replace inside strings too
    return apply_replacements(line)


def process_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    changes = 0
    for cell in notebook['cells']:
        new_source = []
        if isinstance(cell['source'], list):
            for line in cell['source']:
                original = line
                if cell['cell_type'] == 'markdown':
                    new_line = apply_replacements(line)
                elif cell['cell_type'] == 'code':
                    new_line = process_code_line(line)
                else:
                    new_line = line
                if new_line != original:
                    changes += 1
                new_source.append(new_line)
        else:
            original = cell['source']
            if cell['cell_type'] == 'markdown':
                new_source = apply_replacements(original)
            elif cell['cell_type'] == 'code':
                new_source = process_code_line(original)
            else:
                new_source = original
            if new_source != original:
                changes += 1
        cell['source'] = new_source

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    return changes


files = [
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Basics\Pandas_Basics.ipynb',
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Intermediate\Pandas_Intermediate.ipynb',
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Advance\Pandas_Advance.ipynb',
    r'C:\Users\Quonain\MyFiles\Artificial-Intelligence\Pandas\Intermediate\01_Grouping_Aggregation_and_Pivot_Tables.ipynb',
]

total_changes = 0
for fpath in files:
    if os.path.exists(fpath):
        c = process_notebook(fpath)
        print(f'Processed: {os.path.basename(fpath)} - {c} changes')
        total_changes += c
    else:
        print(f'Not found: {fpath}')

print(f'\nTotal changes across all files: {total_changes}')
