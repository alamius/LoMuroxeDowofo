#!/usr/bin/python3
if __name__ == '__main__':
    from sys        import argv
    from Word       import *
    from sentence   import *
    from print      import *
    from demo       import *
from examples   import *

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
not_valid_message = "The argument %s will not be understood by the program... Use --help for a list of arguments!"

def input_interrupt():
    input("[ENTER] to continue")
def get_arg(arg, key):
    return arg[arg.index(key)+len(key):]
def get_file():
    while True:
        save_inp = input("To which file do you want to save the sentence: ")
        try:
            save_file = open(save_inp, "x")
            break
        except FileExistsError:
            overwrite = input("The file exists! Do you want to overwrite it (Y/n): ")
            if(overwrite == "Y"):
                save_file = open(save_inp, "a")
                break
    return save_file
def help(arg=""):
    helped = False
    if("=" in arg):
        if(get_arg(arg, "=") == "demo"):
            print(HELP["DEMO"])
            helped = True
    if(not helped):
        print(HELP["GENERAL"])
        helped = True

if __name__ == "__main__":
    sentence = []
    argv = argv[1:]
    #checking for ununderstandable arguments
    for arg in argv:
        valid = False
        valid = valid or (arg in ["--print", "-p", "--save", "-s", "--help", "-h", "-?", "-P", "--phonetic", "-R", "--roman"])
        for key in ["-e", "-E=", "-d", "--save=", "-?=", "--help=", "-h="]:
            valid = valid or arg.startswith(key)
        if(not valid):
            print(not_valid_message % arg)
            cont = input("Continue anyway (Y/n):")
            if(cont.upper() != "Y"):
                exit()
    #a list of spelling types used by print_ functions from print.py
    spell = ["standard"] #others: phonetic, roman, draw
    if(len(argv) == 0):
        help()
    for arg in argv:
        #other notations like a phonetic approximation or a stricter romanization
        if(arg == "--phonetic" or arg == "-P"):
            spell += ["phonetic"]
        if(arg == "--roman" or arg == "-R"):
            spell += ["roman"]
        #help
        if(
            arg.startswith("--help") or
            arg.startswith("-h") or
            arg.startswith("-?")
        ):
            help(arg)
        #TODO: rethink variable names
        #examples from examples.py
        if(arg.startswith("-e")):
            value = get_arg(arg, "-e")
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
            print_LANG(spell_sentence(sentence), spell)
        #examples from other files
        if(arg.startswith("-E=")):
            try:
                source = get_arg(arg, "=")
                exec(
                    "from %s import E as e" % source,
                    globals(),
                    locals()
                )
            except ImportError:
                raise ImportError("The input \"%s\" could not be used in the line \"from %s import E as e\". Remove the ending?" % (arg, source))
            sentence = prep_sentence(e)
            print_LANG(spell_sentence(sentence), spell)
        #demos of all sorts
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
        #printing the structure code of the Words
        if(arg == "--print" or arg == "-p"):
            if(sentence == []):
                print(no_active_sentence_message)
                continue
            output = "E = [" + ", ".join([word.export() for word in sentence]) + "]"
            print(output)
        #saving the code to a file
        if(arg == "--save" or arg == "-s" or arg.startswith("--save=")):
            if(sentence == []):
                print(no_active_sentence_message)
                continue
            if(arg in ["--save", "-s"]):
                save_file = get_file()
            else:
                file_name = get_arg(arg, "=")
                try:
                    save_file = open(file_name, "x")
                except FileExistsError:
                    overwrite = input("The file exists! Do you want to overwrite it (Y/n): ")
                    if(overwrite == "Y"):
                        save_file = open(file_name, "a")
                    else:
                        save_file = get_file()
            output = "E = [" + ", ".join([word.export() for word in sentence]) + "]\n"
            save_file.write(output)
            save_file.close()
