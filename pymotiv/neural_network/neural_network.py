import os

from keras.models import Model, model_from_json
from keras.optimizers import SGD
from keras.layers import Dense, Input
from keras.utils import plot_model

file_loc = os.path.dirname(os.path.realpath(__file__))
DEFAULT_MODEL_PATH = os.path.join(file_loc, '..', '..', 'model')


class NeuralNetwork:
    def __init__(self, inputs=1):

        layer_inputs = Input([inputs])
        layer_hidden = Dense(inputs * 3, activation='relu')(layer_inputs)
        layer_outputs = Dense(1, activation='sigmoid')(layer_hidden)

        self.model = Model(inputs=layer_inputs, outputs=layer_outputs)

        sgd = SGD(momentum=0.9, nesterov=False)
        self.model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

    def train(self, data, classes, verbose=False):
        self.model.fit(data, classes, verbose=verbose, batch_size=10, epochs=100)

    def evaluate(self, data, classes, verbose=False):
        return self.model.evaluate(data, classes, verbose=verbose)[1]

    def classify(self, features_data):
        return self.model.predict(features_data.reshape((1, len(features_data))))

    def save_model(self, path=DEFAULT_MODEL_PATH):
        with open(os.path.join(path, "model.json"), "w") as json_file:
            json_file.write(self.model.to_json())
        self.model.save_weights(os.path.join(path, "model.h5"))

    def load_model(self, path=DEFAULT_MODEL_PATH):
        with open(os.path.join(path, "model.json"), 'r') as json_file:
            self.model = model_from_json(json_file.read())
        self.model.load_weights(os.path.join(path, "model.h5"))

    def print_model(self, path=DEFAULT_MODEL_PATH):
        plot_model(self.model, to_file=os.path.join(path, 'model.png'), show_shapes=True, show_layer_names=False)
