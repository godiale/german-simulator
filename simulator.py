from pandas_ods_reader import read_ods
import os

WORDS_STORE = "C:/Users/godiale/Dropbox/Deutsch/Deutsche_Worter.ods"


def clear_viewport():
    os.system('cls')


def read_verbs():
    df = read_ods(WORDS_STORE, "Verben", headers=False,
                  columns=['a', 'verb', 'b', 'translation'])\
        .drop(columns=['a', 'b'])
    return df[df.translation.notnull()]


def main():
    df = read_verbs()

    prefix = input("Enter prefix verbs: ")

    for index, row in df.iterrows():
        if not prefix or row.verb.startswith(prefix):
            clear_viewport()
            input(f"{row.verb} ?")
            print(f"    {row.translation}")
            input()


if __name__ == '__main__':
    main()
