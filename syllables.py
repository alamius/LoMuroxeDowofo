#!/usr/bin/env python3
from notation import vowels, consonants, semivowels, accented
from copy import deepcopy


class CheckSyllable(object):
    """takes a structure (allowed symbols for initial, mid, end; lengths of these parts) and can check a Syllable against it."""
    def __init__(self, allowed=[consonants+semivowels, vowels, consonants+semivowels], lengths=[10, 10, 10]):
        super(CheckSyllable, self).__init__()
        self.init = allowed[0]
        self.mid  = allowed[1]
        self.end  = allowed[2]
        self.lengths = lengths
    def check(self, syll):
        if(len(syll.init) > self.lengths[0]):     return False
        if(len(syll.mid) > self.lengths[1]):      return False
        if(len(syll.end) > self.lengths[2]):      return False
        for c in syll.init:
            if(not c in self.init):               return False
        for c in syll.mid:
            if(not c in self.mid):                return False
        for c in syll.end:
            if(not c in self.end):                return False
        return True
class Syllable(object):
    """a basic Syllable has init, mid, end"""
    def __init__(self, arg, accented=False, check=CheckSyllable()):
        super(Syllable, self).__init__()
        self.accented = accented
        self.init = ""
        self.mid  = ""
        self.end  = ""
        self.check = lambda: check.check(self)
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
            i = 0
            current = 0
            while i < len(arg):
                if(current == 0):
                    if(arg[i] in check.init):
                        self.init += arg[i]
                        i += 1
                    else:
                        current += 1
                if(current == 1):
                    if(arg[i] in check.mid):
                        self.mid += arg[i]
                        i += 1
                    else:
                        current += 1
                if(current == 2):
                    if(arg[i] in check.end):
                        self.end += arg[i]
                        i += 1
                    else:
                        raise ValueError("The arg %s cannot be used to construct a valid Syllable." % repr(arg))
        elif(isinstance(arg, Syllable)):
            self.init = arg.init
            self.mid = arg.mid
            self.end = arg.end
            self.accented = arg.accented
        if(not self.check()):
            raise ValueError("The Syllable %s is not valid." % self.__repr__())
    def __str__(self):
        a, b, c = self.init, self.mid, self.end
        if(self.accented):
            b = accented[b[0]] + b[1:]
        return a + b + c
    def __repr__(self):
        return "S'"+str(self)+"'"
    def __len__(self):
        return len(self.init)+len(self.mid)+len(self.end)
    def __eq__(self, syll):
        if(isinstance(syll, str)):
            syll = Syllable(syll)
        result = True
        result = result and (self.init == syll.init)
        result = result and (self.mid  == syll.mid)
        result = result and (self.end  == syll.end)
        return result
class CVSyllable(Syllable):
    """has only one initial consonant and one vowel"""
    def __init__(self, arg, accented=False):
        if(isinstance(arg, (list, str))):
            super(CVSyllable, self).__init__(arg, accented, check=CheckSyllable([consonants, vowels, semivowels], [1, 1, 1]))
        elif(isinstance(arg, Syllable)):
            # if(self.valid(arg)):
                super(CVSyllable, self).__init__([arg.init, arg.mid, arg.end], arg.accented)
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
class NonSyllable(str):
    """holds any characters so they can be integrated into a SyllableString"""
    def __init__(self, string=""):
        super(NonSyllable, self).__init__()
    def valid(self):
        return True
    def __repr__(self):
        return "nS'%s'" % self

class SyllableString(list):
    """Contains several Syllables"""
    def __init__(self, arg=None, syll_class=Syllable):
        super(SyllableString, self).__init__()
        self.syll_class = syll_class
        if(isinstance(arg, (list, SyllableString))):
            if(all([isinstance(syll, (self.syll_class, str)) for syll in arg])):
                for syll in arg:
                    if(isinstance(syll, NonSyllable)):
                        self.append(syll)
                    else:
                        self.append(self.syll_class(syll))
        elif(isinstance(arg, NonSyllable)):
            self.append(arg)
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
        if(len(string) == 0):
            return self
        if(isinstance(string, SyllableString)):
            self.extend(string)
        elif(isinstance(string, self.syll_class)):
            self.append(string)
        elif(isinstance(string, Syllable)):
            self.append(self.syll_class(string))
        elif(isinstance(string, NonSyllable)):
            self.append(string)
        elif(isinstance(string, (str, list))):
            self.extend(SyllableString(string))
        return self
    def __add__(self, string):
        result = deepcopy(self)
        if(len(string) == 0):
            return result
        result.__iadd__(string)
        return result

if __name__ == '__main__':
    a = SyllableString(["ta", "le"], CVSyllable)
    a += "Py"
    print(a)
    b = SyllableString("Fa", CVSyllable) + "ko" + Syllable("no")
    print(b)
