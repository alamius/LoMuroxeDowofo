from vocab import roots

E0 = [{
        "marker":"V",
        "root":roots["go"],
    	"tense": 'present',
    	"passive": False,
    	"parent_place_string": '',
    	"person": ['me', 'plural-you'],
    	"professional": None,
    	"child_place_string": '',
    	"parent_place": [],
    	"verb_class": 'indicative',
    	"metaphore": False,
    	"child_place": [],
    	"class": 'verb',
    }, # tagykoxixin(ri)
    {
        "marker":"S-V",
        "root":roots["fight"],
    	"number": 'plural',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": True,
    	"metaphore": True,
    	"passive": False,
    	"case_class": None,
    	"parent_place": [],
    	"noun_class": 'actor',
    	"case": None,
    	"child_place": [],
    	"class": 'noun',
    }, # (ri)poPulokema
    {
        "marker":"A-S-V",
        "root":roots["burn"],
    	"number": 'singular',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": None,
    	"metaphore": False,
    	"passive": False,
    	"case_class": 'causal',
    	"parent_place": [],
    	"noun_class": 'action',
    	"case": 'opposite',
    	"child_place": [],
    	"class": 'noun',
    }, # rilomamaxedewOti
    {
        "marker":"A-V",
        "root":roots["teach"],
    	"number": 'singular',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": True,
    	"metaphore": False,
    	"passive": True,
    	"case_class": 'directional',
    	"parent_place": [],
    	"noun_class": 'action',
    	"case": 'near',
    	"child_place": [],
    	"class": 'noun',
    }, # JuvomusaqemalesO
    {
        "marker":"A2-V",
        "root":roots["save"],
    	"number": 'singular',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": None,
    	"metaphore": False,
    	"passive": False,
    	"case_class": 'causal',
    	"parent_place": [],
    	"noun_class": 'action',
    	"case": 'before',
        "child_place": [],
        "class": 'noun',
    }, # lelomuxedan
    {
        "marker":"O-A2-V",
        "root":roots["teach"],
    	"number": 'plural',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": None,
    	"metaphore": False,
    	"passive": True,
    	"case_class": None,
    	"parent_place": [],
    	"noun_class": 'actor',
    	"case": None,
    	"child_place": [],
    	"class": 'noun',
    }, # sOlomidin
    {
        "marker":"O2-A2-V",
        "root":roots["teach"],
    	"number": 'plural',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": True,
    	"metaphore": False,
    	"passive": False,
    	"case_class": None,
    	"parent_place": [],
    	"noun_class": 'actor',
    	"case": None,
    	"child_place": [],
    	"class": 'noun',
    }, { #"regularly in the time of the shone upon", dayly
        "marker":"A-V",
        "root":roots["shine"],
    	"number": 'singular',
    	"parent_place_string": '',
    	"child_place_string": '',
    	"professional": False,
    	"metaphore": True,
    	"passive": True,
    	"case_class": 'temporal',
    	"parent_place": [],
    	"noun_class": 'actor',
    	"case": 'above',
    	"child_place": [],
    	"class": 'attribute',
    }, {
        "marker":"V2",
        "root":roots["kill"],
    	"tense": 'present',
    	"passive": True,
    	"parent_place_string": '',
    	"person": ['me', 'plural-you'],
    	"professional": None,
    	"child_place_string": '',
    	"parent_place": [],
    	"verb_class": 'indicative',
    	"metaphore": False,
    	"child_place": [],
    	"class": 'verb',
}]
#                 /----------------------------\
#  v   !  v     /-|---      v       v     v  --|-v   .   v  ----\ v     v   /----\ v     v     v   v       v   .   v   .  v   .    v
# gáresùnkáj(taríJúwa) tagykóxixìn-póPulokÈma Jùlómamàxedéwoti rívómusaqÈmalèso lèlómuxedán solómidìn wagyvéXekìxenírufo KáPesùnxeJáj.
# gáresunkáj(taríJuwa) tagykóxixín-póPulokéma Julómamáxedéwoti rívómusaqémaléso lélómuxedán solómidín wagyvéXekéxenírufo KáPesúnxeJáj.
# you and I (go) as fighters against fire (go) into schools to save            students and teachers dayly          and we get killed.


E1 = [{
        "root":roots["kill"],
    	"parent_place": [],
    	"passive": True,
    	"verb_class": 'imperative',
    	"professional": None,
    	"child_place": [],
    	"child_place_string": '',
    	"tense": 'future',
    	"metaphore": False,
    	"parent_place_string": '',
    	"class": 'verb',
	    "person": ['me'],
    }, {
        "root":roots["kill"],
    	"parent_place": [],
    	"passive": True,
    	"verb_class": 'imperative',
    	"professional": None,
    	"child_place": [],
    	"child_place_string": '',
    	"tense": 'present',
    	"metaphore": False,
    	"parent_place_string": '',
    	"class": 'verb',
    	"person": ['me'],
    }, {
        "root":roots["kill"],
    	"parent_place": [],
    	"passive": True,
    	"verb_class": 'imperative',
    	"professional": None,
    	"child_place": [],
    	"child_place_string": '',
    	"tense": 'past',
    	"metaphore": False,
    	"parent_place_string": '',
    	"class": 'verb',
    	"person": ['me'],
}]

#taking apart a random german sentence to test the languages usability. looking for needed features.
#It exists in areas
#JáXekí rigykówotájxeXúra legykóxamáne-JudétoLéweré waDáPe'óxekónJene-gykóxamáLine-qóJotájxerúra Lisófaxemá-riléqeméxedé Jelómomadúma gykáxekajné solómixedáne wagykóxamá-Julómaxedá-nepózaPáne

E2 = [
    { #JaX[ek]i
        # Es gibt (V1) –
        "marker":"V1",
        "root":roots["exist"],
        "class":"verb",
        "verb_class":"indicative",
        "tense":"present",
        "person":["undef"]
    }, { #rigykówotájxeXúra
            #ri - attribute
            #gy - metaphorical
            #kó - r1, noun
            #wo - r2, local
            #táj - same
            #xe - passive
            #Xú - r3, local
            #ra - object (noun class)
        #  (A-V1)
        #   in (TA-V1) TA = Local_In
        #     diesen (A/R-NA-V1)
        #    Bereichen (NA-V1) begrenzen_Metaphorical_Noun_TA
        "marker":"A-V1",
        "root":roots["limit"],
        "passive":True,
        "metaphore":True,
        "class":"noun",
        "noun_class":"object",
        "case_class":"local",
        "case":"same"
    }, { #legykóxamáne-
            #le - object
            #gy - metaphore
            #kó - r1, noun
            #xa - r2, action & active
            #má - action & active, professional: None
            #n  - plural
        #  (O-V1)
        #    verschiedene (A-NO-V1) unterscheiden_Attr_possible
        #   Wettbewerbe, (NO-V1) kämpfen_Met_Noun-O-V1
        "marker":"O-V1",
        "root":roots["fight"],
        "metaphore":True,
        "class":"noun",
        "noun_class":"action",
        "number":"plural",
    }, { #-JudétoLéweré
            #dé - r1, attribute
            #to - possible & active
            #Lé - perceived
            #we - r2, active
            #ré - r3, present
        "marker":"A-O-V1",
        "root":roots["differ"],
        "perceived":True,
        "class":"attribute",
        "attribute_class":"possible",
    }, { #waDáPe'óxekónJene-
            #wa - attribute on verb 2
            #Dá - r1, verb
            #Pe - r2, present
            #'ó - imperative
            #xe - passive
            #kón- person: all
            #Je - has an attribute
        # und
        #  (A-V2)
        #   trotz (TA-V) TA = Causal_Opposite
        #   der Relevanz (NA-V) bedenken_Prof_Passive_TA
        "marker":"A-V2",
        "root":roots["think"],
        "passive":True,
        "class":"verb",
        "verb_class":"imperative",
        "person":["plural-me", "plural-you", "plural-they"],
    }, { #-gykóxamáLine-
            #gy - metaphore
            #kó - r1, noun
            #xa - r2, action & active
            #má - action & active, professional=None
            #Li - has attribute
        #    des --wettbewerb (NA-NA-V) kämpfen_Met_Noun_-A
        "marker":"A-A-V2",
        "root":roots["fight"],
        "metaphore":True,
        "class":"noun",
        "noun_class":"action",
    }, { #-qóJotájxerúra
            #qó - r1, noun
            #Jo - r2, local
            #táj- same_case -> in
            #xe - passive
            #rú - r3,
            #ke - passive_object
        #     -Bundes- (NA-NA-NA-V) vereinigen_Pass_Perf_Local_In
        "marker":"A-A-A-V2",
        "root":roots["unite"],
        "passive":True,
        "class":"noun",
        "noun_class":"object",
        "case_class":"local",
        "case":"same",
    }, { #Lisófaxemá-
        #     Fremdsprachen (NA-NA-NA-V) sprechen_Noun_Action lernen_Attr_imperativ
        "marker":"A2-A-A-V2",
        "root":roots["speak_language"],
        "passive":True,
        "class":"noun",
        "noun_class":"object",
    }, { #-riléqeméxedé
        "marker":"A-A2-A-A-V2",
        "root":roots["teach"],
        "passive":True,
        "class":"attribute",
        "attribute_class":"obligate",
    }, { #Jelómomadúma
        #    (A-NA-V)
        #     an (TA-NA-V)
        #     der Schule (NA-NA-V) Lernen_Prof_Noun_Local_Near
        "marker":"A2-A-V2",
        "root":roots["teach"],
        "professionell":True,
        # "passive":True,
        "class":"noun",
        "noun_class":"action",
        "case_class":"local",
        "case":"near",
    }, { #gykáxekájne
        #  nehmen (V2) (Teil) kämpfen_Met_Verb
        "marker":"V2",
        "root":roots["fight"],
        "metaphore":True,
        "class":"verb",
        "verb_class":"indicative",
        "person":["plural-me"],
    }, { #solómuxedán
        #  Schüler (NO-V2) lernen_Noun_Actor_Activ
        "marker":"O-V2",
        "root":roots["teach"],
        "professionell":True,
        "passive":True,
        "class":"noun",
        "noun_class":"actor",
        "number":"plural",
    }, { #wagykóxamá-
        #  (A-V2)
        #   an (TA-V2)
        #   --wettbewerben (NA-V2) kämpfen_Met_Noun_
        "marker":"A2-V2",
        "root":roots["fight"],
        "metaphore":True,
        "class":"noun",
        "noun_class":"action",
    }, { #-lómoxedá-
        #    -Geographie- lernen_über_orte
        "marker":"A-A2-V2",
        "root":roots["teach"],
        "passive":True,
        "class":"noun",
        "noun_class":"action",
    }, { #-pózaPán
        "marker":"O-A-A2-V2",
        "root":roots["place"],
        "class":"noun",
        "number":"plural",
        "noun_class":"object",
    #  Teil, (A-V2)
    # es gibt (V3)
    #    Mathematik- (NA-NO-V3)
    #   und
    #    Biologieolympiaden (NO-V3)
    #  sowie
    #  den Biberwettbewerb (NO-V3)
    #   (A-NO-V3)
    #    für (TA-NO-V3)
    #    die Früherkennung (NA-NO-V3)
    #     (A-NA-NO-V3)
    #      informatischen (A-NA-NA-NO-V3)
    #     Talents (NA-NA-NO-V3) können_Unprof_Noun
    #  und
    #   (O-V3)
    #     schulische (A-NO-V3)
    #    Veranstaltungen, (NO-V)
    #    (A-NO-V)
    #     in denen (TA-NO-V)
    #     Schüler (NS-VA-TA-NO-V)
    #      (A-VA-TA-NO-V)
    #       außerhalb (TA-VA-TA-NO-V)
    #       der Schule (NA-VA-TA-NO-V)
    #     Fachwissen (NO-VA-TA-NO-V)
    #      (A-VA-TA-NO-V)
    #       durch (TA-VA-TA-NO-V)
    #         praktische (A-NA-VA-TA-NO-V)
    #        Erfahrung (NA-VA-TA-NO-V)
    #     vertiefen. (VA-NO-V)
}]
