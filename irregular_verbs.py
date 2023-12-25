import itertools

IRREGULAR_VERBS = {
    "ei -> ie, ie": (
        'bleiben',
        'leihen',
        'meiden',
        'scheiden',
        'scheinen',
        'schreiben',
        'schreien',
        'schweigen',
        'steigen',
        'treiben',
        'verzeihen',
        'weisen'
    ),
    "ei -> i, i": (
        'bleiben',
        'gleichen',
        'gleiten',
        'greifen',
        'leiden',
        'pfeifen',
        'reißen',
        'reiten',
        'schneiden',
        'schreiten',
        'streichen',
        'streiten',
    ),
    "ie -> o, o": (
        'biegen',
        'bieten',
        'fliegen',
        'fliehen',
        'fließen',
        'frieren',
        'gießen',
        'genießen',
        'kriechen',
        'riechen',
        'schieben',
        'schießen',
        'schließen',
        'verlieren',
        'wiegen',
        'ziehen',
    ),
    "i -> a, u": (
        'binden',
        'dringen',
        'finden',
        'gelingen',
        'klingen',
        'singen',
        'sinken',
        'springen',
        'trinken',
        'verschwinden',
        'zwingen'
    ),
    "i -> a, o": (
        'beginnen',
        'gewinnen',
        'schwimmen'
    ),
    "e -> a, o": (
        'befehlen',
        'bergen',
        'bersten',
        'brechen',
        'erschrecken',
        'gelten',
        'helfen',
        'nehmen',
        'sprechen',
        'stehlen',
        'sterben',
        'treffen',
        'werben',
        'werfen',
    ),
    "ä -> a, o": (
        'gebären',
    ),
    "e -> a, e": (
        'essen',
        'geben',
        'genesen',
        'geschehen',
        'lesen',
        'messen',
        'sehen',
        'treten',
        'vergessen',
    ),
    "i -> a, e": (
        'bitten',
        'liegen',
        'sitzen',
    ),
    "a -> u, a": (
        'backen',
        'fahren',
        'graben',
        'laden',
        'schaffen',
        'schlagen',
        'tragen',
        'wachsen',
        'waschen',
    ),
    "e|ä|ü|ö -> o, o": (
        'erwägen',
        'flechten',
        'heben',
        'lügen',
        'schmelzen'
    ),
    "a -> ie, a": (
        'blasen',
        'braten',
        'fallen',
        'gefallen',
        'halten',
        'lassen',
        'raten',
        'schlafen'
    ),
    "a -> i, a": (
        'fangen',
        'hängen',
    ),
    "au|ei|o|u -> ie, au|ei|o|u": (
        'hauen',
        'heißen',
        'laufen',
        'rufen',
        'stoßen',
    ),
    "irregular": (
        'gehen',
        'kommen',
        'stehen',
        'tun'
    ),
    "auxiliary": (
        'sein',
        'haben',
        'werden'
    ),
    "mixed": (
        'brennen',
        'bringen',
        'denken',
        'kennen',
        'nennen',
        'rennen',
        'senden',
        'wenden',
        'wissen'
    ),
    "model": (
        'können',
        'dürfen',
        'sollen',
        'müssen',
        'wollen',
        'mögen'
    )
}


def get_irregular_verbs():
    return list(itertools.chain.from_iterable(IRREGULAR_VERBS.values()))
