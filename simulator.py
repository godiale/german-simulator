from pandas_ods_reader import read_ods

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.ods"
SMALLEST_EXERCISE = 20


def read_verbs_from_file():
    df = read_ods(WORDS_STORE, "Verben", headers=False,
                  columns=['a', 'verb', 'b', 'translation'])\
        .drop(columns=['a', 'b'])
    return df[df.translation.notnull()]


def create_exercise(df):
    df = df.sample(frac=1).reset_index(drop=True)  # random order
    regex = input("Enter words regex: ")
    df = df[df.verb.str.contains(regex)]
    if len(df.index) > SMALLEST_EXERCISE:
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
