# Using ZeroR to predict if a student will graduate or not

"""
___authors___: Zhiwei Yang
"""

import pandas as pd
import numpy as np
#import StratifyAndGenerateDatasets as sd
from sklearn import metrics
from sklearn.metrics import confusion_matrix, roc_auc_score, recall_score, precision_score, accuracy_score
import copy

GRAPH_FILE_PREFIX = 'graph_term_'
STRATIFIED_DATA_PATH = 'data\\test_train\\'
RESULTS_FOLDER = 'ZeroR_Results\\'


#  Iterate through all possible training/testing files and store them in appropriate arrays.
def get_training_testing(term, number):
    return pd.read_csv(STRATIFIED_DATA_PATH + term + '_term_train_' + str(number) + '.csv'),\
           pd.read_csv(STRATIFIED_DATA_PATH + term + '_term_test_' + str(number) + '.csv') # looping through each fold


flatten = lambda l: [item for sublist in l for item in sublist] # equivalent to numpy.reshape(-1, 1)


def zr_predict():
    np.random.seed(313131)
    counter = 1
    all_actual = []
    all_probs = []

    for term in ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']:
        test_total = None
        prediction_array = np.zeros(0)
        target = np.ones(0)
        for set in range(1, 6):   # for 5 folds
            train, test = get_training_testing(term, set)
            nonz = np.count_nonzero(train['graduated'].values)          # Graduated Count
            train_size = train['graduated'].values.size
            probability = nonz/train_size
            temp_predict_array = np.full_like(test['graduated'].values, probability, dtype=np.double)

            if probability < 0.5:
                prediction_array = np.concatenate((prediction_array, temp_predict_array), axis=0)
                target = np.concatenate((target, test['graduated']), axis=0)    # Add prediction
            else:
                prediction_array = np.concatenate((prediction_array, temp_predict_array), axis=0)
                target = np.concatenate((target, test['graduated']), axis=0)    # Add prediction
        del train, test
        predictions = pd.DataFrame.from_records(prediction_array.reshape(-1,1), columns=['prob of grad'])
        del set
        for set in range(1, 6):     # Get all the training set
            train, test = get_training_testing(term, set)
            if set == 1:
                test_total = test
            else:
                test_total = pd.concat([test_total, test], axis=0, ignore_index=True)

        del set

        final = pd.concat([test_total, predictions], axis=1)
        final.to_csv(RESULTS_FOLDER + 'most_frequent_prediction_output\\term_' + str(counter) + '.csv', index=False)
                        # Save results
        actual = final['graduated'].values
        all_actual += list(actual)
        probs = final['prob of grad'].values
        all_probs += list(probs)

        auc = metrics.roc_auc_score(actual, probs)
        acc = metrics.accuracy_score(actual, round_school(probs))

        with open(RESULTS_FOLDER + 'MostFrequent' + str(counter) + '.txt', "w") as text_file:
            text_file.write(
                'AUC = ' + str(auc) + ', Accuracy = ' + str(acc))

        counter += 1

        # tn, fp, fn, tp =confusion_matrix(target, prediction_array).ravel()      # Decompose confusion matrix
        # print()
        # print(str(term) + ' term result:')
        # print('true negative: ', tn, '\nfalse positive: ', fp, '\nfalse negative: ', fn, '\ntrue positive: ', tp)
        # print('Precision score: ', precision_score(target, prediction_array))
        # print('Recall score: ', recall_score(target, prediction_array))
        # print('ROC_AUC score:' + str(roc_auc_score(target, prediction_array)))
        # print('Accuracy score:' + str(accuracy_score(target, prediction_array)))
    auc = metrics.roc_auc_score(all_actual, all_probs)
    acc = metrics.accuracy_score(all_actual, round_school(all_probs))

    with open(RESULTS_FOLDER + 'MostFrequent__all' + '.txt', "w") as text_file:
        text_file.write(
            'AUC = ' + str(auc) + ', Accuracy = ' + str(acc))    # Save results for AUC and Accuracy.


# https://stackoverflow.com/a/43886290
def round_school(x_list):
    temp_list = []
    for x in x_list:
        if x < 0:
            return 0
        else:
            i, f = divmod(x, 1)
            temp_list.append(int(i + ((f >= 0.5) if (x > 0) else (f > 0.5))))
    return temp_list


if __name__ == "__main__":
    zr_predict()