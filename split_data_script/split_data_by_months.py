"""
Script for splitting csv file by months.
github reference: zaitsevv
"""
import pandas as pd

dataframe = pd.read_csv('../archive/database.csv', parse_dates=['departure'])

for group_name, group in dataframe.groupby(pd.Grouper(key='departure', freq='M')):
    group.to_csv('../airflow/dags/data/' + f'data_{group_name:%Y-%m}.csv', index=False)