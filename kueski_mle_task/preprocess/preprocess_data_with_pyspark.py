# coding: utf8
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DateType, DoubleType

from ..utils import log_time


@log_time
def preprocess_data_pyspark(raw_data_file: str, train_data_file: str) -> None:
    """Loads data from raw_data_file, preprocess it and save it in processed_data_file

    Args:
        raw_data_file: File path of raw data
        train_data_file: File path to save the processed data
    """

    spark = SparkSession.builder.getOrCreate()
    schema = StructType([
        StructField("loan_id", IntegerType()),
        StructField("id", IntegerType()),
        StructField("code_gender", StringType()),
        StructField("flag_own_car", StringType()),
        StructField("flag_own_realty", StringType()),
        StructField("cnt_children", IntegerType()),
        StructField("amt_income_total", DoubleType()),
        StructField("name_income_type", StringType()),
        StructField("name_education_type", StringType()),
        StructField("name_family_status", StringType()),
        StructField("name_housing_type", StringType()),
        StructField("days_birth", IntegerType()),
        StructField("days_employed", IntegerType()),
        StructField("flag_mobil", IntegerType()),
        StructField("flag_work_phone", IntegerType()),
        StructField("flag_phone", IntegerType()),
        StructField("flag_email", IntegerType()),
        StructField("occupation_type", StringType()),
        StructField("cnt_fam_members", IntegerType()),
        StructField("status", IntegerType()),
        StructField("birthday", DateType()),
        StructField("job_start_date", DateType()),
        StructField("loan_date", DateType()),
        StructField("loan_amount", DoubleType()),
    ])
    spark_df = spark.read.csv(raw_data_file, header=True, schema=schema)

    spark_df = spark_df.sort(['id', 'loan_date'])
    spark_df_grouped_by_id = spark_df.groupby("id")

    # Feature nb_previous_loans
    spark_df = spark_df.withColumn('nb_previous_loans', spark_df['status'])
    spark_df = spark_df_grouped_by_id.applyInPandas(lambda group: group.assign(nb_previous_loans=range(len(group))),
                                                    schema=spark_df.schema)

    # Feature avg_amount_loans_previous
    spark_df = spark_df.withColumn('avg_amount_loans_previous', spark_df['loan_amount'])
    spark_df = spark_df_grouped_by_id.applyInPandas(
        lambda group: group.assign(avg_amount_loans_previous=group['loan_amount'].expanding().mean()),
        schema=spark_df.schema)

    # Feature age
    spark_df = spark_df.withColumn('age', F.floor(F.datediff(F.to_date(F.lit(datetime.today())), 'birthday') / 365))
    spark_df = spark_df.withColumn('age', F.when(spark_df['age'] < 0, None).otherwise(spark_df['age']))

    # Feature years_on_the_job
    spark_df = spark_df.withColumn('years_on_the_job',
                                   F.floor(F.datediff(F.to_date(F.lit(datetime.today())), 'job_start_date') / 365))
    spark_df = spark_df.withColumn('years_on_the_job',
                                   F.when(spark_df['years_on_the_job'] < 0, None)
                                   .otherwise(spark_df['years_on_the_job']))

    # Feature flag_own_car
    flag_own_car_converter = F.udf(lambda x: 0 if x == 'N' else 1, IntegerType())
    spark_df = spark_df.withColumn('flag_own_car', flag_own_car_converter('flag_own_car'))

    spark_df.collect()
    spark_df.write.csv(train_data_file)
