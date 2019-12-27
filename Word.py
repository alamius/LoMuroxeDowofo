from notation import accented, vowels, consonants, semivowels
from vocab import roots
from syllables import *
def WHICH(switch, ARGS): #TODO: Think about useful version with functions
    try:
        for case, result in ARGS:
            if(switch == case):
                return result
    except:
        if(type(ARGS[-1]) != type((1, 1))):
            return ARGS[-1]

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
def boolify(wtype):
    for k in wtype.keys():
        v = wtype[k]
        if(type(v) == str):
            if(v.lower()  == "false"): wtype[k] = False
            elif(v.lower() == "true"): wtype[k] = True
            elif(v.lower() == "none"): wtype[k] = None
    return wtype
class Word(object):
    def __init__(self, root, wtype, parents=[], children=[], hist=hist):
        super(Word, self).__init__()
        if(root != None):
            self.root = root
        else:
            self.root = wtype["root"]
        for i in range(3-len(self.root)):
            self.root += "k" #gr -> grk
        self.wtype = deepcopy(wtype)
        self.wtype["root"] = self.root
        self.parents = deepcopy(parents)
        self.children = deepcopy(children)
        try:
            self.marker = self.wtype["marker"]
        except:
            pass
        self.hist = hist
        self.syllable_no_accent_count = 0
        self.result = ""
        if("marker" in self.wtype.keys()):
            self.marker = self.wtype["marker"]
            del self.wtype["marker"]
        else:
            self.marker = ""
        try:            self.wtype["parent_place"]
        except KeyError:self.wtype["parent_place"] = []
        try:            self.wtype["parent_place_string"]
        except KeyError:self.wtype["parent_place_string"] = []
        try:            self.wtype["child_place"]
        except KeyError:self.wtype["child_place"] = []
        try:            self.wtype["child_place_string"]
        except KeyError:self.wtype["child_place_string"] = []
        boolify(self.wtype)
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
        else:
            raise TypeError("Unknown class: '%s'" % switch)
        if(len(self.children) != 0 and len(self.parents) != 0):
            self.result += ''.join(self.wtype["child_place_string"])
            self.syllable_no_accent_count += len(self.children)
        return self.result
        # It is questionable in my eyes to accent parent-syllables in words as a consequence of their parents' other child-syllables,
        #   if they cause accent clusters in the child while their parent may not even pronounce the accented child-syllable or any other.
        #   This might however be a complicated result of the history of the language and is not complete horse-shit.
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
        self.result += "gy" + self.root[0] #Jlt -> gyJ
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
        if(switch == "imperative"):
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
        else:
            raise ValueError("Unknown verb_class: '%s'" % switch)
    def spell_tense(self, root_level=1): #looks at "tense"
        if(root_level != None):
            if(root_level == 2):
                self.spell_negative(2) #Jlt -> Jale(xe)t
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
                self.syllable_no_accent_count += 1
        elif(switch == "past"):
            self.result += "o" #Jlt -> Jalo
            self.syllable_no_accent_count += 1
        elif(switch == "future"):
            self.result += "u" #Jlt -> Jalu
            self.syllable_no_accent_count += 1
        else:
            self.result += "i" #Jlt -> Jali
            self.syllable_no_accent_count += 1
        if(self.syllable_no_accent_count > 1 and True): #TODO: replace True with somthing about root2 being far enough away)
            self.result = self.result[:-1]+accented[self.result[-1]] #make the last character in the result accented
            self.syllable_no_accent_count = 0
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
            self.spell_negative()
        self.result += self.root[root_level] #Jlt -> Jale(xe)t
        if(self.hist["negative"] and self.wtype["negative"] and "xek" in self.result):
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
            self.result = accent_syllable(self, self.result, 2, -1)
        if("plural" in switch and result == ["i"]):
            self.result += "ne"
            self.syllable_no_accent_count += 1
    def spell_noun(self, root_level=1): #looks at "noun_class"
        for key in standards_noun.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_noun[key]
        #this switch decides what syllable is to be put in the word
        # - with all the lines ending in ##1 commented in,
        #   it would be dependent on positive/negative
        #   I would rather have it be dependent on something else, voice is represented in too many decisions
        switch = self.wtype["noun_class"]
        # switch += ("negative" if self.wtype["negative"] else "active") ##1
        if("case_class" in self.wtype.keys() and self.wtype["case_class"] != None):
            self.spell_perceived(1)
            self.spell_case_class(None) #Jlt -> Jo<l..t.>
            self.result += WHICH(switch, [
                ("action",  "ma"), #Jlt -> Jo<l..t.>ma
                ("agent",   "Ji"), #Jlt -> Jo<l..t.>Ji
                ("object",  "ru"), #Jlt -> Jo<l..t.>ru
                ("recipient","Po"), #Jlt -> Jo<l..t.>Po
                ("instrument","we"), #Jlt -> Jo<l..t.>we
            ])
            self.result = accent_syllable(self, self.result, 2, -2)
            self.syllable_no_accent_count += 1
            self.spell_professional()
        else:
            self.spell_perceived(1)
            self.result += WHICH(switch, [
                ("action",  "a"), #Jlt -> Jo<l.>a
                ("agent",   "i"), #Jlt -> Jo<l.>i
                ("object",  "u"), #Jlt -> Jo<l.>u
                ("recipient","o"), #Jlt -> Jo<l.>o
                ("instrument","e"), #Jlt -> Jo<l.>a
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
            if(self.wtype["negative"]):
                self.spell_negative()
            if(self.root[2] != "k"):
                self.result += self.root[2] #Jlt -> Jol[aou]t
            else:
                self.result += WHICH(switch, [
                    ("action", "m"),
                    ("agent",  "J"),
                    ("object", "r"),
                    ("recipient","P"),
                    ("instrument", "w"),
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
            self.syllable_no_accent_count += 1
            self.result = accent_syllable(self, self.result, 3, -2)
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
            self.result += WHICH(switch, [
                ("directional", "a"),    #Jlt -> Jola
                ("local",       "o"),    #Jlt \-> Jolo
                ("temporal",    "e"),    #Jlt \-> Jole
                ("causal",      "u"),    #Jlt \-> Jolu
            ])
            self.syllable_no_accent_count += 1
            self.spell_negative(2) #Jlt -> Jol[aoeu](xe)t
            self.result += WHICH(switch, [
                ("directional", "e"),    #Jlt -> Jola(xe)te
                ("local",       "u"),    #Jlt \-> Jolo(xe)tu
                ("temporal",    "i"),    #Jlt \-> Jole(xe)ti
                ("causal",      "o"),    #Jlt \-> Jolu(xe)to
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
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
                self.spell_negative(root_level)
            else:
                self.result += self.root[root_level]
            if(self.syllable_no_accent_count > 2):
                index = index_syllable(self.result, -2) #(beginning, vowel, end)
                i = index[1]
                self.result = self.result[:i] + accented[self.result[i]] + self.result[i+1:]
                self.syllable_no_accent_count = 1 if self.wtype["negative"] else 0
            self.result += second_vowel #Jlt -> Jol[aoeu][[sa][ro]...](xe)t[euio]
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
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
    def spell_negative(self, root_level=None): #looks at "negative"
        if(self.wtype["negative"]):
            self.result += "xe"
            self.syllable_no_accent_count += 1
        self.result = accent_syllable(self, self.result, 3, -2)
        if(root_level != None):
            r = self.root[root_level]
            self.result += r #Jlt -> (Jalju)xet
    def spell_perceived(self, root_level=1): #looks at "perceived"
        if(self.wtype["perceived"]):
            self.result += "L"
            if(not self.hist["perceived"]):
                self.result += "e"
                self.syllable_no_accent_count += 1
        self.result = accent_syllable(self, self.result, 3, -2)
        if(root_level != None):
            self.result += self.root[root_level] #Jlt -> JaLel
    def spell_attribute(self, root_level=None): #looks at "attribute_class"
        for key in standards_attribute.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_attribute[key]
        switch = self.wtype["attribute_class"]
        self.result += WHICH(switch, [
            ("stative",      "za"), #Jlt -> Jo<l..t.>za
            ("possible",     "to"), #Jlt -> Jo<l..t.>to
            ("conjunctive",  "li"), #Jlt -> Jo<l..t.>li
            ("obligate",     "ku"), #Jlt -> Jo<l..t.>ku
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
    def export(self, sentence_structure_markers_as_syllables=False):
        result = "{\n"
        for key in self.wtype.keys():
            if(key in ["parent_place", "parent_place_string", "child_place", "child_place_string"]):
                continue
            result += "\t\"%s\": %s, \n" % (key, repr(self.wtype[key]))
        if(not "root_english" in self.wtype.keys()):
            root_english = "---"
            root = self.root[:2] if self.root[2] == "k" else self.root
            for key in roots.keys():
                if(roots[key] == root):
                    root_english = key
            result += "\t\"%s\": %s, \n" % ("root_english", repr(root_english))
        if(not "marker" in self.wtype.keys()):
            markers = []
            markers += self.get_marker()
            result += "\t\"%s\": %s, " % ("marker", repr(markers))
        result += "\n}"
        return result
    def get_marker(self):
        from marks import marks_reverse
        if(self.marker != ""):
            return self.marker
        else:
            try:
                self.marker = marks_reverse[self.wtype["parent_place"][0]]
                parent_marker = self.parents[0].get_marker()
            except IndexError:
                self.marker = "V" #TODO: make it count the number of root verbs
                parent_marker = [""]
                #TODO: decide if there is need for a detection of root nouns or even root attributes
            result = [selfm+"-"+parentm for selfm in self.marker for parentm in parent_marker]
            return result
