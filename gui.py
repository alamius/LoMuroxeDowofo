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
    "person": 'me',
    "professional": "None",
    "child_place": [],
    "perceived": False,
    "tense": 'future',
    "noun_class":"action",
    "case_class":"None",
    "case":"None",
    "attribute_class":"stative",
    "negative":False,
})

root = 101
wtype_types = {
    #top
    "root": root,
    "class": str,
    #verbs
    "verb_class": str,
    "person": str,
    "tense": str,
    #nouns
    "noun_class":str,
    "case_class":str,
    "case":str,
    #attribute
    "attribute_class":str,
    "negative":bool,
    #general
    "metaphore": bool,
    "passive": bool,
    "professional": str,
    "perceived": bool,
    #structural
    "marker": None,
    "parent_place": None,
    "parent_place_string": None,
    "child_place": None,
    "child_place_string": None,
}
wtype_options = {
    #top
    "root": list(roots.values()),
    "class": ["verb", "noun", "attribute"],
    #verbs
    "verb_class": ["indicative", "imperative"],
    "person": ["me", "you"],
    "tense": ["past", "present", "future"],
    #nouns
    "noun_class":["action", "agent", "object", "recipient", "instrument"],
    "case_class":["None", "directional", "local", "temporal", "causal"],
    "case":["None", "before", "after", "above", "under", "near", "parallel", "same", "opposite"],
    #attribute
    "attribute_class":["stative", "obligate", "conjunctive", "possible"],
    # "negative":[True, False],
    #general
    # "metaphore": [True, False],
    # "passive": [True, False],
    "professional": ["False", "None", "True"],
    # "perceived": [True, False],
    #structural
    "marker": [],
    "parent_place": [],
    "parent_place_string": [],
    "child_place": [],
    "child_place_string": [],
}

class Element(object):
    """an Element contains a Widget or a combination of Widgets in self.element,
    a variable to change when the Widget is used,
    has a key used to get to the variable or as an id,
    a reference to the app, it is part of,
    a variable to check against if its existence depends on other factors,
    and a function exists to use on self.check."""
    def __init__(self, master, key, variable, app, options):
        super(Element, self).__init__()
        self.master = master
        self.key    = key
        self.variable = variable
        self.options = options
        self.app    = app
class Root(Element):
    """DropDown for Roots"""
    def __init__(self, master, variable, app, options=roots.values()):
        super(Root, self).__init__(master, "root", variable, app, options)
        self.element = OptionMenu(
            self.master,
            self.variable,
            *self.options
        )

        # on change dropdown value
        def change_dropdown(*args):
            app.word.root = self.variable.get()
            if(len(app.word.root) < 3):
                app.word.root += "k"
                app.update()

        # link function to change dropdown
        self.variable.trace('w', change_dropdown)
        self.element.pack(side=BOTTOM)
class NamedElement(Element):
    """Can check for its need for existence,
    places a tracer of self.check and
    executes self.exist whenever the tracer activates,
    using self.exists as a bool function or variable to decide."""

    def __init__(self, master, key, name, variable, app, options):
        super(NamedElement, self).__init__(master, key, variable, app, options)
        self.element = Frame(self.master)
        self.name = Button(self.element, text=name)
        self.name.pack(side=LEFT)
        self.element.pack()
class Choice(NamedElement):
    """Multiple choice, only one allowed, Radiobuttons"""
    def __init__(self, master, key, name, app, options):
        super(Choice, self).__init__(master, key, name, app.wtype[key], app, options)
        self.buttons = []
        for option in list(self.options):
            self.buttons += [
                Radiobutton(
                    self.element,
                    text=str(option),
                    value=option,
                    variable=self.variable,
                    command=self.app.update
                )
            ]
        for button in self.buttons:
            button.pack(side=LEFT)
class Bool(NamedElement):
    def __init__(self, master, key, name, app, options=None):
        super(Bool, self).__init__(master, key, name, app.wtype[key], app, options)
        self.button = Checkbutton(
            self.element,
            text=self.key,
            variable=self.variable,
            command=app.update
        )
        self.button.pack()

class App(Frame):
    def __init__(self, master, word=word):
        super().__init__(master)
        self.word = word
        self.wtype = {}
        for key in wtype_types.keys():
            if(wtype_types[key] == bool):
                self.wtype[key] = BooleanVar()
            elif(wtype_types[key] == int):
                self.wtype[key] = IntVar()
            elif(wtype_types[key] == str):
                self.wtype[key] = StringVar()
            elif(wtype_types[key] == root):
                self.wtype[key] = StringVar()
            if(
                not wtype_types[key] == None and
                not wtype_types[key] == root and
                key in self.word.wtype.keys()
            ):
                self.wtype[key].set(self.word.wtype[key])

        self.frames = {
            "top":Frame(self),
            "verb":Frame(self),
            "noun":Frame(self),
            "general":Frame(self),
            "attribute":Frame(self),
        }
        self.buttons = {}
        #top
        self.buttons["root"]        = Root(
            self.frames["top"],
            variable=self.wtype["root"],
            app=self
        )
        self.buttons["class"]       = Choice(
            self.frames["top"],
            key="class",
            name="Class:",
            app=self,
            options=wtype_options["class"]
        )
        #general
        self.buttons["professional"]= Choice(
            self.frames["general"],
            key="professional",
            name="Prof:",
            app=self,
            options=wtype_options["professional"]
        )
        self.buttons["metaphore"]= Bool(
            self.frames["general"],
            key="metaphore",
            name="Metaph:",
            app=self
        )
        self.buttons["perceived"]= Bool(
            self.frames["general"],
            key="perceived",
            name="Perceived:",
            app=self
        )
        #verb
        self.buttons["verb_class"]  = Choice(
            self.frames["verb"],
            key="verb_class",
            name="V.Class:",
            app=self,
            options=wtype_options["verb_class"]
        )
        self.buttons["tense"]  = Choice(
            self.frames["verb"],
            key="tense",
            name="Tense:",
            app=self,
            options=wtype_options["tense"]
        )
        #noun
        self.buttons["noun_class"]  = Choice(
            self.frames["noun"],
            key="noun_class",
            name="N.Class:",
            app=self,
            options=wtype_options["noun_class"]
        )
        self.buttons["case_class"]  = Choice(
            self.frames["noun"],
            key="case_class",
            name="Case Class:",
            app=self,
            options=wtype_options["case_class"]
        )
        self.buttons["case"]        = Choice(
            self.frames["noun"],
            key="case",
            name="Case:",
            app=self,
            options=wtype_options["case"]
        )
        #attribute
        self.buttons["attribute_class"] = Choice(
            self.frames["attribute"],
            key="attribute_class",
            name="Attr.Class:",
            app=self,
            options=wtype_options["attribute_class"]
        )
        self.buttons["negative"]    = Bool(
            self.frames["attribute"],
            key="negative",
            name="Attr.Negation:",
            app=self
        )

        self.frames["top"       ].pack(side=TOP)
        self.frames["general"   ].pack(side=TOP)
        self.frames["verb"      ].pack(side=TOP)
        self.frames["noun"      ].pack(side=TOP)
        self.frames["attribute" ].pack(side=TOP)
        self.displ = Button(
            self,
            text=self.word.spell(),
            bg="green",
            command=self.update
        )
        self.displ.pack(side=BOTTOM)

        self.pack()
    def update(self):
        for key in self.wtype.keys():
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
