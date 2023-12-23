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
    )
}


def get_irregular_verbs():
    return list(itertools.chain.from_iterable(IRREGULAR_VERBS.values()))
