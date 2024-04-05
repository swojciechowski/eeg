import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

from joblib import dump

from sklearn.metrics import accuracy_score

data = pd.read_csv('dataset.csv', index_col=0)
print(data)

X = data.iloc[:, :-3].to_numpy(dtype=np.double)
y = data['CLASS'].to_numpy(dtype=int)

print(X.shape)

test = data['TRACK_ID'].to_numpy(dtype=bool)
train = np.invert(data['TRACK_ID'].to_numpy(dtype=bool))

y = LabelEncoder().fit_transform(y == 0)

# class_map = np.isin(y, [0, 2])
# X = X[class_map]
# y = y[class_map]
# test = test[class_map]
# train = train[class_map]

clf = Pipeline(
    [
        # ('prc', PCA()),
        ('clf', MLPClassifier(hidden_layer_sizes=(512))),
    ]
)

clf.fit(X[train], y[train])
y_pred = clf.predict(X[test])
print(accuracy_score(y[test], y_pred))

dump(clf, "model")