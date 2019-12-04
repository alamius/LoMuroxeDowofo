from notation import vowels, consonants, semivowels, accented

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
