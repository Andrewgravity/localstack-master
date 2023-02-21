</h1> Quick setup without airflow </h1>

Go to airflow dir nad run ``docker-compose up localstack`` (to run only localstack from docker-compose configuartion)</br>
Then navigate to terraform dir and run ``terraform init``, then ``terraform apply`` and type in ``yes``</br>
Wait for terraform to set up the aws infrastructure from the files and when it is done, run: </br>
``docker exec -it localstack_main /bin/bash`` </br>
``cd lambda-src`` </br>
From here run: </br>
``python upload_raw_data_to_s3`` </br>
Don't worry i put break so that it only uploads one file to s3. </br>
By the way, you can checkout the bucket by navigating to **http://localhost:4566/my-bucket** (if i remember correctly) </br>
You can also check one of the dynamodb tables by running this in docker container aws shell: </br>
``aws dynamodb scan --table-name {table_name} --endpoint-url=http://localhost:4566`` </br>
instead of ``{table_name}`` input my_raw_table, my_daily_metrics_table or my_monthly_metrics_table (anyway they should be empty cause lambda returns an error)

</h2> Setting up Airflow (if you've got enough RAM, I don't :boar:) </h2>

Initiate airflow ``docker-compose airflow db init`` </br>
Go to airflow folder and run ``docker-compose up`` to start all the containers </br>
You can access airflow via **http://localhost:8080/** </br>
login: **airflow** </br>
password: **airflow** </br>
P.S. I've haven't provided the necessary csv files </br>
To split the 2gb csv into small files for each month navigate to split_data_script folder and run ``python split_data_by_months.py``</br>
While in airflow, start the localstack_project dag, which runs a spark job and then uploads all the files to s3. (this dag is named dag.py in dags folder, just for reference)




