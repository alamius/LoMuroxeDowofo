#!/usr/bin/env python3
from notation import vowels, consonants, semivowels, accented
from copy import deepcopy

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

class Syllable(object):
    """simple Syllable has initial, middle, ending; each strings without limits"""

    def __init__(self, arg, accented=False):
        super(Syllable, self).__init__()
        self.init = ""
        self.mid  = ""
        self.end  = ""
        if(isinstance(arg, list)):
            if(len(arg) > 0 and all([type(string) == str for string in arg])):
                if(len(arg) == 1):
                    self.mid = arg[0]
                elif(len(arg) == 2):
                    self.init = arg[0]
                    self.mid = arg[1]
                else:
                    self.init = arg[0]
                    self.mid = arg[1]
                    self.end = arg[2]
        elif(isinstance(arg, str)):
            if(len(arg) == 1):
                self.mid = arg[0]
            elif(len(arg) == 2):
                self.init = arg[0]
                self.mid = arg[1]
            else:
                self.init = arg[0]
                self.mid = arg[1]
                self.end = arg[2]
        self.accented = accented
    def __str__(self):
        return self.init+self.mid+self.end
    def __repr__(self):
        return "S'"+self.init+self.mid+self.end+"'"

class CVSyllable(Syllable):
    """has only one initial consonant and one vowel"""

    def __init__(self, arg, accented=False):
        if(isinstance(arg, (list, str))):
            super(CVSyllable, self).__init__(arg, accented)
        elif(isinstance(arg, Syllable)):
            # if(self.valid(arg)):
                super(CVSyllable, self).__init__([arg.init, arg.mid, arg.end], accented)
            # else:
            #     raise ValueError("The Syllable %s cannot be used to create a CV-Syllable." % self.__repr__())
        if(not self.valid()):
            raise ValueError("The CV-Syllable %s is not valid." % self.__repr__())
    def valid(self, arg=None):
        if(arg == None):
            arg = self
        if(len(arg.init) > 1):
            return False
        if(len(arg.mid) > 1):
            return False
        if(len(arg.end) > 0):
            return False
        return True

class SyllableString(list):
    """Contains several Syllables"""

    def __init__(self, arg=None, syll_class=Syllable):
        super(SyllableString, self).__init__()
        self.syll_class = syll_class
        if(isinstance(arg, (list, SyllableString))):
            if(all([isinstance(syll, (self.syll_class, str)) for syll in arg])):
                for syll in arg:
                    self.append(self.syll_class(syll))
        elif(isinstance(arg, (self.syll_class, str))):
            self.append(self.syll_class(arg))
    def valid(self):
        return all([
            syll.valid()
            for syll in self
        ])
    def __str__(self):
        return "".join([str(syll) for syll in self])
    def __repr__(self):
        return "Sstr'"+".".join([str(syll) for syll in self])+"'"
    def __iadd__(self, string):
        if(isinstance(string, SyllableString)):
            self.append(string)
        elif(isinstance(string, (Syllable, str, list))):
            self.append(SyllableString(string))
        return self
    def __add__(self, string):
        result = deepcopy(self)
        if(isinstance(string, SyllableString)):
            result.append(string)
        elif(isinstance(string, self.syll_class)):
            result.append(string)
        elif(isinstance(string, Syllable)):
            result.append(self.syll_class(string))
        elif(isinstance(string, (str, list))):
            result.append(SyllableString(string))
        return result

if __name__ == '__main__':
    a = SyllableString(["ta", "le"], CVSyllable)
    a += "Py"
    print(a)
    b = SyllableString("Fa", CVSyllable) + "ko" + Syllable("no")
    print(b)
