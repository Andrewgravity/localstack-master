from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col
from pyspark.sql.functions import max, avg, min, count
from pyspark.sql.functions import lit
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
from pyspark.sql.functions import when
import configparser
import os

config = configparser.ConfigParser()
config.read('/opt/airflow/airflow.cfg')
dag_path = config['core']['dags_folder']
all_files = os.listdir(f'{dag_path}/data')
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))

master = "spark://spark:7077"
conf = SparkConf().setAppName("Spark_job_metrics_app")

sc = SparkContext(conf=conf)
spark = SparkSession.builder.config(conf=conf).getOrCreate()


for file in csv_files:
    df = spark.read.options(inferSchema=True, header=True).csv(f"{dag_path}/data/{file}")
    departure_name = df.withColumnRenamed("departure_name","name").groupBy("name").agg(count("departure").alias("departure_count"))
    return_name = df.withColumnRenamed("return_name","name").groupBy("name").agg(count("departure").alias("return_count"))
    merged = departure_name.toPandas().merge(return_name.toPandas(), how='outer')
    merged.to_csv('metrics_' + file.split(".")[0] + '.csv', index=False)
    # departure_name.toPandas().to_csv('metrics_' + file.split(".")[0] + '_departure_name.csv')
    # return_name.toPandas().to_csv('metrics_' + file.split(".")[0] + '_return_name.csv')