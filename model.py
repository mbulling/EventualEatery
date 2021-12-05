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

def convert_features(date, day):
    month = int(date[5:7])
    date_of_month = int(date[8:10])
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday = days.index(day)
    pi = np.pi
    return [np.sin(month*pi*2/12), np.cos(month*pi*2/12), np.sin(date_of_month*pi*2/31), np.cos(date_of_month*pi*2/31), np.sin(weekday*pi*2/7), np.cos(weekday*pi*2/7)]

def predict_menu(dinnerfood, features):
    tree = DecisionTreeClassifier(max_depth=10)
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
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 42)
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

print(predict_menu(getFood(), convert_features('2018-05-19','Saturday')))