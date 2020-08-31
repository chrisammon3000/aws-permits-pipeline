[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

aws-building-permits-pipeline
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
* AWS: Lambda, S3, RDS PostgreSQL, Parameter Store
* Serverless framework
* Python
* psycopg2
* PostGIS
* US Census Bureau [TIGER](https://en.wikipedia.org/wiki/Topologically_Integrated_Geographic_Encoding_and_Referencing) data for geocoding (*to be added*)

## Getting Started

### Prerequisites
The following should be installed:
* [awscli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
* [Serverless](https://www.serverless.com/framework/docs/getting-started/) framework
* [Docker](https://docs.docker.com/get-docker/)

### Setting up Environment
1. Clone this repo:
   ```
   git clone \
       --branch master --single-branch --depth 1 --no-tags \
       https://github.com/abk7777/building-permits-aws-pipeline.git
   ```

2. Install serverless-python-requirements plugin:
   ```
   cd aws-permits-pipeline
   npm install --save serverless-python-requirements
   ```
3. Run the script:
   ```
   bash scripts/set_parameters.sh
   ```
   *(optional)* Edit the file `scripts/set_parameters.sh` to set the parameters for the database name, username and password.
### Deploy AWS Infrastructure
1. Deploy the RDS stack with or without VPC:
   
   ```
   # RDS only
   aws cloudformation deploy --template-file cfn/rds.yml --capabilities CAPABILITY_NAMED_IAM --stack-name aws-permits-pipeline-1
   ```
   ```
   # RDS with VPC
   aws cloudformation deploy --template-file cfn/rds-vpc.yml --capabilities CAPABILITY_NAMED_IAM --stack-name aws-permits-pipeline-1
   ```

   Note: The serverlless.yml file contains a custom variable `cfn_stack` which references the CloudFormation `--stack-name` parameter and uses the format [**stack name**]-[**version**], for example *'aws-permits-pipeline-1'*. The version value should match in both the CloudFormation and Serverless .yml files.

2. Deploy Lambda functions with Serverless framework:
   ```
   cd src/functions
   serverless deploy
   ```

### Initialize the Database
   ```
   serverless invoke --function initDatabase --stage dev --region us-east-1 --log
   ```
   This installs the Postgres extensions for S3 import and PostGIS and creates a table `permits_raw`.

### Running the Pipeline
   The fetchData and loadData Lambda functions are scheduled to run once a day to fetch and load fresh data.
   ```
   serverless invoke --function fetchData --stage dev --region us-east-1 --log
   ```

### Accessing the database
   

   Open the notebook `0.1-building-permits-aws-pipeline` to run queries on the database and explore the data:
   ```
   cd notebooks
   jupyter notebook
   ```

### Cleaning up
*Under development*
## Contributors

**Primary (Contact) : [Gregory Lindsey](https://github.com/gclindsey)**

[contributors-shield]: https://img.shields.io/github/contributors/abk7777/building-permits-aws-pipeline.svg?style=flat-square
[contributors-url]: https://github.com/abk7777/building-permits-aws-pipeline/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/abk7777/building-permits-aws-pipeline.svg?style=flat-square
[forks-url]: https://github.com/abk7777/building-permits-aws-pipeline/network/members
[stars-shield]: https://img.shields.io/github/stars/abk7777/building-permits-aws-pipeline.svg?style=flat-square
[stars-url]: https://github.com/abk7777/building-permits-aws-pipeline/stargazers
[issues-shield]: https://img.shields.io/github/issues/abk7777/building-permits-aws-pipeline.svg?style=flat-square
[issues-url]: https://github.com/abk7777/building-permits-aws-pipeline/issues
[license-shield]: https://img.shields.io/github/license/abk7777/building-permits-aws-pipeline.svg?style=flat-square
[license-url]: https://github.com/abk7777/building-permits-aws-pipeline/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/gregory-lindsey/