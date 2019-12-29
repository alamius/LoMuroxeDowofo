from marks import *
from Word import *

def spell_sentence(sentence):
    word_strings = []
    for w in range(len(sentence)):
        word_strings += [str(sentence[w].spell())]
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
            if(word_strings[w-1][-2:] == sentence[w-1].wtype["child_place_string"][0]):
                first_word = word_strings[w-1][:-2]
            else:
                first_word = word_strings[w-1]
            word_strings = word_strings[:w-1] + [first_word + "-" + word_strings[w]] + word_strings[w+1:]
        elif(
            w >= 1 and
            sentence[w-1].wtype["child_place_string"] ==
            sentence[w  ].wtype["parent_place_string"] and
            sentence[w  ] in sentence[w-1].children and
            sentence[w-1] in sentence[w  ].parents
        ):
            word_strings = word_strings[:w-1] + [word_strings[w-1] + "ne-" + word_strings[w][2:]] + word_strings[w+1:]
    return " ".join(word_strings)
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
