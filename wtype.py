from copy import deepcopy

standards_word = {
    "passive":False,
    "metaphore":False,
    "professional":None,
    "perceived":False,
    # "metaphore":False,
    # "class":no std,
}
standards_verb = {
    # "verb_class":no std,
    "person":["undef"],
    "tense":"present",
}
standards_noun = {
    # "noun_class":no standard,
    "case_class":None,
    "case":None,
    "number":"singular",
}
standards_attribute = {
    # "attribute_class":no standard,
    "tense":"present",
    "negative":False,
}
#attribute_class examples:
    #stative active: reading
    #stative passive: read / being read -> tenses?
    #possible active: able to read
    #possible passive: readable = able to be read
    #conjunctive active: should read
    #conjunctive passive: should be read
    #obligate active: must read
    #obligate passive: must be read
person_choice = [[
    ["me", "plural-me", "p-me"],
    ["you", "plural-you", "p-you"],
    ["they", "plural-they", "p-they"],
    ["undef", "plural-undef", "p-undef"],
]]
shortcuts = {
    "p-me":"plural-me",
    "p-you":"plural-you",
    "p-they":"plural-they",
    "p-undef":"plural-undef",
}
basic = {
    "passive":["True", "False"],
    "professional":["True", "False", "None"],
    "metaphore":["True", "False"],
    "perceived":["True", "False"],
}
verb = {
    "class":"verb",
    "verb_class":["imperative", "infinitive", "indicative"],
    "tense":["present", "past", "future"],
    "person":person_choice,
}
verb.update(basic)
imperative = {
    "class":"verb",
    "verb_class":"imperative",
    "person":person_choice,
}
imperative.update(basic)
infinitive = {
    "class":"verb",
    "verb_class":"infinitive",
    "tense":["present", "past", "future"],
}
infinitive.update(basic)
indicative = {
    "class":"verb",
    "verb_class":"indicative",
    "tense":["present", "past", "future"],
    "person":person_choice,
}
indicative.update(basic)
noun = {
    "class":"noun",
    "noun_class":["action", "actor", "object"],
    "case_class":["None", "directional", "local", "temporal", "causal"],
    "case":["None", "before", "after", "above", "under", "near", "parallel", "same", "opposite"],
    #TODO: decide if useful:
    # "scale":["nothing", "tiny", "little", "normal", "large", "huge", "unmeasurable"],
    #about: 0, 0.1, 0.5, 1, 5, 10, oo
    "number":["singular", "plural"],
}
noun.update(basic)
#meanings of the cases in the case_classes:
    #directional:
        #before:     forewards, to the front
        #after:      backwards, to the back
        #above:      above, upwards
        #under:      underneeth, downwards
        #near:       towards
        #parallel:   parallel, but not starting on the same spot
        #same:       together
        #opposite:   opposite direction
    #local:
        #before:     in front
        #after:      behind
        #above:      over
        #under:      under
        #near:       near
        #parallel:   to the side of something
        #same:       here, in
        #opposite:   opposing
    #temporal:
        #before:     before
        #after:      after
        #above:      at a larger time-scale, a larger context, regularly
        #under:      at a smaller time-scale, a smaller context
        #near:       beginning of an interval
        #parallel:   during an interval
        #same:       at one point in time
        #opposite:   end of an interval
    #causal:
        #before:     because of, reason
        #after:      therefore, consequence
        #above:      at a larger scale of reasoning, planning ahead
        #under:      at a smaller scale of reasoning, detail
        #near:       somehow related to the argument
        #parallel:   comparison, the same in another area, metaphore
        #same:       this is completely equivalent
        #opposite:   against
# action = {
#     "class":"noun",
#     "noun_class":"action",
#     "case_class":["directional", "local", "temporal", "causal"],
#     #abbrev.: dir, loc, tmp, cau
#     "case":["before", "after", "above", "under", "near", "parallel", "same", "opposite"],
#     #abbrev.: ←, →, ↑, ↓, o, =, ., O
# }
# actor = {
#     "class":"noun",
#     "noun_class":"actor",
#     "case_class":["directional", "local", "temporal", "causal"],
#     #abbrev.: dir, loc, tmp, cau
#     "case":["before", "after", "above", "under", "near", "parallel", "same", "opposite"],
#     #abbrev.: ←, →, ↑, ↓, o, =, ., O
# }
attribute = {
    "class":"attribute",
    "attribute_class":["stative", "possible", "conjunctive", "obligate"],
    "tense":["present", "past", "future"],
}
attribute.update(basic)

def get_inp(choices):
    out = "\t POSSIBLE VALUES: "
    # out += "\tWRITE THE FIRST FEW DEFINING LETTERS OF YOUR CHOICE\n\tFROM THE POSSIBLE VALUES: "
    if(len(choices) > 0 and type(choices[0]) == type([])):
        choices = [
            ' OR '.join(ch)
            for ch in choices
        ]
    out += ", ".join(choices)+": \n\t"
    inp = input(out).split(',')
    return list(map(lambda S : S.strip(' '), inp))
def get_startswith_from_array(array, start):
    result = []
    i = 0
    while(i < len(array)):
        if(type(array[i]) == type("") and array[i].startswith(start)):
            result += [array[i]]
        elif(type(array[i]) == type([])):
            #subarrays mean that the multiple choice lets only choose one from each subarray
            subresult = get_startswith_from_array(array[i], start)
            if(subresult != -1):
                result += [subresult]
                array.pop(i)
                i -= 1
        i += 1
    if(len(result) == 1):
        result = result[0]
        if(result in shortcuts.keys()):
            result = shortcuts[result]
        return result
    else:
        return -1
def get_new_value(choices, multiple_choice=False):
    choices = deepcopy(choices)
    result = []
    #inp holds all user input as an array, because the user can input several input statements in one line
    inp = get_inp(choices)
    counter = 0
    while(
        multiple_choice and not "X" in inp[0]
        or not multiple_choice and result == []
    ):
        get_startswith = get_startswith_from_array(choices, inp[0])
        while(
            #not exactly one match == get_startswith_from_array returns -1
            get_startswith == -1
            #not the stop character for multiple choice -> used to force an exit
            and not "X" in inp[0]
        ):
            #delete the first entry and get new inp if needed
            inp.pop(0)
            if(len(inp) == 0): inp = get_inp(choices)
            get_startswith = get_startswith_from_array(choices, inp[0])
            counter += 1
            if(counter % 5 == 0):
                print(
                    "\n\tDO YOU NEED AN EXAMPLE?"+
                    "\n\tEXAMPLE: TO CHOOSE 'present' FROM 'present, past, future',"+
                    "\n\tTYPE AT LEAST 'pr'. 'p' IS NOT ENOUGH AND"+
                    "\n\t'prs' OR 'sent' DON'T WORK. (do not type the quotes)"
                )
        if("X" in inp[0]):
            break
        result += [get_startswith]
        inp.pop(0)
        if(len(inp) == 0 and multiple_choice): inp = get_inp(choices)
    if(not multiple_choice):
        try:
            result = result[0]
        except:
            return -1
    return result
def get_wtype(template, set={}):
    # returning a wtype dict to be fed into a Word object using the set values in set and user input
    result = deepcopy(template)
    for key in result.keys():
        if(key in set.keys()):
            # print("tmp.key: ", key, ", set.keys: ", set.keys(), ", matches: ", key in set.keys(), sep="")
            result[key] = set[key]
    for key, value in zip(result.keys(), result.values()):
        if(type(value) != type([])): # value == <arr> = to be chosen from the user (user input filtered to fit <arr>)
            print("\t"+key+" = "+str(value))
    for key, value in zip(result.keys(), result.values()):
        if(type(value) == type([])): # value == <arr> = to be chosen from the user (user input filtered to fit <arr>)
            #value holds choice possibilities or an array of the choice possibilities
            print("\tATTRIBUTE:", key)
            multiple_choice = False
            if(type(value[0]) == type([])): #value == [<arr>] = multiple choice out of <arr>
                print("\tYOU CAN CHOOSE MULTIPLE VALUES! PUT THEM IN ONE LINE AND SEPARATE BY ',' \n\tOR USE SEVERAL LINES. TO STOP ADDING, PUT 'X' IN YOUR INPUT.")
                value = value[0]
                #value holds choice possibilities
                multiple_choice = True
            result[key] = get_new_value(value, multiple_choice)
            print("\tVALUE:", result[key])
    return result
def check_wtype_complete(template, default):
    for key, value in zip(template.keys(), template.values()):
        if(type(value) == type([])):
            if(not(key in default.keys())):
                return False
    return True
def make_wtype(template, default, set={}):
    # returning a wtype dict to be fed into a Word object using the set values in set and user input
    result = deepcopy(template)
    for key in result.keys():
        if(key in set.keys()):
            result[key] = set[key]
    while(True):
        set = {}
        unset = {}
        for key, value in zip(result.keys(), result.values()):
            if(
                type(value) == type([]) and (
                    not key in default.keys() or not (
                        type(default[key]) == type([]) and
                        not type(value[0]) == type([])
                    )
                )
            ):
                unset.update({key: value})
            else:
                set.update({key: value})
        system("clear")
        print("These are set already:")
        for key, value in zip(set.keys(), set.values()):
            print("\t", key, ":", " "*(13-len(key)), str(value), sep='')
        print("These are not set, but some have a default, that you can keep:")
        for key, value in zip(unset.keys(), unset.values()):
            if(key in default.keys()):
                print("\t", key, ",", " "*(13-len(key)), "default:", str(default[key]), sep='')
            else:
                print("\t", key, ";", sep='')
        if(len(unset) == 0):
            print("There is nothing to set for you. ")
            break
        if(check_wtype_complete(result, default)):
            if(input("You are ready, do you want to continue? (Y/n): ").upper() != "Y"):
                break
        print("Choose an attribute to set: ")
        key = get_new_value(list(unset.keys()))
        print("Choose a value for that attribute: ")
        multiple_choice = False
        if(type(unset[key][0]) == type([])): #value == [<arr>] = multiple choice out of <arr>
            print("\tYOU CAN CHOOSE MULTIPLE VALUES! PUT THEM IN ONE LINE AND SEPARATE BY ',' \n\tOR USE SEVERAL LINES. TO STOP ADDING, PUT 'X' IN YOUR INPUT.")
            value = value[0]
            #value holds choice possibilities
            multiple_choice = True
        value = get_new_value(unset[key], multiple_choice)
        result[key] = value
    for key in result.keys():
        if(key in default.keys() and type(default[key]) == type([])):
            #the option is multiple choice => array by standard.
            if(len(result[key]) == 0 or type(result[key][0]) == type([])):
                result[key] = default[key]
        elif(type(result[key]) == type([])):
            result[key] = default[key]
    return result
