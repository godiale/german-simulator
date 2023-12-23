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
    )
}


def get_irregular_verbs():
    return list(itertools.chain.from_iterable(IRREGULAR_VERBS.values()))
