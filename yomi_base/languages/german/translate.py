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
        s = text.content
        p = text.samplePosStart
        p1 = max([s[:p].rfind(d) for d in delimiters]) + 1
        p2 = min([x for x in [s[p:].find(d) for d in delimiters] if x>=0]+[len(s)-1]) + p
        w = s[p1:p2]
        self.word = (text,w) # debug
        results = []
        length = None
        wordType = None
        minw = len(w)-2 if len(w)>2 else 0
        hashs = dict()
        self.words = []
        for i in xrange(len(w), minw, -1):
            word = w[:i]
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
            for w in words:
                for entry in self.dictionary.findTerm(w, wildcards):
                    h = hash(frozenset(entry.items()))
                    if h not in hashs:
                        hashs[h] = entry
                        results.append(entry)
            

        return results, length


    def findCharacters(self, text):
        return []

                
    def validator(self, term):
        return True                
