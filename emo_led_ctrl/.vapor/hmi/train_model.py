import numpy
from sklearn.model_selection import KFold

from emotiv.data_set import EmotivDataSet
from neural_network.neural_network import NeuralNetwork


def normalize(array, max):
    norm = lambda val: val / max
    vfunc = numpy.vectorize(norm)
    return vfunc(array)


if __name__ == '__main__':
    print('=' * 70)
    print("Model Training")
    print('=' * 70)

    print('-' * 70)
    print("Loading set ...")
    X, y = EmotivDataSet().get_set()
    print("Loaded. Shape:")
    print(X.shape, y.shape)
    print('-' * 70)

    print('-' * 70)
    print("Normalizing")
    print(X.max())
    X = normalize(X, X.max())
    print("Set normalized")
    print('-' * 70)

    print('-' * 70)
    print("Constructing network")
    network = NeuralNetwork(X.shape[1])
    print('-' * 70)

    print('-' * 70)
    print("2-Fold Evaluation:")

    kf = KFold(n_splits=2, shuffle=True, random_state=0)

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print("Training")
        network.train(X_train, y_train, verbose=True)
        print("Evaluating")
        result = network.evaluate(X_test, y_test, verbose=True)
        print("Acc:", result)

    print('-' * 70)

    print('-' * 70)
    print("Saving model")
    network.save_model()
    print('-' * 70)

    print('=' * 70)
    print("Done")
    print('=' * 70)
