Create a .env in airflow folder with these variables: </br>
AIRFLOW_UID=501</br>
AIRFLOW_GID=0</br>

initiate airflow ``docker-compose airflow db init``</br>
navigate to spark folder and execute ``docker build -t cluster-apache-spark:3.0.2 .``</br>
go to airflow folder and run ``docker-compose up`` to start all the containers</br>
to access the spark-master go to **http://localhost:9090/**</br>
to access the spark-worker 1 and 2 go to **http://localhost:9091/** and **http://localhost:9092/** accordingly </br>
you can access airflow via **http://localhost:8080/**</br>
login: **airflow**</br>
password: **airflow**</br>
to split the 2gb csv into small files for each month navigate to split_data_script folder and run ``python split_data_by_months.py``</br>




