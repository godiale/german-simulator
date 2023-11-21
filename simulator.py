from collections import defaultdict
import pandas
import random
import datetime
import csv
import pyttsx3

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.xlsx"
STATS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter_Stats.csv"
DEFAULT_EXERCISE_SIZE = 20
LAST_TRIES_TO_CONSIDER = 5

PREFIXES = [
    'ab', 'an', 'auf', 'aus', 'be', 'ein', 'ent', 'er', 'emp',
    'ge', 'him', 'über', 'unter', 'ver', 'vor', 'zu'
]

NON_SPLITTABLE_ROOTS = ['geben', 'gehen']


def read_words_from_file(sheet):
    match sheet:
        case 'Verb':
            usecols = 'B,D,E,F,G'
            columns = ['word', 'translation', 'present', 'past1', 'past2']
        case 'Substantive':
            usecols = 'B,D,E,F'
            columns = ['word', 'translation', 'article', 'plural']
        case 'Adverb':
            usecols = 'B,D'
            columns = ['word', 'translation']
        case _:
            raise ValueError(f"Invalid sheet {sheet}")
    # noinspection PyTypeChecker
    df = pandas.read_excel(WORDS_STORE, sheet_name=sheet, header=None, usecols=usecols)
    df.columns = columns
    df = df[df.translation.notnull()]
    df.word = df.word.str.strip()
    df.drop_duplicates(subset='word')
    df = df.set_index('word', drop=False)
    return df


def append_stats_to_file(word, result):
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    result_str = '+' if result else '-'
    with open(STATS_STORE, "a", encoding='utf-8') as f:
        f.write(f'"{word}","{timestamp}","{result_str}"\n')


def read_stats_from_file():
    tries = defaultdict(list)
    times = defaultdict(list)
    with open(STATS_STORE, encoding='utf-8') as f:
        stats_reader = csv.reader(f)
        for row in stats_reader:
            tries[row[0]].append(1 if row[2] == '+' else 0)
            times[row[0]].append(datetime.datetime.fromisoformat(row[1]))
    return {v: {'tries': tries[v], 'times': times[v]} for v in tries.keys()}


def constant_weight_func(_stat):
    return 1.0


def last_fails_weight_func(stat, last_tries=LAST_TRIES_TO_CONSIDER):
    # weight: number of fails in horizon + avoid non-zero weights
    return last_tries - sum(stat['tries'][-last_tries:] if 'tries' in stat else {}) + 1


def create_word_groups(df, stats):
    r2v = defaultdict(list)
    for v in df.word.tolist():
        root = v
        while True:
            repeat = False
            for p in PREFIXES:
                if root.startswith(p) and root not in NON_SPLITTABLE_ROOTS:
                    root = root.removeprefix(p)
                    repeat = True
            if not repeat:
                break
        r2v[root].append(v)
    roots = list(r2v.keys())
    random.shuffle(roots)
    words = []
    for r in roots:
        if len(r2v[r]) > 1:
            words.extend(r2v[r])
    return df.loc[words]


def create_word_plain(df, stats):
    df['weights'] = list(map(last_fails_weight_func, map(lambda v: stats[v] if v in stats else {}, df.word.tolist())))
    df = df.loc[(df['weights'] > 0.0)]  # remove elements with zero probability
    df = df.sample(frac=1, weights='weights').reset_index(drop=True)  # random order
    regex = input("Enter words regex []: ")
    return df[df.word.str.contains(regex, na=False)]


def create_exercise(df, stats):
    mode = input("Enter mode (plain|group) [plain]: ")
    if mode == '':
        mode = 'plain'

    if mode == 'group':
        df = create_word_groups(df, stats)
    else:  # plain
        df = create_word_plain(df, stats)

    if len(df.index) > DEFAULT_EXERCISE_SIZE:
        exercise_size = input(f"Enter size of exercise: "
                              f"(1-{len(df.index)}) [{DEFAULT_EXERCISE_SIZE}]: ")
        if exercise_size == "":
            exercise_size = DEFAULT_EXERCISE_SIZE
        df = df.head(int(exercise_size))
    return df


def init_voice_engine():
    engine = pyttsx3.init()
    # noinspection PyTypeChecker
    for voice in engine.getProperty('voices'):
        if 'German' in voice.name:
            engine.setProperty('voice', voice.id)
    return engine


def main():
    voice_engine = init_voice_engine()

    word_type = input("Enter type ([V]erb|[S]ubstantive|[A]dverb) [Verb]: ")
    match word_type:
        case '' | 'V':
            word_type = 'Verb'
        case 'S':
            word_type = 'Substantive'
        case 'A':
            word_type = 'Adverb'

    check_forms = False
    if word_type == 'Verb':
        check_forms_input = input("Check verb forms (Yes|No) [No]: ")
        if check_forms_input == '':
            check_forms_input = 'No'
        check_forms = True if check_forms_input == 'Yes' else False

    df = read_words_from_file(word_type)
    stats = read_stats_from_file()

    df = create_exercise(df, stats)

    fail = 0
    failed_words = dict()

    for index, (_, row) in enumerate(df.iterrows()):
        stat = ''.join('+' if v else '-' for v in stats[row.word]['tries'][-5:]) if row.word in stats else ''
        voice_engine.say(row.word)
        voice_engine.runAndWait()
        input(f"{int(index)+1}. {row.word} ({stat})? ")
        print(f"    {row.translation}")
        if word_type == 'Substantive':
            print(f"    {row.article}")
        if check_forms and None not in (row.present, row.past1, row.past2):
            forms = f"{row.present}, {row.past1}, {row.past2}"
            print(f"    {forms}")
            voice_engine.say(forms)
            voice_engine.runAndWait()
        known = (input() == '')  # user hit Enter
        if not known:
            fail += 1
            failed_words[row.word] = row.translation
        append_stats_to_file(row.word, known)

    total = len(df.index)
    print(f"Pass={total-fail}, Fail={fail} (Total {total})")
    for word in sorted(failed_words.keys()):
        print(f'    {word:<20}  {failed_words[word]}')


if __name__ == '__main__':
    main()
