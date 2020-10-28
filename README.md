[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

aws-permits-pipeline
==============================

An ETL pipeline for construction permits data from the [Los Angeles Open Data Portal](https://data.lacity.org/) hosted on AWS using  Lambda, RDS PostgreSQL, and S3. Once deployed the pipeline fetches fresh data once a day from the internet and loads it into an RDS instance running PostgreSQL/PostGIS. 

## Background
Cited from [Building and Safety Permit Information](https://data.lacity.org/A-Prosperous-City/Building-and-Safety-Permit-Information-Old/yv23-pmwf):<br>
>*"The Department of Building and Safety issues permits for the construction, remodeling, and repair of buildings and structures in the City of Los Angeles. Permits are categorized into building permits, electrical permits, and mechanical permits"*

The raw permits data available from the [Los Angeles Open Data Portal](https://data.lacity.org/) contains information on building and construction permits for both residential and commercial properties. 

### Data source
Data can be downloaded directly here (~500MB):<br>
https://data.lacity.org/api/views/yv23-pmwf/rows.csv?accessType=DOWNLOAD

## Built With
The pipeline is built on these frameworks and platforms:
* AWS: Lambda, S3, RDS PostgreSQL, Parameter Store
* CloudFormation
* Serverless framework
* Python
* psycopg2
* PostGIS

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
       https://github.com/abk7777/aws-permits-pipeline.git
   ```

2. Install serverless-python-requirements plugin:
   ```
   cd aws-permits-pipeline &&
   npm install --save serverless-python-requirements
   ```
3. Run the script:
   ```
   bash scripts/set_parameters.sh
   ```
   *(optional)* Edit the file `scripts/set_parameters.sh` to set your own parameters for the database name, username and password.

### Deploy AWS Infrastructure
These instructions will deploy a stack named `aws-permits-pipeline` or `aws-permits-pipeline-vpc` using AWS CloudFormation. Note that the `--stack-name` parameter must match the `service` variable in `serverless.yml` so that Serverless can import the CloudFormation output values:

1. Deploy the RDS stack with or without VPC & read replica:
   
   ```
   # RDS only (deploys fastest)
   aws --region us-east-1 cloudformation deploy \
   --template-file cfn/rds.yml \
   --capabilities CAPABILITY_NAMED_IAM \
   --stack-name aws-permits-pipeline
   ```
   ```
   # RDS with VPC & read replica
   aws --region us-east-1 cloudformation deploy \
   --template-file cfn/rds-vpc.yml \
   --capabilities CAPABILITY_NAMED_IAM \
   --stack-name aws-permits-pipeline-vpc
   ```
   If deploying RDS only without the VPC you will need to update the default VPC's security group to allow connections on port 5432. This can be done through the AWS RDS and EC2 console. Deploying RDS with VPC can take a while since it provisions two instances instead of just one.

2. Deploy Lambda functions with Serverless framework:
   ```
   cd src/functions &&
   serverless deploy
   ```

### Initialize the Database
   ```
   serverless invoke --function initDatabase \
   --stage dev \
   --region us-east-1 \
   --log
   ```
   This installs the Postgres extensions for S3 import and PostGIS and creates a table `permits_raw`.

### Running the Pipeline
   The fetchData and loadData Lambda functions are scheduled to run once a day to fetch and load fresh data.
   ```
   serverless invoke --function fetchData \
   --stage dev \
   --region us-east-1 \
   --log
   ```

### Accessing the database
Once the instance is running any SQL client such as `psql` can access the database on port 5432 using the parameters specified in `set_parameters.sh`. To retrieve the endpoint:
   
   ```
   aws cloudformation describe-stacks \
   --stack-name aws-permits-pipeline \
   --query "Stacks[0].Outputs[?OutputKey=='MasterEndpointDB'].OutputValue" \
   --output text
   ```

   Using `psql`:
   ```
   psql -h <MasterEndpointDB> -U postgres -p 5432 -d permitsDB
   ```

### Cleaning up
1. Delete the Serverless stack:
   ```
   serverless remove
   ```
   
2. Get the S3 data bucket name:
   ```
   aws cloudformation describe-stacks \
   --stack-name aws-permits-pipeline \
   --query "Stacks[0].Outputs[?OutputKey=='DataBucket'].OutputValue" \
   --output text
   ```
   
3. Delete all data from the S3 bucket:
   ```
   aws s3 rm --recursive s3://<your_bucket_name>
   ```
4. Delete the CloudFormation stack:
   ```
   aws cloudformation delete-stack \
   --stack-name aws-permits-pipeline
   ```
   
## Contributors

**Primary (Contact) : [Gregory Lindsey](https://github.com/gclindsey)**

[contributors-shield]: https://img.shields.io/github/contributors/abk7777/aws-permits-pipeline.svg?style=flat-square
[contributors-url]: https://github.com/abk7777/aws-permits-pipeline/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/abk7777/aws-permits-pipeline.svg?style=flat-square
[forks-url]: https://github.com/abk7777/aws-permits-pipeline/network/members
[stars-shield]: https://img.shields.io/github/stars/abk7777/aws-permits-pipeline.svg?style=flat-square
[stars-url]: https://github.com/abk7777/aws-permits-pipeline/stargazers
[issues-shield]: https://img.shields.io/github/issues/abk7777/aws-permits-pipeline.svg?style=flat-square
[issues-url]: https://github.com/abk7777/aws-permits-pipeline/issues
[license-shield]: https://img.shields.io/github/license/abk7777/aws-permits-pipeline.svg?style=flat-square
[license-url]: https://github.com/abk7777/aws-permits-pipeline/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/gregory-lindsey/
