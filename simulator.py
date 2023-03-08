from pandas_ods_reader import read_ods

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.ods"


def read_verbs():
    df = read_ods(WORDS_STORE, "Verben", headers=False,
                  columns=['a', 'verb', 'b', 'translation'])\
        .drop(columns=['a', 'b'])
    return df[df.translation.notnull()]


def main():
    df = read_verbs()
    df = df.sample(frac=1).reset_index(drop=True)  # random order

    prefix = input("Enter prefix verbs: ")

    total, fail = 0, 0

    for index, row in df.iterrows():
        if not prefix or row.verb.startswith(prefix):
            total += 1
            input(f"{row.verb} ? ")
            print(f"    {row.translation}")
            known = input()
            if known != '':  # user hit Enter
                fail += 1

    print(f"Pass={total-fail}, Fail={fail} (Total {total})")


if __name__ == '__main__':
    main()
