from pandas_ods_reader import read_ods
from collections import defaultdict
import random

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.ods"
SMALLEST_EXERCISE_SIZE = 20

PREFIXES = [
    'ab', 'an', 'auf', 'aus', 'be', 'ein', 'ent', 'er',
    'ge', 'him', 'über', 'unter', 'ver', 'vor', 'zu'
]


def read_verbs_from_file():
    df = read_ods(WORDS_STORE, "Verben", headers=False,
                  columns=['a', 'verb', 'b', 'translation'])\
        .drop(columns=['a', 'b'])
    df = df[df.translation.notnull()]
    df.verb = df.verb.str.strip()
    df.drop_duplicates(subset='verb')
    df = df.set_index('verb', drop=False)
    return df


def create_exercise(df):
    mode = input("Enter mode (plain|group) [plain]: ")
    if mode == '':
        mode = 'plain'

    if mode == 'group':
        r2v = defaultdict(list)
        for v in df.verb.tolist():
            r2v[v].append(v)
            for p in PREFIXES:
                if v.startswith(p):
                    r2v[v.removeprefix(p)].append(v)
        roots = list(r2v.keys())
        random.shuffle(roots)
        verbs = []
        for r in roots:
            if len(r2v[r]) > 1:
                verbs.extend(r2v[r])
        df = df.loc[verbs]
    else:  # plain
        df = df.sample(frac=1).reset_index(drop=True)  # random order
        regex = input("Enter words regex: ")
        df = df[df.verb.str.contains(regex)]

    if len(df.index) > SMALLEST_EXERCISE_SIZE:
        exercise_size = input(f"Enter size of exercise: (1-{len(df.index)}): ")
        df = df.head(int(exercise_size))
    return df


def main():
    df = read_verbs_from_file()
    df = create_exercise(df)

    fail = 0

    for index, row in df.iterrows():
        input(f"{row.verb} ? ")
        print(f"    {row.translation}")
        known = input()
        if known != '':  # user hit Enter
            fail += 1

    total = len(df.index)
    print(f"Pass={total-fail}, Fail={fail} (Total {total})")


if __name__ == '__main__':
    main()
