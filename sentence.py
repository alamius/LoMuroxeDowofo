from marks import *
from Word import *

def spell_sentence(sentence):
    word_strings = []
    for w in range(len(sentence)):
        word_strings += [sentence[w].spell()]
    for w in range(len(sentence)-1, -1, -1):
        word = sentence[w]
        if(
            w >= 1 and
            sentence[w-1].wtype["child_place_string"] ==
            sentence[w  ].wtype["parent_place_string"] and
            sentence[w-1].children == [sentence[w]] and
            sentence[w-1] in sentence[w  ].parents
        ):
            #the main verb loses its sentence structure endings and thus it has to be treated differently
            if(str(word_strings[w-1][-1]) == sentence[w-1].wtype["child_place_string"][0]):
                word_strings[w-1].pop()
            word_strings = word_strings[:w-1] + [word_strings[w-1] + NonSyllable("-") + word_strings[w]] + word_strings[w+1:]
        elif(
            w >= 1 and
            sentence[w-1].wtype["child_place_string"] ==
            sentence[w  ].wtype["parent_place_string"] and
            sentence[w  ] in sentence[w-1].children and
            sentence[w-1] in sentence[w  ].parents
        ):
            if(not word_strings[w-1][-2].accented):
                word_strings[w-1][-1].accented = True #the last syllable can be accented if the previous wasn't
            word_strings[w-1] += "ne"
            word_strings = word_strings[:w-1] + [word_strings[w-1] + NonSyllable("-") + word_strings[w][1:]] + word_strings[w+1:]
    return " ".join([str(Sstr) for Sstr in word_strings])
def prep_sentence(sentence):
    W = []
    Markers = {}
    for w in range(len(sentence)):
        #every non-list marker of type string gets his own one-element list
        if(type(sentence[w]["marker"]) == (type(""))):
            sentence[w]["marker"] = [sentence[w]["marker"]]
        W += [Word(None, sentence[w])]
        for m in W[-1].marker:
            Markers[m] = W[-1]
    for word in W:
        try:
            for marker in word.marker:
                parent = marker[marker.index("-")+1:] #marker "A-S-V2" -> parent "S-V2"
                Markers[parent].add_child(word, marks[marker[0]])
        except:
            pass
    return W
