building-permits-aws-pipeline
==============================

An ETL pipeline for construction permits data from the [Los Angeles Open Data Portal](https://data.lacity.org/) hosted on AWS using  *Lambda*, *PostgreSQL RDS* with PostGIS, and *S3*. Running the pipeline fetches the data from the internet and loads it into an RDS instance running PostgreSQL/PostGIS.

## Background
Cited from [Building and Safety Permit Information](https://data.lacity.org/A-Prosperous-City/Building-and-Safety-Permit-Information-Old/yv23-pmwf):<br>
>*"The Department of Building and Safety issues permits for the construction, remodeling, and repair of buildings and structures in the City of Los Angeles. Permits are categorized into building permits, electrical permits, and mechanical permits"*

The raw permits data available from the [Los Angeles Open Data Portal](https://data.lacity.org/) contains missing latitude and longitude coordinates for some properties. The pipeline includes a geocoding step to enrich the data.

### Data source
Data can be downloaded directly here:<br>
https://data.lacity.org/api/views/yv23-pmwf/rows.csv?accessType=DOWNLOAD

## Built With
The pipeline is built on these frameworks and platforms:
* Lambda
* S3
* RDS (PostgreSQL with PostGIS extension)
* AWS Parameter Store
* US Census Bureau [TIGER](https://en.wikipedia.org/wiki/Topologically_Integrated_Geographic_Encoding_and_Referencing) data for geocoding
* Python
* [psycopg2](https://pypi.org/project/psycopg2/)

## Getting Started
*Under development*<br>

1. Edit the file `scripts/set_parameters.sh` to set the parameters for the database name, username and password. *(optional)*
2. Run the script:
   ```
   bash scripts/set_parameters.sh
   ```
3. Deploy the RDS stack:
   ```
   aws cloudformation deploy --template-file cfn/rds.yml --stack-name building-permits-aws-pipeline --capabilities CAPABILITY_IAM
   ```
4. Deploy Serverless stack:
   ```
   cd src/functions
   serverless deploy
   ```
5. Once the RDS instance is up and running, ping API Gateway to start the pipeline:
   ```
   curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/start
   ```



### Prerequisites
*Under development*

### Setting up Environment


### Running the Pipeline

  Option 1: Run the entire pipeline start to finish using GNU Make:
  ```
  make data
  ``` 

  Option 2: Load the raw data using GNU Make and run the rest of the pipeline from Jupyter Notebook:
  ```
  make load_db \
  && cd notebooks \
  && jupyter notebook ## Select 0.1-pipeline notebook
  ```

### Accessing the database
The PostgreSQL database within the Docker container can be accessed by running:
```
docker exec -it postgres_db psql -U postgres -d permits
```
It is useful to check that new columns were correctly populated by running a query such as:
```
SELECT full_address, latitude, longitude FROM permits_raw LIMIT 10;
```

### Cleaning up
A single command will delete the database as well as the Docker container and any cache files:
```
make tear_down
```


## Contributors

**Primary (Contact) : [Gregory Lindsey](https://github.com/gclindsey)**