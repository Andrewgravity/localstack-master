import os

dir = os.getcwd() + '/metrics/'
files = os.listdir(dir)
csv_files = list(filter(lambda f: f.endswith('.csv'), files))

def upload_file(file):
    os.system(f'aws s3 cp metrics/{file} s3://my-bucket --endpoint-url=http://localhost:4566')
    return f"{file} uploaded to metrics successfully!"

for file in csv_files:
    upload_file(file)
    break