from pandas_ods_reader import read_ods
from collections import defaultdict
import random
import datetime
import csv

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.ods"
STATS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter_Stats.csv"
DEFAULT_EXERCISE_SIZE = 20

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


def append_stats_to_file(word, result):
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    result_str = '1' if result else '0'
    with open(STATS_STORE, "a", encoding='utf-8') as f:
        f.write(f'"{word}","{timestamp}","{result_str}"\n')


def read_stats_from_file():
    stats = defaultdict(list)
    with open(STATS_STORE, encoding='utf-8') as f:
        stats_reader = csv.reader(f)
        for row in stats_reader:
            stats[row[0]].append(row[2])
    return stats


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

    if len(df.index) > DEFAULT_EXERCISE_SIZE:
        exercise_size = input(f"Enter size of exercise: "
                              f"(1-{len(df.index)}) [{DEFAULT_EXERCISE_SIZE}]: ")
        if exercise_size == "":
            exercise_size = DEFAULT_EXERCISE_SIZE
        df = df.head(int(exercise_size))
    return df


def main():
    df = read_verbs_from_file()
    df = create_exercise(df)

    stats = read_stats_from_file()

    fail = 0

    for index, row in df.iterrows():
        stat = ''.join(stats[row.verb]).replace('1', '+').replace('0', '-')[:5]
        input(f"{row.verb} ({stat})? ")
        print(f"    {row.translation}")
        known = (input() == '')  # user hit Enter
        if not known:
            fail += 1
        append_stats_to_file(row.verb, known)

    total = len(df.index)
    print(f"Pass={total-fail}, Fail={fail} (Total {total})")


if __name__ == '__main__':
    main()
