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

    def preprocess_data(self):

        raw_data_file = self.config['raw_data_file']
        train_data_file = self.config['train_data_file']
        force_preprocess = self.config.get('force_preprocess', False)

        if os.path.exists(train_data_file) and not force_preprocess:
            print(f'Skipping preprocessing as {train_data_file} already exists. Set "force_preprocess: True" to ignore')
            return

        if self.config['use_pyspark']:
            preprocess_data_pyspark(raw_data_file, train_data_file)
        else:
            preprocess_data_pandas(raw_data_file, train_data_file)

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

    def predict(self, inputs: List[list]) -> List[int]:
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
