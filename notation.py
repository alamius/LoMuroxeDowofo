consonants = "bdfghklmnpqrstvwxzJXDCLNGKRP'" #w is semivowel
vowels = "aeiouy" #accented are added after they are defined
semivowels="j" #w?

accented = {
    "a":"á",
    "e":"é",
    "i":"í",
    "o":"ó",
    "u":"ú",
    "y":"ý",
}
for c in vowels:
    try:
        vowels += accented[c]
    except KeyError:
        pass

ROMAN = {
    "J":"jh",
    "X":"sh",
    "D":"dh",
    "K":"kh", #weird trill using a lot of pressure on the soft palate, appriximate by χ
    "G":"gh", #can you voice K?
    "C":"ch",
    "L":"lh",
    "R":"rh", #german, franch r
    "N":"nh", #roman: ng
    "P":"ph",
}
PHON = {
    "J":"ʒ",
    "'":"ʔ",
    "x":"χ",
    "X":"ʃ",
    "C":"ç",
    "D":"ð",
    "K":"Я", #voiced/voiceless? pressurized uvular trill
    # "G":"vЯ", #voiced pressurized uvular trill
    "L":"ɬ", #ɮ
    "R":"ʁ",
    "N":"ŋ",
    "P":"r°"
}

def romanize(word):
    for i in range(len(word)):
        c = word[i]
        if(c in ROMAN.keys()):
            word = word[:i]+ROMAN[c]+word[i+1:]
        #trying to detect capitals but not non-letters
        elif(c == c.upper() and not c == c.lower()):
            word = word[:i-1]+c.lower()+'h'+word[i:]
    return word

def phoneticize(word):
    for i in range(len(word)):
        c = word[i]
        if(c in PHON.keys()):
            word = word[:i]+PHON[c]+word[i+1:]
    return word
