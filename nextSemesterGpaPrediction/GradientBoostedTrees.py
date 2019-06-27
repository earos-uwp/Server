"""
___authors___: Nate Braukhoff and Zhiwei Yang and Austin FitzGerald
"""
from sklearn import metrics
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
import math
import urllib.request
import BaseDataSetGenerator as bd

RESULTS_FOLDER = 'GBTRegressorResults\\'
GRAPH_FILE_PREFIX = 'graphs\\graph_'
RESULTS_TEXTFILE = 'GBTRegressor_Results.txt'
PREDICTION_OUTPUT_PREFIX = 'predictions'


def get_training_testing():
    # Creating arrays that contain arrays holding the testing and training data. Reshaped to form a 1 row multi
    # column array
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    for i in range(0, bd.NUMBER_OF_FOLDS):
        X_train.append(pd.read_csv('data\\test_train\\train_' + str(i + 1) + '.csv')['prev GPA'].values.reshape(-1, 1))
        y_train.append(
            pd.read_csv('data\\test_train\\train_' + str(i + 1) + '.csv')['current GPA'].values.reshape(-1, 1))
        X_test.append(pd.read_csv('data\\test_train\\test_' + str(i + 1) + '.csv')['prev GPA'].values.reshape(-1, 1))
        y_test.append(pd.read_csv('data\\test_train\\test_' + str(i + 1) + '.csv')['current GPA'].values.reshape(-1, 1))

    return X_train, y_train, X_test, y_test


def gbt_predict(X_train, y_train, X_test, y_test):
    np.random.seed(bd.RANDOM_SEED)
    model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_features=1, max_depth=4, loss='ls',
                                      random_state=bd.RANDOM_SEED)

    # hold all tests and predictions in order to calculate R^2 AND RMSE.
    y_tests = []
    y_preds = []

    for i in range(0, bd.NUMBER_OF_FOLDS):
        # fitting the model and storing the predicted value from the test set
        model.fit(X_train[i], y_train[i])
        y_pred = model.predict(X_test[i])

        y_tests += list(y_test[i])  # the real value
        y_preds += list(y_pred)  # the predicted value

        plt.scatter(X_test[i], y_test[i], color='g', label='real')  # the real data from the tests, in green
        # plt.scatter(X_test[i], y_pred, color='r', label='predicted')  # the predicted data from the tests, in red
        plt.plot(X_test[i], model.predict(X_test[i]), color='k', label='predicted')  # the linear regression line
        plt.title('test #' + str(i + 1))
        plt.xlabel('Prev term GPA')
        plt.ylabel('Curr term GPA')
        plt.legend(loc='upper left')
        plt.savefig(RESULTS_FOLDER + GRAPH_FILE_PREFIX + str(i + 1))  # saving graphs
        plt.close()

    # Calculating the stats from the actual curr-term GPAs and predicted curr-term GPAs
    rr = metrics.r2_score(y_tests, y_preds)
    rmse = np.math.sqrt(metrics.mean_squared_error(y_tests, y_preds)) / 4

    # Saving the stats to a text file.
    with open(RESULTS_FOLDER + RESULTS_TEXTFILE, "w") as text_file:
        text_file.write( 'R^2 = ' + str(rr) + ', RMSE = ' + str(rmse))

    # save predictions (matching with tests) to files
    predictions = pd.DataFrame({'next term gpa prediction': y_preds})
    predictions.to_csv(RESULTS_FOLDER + PREDICTION_OUTPUT_PREFIX + '.csv', index=False)


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = get_training_testing()
    gbt_predict(X_train, y_train, X_test, y_test)
