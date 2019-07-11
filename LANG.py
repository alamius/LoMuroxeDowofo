from sys import argv
from Word import *
from wtype import *
from notation import *
from hist import *
from vocab import roots

def print_Word(word):
    word = word.spell()
    print(word)
    if("-p" in argv):
        print("phon: "+phoneticize(word))
def print_LANG(string):
    print(string)
    if("-p" in argv):
        print(phoneticize(string))
def demo_input_fragments():
    print("STEM: g·r")
    print("MEANS: GO, WALK, JOURNEY")
    print_Word(Word("gr",  get_wtype(infinitive, {"tense":"present"})))
    print_Word(Word("gr",  get_wtype(imperative, {"person":("plural-me", "you")})))
    print_Word(Word("gr",  get_wtype(indicative, {"tense":"present", "person":("plural-they")})))
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"action",   "case_class":"local",   "case":"near",  "professional":False, "passive":False})))
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"action",   "case_class":"temporal","case":"under", "professional":True,  "passive":True })))
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"actor",    "case_class":"causal",  "case":"above", "professional":False, "passive":False})))
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"actor",    "case_class":"causal",  "case":"before","professional":True,  "passive":True })))
def demo_input_presets():
    print("STEM: J·l·t")
    print("MEANS: HELP, ASSIST(ANCE)")
    print_Word(Word("Jlt", get_wtype(infinitive)))
    print_Word(Word("Jlt", get_wtype(imperative)))
    print_Word(Word("Jlt", get_wtype(indicative)))
    print_Word(Word("Jlt", get_wtype(noun)))
def demo_input_free():
    words = []
    word_strings = []
    word_list = list(roots.keys())
    for key in word_list:
        print(roots[key], "means", key)
    try:
        while True:
            tpl_class = get_new_value(["verb", "noun"])
            tpl = verb if tpl_class == "verb" else noun
            word = Word(roots[get_new_value(word_list)], get_wtype(tpl))
            print_Word(word)
            if(len(words) > 0):
                print("WHAT PLACE DOES THE NEW WORD TAKE IN YOUR SENTENCE RELATIVE TO WHAT OTHER WORD?")
                place = get_new_value(list(PLACE.keys())+["None"])
                if(place != "None"):
                    index = word_strings.index(get_new_value(word_strings))
                    words[index].add_child(word, place)
                    word_strings[index] = words[index].spell()
            words += [word]
            word_strings += [word.spell()]
            print_LANG(" ".join(word_strings))
    except KeyboardInterrupt:
        print("FINAL SENTENCE: "+" ".join(word_strings))
        for word in words:
            print_LANG(word.spell())
            print("w"+str(words.index(word))+" = {")
            for key in word.wtype.keys():
                print("\t\""+str(key)+"\": "+repr(word.wtype[key])+", ")
            print("}")
def demo_place():
    w1 = Word("gr", {
        'verb_class': 'imperative',
        'person': ['plural-you'],
        'class': 'verb'
    })
    w2 = Word("mPk", {
        'class': 'noun',
        'case_class': 'directional',
        'noun_class': 'actor',
        'passive': True,
        'professional': 'True',
        'case': 'near',
        'number': 'plural',
        'metaphore':True,
    })
    print("go_you_pl: ", end='')
    print_LANG(w1.spell())
    print("to the kindergardeners: ", end='')
    print_LANG(w2.spell())
    w1.add_child(w2)
    print_LANG(w1.spell(), w2.spell())
def demo_verb():
    t = {"class":"verb"}
    print("VERBS:")
    for t["passive"] in [False, True]:
        print("ACTIVE:" if not t["passive"] else "PASSIVE:")
        for t["verb_class"] in ["indicative"]:#, "imperative", "indicative"]:
            print(t["verb_class"].upper()+":")
            for t["professional"] in [None, True, False]:
                for t["tense"] in [None, "present", "past", "future"]:
                    print("tense: %-8s" % t["tense"], end="")
                    for t["person"] in [
                        ["me"],
                        ["you"],
                        ["you", "they"],
                        ["plural-they"],
                        ["undef"],
                        ["plural-me", "plural-you", "plural-they"]
                    ]:
                        print("%-18s" % Word("lmd", t).spell(), end="")
                    print()
                print()
            print()
        print()
def demo_noun():
    t = {"class":"noun"}
    t["number"] = "singular"
    print("NOUNS:")
    for t["passive"] in [False, True]:
        print("ACTIVE:" if not t["passive"] else "PASSIVE:")
        for t["noun_class"] in ["action", "actor"]:
            print("ACTOR:" if t["noun_class"] == "actor" else "ACTION:")
            for t["professional"] in [None, True, False]:
                for t["case_class"] in [None, "directional", "local", "temporal", "causal"]:
                    print("case_class: %-12s" % t["case_class"], end="")
                    for t["case"] in [None, "before", "after", "above", "under", "near", "parallel", "same", "opposite"]:
                        print("%-16s" % Word("lmd", t).spell(), end="")
                    print()
                print()
            print()
        print()
    exit(0)
def spell_sentence(sentence):
    word_strings = []
    for w in range(len(sentence)):
        word_strings += [sentence[w].spell()]
    for w in range(len(sentence)-1, -1, -1):
        word = sentence[w]
        if(
            w > 1 and
            sentence[w-1].wtype["child_place_string"] ==
            sentence[w  ].wtype["parent_place_string"] and
            sentence[w-1].children == [sentence[w]] and
            sentence[w-1] in sentence[w  ].parents
        ):
            word_strings = word_strings[:w-1] + [word_strings[w-1][:-2] + "-" + word_strings[w]] + word_strings[w+1:]
        elif(
            w > 1 and
            sentence[w-1].wtype["child_place_string"] ==
            sentence[w  ].wtype["parent_place_string"] and
            sentence[w  ] in sentence[w-1].children and
            sentence[w-1] in sentence[w  ].parents
        ):
            word_strings = word_strings[:w-1] + [word_strings[w-1] + "ne-" + word_strings[w][2:]] + word_strings[w+1:]
    return " ".join(word_strings)

marks = {
    "S":"subject",
    "O":"object",
    "A":"attribute",
    "C":"clause",
}

from examples import *
if __name__ == "__main__":
    W = []
    Markers = {}
    for w in range(len(E2)):
        W += [Word(None, E2[w])]
        Markers[W[-1].marker] = W[-1]
    for word in W:
        try:
            parent = word.marker[word.marker.index("-")+1:]
            Markers[parent].add_child(word, marks[word.marker[0]])
        except:
            pass
    print_LANG(spell_sentence(W))
    exit(0)
    # demo_input_free()
    # exit(0)
    # print_LANG(Word("lmd", get_wtype(noun)).spell())
    for w in range(len(E0)):
        word = E0[w]
        E0[w] = Word(word["root"], word)
    E0[0].add_child(E0[1], "subject")
    E0[1].add_child(E0[2], "attribute")
    E0[0].add_child(E0[4], "attribute")
    E0[0].add_child(E0[3], "attribute")
    E0[4].add_child(E0[5], "object")
    E0[4].add_child(E0[6], "object")
    E0[0].add_child(E0[7], "attribute")
    E0[8].add_child(E0[1], "subject")
    print_LANG(spell_sentence(E0))
#{'verb_class': 'imperative', 'person': ('plural-you'), 'class': 'verb'}
#{'class': 'noun', 'case_class': 'directional', 'noun_class': 'acted_on', 'professional': 'True', 'case': 'near'}
