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
    if(self.syllable_no_accent_count > syllable_no_accent_threshhold):
        index = index_syllable(string, syllable_index) #(beginning, vowel, end)
        i = index[1]
        string = string[:i] + accented[string[i]] + string[i+1:]
        self.syllable_no_accent_count = 0
    return string

PLACE = {
    "subject":      ["ta", "vo", "kô"],
    "object":       ["le", "so", "ne"],
    "attribute":    ["ri", "Ju", "wa", "Je", "Li"],
    "clause":       ["xs", "Xl", "Qr", "ðJ", "wj", "CL", "ps", "df"],
}

from copy import deepcopy
from hist import hist
from wtype import standards_word, standards_verb, standards_noun
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
<<<<<<< HEAD
=======
        self.wtype["root"] = self.root
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
        self.parents = deepcopy(parents)
        self.children = deepcopy(children)
        self.subject = None
        self.hist = hist
        self.syllable_no_accent_count = 0
<<<<<<< HEAD
=======
        self.result = ""
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
        try:            self.wtype["parent_place"]
        except KeyError:self.wtype["parent_place"] = []
        try:            self.wtype["parent_place_string"]
        except KeyError:self.wtype["parent_place_string"] = ""
        try:            self.wtype["child_place"]
        except KeyError:self.wtype["child_place"] = []
        try:            self.wtype["child_place_string"]
        except KeyError:self.wtype["child_place_string"] = ""
        for k in self.wtype.keys():
            if(type(self.wtype[k]) == type(" ") and self.wtype[k].lower() == "false"):  self.wtype[k] = False
            elif(type(self.wtype[k]) == type(" ") and self.wtype[k].lower() == "true"): self.wtype[k] = True
            elif(type(self.wtype[k]) == type(" ") and self.wtype[k].lower() == "none"): self.wtype[k] = None
    def add_child(self, child, place="attribute"):
        child.parents += [self]
        self.children += [child]
        if(place in PLACE.keys()):
            #adding the place at the beginning in the internal index in every following generation
            count_place = self.wtype["child_place"].count(place)
            string = PLACE[place][count_place % len(PLACE[place])]
            child_place = child.add_place(place, string)
            self.wtype["child_place"] += [place]
            self.wtype["child_place_string"] += string
    def add_place(self, place, string):
        self.wtype["parent_place"] += [place]
        self.wtype["parent_place_string"] += string
    def spell(self): #looks at "class"
        for key in standards_word.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_word[key]
<<<<<<< HEAD
        result = ""
        result += self.wtype["parent_place_string"]
        if(self.wtype["metaphore"]):
            result += self.spell_metaphore()
            self.syllable_no_accent_count += 1 #metaphore
        else:
            result += self.root[0]
        self.syllable_no_accent_count = 0 #root0 vowel always accented
        switch = self.wtype["class"]
        if(switch == "verb"):
            result += "á" + self.spell_verb() #Jlt -> Ja
        elif(switch == "noun"):
            result += "ó" + self.spell_noun() #Jlt -> Jo
        elif(switch == "adjective"):
            result += "é" + self.spell_noun() #Jlt -> Je
        elif(switch == "other"): #TODO
            result += "Ú" #Jlt -> Ju
        if(len(self.parents) != 0):
            result += self.wtype["child_place_string"]
            self.syllable_no_accent_count += len(self.children)
        if(self.syllable_no_accent_count > 2):
            index = index_syllable(result, -2) #(beginning, vowel, end)
            i = index[1]
            syllable_original = result[index[0]:index[2]]
            result = result[:i] + accented[result[i]] + result[i+1:]
            syllable_accented = result[index[0]:index[2]]
=======
        self.result = ""
        self.result += self.wtype["parent_place_string"]
        if(self.wtype["metaphore"]):
            self.spell_metaphore()
            self.syllable_no_accent_count += 1 #metaphore
        else:
            self.result += self.root[0]
        self.syllable_no_accent_count = 0 #root0 vowel always accented
        switch = self.wtype["class"]
        if(switch == "verb"):
            self.result += "á"
            self.spell_verb() #Jlt -> Ja
        elif(switch == "noun"):
            self.result += "ó"
            self.spell_noun() #Jlt -> Jo
        elif(switch == "adjective"):
            self.result += "é"
            self.spell_noun() #Jlt -> Je
        elif(switch == "other"): #TODO
            self.result += "ú" #Jlt -> Ju
        if(len(self.parents) != 0):
            self.result += self.wtype["child_place_string"]
            self.syllable_no_accent_count += len(self.children)
        if(self.syllable_no_accent_count > 2):
            index = index_syllable(self.result, -2) #(beginning, vowel, end)
            i = index[1]
            syllable_original = self.result[index[0]:index[2]]
            self.result = self.result[:i] + accented[self.result[i]] + self.result[i+1:]
            syllable_accented = self.result[index[0]:index[2]]
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
            if(syllable_original in self.wtype["child_place_string"]):
                c_place_str = self.wtype["child_place_string"]
                i = c_place_str.index(syllable_original)
                self.wtype["child_place_string"] = c_place_str[:i+1] + accented[c_place_str[i+1]] + c_place_str[i+2:]
                p_place_str = self.children[i//2].wtype["parent_place_string"]
                j = p_place_str.index(syllable_original)
                self.children[i//2].wtype["parent_place_string"] = p_place_str[:j+1] + accented[p_place_str[j+1]] + p_place_str[j+2:]
<<<<<<< HEAD
        return result
    def spell_metaphore(self):
        result = ""
        if(not hist["metaphor-merge"]):
            result += "gö" + self.root[0] #Jlt -> J
        else:
            result += "'ö"
            try:
                result += g_merge[self.root[0]]
            except:
                result += g_merge[""] + self.root[0]
        return result
=======
        return self.result
    def spell_metaphore(self):
        # self.result = ""
        if(not hist["metaphor-merge"]):
            self.result += "gö" + self.root[0] #Jlt -> J
        else:
            self.result += "'ö"
            try:
                self.result += g_merge[self.root[0]]
            except:
                self.result += g_merge[""] + self.root[0]
        # return result
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
    def spell_verb(self, root_level=1): #looks at "verb_class"
        for key in standards_verb.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_verb[key]
<<<<<<< HEAD
        result = ""
        if(root_level != None):
            result += self.root[root_level] #Jlt -> Jal
        switch = self.wtype["verb_class"]
        if(switch == "infinitive"):
            self.syllable_no_accent_count += 1
            result += "ju" #Jlt -> Jalju
            result += self.spell_tense(2)
        elif(switch == "imperative"):
            self.syllable_no_accent_count += 1
            result += "o" + self.spell_person(2)
        elif(switch == "indicative"):
            # resetting and not using a character from self.root yet (leaving that to the subroutines)
            result = self.spell_tense(1)
            result += self.spell_person(2)
        elif(switch == "other"): # TODO: other verb classes?
            result += "u" #Jlt -> Jalu
        return result
    def spell_tense(self, root_level=1): #looks at "tense"
        result = ""
        if(root_level != None):
            if(root_level == 2):
                result += self.spell_passive(root_level) + self.spell_professional(flipped=True) #Jlt -> Jale(xe)t[[it][of]]
            else:
                result += self.root[root_level]
            result = accent_syllable(self, result, 2, -2)
        switch = self.wtype["tense"]
        if(switch == "present"):
            if(result == "k"):
                return "" #Jl -> Jal
            elif(not self.hist["present"]):
                result += "e" #Jlt -> Jale
        elif(switch == "past"):
            result += "o" #Jlt -> Jalo
        elif(switch == "future"):
            result += "u" #Jlt -> Jalu
        else:
            result += "i" #Jlt -> Jali
        if(not self.hist["present"] or switch in ["past", "future"]):
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1 and True): #TODO: replace True with somthing about root2 being far enough away)
                result = result[:-1]+accented[result[-1]] #make the last character in the result accented
                self.syllable_no_accent_count = 0
        return result
=======
        if(root_level != None):
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
            self.syllable_no_accent_count += 1
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
                self.result += self.spell_passive(root_level) + self.spell_professional(flipped=True) #Jlt -> Jale(xe)t[[it][of]]
            else:
                self.result += self.root[root_level]
            self.result = accent_syllable(self, self.result, 2, -2)
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
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
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
                    result += [person_ending[person]+"n"] #Jlt -> Jaloten
                elif(person in switch): #checking for "you" in wtype["person"]
                    result += [person_ending[person]] #Jlt -> Jalote
<<<<<<< HEAD
        result_str = ""
        #adding all the person-forms with s as filler-consonants
        while(len(result) > 1):
            result_str += "s" + result.pop(-1)
            self.syllable_no_accent_count += 1
        if(root_level == 2):
            result_str += self.spell_passive()
            # if(self.root[root_level] != "k"):
            result_str += self.root[root_level] #Jlt -> Jale(xe)t
            if(self.hist["passive"] and self.wtype["passive"] and "xek" in result):
                i = result.index("xek")
                result = result[:i]+"x"+result[i+2]
                self.syllable_no_accent_count -= 1
            result_str = accent_syllable(self, result_str, 2, -2)
            self.syllable_no_accent_count += 1 if "xe" in result_str else 0
            result_str += self.spell_professional( #Jlt -> Jalse(xe)t[[it][of]][aj|u|e|i|o][n]
                flipped=True,
                accentable=(self.syllable_no_accent_count > 1)
            )
            result_str += result[0]
            self.syllable_no_accent_count += 1
            result_str = accent_syllable(self, result_str, 1, -1)
            # else:
            #     result_str += result[0]
        if("plural" in switch and result == ["i"]):
            result_str += "n"
        return result_str
=======
        #adding all the person-forms with s as filler-consonants
        while(len(result) > 1):
            self.result += "s" + result.pop(-1)
            self.syllable_no_accent_count += 1
        if(root_level == 2):
            self.spell_passive()
            # if(self.root[root_level] != "k"):
            self.result += self.root[root_level] #Jlt -> Jale(xe)t
            if(self.hist["passive"] and self.wtype["passive"] and "xek" in self.result):
                i = self.result.index("xek")
                self.result = self.result[:i]+"x"+self.result[i+2]
                self.syllable_no_accent_count -= 1
            self.result = accent_syllable(self, self.result, 2, -2)
            self.syllable_no_accent_count += 1 if "xe" in self.result else 0
            self.spell_professional( #Jlt -> Jalse(xe)t[[it][of]][aj|u|e|i|o][n]
                flipped=True,
                accentable=(self.syllable_no_accent_count > 1)
            )
            self.result += result[0]
            self.syllable_no_accent_count += 1
            self.result = accent_syllable(self, self.result, 1, -1)
            # else:
            #     self.result += result[0]
        if("plural" in switch and result == ["i"]):
            self.result += "n"
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
    def spell_noun(self, root_level=1): #looks at "noun_class"
        for key in standards_noun.keys():
            if(not key in self.wtype.keys()):
                self.wtype[key] = standards_noun[key]
<<<<<<< HEAD
        result = "" #Jlt -> Jo
        switch = self.wtype["noun_class"]+("passive" if self.wtype["passive"] else "active")
        if("case_class" in self.wtype.keys() and self.wtype["case_class"] != None):
            result += self.spell_case_class(1) #Jlt -> Jo<l..t.>
            result += WHICH(switch, [
=======
        switch = self.wtype["noun_class"]+("passive" if self.wtype["passive"] else "active")
        if("case_class" in self.wtype.keys() and self.wtype["case_class"] != None):
            self.spell_case_class(1) #Jlt -> Jo<l..t.>
            self.result += WHICH(switch, [
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
                ("actionactive",  "ma"), #Jlt -> Jo<l..t.>ma
                ("actionpassive", "wo"), #Jlt -> Jo<l..t.>wo
                ("actoractive",   "ji"), #Jlt -> Jo<l..t.>ji
                ("actorpassive",  "ru"), #Jlt -> Jo<l..t.>ru
            ])
            self.syllable_no_accent_count += 1
<<<<<<< HEAD
            result = accent_syllable(self, result, 2, -2)
            result += self.spell_professional()
        else:
            result += self.root[1] #Jlt -> Jol
            result += WHICH(switch, [
=======
            self.result = accent_syllable(self, self.result, 2, -2)
            self.spell_professional()
        else:
            self.result += self.root[1] #Jlt -> Jol
            self.result += WHICH(switch, [
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
                ("actionactive",  "a"), #Jlt -> Jola
                ("actionpassive", "o"), #Jlt -> Jolo
                ("actoractive",   "i"), #Jlt -> Joli
                ("actorpassive",  "u"), #Jlt -> Jolu
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
<<<<<<< HEAD
                result = result[:-1]+accented[result[-1]]
                self.syllable_no_accent_count = 0
            if(self.wtype["passive"]):
                result += self.spell_passive()
                result = accent_syllable(self, result, 2, -2)
            if(self.root[2] != "k"):
                result += self.root[2] #Jlt -> Jol[aou]t
            else:
                result += WHICH(switch, [
=======
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
            if(self.wtype["passive"]):
                self.spell_passive()
                self.result = accent_syllable(self, self.result, 2, -2)
            if(self.root[2] != "k"):
                self.result += self.root[2] #Jlt -> Jol[aou]t
            else:
                self.result += WHICH(switch, [
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
                    ("actionactive",  "m"), #Jlt -> Jolam
                    ("actionpassive", "v"), #Jlt -> Jolov
                    ("actoractive",   "x"), #Jlt -> Jolix
                    ("actorpassive",  "r"), #Jlt -> Jolur
                ])
<<<<<<< HEAD
            result += WHICH(self.wtype["professional"],[
=======
            self.result += WHICH(self.wtype["professional"],[
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
                (True, "i"), #Jlt -> Jol[aoiu][mvxr]i
                (False, "e"),
                (None, "a"),
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
<<<<<<< HEAD
                result = result[:-1]+accented[result[-1]]
                self.syllable_no_accent_count = 0
        if(self.wtype["number"] == "plural"):
            result += "n"
        return result
    def spell_case_class(self, root_level=1): #looks at "case_class"
        result = ""
        if(root_level != None):
            result += self.root[root_level] #Jlt -> Jol
=======
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
        if(self.wtype["number"] == "plural"):
            self.result += "n"
        # return result
    def spell_case_class(self, root_level=1): #looks at "case_class"
        if(root_level != None):
            self.result += self.root[root_level] #Jlt -> Jol
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
        self.syllable_no_accent_count += 1 #counting the switch vowel already
        switch = self.wtype["case_class"]
        if("case" in self.wtype.keys() and self.wtype["case"] != None):
            if(switch == "directional"):
<<<<<<< HEAD
                result += "a" + self.spell_case(2, "e") #Jlt -> Jola<.t.e.>
            elif(switch == "local"):
                result += "o" + self.spell_case(2, "u") #Jlt -> Jolo<.t.u.>
            elif(switch == "temporal"):
                result += "e" + self.spell_case(2, "i") #Jlt -> Jole<.t.i.>
            elif(switch == "causal"):
                result += "u" + self.spell_case(2, "o") #Jlt -> Jolu<.t.o.>
        else:
            r2 = self.spell_passive(2) #Jlt -> Jol[aoeu](xe)t
            result = accent_syllable(self, result, 2, -2)
            result += WHICH(switch, [
=======
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
            self.result = accent_syllable(self, self.result, 2, -2)
            self.result += WHICH(switch, [
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
                ("directional", "a" + r2 + "e"),    #Jlt -> Jola(xe)te
                ("local",       "o" + r2 + "u"),    #Jlt \-> Jolo(xe)tu
                ("temporal",    "e" + r2 + "i"),    #Jlt \-> Jole(xe)ti
                ("causal",      "u" + r2 + "o"),    #Jlt \-> Jolu(xe)to
            ])
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
<<<<<<< HEAD
                result = result[:-1]+accented[result[-1]]
                self.syllable_no_accent_count = 0
        return result
    def spell_case(self, root_level, second_vowel): #looks at "case"
        result = ""
        switch = self.wtype["case"]
        result += WHICH(
=======
                self.result = self.result[:-1]+accented[self.result[-1]]
                self.syllable_no_accent_count = 0
        # return result
    def spell_case(self, root_level, second_vowel): #looks at "case"
        switch = self.wtype["case"]
        self.result += WHICH(
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
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
<<<<<<< HEAD
            r = self.root[root_level]
            if(root_level == 2):
                r = self.spell_passive(root_level)
            if(self.syllable_no_accent_count > 2):
                index = index_syllable(result, -2) #(beginning, vowel, end)
                i = index[1]
                result = result[:i] + accented[result[i]] + result[i+1:]
                self.syllable_no_accent_count = 1 if self.wtype["passive"] and not self.hist["passive"] else 0
            result += r + second_vowel #Jlt -> Jol[aoeu][[sa][ro]...](xe)t[euio]
            self.syllable_no_accent_count += 1
            if(self.syllable_no_accent_count > 1):
                result = result[:-1]+accented[result[-1]]
                self.syllable_no_accent_count = 0
        if(self.hist["passive"] and self.wtype["passive"] and "jx" in result):
            i = result.index("jx")
            result = result[:i]+"X"+result[i+2]
        return result
=======
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
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
    def spell_professional(self, flipped=False, accentable=False): #looks at "professional"
        result = WHICH(self.wtype["professional"],[
            (True, "ti"),
            (False, "fo"),
            (None, ""),
        ])
        if(self.wtype["professional"] != None):
            if(flipped):
                if(accentable):
                    result = result[:-1]+accented[result[-1]]
                    self.syllable_no_accent_count = 0
                result = list(result)
                result.reverse()
                result = "".join(result)
            self.syllable_no_accent_count += len(result)//2
<<<<<<< HEAD
        return result
    def spell_passive(self, root_level=None): #looks at "passive"
        if(self.wtype["passive"]):
            result = "x"
            if(not self.hist["passive"]):
                result += "e"
                self.syllable_no_accent_count += 1
        else:
            result = ""
        if(root_level != None):
            r = self.root[root_level]
            result += r #Jlt -> (Jalju)xet
        return result
=======
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
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b

# Es gibt (V1) –
#  (A-V1)
#   in (TA-V1) TA = Local_In_Metaphorical
#     diesen (A/R-NA-V1)
#    Bereichen (NA-V1) begrenzen_Prof_Metaphorical_Noun_TA
#  (O-V1)
#    verschiedene (A-NO-V1) unterscheiden_Prof_Met_Attr_possible
#   Wettbewerbe, (NO-V1) kämpfen_Met_Noun-O-V1
# und
#  (A-V2)
#   trotz (TA-V) TA = Causal_Near
#   der Relevanz (NA-V) bedenken_Prof_Passive_TA
#    des --wettbewerb (NA-NA-V) kämpfen_Met_Noun_-A
#     -Bundes- (NA-NA-NA-V) vereinigen_Pass_Perf_Local_In
#     Fremdsprachen (NA-NA-NA-V) sprechen_Noun_Action lernen_Attr_imperativ
#    (A-NA-V)
#     an (TA-NA-V)
#     der Schule (NA-NA-V) Lernen_Prof_Noun_Local_Near
#  nehmen (V2) (Teil) kämpfen_Met_Verb
#  Schüler (NO-V2) lernen_Noun_Actor_Activ
#  (A-V2)
#   an (TA-V2)
#   --wettbewerben (NA-V2) kämpfen_Met_Noun_
#    -Geographie- lernen_über_orte
#  Teil, (A-V2)
# es gibt (V3)
#    Mathematik- (NA-NO-V3)
#   und
#    Biologieolympiaden (NO-V3)
#  sowie
#  den Biberwettbewerb (NO-V3)
#   (A-NO-V3)
#    für (TA-NO-V3)
#    die Früherkennung (NA-NO-V3)
#     (A-NA-NO-V3)
#      informatischen (A-NA-NA-NO-V3)
#     Talents (NA-NA-NO-V3) können_Unprof_Noun
#  und
#   (O-V3)
#     schulische (A-NO-V3)
#    Veranstaltungen, (NO-V)
#    (A-NO-V)
#     in denen (TA-NO-V)
#     Schüler (NS-VA-TA-NO-V)
#      (A-VA-TA-NO-V)
#       außerhalb (TA-VA-TA-NO-V)
#       der Schule (NA-VA-TA-NO-V)
#     Fachwissen (NO-VA-TA-NO-V)
#      (A-VA-TA-NO-V)
#       durch (TA-VA-TA-NO-V)
#         praktische (A-NA-VA-TA-NO-V)
#        Erfahrung (NA-VA-TA-NO-V)
#     vertiefen. (VA-NO-V)
