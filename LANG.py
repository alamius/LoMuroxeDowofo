#!/usr/bin/python3
if __name__ == '__main__':
    from sys import argv
    from Word import *
    from wtype import *
    from notation import *
    from hist import *
    from vocab import roots
from examples import *

HELP = {
    "DEMO":"Help for demo options: <this command> -d<specifier> \nThese are the demo options: \n -dif for input_framgents, \n -dip for input_presets, \n -df for input_free; \n -dp for place, \n -dv for verb, \n -dn for noun",
    "GENERAL":
"""General help for this command: <this command> [options]
Options:
 -d, -?=demo    demo help / options
 -d<demo>       runs a (possibly interactive) demo function. Some force you to press ctrl+C.
 -e<int>        load the built-in example number <int> (existent: 0.."""+str(len(E)-1)+""")
 -E=<file>      import an example called E from a .py file whose name is <file>,
                (pseudo-python: 'from <file[:-3]> import E' must be valid)
 -?, --help     prints this
 -p, --print    prints the text format of the current sentence to output
 -s, --save     saves a file containing text format of the current sentence
 -P, --phonetic prints the (rough) IPA along the normal output
 -R, --roman    prints the romanization along the normal output

Notes:
 On order:
  The order of the options is directly reflected in the order of execution.
  The currently active sentence changes with some demos and all examples.
  When <this command> -df -e0 -p is executed, the input from the demo is lost
  and only the example 0 is printed.
"""
}
no_active_sentence_message = "There is no active sentence to be printed. The program has to create or load on first."

marks = {
    "S":"subject",
    "O":"object",
    "A":"attribute",
    "C":"clause",
}
marks_reverse = {
    "subject":"S",
    "object":"O",
    "attribute":"A",
    "clause":"C",
}

def print_Word(word, sentence=[]):
    sentence += [word]
    word = word.spell()
    print(word)
    if("--phonetic" in argv or "-P" in argv):
        print("phon: "+phoneticize(word))
    if("--roman" in argv or "-R" in argv):
        print("roman:"+romanize(word))
def print_LANG(string):
    print(string)
    if("-p" in argv):
        print(phoneticize(string))
def demo_input_fragments():
    sentence = []
    print("STEM: g·r")
    print("MEANS: GO, WALK, JOURNEY")
    # print_Word(Word("gr",  get_wtype(infinitive, {"tense":"present"})), sentence)
    print_Word(Word("gr",  get_wtype(imperative, {"person":("plural-me", "you")})), sentence)
    print_Word(Word("gr",  get_wtype(indicative, {"tense":"present", "person":("plural-they")})), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"action",   "case_class":"local",   "case":"near",  "professional":False, "passive":False})), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"action",   "case_class":"temporal","case":"under", "professional":True,  "passive":True })), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"agent",    "case_class":"causal",  "case":"above", "professional":False, "passive":False})), sentence)
    print_Word(Word("gr",  get_wtype(noun, {"noun_class":"agent",    "case_class":"causal",  "case":"before","professional":True,  "passive":True })), sentence)
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
    return []
def demo_verb():
    t = {"class":"verb"}
    print("VERBS:")
    for t["passive"] in [False, True]:
        print("ACTIVE:" if not t["passive"] else "PASSIVE:")
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
    for t["passive"] in [False, True]:
        print("ACTIVE:" if not t["passive"] else "PASSIVE:")
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

def input_interrupt():
    input("[ENTER] to continue")

if __name__ == "__main__":
    sentence = []
    for arg in argv:
        if(
            len(argv) == 1 or
            arg.startswith("--help") or
            arg.startswith("-?")
        ):
            helped = False
            if("=" in arg):
                if(arg[arg.index("=")+1:] == "demo"):
                    print(HELP["DEMO"])
                    helped = True
            if(not helped):
                print(HELP["GENERAL"])
                helped = True
        #TODO: rethink variable names
        if(arg.startswith("-e")):
            value = arg[arg.index("-e")+2:]
            try:
                int(value)
            except ValueError:
                raise ValueError("The -e option must be directly followed by an integer, that is recognized as such by the interpreter. -e0 should always work.")
                continue
            value = int(value)
            try:
                E[value]
            except IndexError:
                raise ValueError("The -e option must be directly followed by an integer, that is not negative and less than "+str(len(E))+". -e0 should always work if the examples file is intact.")
                continue
            sentence = prep_sentence(E[value])
            print_LANG(spell_sentence(sentence))
        if(arg.startswith("-E=")):
            exec(
                "from "+arg[arg.index("-E=")+3:-3]+" import E as e",
                globals(),
                locals()
            )
            sentence = prep_sentence(e)
            print_LANG(spell_sentence(sentence))
        if(arg == "-d"):
            print(HELP["DEMO"])
        elif(arg.startswith("-d")):
            demo_func = None
            try:
                demo_func = {
                    "-dif":demo_input_fragments,
                    "-dip":demo_input_presets,
                    "-df": demo_input_free,
                    "-dp": demo_place,
                    "-dv": demo_verb,
                    "-dn": demo_noun,
                }[arg]
            except:
                print("your demo request was not undestood, please use -d to see the options")
            if(demo_func):
                sentence = demo_func()
        if(arg == "--print" or arg == "-p"):
            if(sentence == []):
                print(no_active_sentence_message)
                continue
            output = "E = [" + ", ".join([word.export() for word in sentence]) + "]"
            print(output)
        if(arg == "--save" or arg == "-s"):
            if(sentence == []):
                print(no_active_sentence_message)
                continue
            while True:
                save_inp = input("To which file do you want to save the sentence: ")
                try:
                    save_file = open(save_inp, "x")
                    break
                except FileExistsError:
                    save_file = open(save_inp, "a")
                    break
            output = "E = [" + ", ".join([word.export() for word in sentence]) + "]\n"
            save_file.write(output)
            save_file.close()
