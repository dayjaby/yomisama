from pattern.text.es import conjugate, singularize, pluralize, predicative, attributive, MALE, FEMALE, NEUTRAL, PLURAL


delimiters = [";",","," ","!","?","\"","'",".",":"]
conjugations = ["inf","1sg","2sg","3sg","1pl","2pl","3pl","part","2sg!","2pl!","1sg?","2sg?","3sg?","1pl?","2pl?","3pl?","1sgp","2sgp","3sgp","1ppl","2ppl","3ppl","ppart","1sgp+","2sgp+","3sgp+","1ppl+","2ppl+","3ppl+","1sgp?","2sgp?","3sgp?","1ppl?","2ppl?","3ppl?","1sgf","2sgf","3sgf","1plf","2plf","3plf","1sg->","2sg->","3sg->","1pl->","2pl->","3pl->"]

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
                if conjugate(infinitive,conjugation) == word:
                    if infinitive != word:
                        words.append(infinitive)
            # Nomen
            sg = singularize(word)
            pl = pluralize(word)
            if sg != word:
                words.append(sg)
                
            # Adjektive
            p = predicative(word)
            for gender in [MALE,FEMALE,NEUTRAL,MALE+PLURAL,FEMALE+PLURAL,NEUTRAL+PLURAL]:
                if attributive(p,gender=gender) == word:
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
