import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# Single Decision Tree Classifier 
# Initial look: (Becker, Dinner, Hot Traditional)

def MultiOutputModel(df):
    mlb = MultiLabelBinarizer()
    X = df[['Date','Day']]
    Y=pd.DataFrame(mlb.fit_transform(df.drop(columns=X).values), columns=mlb.classes_, index=df.index)

    tree = DecisionTreeClassifier()

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

    tree.fit(X_train, Y_train)

    tree_pred_train = tree.predict(X_train)
    tree_pred_test = tree.predict(X_test)

    return tree_pred_train, tree_pred_test

    print("Test Accuracy: ", accuracy_score(Y_test, tree_pred_test))
    print("Training Accuracy: ", accuracy_score(Y_train, tree_pred_train))



