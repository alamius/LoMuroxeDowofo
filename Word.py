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
accent_level = {
    "person": 2,
    "root_0": 5,
    "root_1": 4,
    "root_2": 5,
    "tense": 2,
    "imperative": 3,
    "noun_class": 2,
    "case": 3,
    "attribute_class": 3,
    "professional": 1,
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
        # self.result = SyllableString()
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
    def __repr__(self):
        return "Word"+repr(self.result)[4:]
    def __str__(self):
        return str(self.result)
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
                self.wtype["child_place_string"] += [Syllable(string)]
    def add_place(self, place, string):
        self.wtype["parent_place"] += [place]
        self.wtype["parent_place_string"] += [Syllable(string)]
    def spell(self): #looks at "class"
        for key in standards_word.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_word[key]
        self.result = SyllableString(None, CVSyllable)
        self.result += self.wtype["parent_place_string"]
        if(self.wtype["metaphore"]):
            self.spell_metaphore()
        switch = self.wtype["class"]
        if(switch == "verb"):
            self.result += self.root[0] + "a"
            self.result[-1].accent_level = accent_level["root_0"]
            self.spell_verb() #Jlt -> Ja
        elif(switch == "noun"):
            self.result += self.root[0] + "o"
            self.result[-1].accent_level = accent_level["root_0"]
            self.spell_noun() #Jlt -> Jo
        elif(switch == "attribute"):
            self.result += self.root[0] + "e"
            self.result[-1].accent_level = accent_level["root_0"]
            self.spell_attribute() #Jlt -> Je
        else:
            raise TypeError("Unknown class: '%s'" % switch)
        if(len(self.children) != 0 and len(self.parents) != 0):
            self.result += self.wtype["child_place_string"]
        self.result.accent()
        return self.result
        # It is questionable in my eyes to accent parent-syllables in words as a consequence of their parents' other child-syllables,
        #   if they cause accent clusters in the child while their parent may not even pronounce the accented child-syllable or any other.
        #   This might however be a complicated result of the history of the language and is not complete horse-shit.
        if(self.non_accented_syllables() > 2):
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
        self.result += "gy" #Jlt -> gy
    def spell_verb(self): #looks at "verb_class"
        for key in standards_verb.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_verb[key]
        self.spell_perceived() #Jlt -> JaLe
        switch = self.wtype["verb_class"]
        if(switch == "imperative"):
            self.spell_tense(1)
            self.result += "'o"
            self.result[-1].accent_level = accent_level["imperative"]
            self.spell_person(2)
        elif(switch == "indicative"):
            self.spell_tense(1)
            self.spell_person(2)
        else:
            raise ValueError("Unknown verb_class: '%s'" % switch)
    def spell_tense(self, root_level=1): #looks at "tense"
        if(root_level != None):
            if(root_level == 2):
                self.spell_negative() #Jlt -> Jale(xe)
                self.spell_professional() #Jlt -> Jale(xe)[ti|fo]
        r_ = self.root[root_level]
        switch = self.wtype["tense"]
        if(switch == "present"):
            if(r_ != "k"):
                self.result += r_ + "e" #Jlt -> Jale
        elif(switch == "past"):
            self.result += r_ + "o" #Jlt -> Jalo
        elif(switch == "future"):
            self.result += r_ + "u" #Jlt -> Jalu
        else:
            self.result += r_ + "i" #Jlt -> Jali
        self.result[-1].accent_level = accent_level["root_"+str(root_level)]
        # if(self.non_accented_syllables() > 1 and True): #TODO: replace True with somthing about root2 being far enough away)?
        #     self.result[-1].accented = True #make the last syllable in the result accented
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
            result = [["o"]] #Jlt -> Jaloto
        elif(["plural-me", "plural-you", "plural-they"] == switch):
            result = [["on"]] #Jlt -> Jaloton
        else:
            for person in persons:
                if(person in switch): #checking for "you" and similar in wtype["person"]
                    result += [[person_ending[person]]]
                if("plural-"+person in switch): #checking for "plural-you" and similar in wtype["person"]
                    result += [[person_ending[person], "ne"]] #adding the plural syllable
        #adding all the person-forms with s as filler-consonants
        while(len(result) > 1):
            self.result += "s" + result[-1][0]
            if(len(result[-1]) > 1):  #if there is a "ne" after the person marker
                self.result += result[-1][1:]
            result.pop(-1)
            if(self.result[-1].__eq__("ne")):
                self.result[-2].accent_level = accent_level["person"]
        if(root_level == 2):
            self.spell_negative()
        r_ = self.root[root_level] #Jlt -> Jale(xe)t
        # self.spell_professional( #Jlt -> Jalse(xe)t[[it][of]][aj|u|e|i|o][ne]
        #     flipped=True,
        #     accentable=(self.non_accented_syllables() > 0)
        # )
        self.result += r_ + result[0][0]
        self.result[-1].accent_level = accent_level["root_"+str(root_level)]
        if(len(result[0]) > 1): #if there is a "ne" after the person marker
            self.result += result[0][1:]
        if("plural" in switch and result == ["i"]):
            self.result += "ne"
    def spell_noun(self): #looks at "noun_class"
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
            self.spell_perceived()
            self.spell_case_class(1) #Jlt -> Jo<l..t.>
            self.result += WHICH(switch, [
                ("action",  "ma"), #Jlt -> Jo<l..t.>ma
                ("agent",   "Ji"), #Jlt -> Jo<l..t.>Ji
                ("object",  "ru"), #Jlt -> Jo<l..t.>ru
                ("recipient","Po"), #Jlt -> Jo<l..t.>Po
                ("instrument","we"), #Jlt -> Jo<l..t.>we
            ])
            self.result[-1].accent_level = accent_level["noun_class"]
            self.spell_professional()
        else:
            self.spell_perceived()
            r1 = self.root[1]
            self.result += WHICH(switch, [
                ("action",  r1+"a"), #Jlt -> Jo<l.>a
                ("agent",   r1+"i"), #Jlt -> Jo<l.>i
                ("object",  r1+"u"), #Jlt -> Jo<l.>u
                ("recipient",r1+"o"), #Jlt -> Jo<l.>o
                ("instrument",r1+"e"), #Jlt -> Jo<l.>a
            ])
            self.result[-1].accent_level = accent_level["root_1"]
            if(self.wtype["negative"]):
                self.spell_negative()
            if(self.root[2] != "k"):
                r2 = self.root[2] #Jlt -> Jol[aou]t
            else:
                r2 = WHICH(switch, [
                    ("action", "m"),
                    ("agent",  "J"),
                    ("object", "r"),
                    ("recipient","P"),
                    ("instrument", "w"),
                ])
            r2 += WHICH(self.wtype["professional"],[
                (True, "i"), #Jlt -> Jol[aoiu][mvxr]i
                (False, "e"),
                (None, "a"),
            ])
            self.result += r2
            self.result[-1].accent_level = accent_level["root_2"]
        if(self.wtype["number"] == "plural"):
            self.result += "ne"
    def spell_case_class(self, root_level=1): #looks at "case_class"
        if(root_level != None):
            r_ = self.root[root_level] #Jlt -> Jol
        switch = self.wtype["case_class"]
        if("case" in self.wtype.keys() and self.wtype["case"] != None):
            if(switch == "directional"):
                self.result += r_ + "a"
                self.result[-1].accent_level = accent_level["root_"+str(root_level)]
                self.spell_case(2, "e") #Jlt -> Jola<.t.e.>
            elif(switch == "local"):
                self.result += r_ + "o"
                self.result[-1].accent_level = accent_level["root_"+str(root_level)]
                self.spell_case(2, "u") #Jlt -> Jolo<.t.u.>
            elif(switch == "temporal"):
                self.result += r_ + "e"
                self.result[-1].accent_level = accent_level["root_"+str(root_level)]
                self.spell_case(2, "i") #Jlt -> Jole<.t.i.>
            elif(switch == "causal"):
                self.result += r_ + "u"
                self.result[-1].accent_level = accent_level["root_"+str(root_level)]
                self.spell_case(2, "o") #Jlt -> Jolu<.t.o.>
        else:
            self.result += WHICH(switch, [
                ("directional", r_ + "a"),    #Jlt -> Jola
                ("local",       r_ + "o"),    #Jlt -> Jolo
                ("temporal",    r_ + "e"),    #Jlt -> Jole
                ("causal",      r_ + "u"),    #Jlt -> Jolu
            ])
            self.result[-1].accent_level = accent_level["root_"+str(root_level)]
            self.spell_negative() #Jlt -> Jol[aoeu](xe)
            r2 = self.root[2]
            self.result += WHICH(switch, [
                ("directional", r2 + "e"),    #Jlt -> Jola(xe)te
                ("local",       r2 + "u"),    #Jlt \-> Jolo(xe)tu
                ("temporal",    r2 + "i"),    #Jlt \-> Jole(xe)ti
                ("causal",      r2 + "o"),    #Jlt \-> Jolu(xe)to
            ])
            self.result[-1].accent_level = accent_level["root_2"]
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
        self.result[-1].accent_level = accent_level["case"]
        if(root_level != None):
            if(root_level == 2):
                self.spell_negative()
            self.result += self.root[root_level] + second_vowel #Jlt -> Jol[aoeu][[sa][ro]...](xe)t[euio]
            self.result[-1].accent_level = accent_level["root_"+str(root_level)]
    def spell_professional(self, root_level=None): #looks at "professional"
        if(root_level == None):
            self.result += WHICH(self.wtype["professional"],[
                (True, "ti"),
                (False, "fo"),
                (None, ""),
            ])
            self.result[-1].accent_level = accent_level["professional"]
        else:
            r_ = self.root[root_level]
            self.result += WHICH(self.wtype["professional"],[
                (True, [r_ + "i", "te"]),
                (False, [r_ + "o", "fe"]),
                (None, [r_ + "e"]),
            ])
    def spell_negative(self): #looks at "negative"
        if(self.wtype["negative"]):
            self.result += "xe"
    def spell_perceived(self): #looks at "perceived"
        if(self.wtype["perceived"]):
            self.result += "Le"
    def spell_attribute(self): #looks at "attribute_class"
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
        self.result[-1].accent_level = accent_level["attribute_class"]
        self.spell_perceived()
        r1 = self.root[1]
        if(self.wtype["metaphore"]):
            self.result += r1 + "y"
        else:
            self.result += r1 + "e"
        self.result[-1].accent_level = accent_level["root_1"]
        self.spell_tense(2)
    def non_accented_syllables(self):
        #counting non-accented syllables (backwards)
        for i in range(len(self.result)-1, -1, -1):
            if(self.result[i].accented):
                break
        return len(self.result) - i
    def accent_syllable(self, need, pos):
        if(self.non_accented_syllables() > need):
            self.result[pos].accented = True
        # else:
        #     self.result[pos].accented = False
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
