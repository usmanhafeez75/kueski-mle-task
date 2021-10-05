# coding: utf8
from typing import List
from joblib import dump, load

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score

from ..utils import log_time


@log_time
def train_model(train_data_file: str, feature_cols: List[str], label_col:str, model_file: str, test_size: float,
                random_state: int = None) -> None:
    """Trains the model and save it on the disk.

    Args:
        train_data_file: Training data csv file
        feature_cols: List of column names to be used as features
        label_col: Name of the label column
        model_file: The file path to save the model
        test_size: Fraction of the data to use for testing
        random_state: Random state to pass for train_test_split
    """

    df = pd.read_csv(train_data_file)
    df.fillna(0, inplace=True)

    labels = df[label_col].astype('int')
    features = df[feature_cols]

    # Using Synthetic Minority Over-Sampling Technique(SMOTE) to overcome sample imbalance problem.
    features_balance, labels_balance = SMOTE().fit_resample(features, labels)
    features_balance = pd.DataFrame(features_balance, columns=features.columns)

    x_train, x_test, y_train, y_test = train_test_split(features_balance, labels_balance, stratify=labels_balance,
                                                        test_size=test_size, random_state=random_state)

    model = RandomForestClassifier(n_estimators=5)

    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)

    print('Accuracy Score is {:.5}'.format(accuracy_score(y_test, y_predict)))
    print('Precision Score is {:.5}'.format(precision_score(y_test, y_predict)))
    print('Recall Score is {:.5}'.format(recall_score(y_test, y_predict)))
    print(pd.DataFrame(confusion_matrix(y_test, y_predict)))

    dump(model, model_file)


def load_model(model_file: str) -> RandomForestClassifier:
    """Loads model from the path and returns loaded model.

    Args:
        model_file: Path of the model file

    Returns:
        Model Object
    """

    return load(model_file)
