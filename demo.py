from vocab import roots
from wtype import *
from Word import *
from print import *
from sentence import *

def demo_input_fragments():
    sentence = []
    print("STEM: g·r")
    print("MEANS: GO, WALK, JOURNEY")
    # print_Word(Word("gr",  get_wtype(infinitive, {"tense":"present"})), sentence)
    print_Word(Word("gr",  get_wtype(imperative, {"person":("plural-me", "you")})), sentence)
    print_Word(Word("gr",  get_wtype(indicative, {"tense":"present", "person":("plural-they")})), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"action",   "case_class":"local",   "case":"near",  "professional":False, "negative":False})), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"action",   "case_class":"temporal","case":"under", "professional":True,  "negative":True })), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"agent",    "case_class":"causal",  "case":"above", "professional":False, "negative":False})), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"agent",    "case_class":"causal",  "case":"before","professional":True,  "negative":True })), sentence)
    return sentence
def demo_input_presets():
    sentence = []
    print("STEM: J·l·t")
    print("MEANS: HELP, ASSIST(ANCE)")
    # print_Word(Word("Jlt", get_wtype(infinitive)), sentence)
    print_Word(Word("Jlt", get_wtype(imperative)), sentence)
    print_Word(Word("Jlt", get_wtype(indicative)), sentence)
    print_Word(Word("Jlt", get_wtype(noun)), sentence)
    return sentence
def demo_input_free():
    words = []
    word_strings = []
    word_list = list(roots.keys())
    for key in word_list:
        print(roots[key], "means", key)
    try:
        while True:
            tpl_class = get_new_value(["verb", "noun", "attribute"])
            tpl = {
                "verb":verb,
                "noun":noun,
                "attribute":attribute,
            }[tpl_class]
            tpl_default = {
                "verb":standards_verb,
                "noun":standards_noun,
                "attribute":standards_attribute,
            }[tpl_class]
            tpl_default.update(standards_word)
            word = Word(roots[get_new_value(word_list)], make_wtype(tpl, tpl_default))
            print_Word(word)
            while(len(words) > 0):
                #by standard, word is the child in this new relationship
                print("WHAT PLACE DOES THE NEW WORD TAKE IN YOUR SENTENCE RELATIVE TO WHAT OTHER WORD?\n (write '-' before the place to \n reverse the parent-child relation: a verb adds itself a '-subject'; \n add '+' at the beginning to get another place input)")
                valid_places = []
                for key in PLACE.keys():
                    valid_places += [key, "+"+key, "-"+key, "+-"+key]
                valid_places += ["None"]
                place = get_new_value(valid_places)
                if(place != "None"):
                    #choosing the parent
                    index = word_strings.index(get_new_value(word_strings))
                    if("-" in place[:2]):
                        #parent and child are reversed
                        word.add_child(words[index], place.strip("+-"))
                    else:
                        words[index].add_child(word, place.strip("+-"))
                    word_strings[index] = words[index].spell()
                if(not "+" in place):
                    break
            words += [word]
            word_strings += [word.spell()]
            print_LANG(spell_sentence(words))
    except KeyboardInterrupt:
        print()
        return words
def demo_place():
    w1 = Word("gr", {
        'verb_class': 'imperative',
        'person': ['plural-you'],
        'class': 'verb'
    })
    w2 = Word("mPk", {
        'class': 'noun',
        'case_class': 'directional',
        'noun_class': 'agent',
        'negative': True,
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
    return []
def demo_verb():
    t = {"class":"verb"}
    print("VERBS:")
    for t["negative"] in [False, True]:
        print("ACTIVE:" if not t["negative"] else "negative:")
        for t["verb_class"] in ["indicative"]:#, "imperative", "indicative"]:
            print(t["verb_class"].upper()+":")
            for t["professional"] in [None, True, False]:
                for t["tense"] in verb["tense"]+[None]:
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
    return []
def demo_noun():
    t = {"class":"noun"}
    t["number"] = "singular"
    print("NOUNS:")
    for t["negative"] in [False, True]:
        print("ACTIVE:" if not t["negative"] else "negative:")
        for t["noun_class"] in noun["noun_class"]:
            print(t["noun_class"].upper()+":")
            for t["professional"] in [None, True, False]:
                for t["case_class"] in noun["case_class"]:
                    print("case_class: %-12s" % t["case_class"], end="")
                    for t["case"] in noun["case"]:
                        print("%-16s" % Word("lmd", t).spell(), end="")
                    print()
                print()
            print()
        print()
    return []
