# coding: utf8
import logging

from ..utils import read_yaml
from ..preprocess.preprocess_data_with_pyspark import preprocess_data_pyspark
from ..preprocess.preprocess_data_with_pandas import preprocess_data_pandas


class Pipeline:

    def __init__(self, config_file: str):
        self.config = read_yaml(config_file)

    def preprocess_data(self):
        raw_data_file = self.config['raw_data_file']
        train_data_file = self.config['train_data_file']

        if self.config['use_pyspark']:
            preprocess_data_pyspark(raw_data_file, train_data_file)
        else:
            preprocess_data_pandas(raw_data_file, train_data_file)

    def start_pipeline(self, preprocess_data: bool = False):

        if preprocess_data:
            self.preprocess_data()
