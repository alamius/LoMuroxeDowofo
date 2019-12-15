#!/usr/bin/env python3
from tkinter import *
from time import sleep

# from run import *
from Word       import *
from sentence   import *
from print      import *
# from demo       import *

word = Word("Jlt", {
    "marker":"V",
    "parent_place": [],
    "child_place_string": [],
    "verb_class": 'imperative',
    "parent_place_string": [],
    "class": 'verb',
    "root": 'grk',
    "metaphore": False,
    "passive": False,
    "person": ['me'],
    "professional": True,
    "child_place": [],
    "perceived": False,
    "tense": 'future',
})

root = 101
tri = 111 #options: False, None, True
wtype_types = {
    "marker": None,
    "parent_place": None,
    "child_place_string": None,
    "verb_class": str,
    "parent_place_string": None,
    "class": str,
    "root": root,
    "metaphore": bool,
    "passive": bool,
    "person": str,
    "professional": tri,
    "child_place": None,
    "perceived": bool,
    "tense": str,
}
wtype_options = {
    "marker": [],
    "parent_place": [],
    "child_place_string": [],
    "verb_class": ["indicative", "imperative"],
    "parent_place_string": [],
    "class": ["verb"],
    "root": list(roots.values()),
    "metaphore": [True, False],
    "passive": [True, False],
    "person": ["me", "you"],
    "professional": ["False", "None", "True"],
    "child_place": [],
    "perceived": [True, False],
    "tense": ["past", "present", "future"],
}
def options(key, wtype):
    return wtype_options[key]

class App(Frame):
    def __init__(self, master, word=word):
        super().__init__(master)
        # self.master = master
        self.word = word
        self.wtype = {}
        for key in self.word.wtype.keys():
            if(wtype_types[key] == bool):
                self.wtype[key] = BooleanVar()
            elif(wtype_types[key] == int):
                self.wtype[key] = IntVar()
            elif(wtype_types[key] == str):
                self.wtype[key] = StringVar()
            elif(wtype_types[key] == root):
                self.wtype[key] = StringVar()
            elif(wtype_types[key] == tri):
                self.wtype[key] = IntVar()
            if(not wtype_types[key] == None and not wtype_types[key] == root):
                self.wtype[key].set(self.word.wtype[key])
        self.buttons = {}
        for key in self.wtype.keys():
            if(wtype_types[key] == bool):
                self.buttons[key] = Checkbutton(
                    self, text=key,
                    variable=self.wtype[key],
                    command=self.update
                )
            elif(wtype_types[key] == root):
                self.roots = list(options(key, self.word.wtype))
                self.buttons[key] = OptionMenu(
                    self,
                    self.wtype[key],
                    *self.roots,
                    command=self.update_2arg
                )

                # on change dropdown value
                def change_dropdown(*args):
                    self.word.root = self.wtype["root"].get()
                    if(len(self.word.root) < 3):
                        self.word.root += "k"
                    print(self.word.root)

                # link function to change dropdown
                self.wtype[key].trace('w', change_dropdown)
                self.buttons[key].pack()
                # self.buttons[key+"_scroll"].config(command=self.buttons[key].yview)
            elif(wtype_types[key] == tri):
                self.buttons[key+"_frame"] = Frame(self, bd=1)
                self.buttons[key] = []
                for string in list(options(key, self.word.wtype)):
                    value = {
                        "True":+1,
                        "None":0,
                        "False":-1,
                    }[string]
                    self.buttons[key] += [
                        Radiobutton(
                            self.buttons[key+"_frame"],
                            text=string,
                            state="active" if (self.wtype[key].get() == value) else "normal",
                            value=value,
                            variable=self.wtype[key],
                            command=self.update
                        )
                    ]
                for button in self.buttons[key]:
                    button.pack(side=RIGHT)
                self.buttons[key+"_frame"].pack()
            else:
                self.buttons[key+"_frame"] = Frame(self, bd=1)
                self.buttons[key] = [
                    Radiobutton(
                        self.buttons[key+"_frame"],
                        text=str(number),
                        state="active" if (self.wtype[key].get() == number) else "normal",
                        value=number,
                        variable=self.wtype[key],
                        command=self.update
                    )
                    for number in list(options(key, self.word.wtype))
                ]
                for button in self.buttons[key]:
                    button.pack(side=RIGHT)
                self.buttons[key+"_frame"].pack()
        self.displ = Button(
            self,
            text=self.word.spell(),
            bg="green",
            command=self.update
        )
        self.displ.pack(side=TOP)

        self.pack()
    def update_2arg(self, xxx):
        self.update()
    def update(self):
        for key in self.wtype.keys():
            #decoding input for tri-option values
            if(wtype_types[key] == tri):
                try:
                    value = self.wtype[key].get()
                    self.word.wtype[key] = {
                        +1:True,
                        0:None,
                        -1:False,
                    }[value]
                except KeyError:
                    if(value == True or value == None or value == False):
                        self.word.wtype[key] = value
                    else:
                        raise TypeError(
                        "self.wtype[%s].get() is neither -1, 0 nor +1, but \"%s\"" %
                        (key, self.wtype[key].get())
                        )
            else:
                #everything else
                self.word.wtype[key] = self.wtype[key].get()
        boolify(self.word.wtype) #"True" -> True, "None" -> None, "False" -> False
        self.displ["text"] = self.word.spell()

top = Tk()
top.title("My Do-Nothing Application")
top.maxsize(1000, 400)

app = App(top)
app.pack(side=RIGHT)

app.mainloop()
# root.mainloop()
