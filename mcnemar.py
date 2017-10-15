import numpy as np
from statsmodels.sandbox.stats.runs import mcnemar

def build_contingency_table(y, y_a, y_b):
    '''
    Given true labels and prdictions from two binary classifiers a, b,
    build a 2 x 2 contignecny table:
                 | b Correct | b Incorrect
    _____________|___________|____________
    a Correct    |  n_11     |  n_12
    a Incorrect  |  n_21     |  n_22
    in the format [[n11, n12],[n21, n22]]
    '''
    if len(y) != len(y_a) or len(y)!= len(y_b):
        raise Exception('Input labels have different length')

    correct_incorrect_arr = [
        [
            (predictions[i]==label, predictions[i]!=label)
            for i, label in enumerate(y)
        ] for predictions in (y_a, y_b)
    ]

    contigency_matrix =[]
    for i in [0,1]:
        contigency_matrix.append([])
        for j in [0,1]:
            contigency_matrix[i].append(
                np.sum(
                    np.multiply(
                        [v[i] for v in correct_incorrect_arr[0]],
                        [v[j] for v in correct_incorrect_arr[1]]
                    )
                )
            )
    return contigency_matrix

def mcnemar_test(y, y_a, y_b):
    '''
    Given true labels and predictions from two binary classifiers a, b,
    perfrom McNemar test on the these predictions
    Return (chi2, p): Chi2 of the test statistic, p-value of the null hypothesis
    '''
    chi2, p = mcnemar(build_contingency_table(y, y_a, y_b))
    print('Chi2 = {}, P = {}'.format(chi2, p))
    return chi2, p
