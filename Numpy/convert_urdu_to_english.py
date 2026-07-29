import json
import os
import re

# Comprehensive Urdu/Hindi to English word mappings
REPLACEMENTS = [
    # Core verbs and common words (longer phrases first to avoid partial matches)
    ("kehte hain", "are called"),
    ("kehte hai", "is called"),
    ("bolte hain", "are called"),
    ("bolta hai", "is called"),
    ("samjhaya gaya", "explained"),
    ("samjhaya", "explained"),
    ("samjhao", "explain"),
    ("samjho", "understand"),
    ("samajhna", "understand"),
    ("samajh", "understand"),

    # hai -> is
    (r'\bhai\b', 'is'),

    # hain -> are
    (r'\bhain\b', 'are'),

    # karo/karein/karte/kiya - do/perform/done
    (r'\bkaro\b', 'do'),
    (r'\bkarein\b', 'do'),
    (r'\bkarte hain\b', 'do'),
    (r'\bkarte hai\b', 'does'),
    (r'\bkarte\b', 'do'),
    (r'\bkiya gaya\b', 'was done'),
    (r'\bkiya\b', 'done'),
    (r'\bkar sakte hain\b', 'can do'),
    (r'\bkar sakta hai\b', 'can do'),
    (r'\bkar\b', 'do'),

    # aur -> and
    (r'\baur\b', 'and'),

    # mein/andar -> in/inside
    (r'\bmein\b', 'in'),
    (r'\bme\b', 'in'),
    (r'\bandar\b', 'inside'),

    # ke/ki/ka -> of/for
    (r'\bke liye\b', 'for'),
    (r'\bke saath\b', 'with'),
    (r'\bke baare mein\b', 'about'),
    (r'\bke baare me\b', 'about'),
    (r'\bke hisaab se\b', 'by'),
    (r'\bke tor par\b', 'as'),
    (r'\bke taur par\b', 'as'),
    (r'\bke through\b', 'through'),
    (r'\bke andar\b', 'inside'),
    (r'\bke beech\b', 'between'),
    (r'\bke ilawa\b', 'besides'),
    (r'\bke\b', 'of'),
    (r'\bki taraf\b', 'toward'),
    (r'\bki\b', 'of'),
    (r'\bka\b', 'of'),

    # liye -> for
    (r'\bliye\b', 'for'),

    # se -> from/by/with
    (r'\bse bhi\b', 'also'),
    (r'\bse le kar\b', 'from'),
    (r'\bse\b', 'with'),

    # ko -> to
    (r'\bko\b', 'to'),

    # tarika/tareeqa -> method/way
    (r'\btarika\b', 'method'),
    (r'\btareeqa\b', 'method'),
    (r'\btariqe\b', 'methods'),

    # banao/banayein -> create/make
    (r'\bbanao\b', 'create'),
    (r'\bbanayein\b', 'create'),
    (r'\bbana\b', 'make'),
    (r'\bbanaya\b', 'created'),
    (r'\bbanate hain\b', 'create'),
    (r'\bbanta hai\b', 'is made'),

    # kya -> what
    (r'\bkya\b', 'what'),
    (r'\bkya hai\b', 'what is'),
    (r'\bkya hota hai\b', 'what is'),
    (r'\bkya hain\b', 'what are'),

    # ye/yeh/yah -> this/it
    (r'\byeh\b', 'this'),
    (r'\bye\b', 'this'),
    (r'\byah\b', 'this'),

    # usay/ise -> it
    (r'\busay\b', 'it'),
    (r'\bise\b', 'it'),
    (r'\binhe\b', 'them'),
    (r'\bunhe\b', 'them'),

    # hota/hoti/hote -> is/are
    (r'\bhota hai\b', 'is'),
    (r'\bhota\b', 'is'),
    (r'\bhoti hai\b', 'is'),
    (r'\bhoti\b', 'is'),
    (r'\bhote hain\b', 'are'),
    (r'\bhote\b', 'are'),

    # sakta/sakti/sakte -> can
    (r'\bsakta hai\b', 'can'),
    (r'\bsakti hai\b', 'can'),
    (r'\bsakte hain\b', 'can'),
    (r'\bsakta\b', 'can'),
    (r'\bsakti\b', 'can'),
    (r'\bsakte\b', 'can'),
    (r'\bskta\b', 'can'),
    (r'\bskte\b', 'can'),

    # rakhta/rakhti -> holds/has
    (r'\brakhta hai\b', 'has'),
    (r'\brakhti hai\b', 'has'),
    (r'\brakhta\b', 'has'),
    (r'\brakhti\b', 'has'),
    (r'\brakhte hain\b', 'have'),
    (r'\brakhna\b', 'keep'),

    # dena/deta -> give
    (r'\bdena\b', 'give'),
    (r'\bdeta hai\b', 'gives'),
    (r'\bdeta\b', 'gives'),
    (r'\bdega\b', 'will give'),

    # lena/leta -> take
    (r'\blena\b', 'take'),
    (r'\bleta hai\b', 'takes'),
    (r'\bleta\b', 'takes'),

    # wala/wali/wale -> which/that
    (r'\bwala\b', 'that'),
    (r'\bwali\b', 'that'),
    (r'\bwale\b', 'that'),

    # aasan/asaan -> easy
    (r'\baasan\b', 'easy'),
    (r'\basaan\b', 'easy'),

    # chahiye -> needed/should
    (r'\bchahiye\b', 'needed'),

    # bahut/bohat -> very
    (r'\bbahut\b', 'very'),
    (r'\bbohat\b', 'very'),

    # jese/jaise/jaisa -> like/such as
    (r'\bjese\b', 'like'),
    (r'\bjaise\b', 'like'),
    (r'\bjaisa\b', 'like'),
    (r'\bjaisi\b', 'like'),
    (r'\bjaisay\b', 'like'),

    # Common additional words
    (r'\bbuniyad\b', 'foundation'),
    (r'\bbuniyadi\b', 'fundamental'),
    (r'\btajurba\b', 'experience'),
    (r'\bwajah\b', 'reason'),
    (r'\bjagah\b', 'place'),
    (r'\btez\b', 'fast'),
    (r'\bkam\b', 'less'),
    (r'\bzyada\b', 'more'),
    (r'\bziyada\b', 'more'),
    (r'\bchhota\b', 'small'),
    (r'\bchhoti\b', 'small'),
    (r'\bbara\b', 'large'),
    (r'\bbari\b', 'large'),
    (r'\bbare\b', 'large'),
    (r'\bsaath\b', 'with'),
    (r'\bbaad\b', 'after'),
    (r'\bpehle\b', 'first'),
    (r'\bpehla\b', 'first'),
    (r'\bbaqi\b', 'remaining'),
    (r'\bsirf\b', 'only'),
    (r'\byahan\b', 'here'),
    (r'\bwahan\b', 'there'),
    (r'\bkahan\b', 'where'),
    (r'\btab\b', 'then'),
    (r'\bjab\b', 'when'),
    (r'\bab\b', 'now'),
    (r'\bphir\b', 'then'),
    (r'\bdono\b', 'both'),
    (r'\bagar\b', 'if'),
    (r'\bwarna\b', 'otherwise'),
    (r'\bmagar\b', 'but'),
    (r'\blekin\b', 'but'),
    (r'\bkyun\b', 'why'),
    (r'\bkyu\b', 'why'),
    (r'\bkyunke\b', 'because'),
    (r'\bkyunki\b', 'because'),
    (r'\bisliye\b', 'therefore'),
    (r'\bnikalna\b', 'extract'),
    (r'\bnikaal\b', 'extract'),
    (r'\bnikaalte hain\b', 'extract'),
    (r'\bnikalo\b', 'extract'),
    (r'\bbatao\b', 'tell'),
    (r'\bbatana\b', 'explain'),
    (r'\bbataye\b', 'tell'),
    (r'\bbata\b', 'tell'),
    (r'\bdekh\b', 'see'),
    (r'\bdekho\b', 'see'),
    (r'\bdekhte hain\b', 'see'),
    (r'\bdekhna\b', 'see'),
    (r'\bho\b', 'is'),
    (r'\bhoga\b', 'will be'),
    (r'\bhoge\b', 'will be'),
    (r'\btha\b', 'was'),
    (r'\bthe\b', 'were'),
    (r'\bthi\b', 'was'),
    (r'\bnahi\b', 'not'),
    (r'\bna\b', 'not'),
    (r'\bapna\b', 'own'),
    (r'\bapne\b', 'own'),
    (r'\bapni\b', 'own'),
    (r'\bbaat\b', 'thing'),
    (r'\bmatlab\b', 'meaning'),
    (r'\bmisal\b', 'example'),
    (r'\bmisaal\b', 'example'),
    (r'\bmumkin\b', 'possible'),
    (r'\bzaroori\b', 'necessary'),
    (r'\blazmi\b', 'mandatory'),
    (r'\bahem\b', 'important'),
    (r'\basli\b', 'real'),
    (r'\bsab\b', 'all'),
    (r'\bsaare\b', 'all'),
    (r'\bhar\b', 'each'),
    (r'\bkoi\b', 'any'),
    (r'\bkuch\b', 'some'),
    (r'\bthora\b', 'a little'),
    (r'\bthori\b', 'a little'),
    (r'\bkaam\b', 'work'),
    (r'\balag\b', 'different'),
    (r'\baalag\b', 'separate'),
    (r'\bpoora\b', 'whole'),
    (r'\bpoori\b', 'complete'),
    (r'\bpooray\b', 'complete'),
    (r'\bnaya\b', 'new'),
    (r'\bnaye\b', 'new'),
    (r'\bnayi\b', 'new'),
    (r'\bpurana\b', 'old'),
    (r'\bpuranay\b', 'old'),
    (r'\baakhri\b', 'last'),
    (r'\bagla\b', 'next'),
    (r'\bagli\b', 'next'),
    (r'\bpichla\b', 'previous'),
    (r'\bacha\b', 'good'),
    (r'\bupar\b', 'above'),
    (r'\bneeche\b', 'below'),
    (r'\baage\b', 'forward'),
    (r'\bpeeche\b', 'backward'),
    (r'\bpaas\b', 'near'),
    (r'\bbeech\b', 'middle'),
    (r'\bshuru\b', 'start'),
    (r'\bstart\b', 'start'),
    (r'\bkhatam\b', 'end'),
    (r'\bchalo\b', 'go'),
    (r'\bdikhana\b', 'show'),
    (r'\bdikhao\b', 'show'),
    (r'\bdikhte hain\b', 'appear'),
    (r'\bdikhta hai\b', 'appears'),

    # More nuanced phrases
    (r'\bjaan\b', 'go'),
    (r'\bjao\b', 'go'),
    (r'\bjata hai\b', 'goes'),
    (r'\bjata\b', 'goes'),
    (r'\bdaal\b', 'put'),
    (r'\bdaalo\b', 'put'),
    (r'\brakh\b', 'keep'),
    (r'\brakho\b', 'keep'),
    (r'\brakhte\b', 'keep'),
    (r'\bdo\b', 'two'),
    (r'\bteen\b', 'three'),
    (r'\bcheez\b', 'thing'),
    (r'\bcheezein\b', 'things'),
    (r'\bfarq\b', 'difference'),
    (r'\bfark\b', 'difference'),
    (r'\bnatija\b', 'result'),
    (r'\bjawab\b', 'answer'),
    (r'\bsawaal\b', 'question'),
    (r'\bsawal\b', 'question'),
    (r'\bmasla\b', 'problem'),
    (r'\bmasle\b', 'problems'),
    (r'\bhal\b', 'solution'),
    (r'\bkhel\b', 'game'),
    (r'\bimtihan\b', 'test'),
    (r'\bproof\b', 'proof'),
    (r'\bsaabit\b', 'prove'),
    (r'\bsoch\b', 'thinking'),
    (r'\bzehen\b', 'mind'),
    (r'\bhisaab\b', 'calculation'),
    (r'\bginti\b', 'count'),
    (r'\bjama\b', 'sum'),
    (r'\bzarb\b', 'product'),
    (r'\btaqseem\b', 'division'),
    (r'\bfaida\b', 'benefit'),
    (r'\bfayda\b', 'benefit'),
    (r'\bbachat\b', 'savings'),
    (r'\bkharab\b', 'bad'),
    (r'\btheek\b', 'correct'),
    (r'\bgalat\b', 'wrong'),
    (r'\bsahi\b', 'correct'),
    (r'\bgalti\b', 'mistake'),
    (r'\bbug\b', 'bug'),
    (r'\bbarqarar\b', 'preserved'),
    (r'\bmaujood\b', 'present'),
    (r'\bmilta hai\b', 'is available'),
    (r'\bmilti hai\b', 'is available'),
    (r'\bchahiye\b', 'needed'),
    (r'\blagana\b', 'apply'),
    (r'\blagao\b', 'apply'),
    (r'\blagaye\b', 'apply'),
    (r'\bmilao\b', 'combine'),
    (r'\bjorna\b', 'join'),
    (r'\bjorr\b', 'join'),
    (r'\bjodo\b', 'join'),
    (r'\btodna\b', 'break'),
    (r'\btodo\b', 'break'),
    (r'\bdhoondo\b', 'find'),
    (r'\bdhoondhna\b', 'find'),
    (r'\bpaida\b', 'produced'),
    (r'\bbanate hain\b', 'create'),
    (r'\buthao\b', 'pick'),
    (r'\buthana\b', 'pick'),
    (r'\bjaan boojh kar\b', 'intentionally'),
    (r'\bjaan boojh\b', 'intentional'),
    (r'\bbilkul\b', 'exactly'),
    (r'\bwaise\b', 'like that'),
    (r'\baisa\b', 'like this'),
    (r'\byani\b', 'meaning'),
    (r'\byaani\b', 'meaning'),
    (r'\baby\b', 'now'),
    (r'\bchaliye\b', 'let us'),
    (r'\bchaliye shuru karte hain\b', 'let us begin'),
    (r'\bkarte hain\b', 'let us'),
    (r'\bpadho\b', 'read'),
    (r'\bpata\b', 'know'),
    (r'\bpata hai\b', 'know'),
    (r'\bmaloom\b', 'known'),
    (r'\bbaad me\b', 'later'),
    (r'\bagar\b', 'if'),
    (r'\byakeen\b', 'sure'),
    (r'\bqareeb\b', 'close'),
    (r'\bhamesha\b', 'always'),
    (r'\bkabhi kabhi\b', 'sometimes'),
    (r'\bkabhi\b', 'ever'),
    (r'\baksar\b', 'often'),
    (r'\bphir bhi\b', 'still'),
    (r'\bchahe\b', 'whether'),
    (r'\bchahiye\b', 'needed'),
    (r'\bzaroorat\b', 'need'),
    (r'\btaake\b', 'so that'),
    (r'\btaake\b', 'so that'),
    (r'\bjaise\b', 'like'),
    (r'\bwaghera\b', 'etc.'),
    (r'\bwagerah\b', 'etc.'),
    (r'\bay\b', 'oh'),
    (r'\barrey\b', 'hey'),
    (r'\baray\b', 'hey'),

    # Urdu script phrases (from the first file)
    (r'NumPy کی بنیادی باتیں', 'NumPy Fundamentals'),
    (r'ایک طاقتور لائبریری ہے جو Python میں numerical computing کو ممکن بناتی ہے۔', 'is a powerful library that enables numerical computing in Python.'),
    (r'یہ multidimensional arrays اور matrices کے ساتھ کام کرنے کے لیے بہترین ہے۔', 'It is excellent for working with multidimensional arrays and matrices.'),
    (r'Python lists کے مقابلے میں NumPy کے فوائد:', 'Advantages of NumPy over Python lists:'),
    (r'NumPy arrays C language میں implement ہوتے ہیں', 'NumPy arrays are implemented in C language'),
    (r'کم memory استعمال کرتے ہیں', 'use less memory'),
    (r'Mathematical operations directly arrays پر', 'Mathematical operations directly on arrays'),
    (r'Different shapes کے arrays پر operations', 'Operations on arrays of different shapes'),
    (r'Almost all data science libraries NumPy پر depend کرتی ہیں', 'Almost all data science libraries depend on NumPy'),
    (r'ndarray = N-dimensional array → NumPy کا core object', 'ndarray = N-dimensional array → NumPy core object'),
    (r'Sab zero ka array', 'All zeros array'),
    (r'Sab one ka array', 'All ones array'),
    (r'Sab specified value se fill karna', 'Fill with specified value'),
    (r'Array ke baare mein jaankari dene wale attributes', 'Attributes that provide information about the array'),
    (r'NumPy mein alag-alag data types hote hain:', 'NumPy has various data types:'),
    (r'Different dtypes ke saath arrays', 'Arrays with different dtypes'),
    (r'dtype change karna', 'changing dtype'),
    (r'Arrays se elements access karne ke different tarike', 'Different ways to access array elements'),
    (r'end se count karna', 'counting from the end'),
    (r'condition ke basis pe select karna', 'selecting based on condition'),
    (r'Array ki shape badalna', 'Changing array shape'),
    (r'In-place reshaping', 'In-place reshaping'),
    (r'1D view banana', 'Creating 1D view'),
    (r'Do ya zyada arrays ko jorna', 'Joining two or more arrays'),
    (r'Arrays ko tukdon mein taqseem karna', 'Splitting arrays into parts'),
    (r'Axis ka mental model', 'Axis mental model'),
    (r'Array ko parts mein divide karna', 'Divide array into parts'),
    (r'Arithmetic, comparison, aur universal functions', 'Arithmetic, comparison, and universal functions'),
    (r'کی بنیادی باتیں', 'Basics'),
    (r'مشقی سوالات', 'Practice Problems'),
    (r'Ek 5x5 array banayein jisme: border elements 1 hon, center 3x3 elements 0 hon', 'Create a 5x5 array where: border elements are 1, center 3x3 elements are 0'),
    (r'Ek 4x4 array diya gaya hai. Uske corners \(4 corners\) ke elements nikaal kar ek 2x2 array banayein.', 'Given a 4x4 array. Extract the 4 corner elements and create a 2x2 array.'),
    (r'1000 students ke marks \(0-100\) randomly generate karein. Average, median, highest, lowest, aur passing percentage \(>=40\) calculate karein.', 'Randomly generate marks (0-100) for 1000 students. Calculate average, median, highest, lowest, and passing percentage (>=40).'),
    (r'Do 3x3 matrices A aur B banayein. A\*B \(element-wise\), A@B \(matrix multiplication\), A transpose, determinant nikaalein.', 'Create two 3x3 matrices A and B. Compute A*B (element-wise), A@B (matrix multiplication), A transpose, and determinant.'),
    (r'Ek array mein se saare even numbers ko 0 se replace karein aur odd numbers ko 1 se.', 'Replace all even numbers with 0 and odd numbers with 1 in an array.'),

    # Intermediate notebook translations
    (r'NumPy Intermediate Level', 'NumPy Intermediate Level'),
    (r'Is notebook mein hum NumPy ke intermediate topics cover karenge: advanced array manipulation, linear algebra, random module, statistics, set operations, structured arrays, masked arrays, polynomials, aur file I/O.', 'In this notebook we will cover intermediate NumPy topics: advanced array manipulation, linear algebra, random module, statistics, set operations, structured arrays, masked arrays, polynomials, and file I/O.'),
    (r'NumPy arrays ke saath advanced operations', 'Advanced operations with NumPy arrays'),
    (r'Array ka dimension badhana', 'Adding array dimensions'),
    (r'Row vector ko column mein convert karna', 'Converting row vector to column'),
    (r'Size 1 wale dimensions hata dena', 'Removing size-1 dimensions'),
    (r'Elements ko repeat karna', 'Repeating elements'),
    (r'Pura array repeat karna', 'Repeating entire array'),
    (r'Unique elements nikaalna', 'Extracting unique elements'),
    (r'Conditional indexing', 'Conditional indexing'),
    (r'Simple usage: indices return karna jahan condition True hai', 'Simple usage: return indices where condition is True'),
    (r'np.where with x and y \(ternary operator jaisa\)', 'np.where with x and y (like ternary operator)'),
    (r'Non-zero elements ke indices', 'Indices of non-zero elements'),
    (r'Multiple keys ke according sort', 'Sorting by multiple keys'),
    (r'NumPy linear algebra operations ke liye np.linalg module provide karta hai', 'NumPy provides the np.linalg module for linear algebra operations'),
    (r'NumPy random module se different probability distributions se samples generate karna', 'Generating samples from different probability distributions using NumPy random module'),
    (r'Reproducibility ke liye', 'For reproducibility'),
    (r'Kisi array se random select karna', 'Randomly selecting from an array'),
    (r'numPy random module se different probability distributions se samples generate karna', 'Generating samples from different probability distributions using NumPy random module'),
    (r'Advanced statistical functions', 'Advanced statistical functions'),
    (r'Do variables ke beech correlation nikaalna', 'Find correlation between two variables'),
    (r'Set theory operations on 1D arrays', 'Set theory operations on 1D arrays'),
    (r'Structured arrays multiple data types ko ek array mein combine karne dete hain \(table jaisa\)', 'Structured arrays allow combining multiple data types in one array (like a table)'),
    (r'Masked arrays missing ya invalid data handle karne ke liye', 'Masked arrays for handling missing or invalid data'),
    (r'Missing data ke saath kaam karna', 'Working with missing data'),
    (r'Nan-safe functions jo NaN values ko ignore karte hain', 'NaN-safe functions that ignore NaN values'),
    (r'Polynomial fitting and evaluation', 'Polynomial fitting and evaluation'),
    (r'Data points ke through curve fit karna', 'Curve fitting through data points'),
    (r'NumPy arrays ko file mein save aur load karna', 'Saving and loading NumPy arrays to/from file'),
    (r'Multiple arrays save karna', 'Saving multiple arrays'),
    (r'Do 3x3 matrices A aur B diye gaye hain. A*B, A@B, A inverse, determinant, eigenvalues, aur solve\(Ax=b\) calculate karein.', 'Given two 3x3 matrices A and B. Calculate A*B, A@B, A inverse, determinant, eigenvalues, and solve(Ax=b).'),
    (r'10000 trials mein do dice roll ka sum 7 aane ki probability estimate karein.', 'Estimate the probability of getting sum 7 from two dice rolls in 10000 trials.'),
    (r'Students ke marks ka data diya gaya hai. Percentiles, histogram, correlation with study hours nikaalein.', 'Student marks data is given. Calculate percentiles, histogram, and correlation with study hours.'),
    (r'Employees ka structured array banayein aur filtering karein.', 'Create a structured array of employees and perform filtering.'),
    (r'Marks ke aadhar par grade dena', 'Assign grades based on marks'),

    # Advance notebook
    (r'NumPy Advanced Concepts', 'NumPy Advanced Concepts'),
    (r'Advanced broadcasting, einstein summation, stride tricks, vectorization, memory layout, performance optimization, interoperability, advanced linear algebra, Fourier transforms, aur NumPy C API.', 'Advanced broadcasting, einstein summation, stride tricks, vectorization, memory layout, performance optimization, interoperability, advanced linear algebra, Fourier transforms, and NumPy C API.'),
    (r'Broadcasting NumPy ka sab se powerful feature hai. Iske rules ko deeply samajhna zaroori hai.', 'Broadcasting is NumPy\'s most powerful feature. It is important to understand its rules deeply.'),
    (r'Dimensions right-aligned hote hain', 'Dimensions are right-aligned'),
    (r'Agar dimension size 1 hai to broadcast ho sakta hai', 'If dimension size is 1, it can be broadcast'),

    # Common phrases across files
    (r'Kya hai', 'What is'),
    (r'Kya hai:', 'What is:'),
    (r'Kyun', 'Why'),
    (r'Kyun:', 'Why:'),
    (r'Kyun / kahan', 'Why / where'),
    (r'Kab', 'When'),
    (r'Kahan', 'Where'),
    (r'Kaise', 'How'),
    (r'Jahan', 'Where'),
    (r'Tareeqa', 'Method'),
    (r'Tarika', 'Method'),

    # Cleanup remnants
    (r'  ', ' '),
    (r' .', '.'),
    (r' ,', ','),
    (r'  \.', '.'),
    (r'\s+\.', '.'),
]

def translate_text(text):
    """Apply all Urdu/Hindi to English replacements to text."""
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def process_cell(cell):
    """Process a notebook cell's source content."""
    source = cell.get('source', '')
    if isinstance(source, list):
        new_source = []
        for line in source:
            new_source.append(translate_text(line))
        cell['source'] = new_source
    elif isinstance(source, str):
        cell['source'] = translate_text(source)
    return cell

def process_notebook(filepath):
    """Read, process, and write a notebook file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for cell in data['cells']:
        process_cell(cell)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)

    print(f"  OK Processed: {filepath}")

# List of files to process (in order)
files = [
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Basics\NumPy_Basics.ipynb",
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Basics\01_Numpy_Introduction_Arrays_aur_Creation.ipynb",
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Basics\02_Indexing_Slicing_Reshaping_aur_Joining.ipynb",
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Basics\03_Operations_Broadcasting_aur_Aggregations.ipynb",
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Intermediate\NumPy_Intermediate.ipynb",
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Intermediate\01_Axis_Mastery_Aggregations_aur_Advanced_Indexing.ipynb",
    r"C:\Users\Quonain\MyFiles\Artificial-Intelligence\Numpy\Advance\NumPy_Advance.ipynb",
]

print("Starting Urdu/Hindi to English conversion...")
print("=" * 60)

for fp in files:
    if os.path.exists(fp):
        process_notebook(fp)
    else:
        print(f"  X File not found: {fp}")

print("=" * 60)
print("Conversion complete!")
