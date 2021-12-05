import numpy as np
import pandas as pd
from dict_to_df import to_df
from get_data import getFood
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import warnings
warnings.filterwarnings("ignore")

# Single Decision Tree Classifier 
# Initial look: (Becker, Dinner, Hot Traditional)



def predict_menu(dinnerfood, features):
    tree = DecisionTreeClassifier()
    tree, items = train_decision_tree(dinnerfood, tree)
    preds = tree.predict([features])[0]
    menu_items = []
    for x in range(len(items)):
        if preds[x] == 1:
            menu_items.append(items[x])
    return menu_items


def train_decision_tree(dinnerfood, tree):
    data = to_df(dinnerfood)
    data['month'] = pd.DatetimeIndex(data['Date']).month
    data = encode(data, 'month', 12)
    data['date'] = pd.DatetimeIndex(data['Date']).day
    data = encode(data, 'date', 365)
    data['week_day'] = pd.DatetimeIndex(data['Date']).dayofweek
    data = encode(data, 'week_day', 7)
    X = data[['month_sin','month_cos','date_sin','date_cos', 'week_day_cos', 'week_day_sin']]
    Y= data.drop(columns=['month_sin','month_cos','date_sin','date_cos', 'week_day_cos', 'week_day_sin','month','date','week_day','Date','Day'])
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
    tree.fit(X_train, Y_train)
    tree_pred_train = tree.predict(X_train)
    tree_pred_test = tree.predict(X_test)

    print("Test Accuracy: ", accuracy_score(Y_test, tree_pred_test))
    print("Training Accuracy: ", accuracy_score(Y_train, tree_pred_train))

    return tree, Y.columns

def encode(df, col, max_val):
    df[col + '_sin'] = np.sin(df[col]*np.pi*2/max_val)
    df[col + '_cos'] = np.cos(df[col]*np.pi*2/max_val)
    return df

print(predict_menu(getFood(), [0.5,-0.866025,0.321270,0.946988,-0.974928,-0.222521]))