# =========================================================
# 1. DIZIONARI, PILLS E DATABASE CENTRALIZZATO
# =========================================================
COPPIE_INCOMPATIBILI = [
    {"Statico", "Antisismico"}, {"Angolo aperto", "Angolo chiuso"},
    {"Portante", "Non portante"}, {"Singolo", "Doppio"},
    {"Per ripiano in vetro", "Per ripiano in legno"}, {"Con serratura", "Senza serratura"},
    {"Passo 25", "Passo 50"}, {"L50", "L55"}, {"Scorrevoli", "A saracinesca"},
    {"Per attacco montante", "Per attacco fiancata"}, {"Superiore", "Tra ripiani di base"},
    {"Dritto", "Inclinato"}, {"Cromato", "Verniciato"},
    {"Multibarra", "Multilame", "In rete"}, {"Profilo a L", "Profilo a U"},
    {"Per ripiano di base", "Per fiancata"}, {"Terminale", "Centrale"},
    {"Liscio", "Liscia", "Forato", "Forata", "In filo"}, {"Zincato", "Verniciata"}
]

GLOSSARIO_TECNICO = {
    "mensola": "BRACKET", "mensole": "BRACKETS", "gondola": "GONDOLA",
    "spalla": "FRAME", "innesto": "COUPLING", "montante": "UPRIGHT",
    "per": "FOR", "losanga": "LOSANGA", "cancelletto": "GATE", "vasca": "TANK"
}

SUB_OPTIONS_CONFIG = {
    "VPA (+)": {"Serie S": "S SERIES", "Serie SS": "SS SERIES", "Serie M": "M SERIES", "Serie L": "L SERIES"},
    "Con distanziale (+)": {"L100": "S100", "L150": "S150", "L200": "S200", "L250": "S250"},
    "Numero diagonali (+)": {"Doppie": "DD", "Triple": "TD", "Quadruple": "QD"},
    "Sezione montante (+)": {"L55": "L55", "L80 Z/S": "L80 Z/S", "L80 Z/M": "L80 Z/M", "L100 Z/S": "L100 Z/S", "L100 Z/M": "L100 Z/M", "L120 Z/S": "L120 Z/S", "70X30": "70X30", "90X30": "90X30", "30X30": "30X30"},
    "Tipologia di mensola (+)": {"Mensola saldata a filo superiore": "UPPER BRACKET", "Mensola saldata a filo inferiore": "LOWER BRACKET"},
    "Compatibilità piede di base (+)": {"Per piede H90": "FOR H90 BASE FOOT", "Per piede H100": "FOR H100 BASE FOOT", "Per piede H150": "FOR H150 BASE FOOT"},
    "Attacco gancio (+)": {"Attacco barra": "HOOK FOR BAR", "Attacco multilame": "HOOK FOR MULTISTRIP", "Attacco pannello forato": "HOOK FOR SLOTTED PANEL"},
    "Orientamento Destro / Sinistro (+)": {"Destra": "RIGHT", "Sinistra": "LEFT"},
    "Posizioni multiple (+)": {"1 posizione": "1 POSITION", "2 posizioni": "2 POSITIONS", "3 posizioni": "3 POSITIONS"},
    "Altezza piede (+)": {"H90": "H90", "H100": "H100", "H150": "H150"},
    "Predisposto per montante (+)": {"L80": "FOR L80 UPRIGHT", "L100/L120": "FOR L100/L120 UPRIGHT"},
    "Numero tasche (+)": {"1 Tasca": "1 POCKET", "2 Tasche": "2 POCKETS"},
    "Numero gradoni (+)": {"1 gradone": "1 STEP", "2 gradoni": "2 STEPS", "3 gradoni": "3 STEPS"},
    "Asimmetrica (+)": {"AS240": "AS240", "AS340": "AS340", "AS440": "AS440"}
}

EXTRA_CON_INPUT_MANUALE = ["Sezione circolare", "Sezione quadrata"]

MATERIALI_CONFIG = {
    "METAL COMP": {"METAL": "METAL", "ZINCATO": "GALVANIZED", "INOX": "STAINLESS STEEL", "ALLUMINIO": "ALUMINIUM"},
    "WOOD COMP": {"LAMINATO": "LAMINATED", "NOBILITATO": "MELAMINE", "TRUCIOLARE": "CHIPBOARD", "OBS": "OSB", "HPL": "HPL"},
    "PLASTIC COMP": {"PLX": "PLX", "POLICARBONATO": "POLYCARBONATE", "PVC": "PVC", "GOMMA": "RUBBER"},
    "GLASS COMP": {"VETRO TEMPRATO": "TEMPERED", "VETRO SATINATO": "SATIN"},
    "FASTENER": {"NERO": "", "ZINCATO": "GALVANIZED", "BRUNITO": "BURNISHED"},
    "ASSEMBLY": {}
}

DATABASE = {
    "METAL COMP": {
        "macro_en": "METAL COMPONENT",
        "Particolari": {
            "Adattatore": [
                "ADAPTER",
                {
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Anta/sportello": [
                "DOOR",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con finestra": "WITH WINDOW",
                    "Con foro serratura": "WITH LOCK HOLE",
                    "Con inserti filettati": "WITH RIVET",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Canalina passa cavi": [
                "CABLE TRAY",
                {
                    "Asolato/a": "SLOTTED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Con inserti filettati": "WITH RIVET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Cassetto estraibile": [
                "PULL-OUT DRAWER",
                {
                    "Antisgancio": "ANTI-RELEASE",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con finestra": "WITH WINDOW",
                    "Con foro serratura": "WITH LOCK HOLE",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con rinforzo": "REINFORCED",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Impilabile": "STACKABLE",
                    "Regolabile": "ADJUSTABLE",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Cesto in filo": [
                "WIRE-BASKET",
                {
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con rinforzo": "REINFORCED",
                    "Con viteria": "WITH SCREWS",
                    "Impilabile": "STACKABLE",
                    "Inclinato": "SLOPING",
                    "Minirack": "MINIRACK",
                    "Multibarra": "MULTIBAR",
                    "Multilame": "MULTISTRIP",
                    "Regolabile": "ADJUSTABLE",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Chiusura": [
                "COVER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Cielino": [
                "CANOPY",
                {
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con finestra": "WITH WINDOW",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con inserti filettati": "WITH RIVET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Compensazione": [
                "FILLER PIECE",
                {
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Controventatura": [
                "BRACING",
                {
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Coprimontante": [
                "UPRIGHT-COVER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Copripiede": [
                "FOOT COVER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Corrente": [
                "BEAM",
                {
                    "Antisgancio": "ANTI-RELEASE",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Tipologia di mensola saldata (+)": "",
                    "VPA (+)": "VPA",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Diagonale": [
                "DIAGONAL",
                {
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Distanziale": [
                "SPACER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Scantonato": "NOTCHED",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Divisorio": [
                "DIVIDER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Asolato/a": "SLOTTED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Scantonato": "NOTCHED",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Fiancata laterale": [
                "SIDE PANEL",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Filo": [
                "WIRE",
                {
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Frontalino": [
                "RISER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Gancio": [
                "HOOK",
                {
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Inclinato": "SLOPING",
                    "Minirack": "MINIRACK",
                    "Multibarra": "MULTIBAR",
                    "Multilame": "MULTISTRIP",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Lamiera generica": [
                "SHEET METAL",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Asolato/a": "SLOTTED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Mensola": [
                "BRACKET",
                {
                    "Antisgancio": "ANTI-RELEASE",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con viteria": "WITH SCREWS",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Nervata": "RIBBED",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Per ripiano di base": "FOR BASE SHELF",
                    "Per ripiano in legno": "FOR WOODEN SHELF",
                    "Per ripiano in vetro": "FOR GLASS SHELF",
                    "Posizioni multiple (+)": "",
                    "Regolabile": "ADJUSTABLE",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Montante": [
                "UPRIGHT",
                {
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Biasolato": "SLOTTED ON TWO SIDES",
                    "Compatibilità piede di base (+)": "",
                    "Con collegamento superiore": "WITH UPPER CONNECTION",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Sezione montante (+)": "",
                    "Sezione circolare": "CIRCULAR SECTION",
                    "Sezione quadrata": "SQUARE SECTION",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Pannello frontale": [
                "FRONT PANEL",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con foro serratura": "WITH LOCK HOLE",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Minirack": "MINIRACK",
                    "Multibarra": "MULTIBAR",
                    "Multilame": "MULTISTRIP",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Pannello rivestimento": [
                "BACK PANEL",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Liscio": "PLAIN",
                    "Minirack": "MINIRACK",
                    "Multibarra": "MULTIBAR",
                    "Multilame": "MULTISTRIP",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Pedana di base": [
                "BASE PLATFORM",
                {
                    "Asolato/a": "SLOTTED",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con rinforzo": "REINFORCED",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Piastra di fissaggio": [
                "FIXING PLATE",
                {
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Piede di base": [
                "BASE FOOT",
                {
                    "Altezza piede (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Predisposto per montante (+)": "",
                    "Regolabile": "ADJUSTABLE",
                    "Statico": "STATIC",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Porta cartello": [
                "SIGN HOLDER",
                {
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Inclinato": "SLOPING",
                    "Regolabile": "ADJUSTABLE",
                    "Scorrevoli": "SLIDING",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Portaprezzo": [
                "TICKET-HOLDER",
                {
                    "Asolato/a": "SLOTTED",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Profilo": [
                "PROFILE",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Profilo a L": "L-SHAPED",
                    "Profilo a U": "U-SHAPED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Protezione": [
                "PROTECTION FOR PERFORATED SHELF",
                {
                    "Con inserti filettati": "WITH RIVET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Liscio": "PLAIN",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Rinforzo": [
                "STIFFENER",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Asolato/a": "SLOTTED",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Ripiano": [
                "SHELF",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con inserti filettati": "WITH RIVET",
                    "Con portaprezzo": "WITH TICKET-HOLDER",
                    "Con rinforzo": "REINFORCED",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "In filo": "WIRE",
                    "In rete": "MESH",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Minirack": "MINIRACK",
                    "Multibarra": "MULTIBAR",
                    "Multilame": "MULTISTRIP",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Staffa": [
                "PLATE",
                {
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Tamponamento": [
                "BUFFER PANEL",
                {
                    "Asolato/a": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Regolabile": "ADJUSTABLE",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Traversino": [
                "CROSS BAR",
                {
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Tubolare": [
                "TUBULAR",
                {
                    "Asolato/a": "SLOTTED",
                    "Biasolato": "SLOTTED ON TWO SIDES",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Inclinato": "SLOPING",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Sezione circolare": "CIRCULAR SECTION",
                    "Sezione quadrata": "SQUARE SECTION",
                    "Tipologia di mensola saldata (+)": "",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Vasca": [
                "TANK",
                {
                    "Compatibilità piede di base (+)": "",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole saldate": "WITH WELDING BRACKET",
                    "Con rinforzo": "REINFORCED",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ],
            "Zoccolatura": [
                "PLINTH",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Antisgancio": "ANTI-RELEASE",
                    "Asolato/a": "SLOTTED",
                    "Attacco a seggiola": "L-SHAPED PROFILE",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Completa di paracolpo ABS": "WITH ABS BUFFER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con inserti filettati": "WITH RIVET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Liscio": "PLAIN",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Piegato": "BENT",
                    "Piegato-saldato": "BENT AND WELDED",
                    "Scantonato": "NOTCHED",
                    "Verniciata": "POWDER COATED"
                }
            ]
        }
    }
},

"WOOD COMP": {
        "macro_en": "WOOD COMPONENT",
        "Particolari": {
            "Anta/sportello": [
                "DOOR",
                {
                    "Asolato": "SLOTTED",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Asta in legno": [
                "WOODEN ROD",
                {
                    "Asolato": "SLOTTED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Cielino": [
                "WOODEN CANOPY",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Compensazione": [
                "WOODEN FILLER PIECE",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Coprimontante": [
                "WOODEN UPRIGHT-COVER",
                {
                    "Asolato": "SLOTTED",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Copripiede": [
                "WOODEN FOOT-COVER",
                {
                    "Asolato": "SLOTTED",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Fiancata": [
                "WOODEN SIDE PANEL",
                {
                    "Asolato": "SLOTTED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Mobiletto in legno": [
                "WOODEN CABINET",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Completa di paracolpo ABS": "WITH ABS BUFFER",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole": "WITH BRACKET",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Pannello in legno": [
                "WOODEN PANEL",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Ripiano Legno": [
                "WOODEN SHELF",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Schienale Legno": [
                "WOODEN BACK",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Tamponamento": [
                "BUFFER PANEL",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Zoccolatura": [
                "WOODEN PLINTH",
                {
                    "Asolato": "SLOTTED",
                    "Attacco gancio (+)": "",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Compatibilità piede di base (+)": "",
                    "Completa di paracolpo ABS": "WITH ABS BUFFER",
                    "Con inserti filettati": "WITH RIVET",
                    "Con lati bordati": "WITH EDGED SIDES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Fresata": "MILLING",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ]
        }
    },

"PLASTIC COMP": {
        "macro_en": "PLASTIC COMPONENT",
        "Particolari": {
            "Anta": [
                "DOOR",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con foro serratura": "WITH LOCK HOLE",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Cerniera": [
                "HINGE",
                {}
            ],
            "Divisorio": [
                "DIVIDER",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Frontalino": [
                "RISER",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Guarnizione": [
                "GASKET",
                {}
            ],
            "Pannello": [
                "PANEL",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Portaprezzo": [
                "TICKET-HOLDER",
                {
                    "Con scasso": "WITH RECESS"
                }
            ],
            "Tappo": [
                "PLASTIC CAP",
                {}
            ]
        }
    },

"GLASS COMP": {
        "macro_en": "GLASS COMPONENT",
        "Particolari": {
            "Anta": [
                "GLASS DOOR",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con foro serratura": "WITH LOCK HOLE",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Cancelletto": [
                "GLASS ARM",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Chiusura": [
                "COVER",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ],
            "Ripiano": [
                "GLASS SHELF",
                {
                    "Antiurto": "SHOCKPROOF",
                    "Asolato": "SLOTTED",
                    "Attacco a pinza": "GRIPPED",
                    "Attacco gancio (+)": "",
                    "Attacco montante": "HOOK ONTO UPRIGHT",
                    "Bordi smussati": "CHAMFERED EDGES",
                    "Con mensole": "WITH BRACKET",
                    "Con scasso": "WITH RECESS",
                    "Con viteria": "WITH SCREWS",
                    "Forato": "PERFORATED",
                    "Orientamento Destro / Sinistro (+)": ""
                }
            ]
        }
    },

"ASSEMBLY": {
        "macro_en": "ASSEMBLY",
        "Particolari": {
            "Avancassa": [
                "IMPULSE UNIT",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Banco espositore di legno": [
                "WOODEN DESK",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con ante scorrevoli": "WITH SLIDING DOOR",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Rotante": "ROTATING",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Cassa pagamento automatico": [
                "SELF CHECKOUT",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Compatibilità piede di base (+)": "",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con macchine di pagamento": "WITH GLORY MACHINES PAYMENT",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Cassettiera": [
                "CHEST OF DRAWERS",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con ante scorrevoli": "WITH SLIDING DOOR",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Controventatura": [
                "CROSS-BRACING",
                {
                    "Antisismico": "SEISMIC-RESISTANT",
                    "Con distanziale (+)": "WITH SPACER",
                    "Numero diagonali (+)": "",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Espositore": [
                "DISPLAY",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con ante scorrevoli": "WITH SLIDING DOOR",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con tasca oscillante": "WITH LIFT-UP POCKET",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Rotante": "ROTATING",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Espositore a gradoni": [
                "STEPLADDER DISPLAY",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con tasca oscillante": "WITH LIFT-UP POCKET",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Rotante": "ROTATING",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Espositore riviste": [
                "DISPLAY FOR MAGAZINE",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con tasca oscillante": "WITH LIFT-UP POCKET",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Rotante": "ROTATING",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Spalla": [
                "FRAME",
                {
                    "Antisismico": "SEISMIC-RESISTANT",
                    "Asimmetrica (+)": "",
                    "Compatibilità piede di base (+)": "",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Telaio saldato": [
                "METAL WELDMENT",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con inserti filettati": "WITH RIVET",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con tasca oscillante": "WITH LIFT-UP POCKET",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Rotante": "ROTATING",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Totem": [
                "TOTEM",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con ante scorrevoli": "WITH SLIDING DOOR",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con componente saldato": "WITH WELDED ELEMENT",
                    "Con guide RAM": "WITH RAM GUIDE",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con mensole": "WITH BRACKET",
                    "Con mensole saldate": "WITH WELDED BRACKETS",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con tasca oscillante": "WITH LIFT-UP POCKET",
                    "Con viteria": "WITH SCREWS",
                    "Con viteria saldata": "WITH WELDING SCREWS",
                    "Mobile": "MOBILE",
                    "Numero gradoni (+)": "",
                    "Numero tasche (+)": "",
                    "Orientamento Destro / Sinistro (+)": "",
                    "Rotante": "ROTATING",
                    "Verniciata": "POWDER COATED",
                    "Zincato": "GALVANIZED"
                }
            ],
            "Vetrina": [
                "SHOWCASE",
                {
                    "Angolo aperto": "EXTERNAL CORNER",
                    "Angolo chiuso": "INNER CORNER",
                    "Attacco montante": "ONTO THE UPRIGHT",
                    "Compatibilità piede di base (+)": "",
                    "Con ante scorrevoli": "WITH SLIDING DOOR",
                    "Con batticarrello": "WITH TROLLEY BEATER",
                    "Con illuminazione": "WITH LIGHTING",
                    "Con ripiani": "WITH SHELF",
                    "Con ripiani inclinati": "WITH INCLINED SHELF",
                    "Con ruote": "WITH WHEELS",
                    "Con scasso": "WITH RECESS",
                    "Con serratura": "WITH LOCK",
                    "Con viteria": "WITH SCREWS"
                }
            ]
        }
    },

"FASTENER": {
        "macro_en": "FASTENER",
        "Particolari": {
            "Bullone": [
                "BOLT",
                {
                    "Testa Bombata": "ROUND HEAD",
                    "Testa a croce": "CROSS HEAD",
                    "Testa esagonale": "HEX HEAD",
                    "Testa esagono incassato": "HEXAGON SOCKET HEAD",
                    "Testa svasata": "COUNTERSUNK HEAD"
                }
            ],
            "Dado": [
                "NUT",
                {
                    "Flangiato": "FLANGED"
                }
            ],
            "Inserti filettati": [
                "RIVET",
                {
                    "Con testa": "WITH HEAD",
                    "Senza testa": "WITHOUT HEAD"
                }
            ],
            "Rondella": [
                "WASHER",
                {
                    "Dentellata": "SERRATED LOCK",
                    "Elastica": "GROWER",
                    "Fascia Larga": "WIDE BAND"
                }
            ],
            "Vite": [
                "SCREW",
                {
                    "Autobloccante": "SELF-LOCKING",
                    "Autoperforanti": "SELF-DRILLING",
                    "Testa Bombata": "ROUND HEAD",
                    "Testa a croce": "CROSS HEAD",
                    "Testa esagonale": "HEX HEAD",
                    "Testa esagono incassato": "HEXAGON SOCKET HEAD",
                    "Testa svasata": "COUNTERSUNK HEAD"
                }
            ]
        }
    },

OPZIONI_COMPATIBILITA = ["", "F25", "F25 BESPOKE", "F25 READY", "F50", "F50 BESPOKE", "F50 READY", "UNIVERSAL", "BC", "FORTISSIMO", "MINIRACK", "UNIMOB"]

MAPPA_NORMATIVE_FASTENER = {
    "Vite": {
        "": "", "DIN 912 - Testa cilindrica": "DIN 912", "DIN 933 - Esagonale filetto totale": "DIN 933",
        "DIN 931 - Esagonale filetto parziale": "DIN 931", "DIN 7991 - Testa svasata esagono incassato": "DIN 7991",
        "ISO 7380 - Testa bombata esagono incassato": "ISO 7380", "DIN 571 - Tirafondo per legno": "DIN 571",
        "DIN 7504-K - Autoperforante Esagonale": "DIN 7504-K", "DIN 7504-N - Autoperforante Bombata": "DIN 7504-N",
        "DIN 7504-P - Autoperforante Svasata": "DIN 7504-P"
    },
    "Dado": {"": "", "DIN 934 - Esagonale standard": "DIN 934", "DIN 985 - Autobloccante nylon": "DIN 985", "DIN 6923 - Flangiato zigrinato": "DIN 6923"},
    "Rondella": {"": "", "DIN 125 - Piana standard": "DIN 125", "DIN 9021 - Fascia larga": "DIN 9021", "DIN 6798 - Dentellata": "DIN 6798", "DIN 127 - Grower (elastica)": "DIN 127"},
    "Bullone": {"": ""}, "Inserti filettati": {"": ""}
}

TERMINI_ANTICIPATI = [
    "CENTRAL", "LEFT", "RIGHT", "REINFORCED", "INTERNAL", "EXTERNAL", "STATIC", "ADJUSTABLE", "SEISMIC",
    "MULTIBAR", "MULTISTRIP", "TOP", "INTER-BASE SHELF", "ROUNDED", "SLOPING", "SHAPED", "CONNECTING", "SHUTTER", "COUPLING",
    "WIRE", "GRIPPED", "CHROMED", "PAINTED", "MESH", "SLIDING", "CURVED", "STRAIGHT", "MILLING", "WIRE-BASKET",
    "SEMICIRCULAR", "SINGLE", "DOUBLE", "END", "L-SHAPED", "U-SHAPED", "SERRATED LOCK", "ROTATING", "CTR", "UPRIGHT-GRAFT"
]
