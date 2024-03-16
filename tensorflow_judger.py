import tensorflow as tf
import numpy as np

def prepare_data():
    xs = np.array([1, 2,  3,  4, 5, 6, 100000],  dtype=float)
    ys = np.array([1.0, 1.5,  2.0,  2.5, 3.0, 3.5, 50000.5],  dtype=float)
    return xs, ys

def score(predictions, ansers):
    score = 0
    tem = 0
    counter = 0
    for i in predictions[0]:
        tem = ansers[counter] - i
        counter = counter + 1
        if (tem < 0) :
            tem = tem * -1
        if (tem**2 > 10) :
            continue
        score = score + (10 - tem**2)/10
    score = score*(100/counter)
    return score

def judger(file_name):
    model = tf.keras.models.load_model(file_name)
    xs, ys = prepare_data()
    predictions = model.predict(xs)
    result = score(predictions, ys)
    return result

if __name__ == '__main__':
    print('tensorflow_judger: This file should not be __main__.')