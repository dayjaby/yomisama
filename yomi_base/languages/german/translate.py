from pattern.text.de import conjugate, singularize, pluralize, predicative, attributive, MALE, FEMALE, NEUTRAL, SUBJECT, OBJECT, INDIRECT, PROPERTY


delimiters = [";",","," ","!","?","\"","'",".",":"]
conjugations = [
    ("inf","Infinitiv"),
    ("1sg","1. Person Singular"),
    ("2sg","2. Person Singular"),
    ("3sg","3. Person Singular"),
    ("1pl","1. Person Plural"),
    ("2pl","2. Person Plural"),
    ("3pl","3. Person Plural"),
    ("2sg!","Imperativ, Singular"),
    ("1pl!","Imperativ, 1. Person Plural"),
    ("2pl!","Imperativ, 2. Person Plural"),
    ("1sg?","Subjunktiv, 1. Person Singular"),
    ("2sg?","Subjunktiv, 2. Person Singular"),
    ("3sg?","Subjunktiv, 3. Person Singular"),
    ("1pl?","Subjunktiv, 1. Person Plural"),
    ("2pl?","Subjunktiv, 2. Person Plural"),
    ("3pl?","Subjunktiv, 3. Person Plural"),
    ("1sgp","Vergangenheit, 1. Person Singular"),
    ("2sgp","Vergangenheit, 2. Person Singular"),
    ("3sgp","Vergangenheit, 3. Person Singular"),
    ("1plp","Vergangenheit, 1. Person Plural"),
    ("2plp","Vergangenheit, 2. Person Plural"),
    ("3plp","Vergangenheit, 3. Person Plural"),
    ("ppart","Partizip"),
    ("1sgp?","Vergangenheit, Subjunktiv, 1. Person Singular"),
    ("2sgp?","Vergangenheit, Subjunktiv, 2. Person Singular"),
    ("3sgp?","Vergangenheit, Subjunktiv, 3. Person Singular"),
    ("1plp?","Vergangenheit, Subjunktiv, 1. Person Plural"),
    ("2plp?","Vergangenheit, Subjunktiv, 2. Person Plural"),
    ("3plp?","Vergangenheit, Subjunktiv, 3. Person Plural")]

class Translator:
    def __init__(self, deinflector, dictionary):
        self.deinflector = deinflector
        self.dictionary = dictionary

    def findTerm(self, text, wildcards=False):
        s = text['content']
        p = text['samplePosStart']
        p1 = max([s[:p].rfind(d) for d in delimiters]) + 1
        p2 = min([x for x in [s[p:].find(d) for d in delimiters] if x>=0]+[len(s)-1]) + p
        w = s[p1:p2]
        self.word = (text,w) # debug
        results = []
        length = None
        wordType = None
        minw = len(w)-2 if len(w)>2 else 0
        hashs = set()
        self.words = []
        genRanges = [0]
        def gen(w,arr):
            start = 0
            while len(arr)>0:
                start = arr.pop(0)
                for i in xrange(len(w), 0, -1):  # xrange(len(w), minw, -1):
                    yield (start, i, len(w)-start)
        entriesBefore = 0
        originalWord = w
        self.test = []

        for s,i,l in gen(w,genRanges):
            word = originalWord[s:i]
            self.test.append((word,originalWord,s,i))
            words = [word]
            
            # Verben
            infinitive = conjugate(word,"inf")
            for conjugation in conjugations:
                if conjugate(infinitive,conjugation[0]) == word:
                    if infinitive != word:
                        words.append(infinitive)
            # Nomen
            sg = singularize(word)
            pl = pluralize(word)
            if sg != word:
                words.append(sg)
                
            # Adjektive
            p = predicative(word)
            for gender in [MALE,FEMALE,NEUTRAL]:
                for role in [SUBJECT,OBJECT,INDIRECT,PROPERTY]:
                    if attributive(p,gender=gender,role=role) == word:
                        wordType = "Adjektiv"
                        if p!=word:
                            words.append(p)
            if word.lower()!=word:
                words.append(word.lower())
            self.words += words
            entriesBeforeAdd = len(results)
            for w in words:
                for entry in self.dictionary.findTerm(w, wildcards):
                    h = "??".join(entry.values()[:-1])
                    if h not in hashs:
                        hashs.add(h)
                        results.append({
                            "expression": entry['expression'],
                            "search": entry['search'],
                            "gender": entry['gender'],
                            "glossary": entry['glossary'],
                            "tags": entry['tags'],
                            "language": "German"
                        })
            self.test.append((word,len(results),entriesBeforeAdd,entriesBefore,l,i,s))
            if len(results)-entriesBeforeAdd > 0 and entriesBeforeAdd-entriesBefore == 0 and l>2:
                genRanges.append(i+s)
                entriesBefore = len(results)


        self.results = results
        results = sorted(results,
                         key=lambda d: (len(d['search']), d['search'],-len(d['expression']),d['expression']),reverse=True)
        return results, length


    def findCharacters(self, text):
        return []

                
    def validator(self, term):
        return True                
