# coding: utf8
from typing import List

import pandas as pd

from ..utils import log_time


@log_time
def preprocess_data_pandas(raw_data_file: str, features_file: str, cols_to_save: List[str]) -> None:
    """Loads data from raw_data_file, preprocess it and save it in processed_data_file

    Args:
        raw_data_file: File path of raw data
        features_file: File path to save the processed data
        cols_to_save: List of columns to save in features file
    """

    df = pd.read_csv(raw_data_file)

    df.sort_values(by=["id", "loan_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df["loan_date"] = pd.to_datetime(df['loan_date'], errors='coerce')
    df["birthday"] = pd.to_datetime(df['birthday'], errors='coerce')
    df["job_start_date"] = pd.to_datetime(df['job_start_date'], errors='coerce')

    df_grouped_by_id = df.groupby('id')

    # Feature nb_previous_loans
    df["nb_previous_loans"] = df_grouped_by_id["loan_date"].rank(method="first") - 1

    # Feature avg_amount_loans_previous
    df["avg_amount_loans_previous"] = df_grouped_by_id["loan_amount"].transform(lambda x: x.expanding().mean())

    # Feature age
    df['age'] = (pd.to_datetime('today').normalize() - df['birthday']).dt.days // 365

    # Feature years_on_the_job
    df['years_on_the_job'] = (pd.to_datetime('today').normalize() - df['job_start_date']).dt.days // 365

    # Feature flag_own_car
    df['flag_own_car'] = df.flag_own_car.apply(lambda x: 0 if x == 'N' else 1)

    df = df[cols_to_save]
    df.to_csv(features_file, index=False)
