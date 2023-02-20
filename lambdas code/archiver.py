import os
import concurrent.futures

files = ['load_file_to_daily_metrics_table','load_file_to_metrics_table',
         'load_file_to_monthly_metrics_table','load_file_to_raw_table']

def compress_file(file):
    os.system(f'zip -r {file}.zip {file}')
    return f"{file} compressed successfully!"

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(compress_file, file) for file in files]

    for f in concurrent.futures.as_completed(results):
        print(f.result())