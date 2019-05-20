<<<<<<< HEAD
consonants = "bdfghklmnopqrstvwxzJXDCLNGKRP'"
=======
<<<<<<< HEAD
consonants = "bdfghklmnoprstvwxzJXQDCLNGK"
=======
consonants = "bdfghklmnopqrstvwxzJXDCLNGKRP'"
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
>>>>>>> master
vowels = "aeiouäöyêô" #accented are added after they are defined
semivowels="j"

accented = {
    "a":"á",
    "e":"é",
    "i":"í",
    "o":"ó",
    "u":"ú",
    "ä":"Ä",
    "ö":"Ö",
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
<<<<<<< HEAD
    # "Q":"qh",
=======
<<<<<<< HEAD
    "Q":"qh",
=======
    # "Q":"qh",
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
>>>>>>> master
    "D":"dh",
    "K":"kh", #weird trill using a lot of pressure on the soft palate, appriximate by χ
    "G":"gh", #can you voice K?
    "ä":"ae",
    "ö":"oe",
    "ê":"e", #short, open
    "ô":"o", #short, open
    "C":"ch",
    "L":"lh",
    "R":"rh", #german, franch r
<<<<<<< HEAD
    "N":"nh", #roman: ng
    "P":"ph",
=======
<<<<<<< HEAD
    "N":"ng", #roman: ng
=======
    "N":"nh", #roman: ng
    "P":"ph",
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
>>>>>>> master
}
PHON = {
    "J":"ʒ",
    "'":"ʔ",
    "x":"χ",
    "X":"ʃ",
    "C":"ç",
<<<<<<< HEAD
=======
<<<<<<< HEAD
    "Q":"q",
    "D":"ð",
    "K":"Я", #voiceless pressurized uvular trill
    "G":"vЯ", #voiced pressurized uvular trill
=======
>>>>>>> master
    # "q":"q",
    "D":"ð",
    "K":"Я", #voiced/voiceless? pressurized uvular trill
    # "G":"vЯ", #voiced pressurized uvular trill
<<<<<<< HEAD
=======
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
>>>>>>> master
    "ä":"æ",
    "ö":"ø",
    "ô":"ɔ",
    "ê":"ɛ",
    "L":"ɮ",
    "R":"ʁ",
    "N":"ŋ",
<<<<<<< HEAD
    "P":"r°"
=======
<<<<<<< HEAD
=======
    "P":"r°"
>>>>>>> c4d973dd4e065f5a2c5a61891be8a5a01800cb4b
>>>>>>> master
}

def romanization(word):
    for i in range(len(word)):
        c = word[i]
        if(c in ROMAN.keys()):
            word = word[:i]+ROMAN[c]+word[i+1:]
        elif(c == c.upper()):
            word = word[:i-1]+c.lower()+'h'+word[i:]
    return word

def phoneticize(word):
    for i in range(len(word)):
        c = word[i]
        if(c in PHON.keys()):
            word = word[:i]+PHON[c]+word[i+1:]
    return word
