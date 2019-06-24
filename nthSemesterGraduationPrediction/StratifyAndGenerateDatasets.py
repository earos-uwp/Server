# Generating the stratified and k-fold training/testing data for each term type
"""
___authors___: Austin FitzGerald and Zhiwei Yang
"""

import pandas as pd
from sklearn.model_selection import StratifiedKFold

RANDOM_SEED = 313131
NUMBER_FOLDS = 5
NUM_TERMS = 3
TESTING_TRAINING_DATA_FOLDER = 'data\\test_train\\'
RAW_DATA_FIRST = 'data\\first_term.csv'
RAW_DATA_SECOND = 'data\\second_term.csv'
RAW_DATA_THIRD = 'data\\third_term.csv'
RAW_DATA_ARRAY = [RAW_DATA_FIRST, RAW_DATA_SECOND, RAW_DATA_THIRD]
FIRST_HEADERS = ['first term gpa', 'first term standing']
SECOND_HEADERS = ['first term gpa', 'first term standing', 'second term gpa', 'second term standing']
THIRD_HEADERS = ['first term gpa', 'first term standing', 'second term gpa', 'second term standing', 'third term gpa',
                 'third term standing']
HEADERS_ARRAY = [FIRST_HEADERS, SECOND_HEADERS, THIRD_HEADERS]
FILENAME_ARRAY = ['first_term_', 'second_term_', 'third_term_']
GRADUATED_HEADER = 'graduated'
TRAIN_PREFIX = 'train_'
TEST_PREFIX = 'test_'
FIRST_TERM = 0
SECOND_TERM = 1
THIRD_TERM = 2


def stratify_fold():
    for i in range(0, NUM_TERMS):

        term = pd.read_csv(RAW_DATA_ARRAY[i])  # reading each term file
        X = term[HEADERS_ARRAY[i]].copy().values  # each term file has a different headers array
        y = term[GRADUATED_HEADER].copy().values.reshape(-1, 1)  # reshape to one column

        skf = StratifiedKFold(n_splits=NUMBER_FOLDS, shuffle=True, random_state=RANDOM_SEED)

        loop_count = 0

        for train_index, test_index in skf.split(X, y):  # actually stratify and fold
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            # create a new training and testing csv for each fold of each term
            (pd.concat(
                [pd.DataFrame(X_train, columns=HEADERS_ARRAY[i]),
                 pd.DataFrame(y_train, columns=[GRADUATED_HEADER])],
                axis=1)).to_csv(TESTING_TRAINING_DATA_FOLDER + FILENAME_ARRAY[i] +
                                TRAIN_PREFIX + str(loop_count + 1) + '.csv', encoding='utf-8', index=False)

            (pd.concat(
                [pd.DataFrame(X_test, columns=HEADERS_ARRAY[i]),
                 pd.DataFrame(y_test, columns=[GRADUATED_HEADER])],
                axis=1)).to_csv(TESTING_TRAINING_DATA_FOLDER + FILENAME_ARRAY[i] +
                                TEST_PREFIX + str(loop_count + 1) + '.csv', encoding='utf-8', index=False)

            loop_count += 1


# https://stackoverflow.com/a/43886290
def round_school(x):
    if x < 0:
        return 0
    else:
        i, f = divmod(x, 1)
        return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))


if __name__ == "__main__":
    stratify_fold()
