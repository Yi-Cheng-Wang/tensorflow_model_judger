# This is an example where you must define an 'evaluate' function.
# It takes a 'file_name' as input and returns a score.
# Place any resources you need in this folder

import os
import tensorflow as tf
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def evaluate(file_name):
    model = tf.keras.models.load_model(file_name)
    xs, ys = prepare_data()
    predictions = model.predict(xs, verbose=0)
    score = judger(predictions, ys)
    return score

def judger(predictions, ansers):
    score = 0
    tem = 0
    counter = 0
    for i in predictions:
        tem = ansers[counter] - i[0]
        counter = counter + 1
        if (tem < 0) :
            tem = tem * -1
        if (tem > 100) :
            continue
        score = score + (100 - tem)/100
    score = score*(100/counter)
    return score


def prepare_data():
    xs = np.array([1, 2,  3,  4, 5, 6, 100000],  dtype=float)
    ys = np.array([1.0, 1.5,  2.0,  2.5, 3.0, 3.5, 50000.5],  dtype=float)
    return xs, ys

if __name__ == '__main__':
    print('evaluate: This file should not be __main__.')
