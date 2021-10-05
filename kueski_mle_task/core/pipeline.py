# coding: utf8
import os
from typing import List

import pandas as pd

from ..utils import read_yaml
from .model import train_model, load_model
from ..preprocess.preprocess_data_with_pandas import preprocess_data_pandas
from ..preprocess.preprocess_data_with_pyspark import preprocess_data_pyspark


class Pipeline:

    def __init__(self, config_file: str = 'config.yaml'):
        self.config = read_yaml(config_file)
        self.model = None
        self.features_data = None

    def preprocess_data(self):

        raw_data_file = self.config['raw_data_file']
        features_file = self.config['features_file']
        force_preprocess = self.config.get('force_preprocess', False)
        feature_cols = self.config['feature_cols']
        label_col = self.config['label_col']
        cols_to_save = ['id'] + feature_cols + [label_col]

        if os.path.exists(features_file) and not force_preprocess:
            print(f'Skipping preprocessing as {features_file} already exists. Set "force_preprocess: True" to ignore')
            return

        if self.config['use_pyspark']:
            preprocess_data_pyspark(raw_data_file, features_file, cols_to_save)
        else:
            preprocess_data_pandas(raw_data_file, features_file, cols_to_save)

    def train_model(self):

        train_data_file = self.config['train_data_file']
        feature_cols = self.config['feature_cols']
        label_col = self.config['label_col']
        model_file = self.config['model_file']
        test_size = self.config['test_size']
        random_state = self.config.get('random_state')
        force_train = self.config.get('force_train', False)

        if os.path.exists(model_file) and not force_train:
            print(f'Skipping model training as {model_file} already exists. Set "force_train: True" to override.')
            return

        train_model(train_data_file, feature_cols, label_col, model_file, test_size, random_state)

    def load_model(self):
        model_file = self.config['model_file']
        try:
            self.model = load_model(model_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model File {model_file} does not exist.")

    def predict(self, inputs: List[List[float]]) -> List[int]:
        return self.model.predict(inputs)

    def generate_prediction(self, input_file: str, output_file: str):

        if self.model is None:
            self.load_model()

        feature_cols = self.config['feature_cols']
        df = pd.read_csv(input_file).dropna()

        features = df[feature_cols].values.tolist()
        predictions = self.predict(features)

        df['predictions'] = predictions
        df.to_csv(output_file)

    def prepare_for_serving(self):
        self.load_model()
        self.features_data = pd.read_csv(self.config['features_file']).fillna(0)

    def get_features(self, user_ids: List[int]) -> List[List[float]]:
        """Returns features for the given user ids

        Args:
            user_ids: List user ids

        Returns: List of features for each user id. Empty list for non existent users

        """
        df = self.features_data
        feature_cols = self.config['feature_cols']
        features_list = []
        for user_id in user_ids:
            user_df = df[df['id'] == user_id][feature_cols]
            features = user_df[user_df['nb_previous_loans'] == user_df['nb_previous_loans'].max()].values.tolist()
            if features:
                features = features[0]
            features_list.append(features)

        return features_list

    def start_pipeline(self, preprocess_data: bool, train_model: bool, load_model: bool, generate_prediction: bool,
                       input_file: str, output_file: str):

        if preprocess_data:
            self.preprocess_data()

        if train_model:
            self.train_model()

        if load_model:
            self.load_model()

        if generate_prediction:
            self.generate_prediction(input_file, output_file)
