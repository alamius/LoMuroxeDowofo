from notation import romanize, phoneticize

def print_Word(word, sentence=[], spell=["standard"]):
    sentence += [word]
    word = word.spell()
    if("standard" in spell):
        print(word)
    if("phonetic" in spell):
        print("phon: "+phoneticize(word))
    if("roman" in spell):
        print("roman:"+romanize(word))
def print_LANG(string, spell=["standard"]):
    if("standard" in spell):
        print(string)
    if("phonetic" in spell):
        print("phon: "+phoneticize(string))
    if("roman" in spell):
        print("roman:"+romanize(string))
