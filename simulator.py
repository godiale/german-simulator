from pandas_ods_reader import read_ods
from collections import defaultdict
import random
import datetime
import csv
import pandas

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.ods"
STATS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter_Stats.csv"
DEFAULT_EXERCISE_SIZE = 20

PREFIXES = [
    'ab', 'an', 'auf', 'aus', 'be', 'ein', 'ent', 'er',
    'ge', 'him', 'über', 'unter', 'ver', 'vor', 'zu'
]


def read_words_from_file(sheet):
    df = read_ods(WORDS_STORE, sheet, headers=False,
                  columns=['a', 'word', 'b', 'translation'])\
        .drop(columns=['a', 'b'])
    df = df[df.translation.notnull()]
    df.word = df.word.str.strip()
    df.drop_duplicates(subset='word')
    df = df.set_index('word', drop=False)
    return df


def append_stats_to_file(word, result):
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    result_str = '1' if result else '0'
    with open(STATS_STORE, "a", encoding='utf-8') as f:
        f.write(f'"{word}","{timestamp}","{result_str}"\n')


def read_stats_from_file():
    tries = defaultdict(list)
    times = dict()
    with open(STATS_STORE, encoding='utf-8') as f:
        stats_reader = csv.reader(f)
        for row in stats_reader:
            tries[row[0]].append(row[2])
            times[row[0]] = row[1]
    stats = dict()
    for v in tries.keys():
        stats[v] = {'tries': ''.join(tries[v]),
                    'last_timestamp': datetime.datetime.fromisoformat(times[v])}
    return stats


def create_word_groups(df):
    r2v = defaultdict(list)
    for v in df.word.tolist():
        r2v[v].append(v)
        for p in PREFIXES:
            if v.startswith(p):
                r2v[v.removeprefix(p)].append(v)
    roots = list(r2v.keys())
    random.shuffle(roots)
    words = []
    for r in roots:
        if len(r2v[r]) > 1:
            words.extend(r2v[r])
    return df.loc[words]


# Move words, that were last 5 times correctly answered,
# and last question on the word was less than 5 days ago, to the end.
def move_down_known_words(df, stats):
    def is_known(word):
        if word not in stats:
            return False
        st = stats[word]
        return st['tries'].endswith('11111') and \
            datetime.datetime.now() - st['last_timestamp'] < datetime.timedelta(days=5)
    return pandas.concat([df.loc[~df.word.apply(is_known)],
                          df.loc[df.word.apply(is_known)]])


def create_exercise(df, stats):
    mode = input("Enter mode (plain|group) [plain]: ")
    if mode == '':
        mode = 'plain'

    if mode == 'group':
        df = create_word_groups(df)
    else:  # plain
        df = df.sample(frac=1).reset_index(drop=True)  # random order
        regex = input("Enter words regex: ")
        df = df[df.word.str.contains(regex)]
        df = move_down_known_words(df, stats)

    if len(df.index) > DEFAULT_EXERCISE_SIZE:
        exercise_size = input(f"Enter size of exercise: "
                              f"(1-{len(df.index)}) [{DEFAULT_EXERCISE_SIZE}]: ")
        if exercise_size == "":
            exercise_size = DEFAULT_EXERCISE_SIZE
        df = df.head(int(exercise_size))
    return df


def main():
    df = read_words_from_file('Verben')
    stats = read_stats_from_file()

    df = create_exercise(df, stats)

    fail = 0

    for index, (_, row) in enumerate(df.iterrows()):
        stat = stats[row.word]['tries'].replace('1', '+').replace('0', '-')[:5] \
            if row.word in stats else ''
        input(f"{index+1}. {row.word} ({stat})? ")
        print(f"    {row.translation}")
        known = (input() == '')  # user hit Enter
        if not known:
            fail += 1
        append_stats_to_file(row.word, known)

    total = len(df.index)
    print(f"Pass={total-fail}, Fail={fail} (Total {total})")


if __name__ == '__main__':
    main()
