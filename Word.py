from notation import accented, vowels, consonants, semivowels
def WHICH(switch, ARGS): #TODO: Think about useful version with functions
    try:
        for case, result in ARGS:
            if(switch == case):
                return result
    except:
        if(type(ARGS[-1]) != type((1, 1))):
            return ARGS[-1]
def index_syllable(string, syl_index):
    b = 0 #beginning of the syllable
    v = 0 #vowel of the syllable
    e = 0 #end of the syllable
    vowel_indices = []
    for c in range(len(string)):
        if(string[c] in vowels):
            vowel_indices += [c]
    if(syl_index < 0):
        syl_index = len(vowel_indices)+syl_index
    v = vowel_indices[syl_index]
    if(syl_index-1 >= 0):
        p = vowel_indices[syl_index-1] #previous vowel index
        while(p+1 < len(string) and string[p+1] in semivowels):    p += 1
        b = v
        while(b > 0 and string[b-1] in semivowels):    b -= 1
        b = int((p + b + 1)/2)
    else:
        b = 0
    if(syl_index+1 < len(vowel_indices)):
        n = vowel_indices[syl_index+1] #next vowel index
        while(n > 0 and string[n-1] in semivowels):    n -= 1
        e = v
        while(e+1 < len(string) and string[e+1] in semivowels):    e += 1
        e = int((n + e)/2)
    else:
        e = len(string)
    return (b, v, e)
def accent_syllable(self, string, syllable_no_accent_threshhold=2, syllable_index=-2):
    if(self.syllable_no_accent_count >= syllable_no_accent_threshhold):
        index = index_syllable(string, syllable_index) #(beginning, vowel, end)
        i = index[1]
        string = string[:i] + accented[string[i]] + string[i+1:]
        self.syllable_no_accent_count = -syllable_index - 1
    return string
def count_syllables(string):
    result = 0
    for c in string:
        if c in vowels:
            result += 1
    return result

PLACE = {
    "subject":      ["ta", "vo", "ko"],
    "object":       ["le", "so", "ne"],
    "attribute":    ["ri", "Ju", "wa", "Je", "Li"],
    "clause":       ["xs", "Xl", "Qr", "DJ", "wj", "CL", "ps", "df"],
}
USED = {
    "subject":  0,
    "object":   0,
    "attribute":0,
    "clause":   0,
}

from copy import deepcopy
from hist import hist
from wtype import standards_word, standards_verb, standards_noun, standards_attribute
class Word(object):
    def __init__(self, root, wtype, parents=[], children=[], hist=hist):
        super(Word, self).__init__()
        if(root != None):
            self.root = root
        else:
            self.root = wtype["root"]
        for i in range(3-len(self.root)):
            self.root += "k" #gr -> grk
        self.wtype = wtype
        self.wtype["root"] = self.root
        self.parents = deepcopy(parents)
        self.children = deepcopy(children)
        # self.subject = None
        try:
            self.marker = self.wtype["marker"]
        except:
            pass
        self.hist = hist
        self.syllable_no_accent_count = 0
        self.result = ""
        try:            self.wtype["parent_place"]
        except KeyError:self.wtype["parent_place"] = []
        try:            self.wtype["parent_place_string"]
        except KeyError:self.wtype["parent_place_string"] = []
        try:            self.wtype["child_place"]
        except KeyError:self.wtype["child_place"] = []
        try:            self.wtype["child_place_string"]
        except KeyError:self.wtype["child_place_string"] = []
        for k in self.wtype.keys():
            if(type(self.wtype[k]) == type(" ") and self.wtype[k].lower() == "false"):  self.wtype[k] = False
            elif(type(self.wtype[k]) == type(" ") and self.wtype[k].lower() == "true"): self.wtype[k] = True
            elif(type(self.wtype[k]) == type(" ") and self.wtype[k].lower() == "none"): self.wtype[k] = None
    def add_child(self, child, place="attribute"):
        global USED
        child.parents += [self]
        self.children += [child]
        if(place in PLACE.keys()):
            try:
                index = self.wtype["child_place"].index(place)
                child.add_place(place, self.wtype["child_place_string"][index])
            except ValueError:
                #getting the one that wasn't last used by any other word that wanted to add a place of this type to itself
                string = PLACE[place][USED[place] % len(PLACE[place])]
                USED[place] += 1
                child.add_place(place, string)
                self.wtype["child_place"] += [place]
                self.wtype["child_place_string"] += [string]
    def add_place(self, place, string):
        self.wtype["parent_place"] += [place]
        self.wtype["parent_place_string"] += [string]
    def spell(self): #looks at "class"
        for key in standards_word.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_word[key]
        self.result = ""
        self.result += ''.join(self.wtype["parent_place_string"])
        if(self.wtype["metaphore"]):
            self.spell_metaphore()
            self.syllable_no_accent_count += 1 #metaphore
        else:
            self.result += self.root[0]
        self.syllable_no_accent_count = 0 #root0 vowel always accented
        switch = self.wtype["class"]
        if(switch == "verb"):
            self.result += "á"
            self.spell_verb(1) #Jlt -> Ja
        elif(switch == "noun"):
            self.result += "ó"
            self.spell_noun(1) #Jlt -> Jo
        elif(switch == "attribute"):
            self.result += "é"
            self.spell_attribute(1) #Jlt -> Je
        elif(switch == "other"): #TODO
            self.result += "ú" #Jlt -> Ju
        if(len(self.children) != 0 and len(self.parents) != 0):
            self.result += ''.join(self.wtype["child_place_string"])
            self.syllable_no_accent_count += len(self.children)
        return self.result
        # It is questionable in my eyes to accent parent-syllables in words as a consequence of their parents' other child-syllables, if they cause accent clusters in the child while their parent may not even pronounce the accented child-syllable or any other. This might however be a complicated result of the history of the language and is not complete horse-shit.
        if(self.syllable_no_accent_count > 2):
            index = index_syllable(self.result, -2) #(beginning, vowel, end)
            i = index[1]
            syllable_original = self.result[index[0]:index[2]]
            self.result = self.result[:i] + accented[self.result[i]] + self.result[i+1:]
            syllable_accented = self.result[index[0]:index[2]]
            if(syllable_original in self.wtype["child_place_string"]):
                c_place_str = self.wtype["child_place_string"]
                i = c_place_str.index(syllable_original)
                self.wtype["child_place_string"] = c_place_str[:i+1] + accented[c_place_str[i+1]] + c_place_str[i+2:]
                p_place_str = self.children[i//2].wtype["parent_place_string"]
                j = p_place_str.index(syllable_original)
                self.children[i//2].wtype["parent_place_string"] = p_place_str[:j+1] + accented[p_place_str[j+1]] + p_place_str[j+2:]
        return self.result
    def spell_metaphore(self):
        # self.result = ""
        if(not hist["metaphor-merge"]):
            self.result += "gy" + self.root[0] #Jlt -> J
        else:
            self.result += "'y"
            try:
                self.result += g_merge[self.root[0]]
            except:
                self.result += g_merge[""] + self.root[0]
        # return result
    def spell_verb(self, root_level=1): #looks at "verb_class"
        for key in standards_verb.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_verb[key]
        if(root_level != None):
            if(root_level == 1):
                self.spell_perceived(root_level) #Jlt -> Ja(Le)l
            else:
                self.result += self.root[root_level] #Jlt -> Jal
        switch = self.wtype["verb_class"]
        if(switch == "infinitive"):
            self.syllable_no_accent_count += 1
            self.result += "ju" #Jlt -> Jalju
            self.spell_tense(2)
        elif(switch == "imperative"):
            self.result = self.result[:-1]
            self.spell_tense(1)
            self.result += "'o"
            self.syllable_no_accent_count += 1
            self.spell_person(2)
        elif(switch == "indicative"):
            # resetting and not using a character from self.root yet (leaving that to the subroutines)
            self.result = self.result[:-1]
            self.spell_tense(1)
            self.spell_person(2)
        elif(switch == "other"): # TODO: other verb classes?
            self.result += "u" #Jlt -> Jalu
        # return result
    def spell_tense(self, root_level=1): #looks at "tense"
        # result = ""
        if(root_level != None):
            if(root_level == 2):
                self.spell_passive(root_level) #Jlt -> Jale(xe)t
                self.spell_professional(flipped=True) #Jlt -> Jale(xe)t[[it][of]]
                self.result = accent_syllable(self, self.result, 2, -2)
            else:
                self.result += self.root[root_level]
                self.result = accent_syllable(self, self.result, 3, -2)
        switch = self.wtype["tense"]
        if(switch == "present"):
            if(self.result[-1] == "k"):
                self.result = self.result[:-1] #Jl -> Jal
            elif(not self.hist["present"]):
                self.result += "e" #Jlt -> Jale
        elif(switch == "past"):
            self.result += "o" #Jlt -> Jalo
        elif(switch == "future"):
            self.result += "u" #Jlt -> Jalu
        else:
            self.result += "i" #Jlt -> Jali
        if(not self.hist["present"] or switch in ["past", "future"]):
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1 and True): #TODO: replace True with somthing about root2 being far enough away)
                self.result = self.result[:-1]+accented[self.result[-1]] #make the last character in the result accented
                self.syllable_no_accent_count = 0
        # return result
    def spell_person(self, root_level=1): #looks at "person"
        result = []
        switch = self.wtype["person"]
        person_ending = {
            "they":"e", #Jlt -> Jalote
            "you":"u", #Jlt -> Jalosetu
            "me":"aj", #Jlt -> Jalosesutaj
            "undef":"i", #Jlt -> Jaloti
        }
        persons = ["me", "you", "they", "undef"]
        if(switch == []):
            switch = ["undef"]
        else:
            if("undef" in switch and len(switch) != 1):
                switch.pop(switch.index("undef"))
            if("plural-undef" in switch and len(switch) != 1):
                switch.pop(switch.index("plural-undef"))
            if("undef" in switch and "plural-undef" in switch and len(switch) != 2):
                switch.pop(switch.index("undef"))
                switch.pop(switch.index("plural-undef"))
        if(["me", "you", "they"] == switch):
            result = ["o"] #Jlt -> Jaloto
        elif(["plural-me", "plural-you", "plural-they"] == switch):
            result = ["on"] #Jlt -> Jaloton
        else:
            for person in persons:
                if("plural-"+person in switch): #checking for "plural-you" in wtype["person"]
                    result += [person_ending[person]+"ne"] #Jlt -> Jalotene
                elif(person in switch): #checking for "you" in wtype["person"]
                    result += [person_ending[person]] #Jlt -> Jalote
        #adding all the person-forms with s as filler-consonants
        while(len(result) > 1):
            self.result += "s" + result[-1]
            self.syllable_no_accent_count += count_syllables(result[-1])
            result.pop(-1)
            if(self.result.endswith("ne")):
                self.result = accent_syllable(self, self.result, 3, -2)
            elif(len(result) > 1):
                self.result = accent_syllable(self, self.result, 2, -1)
        if(root_level == 2):
            self.spell_passive()
        self.result += self.root[root_level] #Jlt -> Jale(xe)t
        if(self.hist["passive"] and self.wtype["passive"] and "xek" in self.result):
            i = self.result.index("xek")
            self.result = self.result[:i]+"x"+self.result[i+2]
            self.syllable_no_accent_count -= 1
        self.spell_professional( #Jlt -> Jalse(xe)t[[it][of]][aj|u|e|i|o][ne]
            flipped=True,
            accentable=(self.syllable_no_accent_count > 0)
        )
        self.result += result[0]
        self.syllable_no_accent_count += count_syllables(result[0])
        if(self.result.endswith("ne")):
            self.result = accent_syllable(self, self.result, 3, -2)
        else:
            self.result = accent_syllable(self, self.result, 1, -1)
        if("plural" in switch and result == ["i"]):
            self.result += "ne"
            self.syllable_no_accent_count += 1
    def spell_noun(self, root_level=1): #looks at "noun_class"
        for key in standards_noun.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_noun[key]
        #this switch decides what syllable is to be put in the word
        # - with all the lines ending in ##1 commented in,
        #   it would be dependent on active/passive (voice)
        #   I would rather have it be dependent on something else, voice is represented in too many decisions
        switch = self.wtype["noun_class"]
        # switch += ("passive" if self.wtype["passive"] else "active") ##1
        if("case_class" in self.wtype.keys() and self.wtype["case_class"] != None):
            self.spell_perceived(1)
            self.spell_case_class(None) #Jlt -> Jo<l..t.>
            self.result += WHICH(switch, [
                ("action",  "ma"), #Jlt -> Jo<l..t.>ma
                ("actor",   "ji"), #Jlt -> Jo<l..t.>ji
                ("object",  "ra"), #Jlt -> Jo<l..t.>ra
                # ("actionactive",  "ma"), #Jlt -> Jo<l..t.>ma ##1
                # ("actionpassive", "wo"), #Jlt -> Jo<l..t.>wo ##1
                # ("actoractive",   "ji"), #Jlt -> Jo<l..t.>ji ##1
                # ("actorpassive",  "ru"), #Jlt -> Jo<l..t.>ru ##1
                # ("objectactive",  "ra"), #Jlt -> Jo<l..t.>ra ##1
                # ("objectpassive", "ke"), #Jlt -> Jo<l..t.>ke ##1
            ])
            self.result = accent_syllable(self, self.result, 2, -2)
            self.syllable_no_accent_count += 1
            self.spell_professional()
        else:
            # self.result += self.root[1] #Jlt -> Jol
            self.spell_perceived(1)
            self.result += WHICH(switch, [
                ("action",  "a"), #Jlt -> Jo<l..t.>a
                ("actor",   "i"), #Jlt -> Jo<l..t.>i
                ("object",  "a"), #Jlt -> Jo<l..t.>a
                # ("actionactive",  "a"), #Jlt -> Jola ##1
                # ("actionpassive", "o"), #Jlt -> Jolo ##1
                # ("actoractive",   "i"), #Jlt -> Joli ##1
                # ("actorpassive",  "u"), #Jlt -> Jolu ##1
                # ("objectactive",  "a"), #Jlt -> Jola ##1
                # ("objectpassive", "e"), #Jlt -> Jole ##1
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
            if(self.wtype["passive"]):
                self.spell_passive()
                # self.result = accent_syllable(self, self.result, 2, -2)
            if(self.root[2] != "k"):
                self.result += self.root[2] #Jlt -> Jol[aou]t
            else:
                self.result += WHICH(switch, [
                    ("action", "m"),
                    ("actor",  "x"),
                    ("object", "P"),
                    # ("actionactive",  "m"), #Jlt -> Jolam ##1
                    # ("actionpassive", "v"), #Jlt -> Jolov ##1
                    # ("actoractive",   "x"), #Jlt -> Jolix ##1
                    # ("actorpassive",  "r"), #Jlt -> Jolur ##1
                    # ("objectactive",  "P"), #Jlt -> JolaP ##1
                    # ("objectpassive", "k"), #Jlt -> Jolek ##1
                ])
            self.result += WHICH(self.wtype["professional"],[
                (True, "i"), #Jlt -> Jol[aoiu][mvxr]i
                (False, "e"),
                (None, "a"),
            ])
            self.syllable_no_accent_count += 1
            self.result = accent_syllable(self, self.result, 1, -1)
        if(self.wtype["number"] == "plural"):
            self.result += "ne"
        # return result
    def spell_case_class(self, root_level=1): #looks at "case_class"
        if(root_level != None):
            self.result += self.root[root_level] #Jlt -> Jol
        self.syllable_no_accent_count += 1 #counting the switch vowel already
        switch = self.wtype["case_class"]
        if("case" in self.wtype.keys() and self.wtype["case"] != None):
            if(switch == "directional"):
                self.result += "a"
                self.spell_case(2, "e") #Jlt -> Jola<.t.e.>
            elif(switch == "local"):
                self.result += "o"
                self.spell_case(2, "u") #Jlt -> Jolo<.t.u.>
            elif(switch == "temporal"):
                self.result += "e"
                self.spell_case(2, "i") #Jlt -> Jole<.t.i.>
            elif(switch == "causal"):
                self.result += "u"
                self.spell_case(2, "o") #Jlt -> Jolu<.t.o.>
        else:
            r2 = self.spell_passive(2) #Jlt -> Jol[aoeu](xe)t
            # self.result = accent_syllable(self, self.result, 2, -2)
            self.result += WHICH(switch, [
                ("directional", "a" + r2 + "e"),    #Jlt -> Jola(xe)te
                ("local",       "o" + r2 + "u"),    #Jlt \-> Jolo(xe)tu
                ("temporal",    "e" + r2 + "i"),    #Jlt \-> Jole(xe)ti
                ("causal",      "u" + r2 + "o"),    #Jlt \-> Jolu(xe)to
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
        # return result
    def spell_case(self, root_level, second_vowel): #looks at "case"
        switch = self.wtype["case"]
        self.result += WHICH(
            self.wtype["case"],
            [
                ("before",  "sa"), #Jlt -> Jol[aeou]sa
                ("after",   "ro"), #Jlt -> Jol[aeou]ro
                ("above",   "ke"), #Jlt -> Jol[aeou]ke
                ("under",   "lu"), #Jlt -> Jol[aeou]lu
                ("near",    "ma"), #Jlt -> Jol[aeou]ma
                ("parallel","pi"), #Jlt -> Jol[aeou]pi
                ("same",    "taj"),#Jlt -> Jol[aeou]taj
                ("opposite",  "lo"), #Jlt -> Jol[aeou]fo
            ]
        )
        self.syllable_no_accent_count += 1
        if(root_level != None):
            if(root_level == 2):
                self.spell_passive(root_level)
            else:
                self.result += self.root[root_level]
            if(self.syllable_no_accent_count > 2):
                index = index_syllable(self.result, -2) #(beginning, vowel, end)
                i = index[1]
                self.result = self.result[:i] + accented[self.result[i]] + self.result[i+1:]
                self.syllable_no_accent_count = 1 if self.wtype["passive"] and not self.hist["passive"] else 0
            self.result += second_vowel #Jlt -> Jol[aoeu][[sa][ro]...](xe)t[euio]
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
        if(self.hist["passive"] and self.wtype["passive"] and "jx" in result):
            i = self.result.index("jx")
            self.result = self.result[:i]+"X"+self.result[i+2]
        # return result
    def spell_professional(self, flipped=False, accentable=False): #looks at "professional"
        if(not flipped):
            result = WHICH(self.wtype["professional"],[
                (True, "ti"),
                (False, "fo"),
                (None, ""),
            ])
        else:
            result = WHICH(self.wtype["professional"],[
                (True, "it"),
                (False, "of"),
                (None, ""),
            ])
        if(self.wtype["professional"] != None):
            self.syllable_no_accent_count += len(result)//2
            if(flipped and accentable):
                result = accented[result[0]]+result[1]
                self.syllable_no_accent_count = 0
        self.result += result
        # return result
    def spell_passive(self, root_level=None): #looks at "passive"
        if(self.wtype["passive"]):
            self.result += "x"
            if(not self.hist["passive"]):
                self.result += "e"
                self.syllable_no_accent_count += 1
        self.result = accent_syllable(self, self.result, 3, -2)
        if(root_level != None):
            r = self.root[root_level]
            self.result += r #Jlt -> (Jalju)xet
        # return result
    def spell_perceived(self, root_level=1): #looks at "perceived"
        if(self.wtype["perceived"]):
            self.result += "L"
            if(not self.hist["perceived"]):
                self.result += "e"
                self.syllable_no_accent_count += 1
        self.result = accent_syllable(self, self.result, 3, -2)
        if(root_level != None):
            self.result += self.root[root_level] #Jlt -> (Jalju)xet
        # return result
    def spell_attribute(self, root_level=None): #looks at "attribute_class"
        for key in standards_attribute.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_attribute[key]
        #attribute_class:
        #  stative active: reading
        #  stative passive: read / being read -> tenses?
        #  possible active: able to read
        #  possible passive: readable = able to be read
        #  conjunctive active: should read
        #  conjunctive passive: should be read
        #  obligate active: must read
        #  obligate passive: must be read
        switch = self.wtype["attribute_class"]+("passive" if self.wtype["passive"] else "active")
        self.result += WHICH(switch, [
            ("stativeactive",      "za"), #Jlt -> Jo<l..t.>za
            ("stativepassive",     "Xa"), #Jlt -> Jo<l..t.>Xa
            ("possibleactive",     "to"), #Jlt -> Jo<l..t.>to
            ("possiblepassive",    "Do"), #Jlt -> Jo<l..t.>Do
            ("conjunctiveactive",  "li"), #Jlt -> Jo<l..t.>li
            ("conjunctivepassive", "wy"), #Jlt -> Jo<l..t.>wy
            ("obligateactive",     "ku"), #Jlt -> Jo<l..t.>ku
            ("obligatepassive",    "qe"), #Jlt -> Jo<l..t.>qe
        ])
        self.syllable_no_accent_count += 1
        self.result = accent_syllable(self, self.result, 2, -2)
        self.spell_perceived(1)
        if(self.wtype["metaphore"]):
            self.result += "y"
        else:
            self.result += "e"
        self.result = accent_syllable(self, self.result, 2, -2)
        self.spell_tense(2)
        self.result = accent_syllable(self, self.result, 1, -1)
        # return result
