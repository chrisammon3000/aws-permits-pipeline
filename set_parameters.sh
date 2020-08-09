#!/usr/bin/env bash

aws ssm put-parameter \
  --name /permits/db_name \
  --type String \
  --value "permits-data" \
  --description "Database name" \
  --overwrite

aws ssm put-parameter \
  --name /permits/db_user \
  --type String \
  --value "postgres" \
  --description "Database username" \
  --overwrite

aws ssm put-parameter \
  --name /permits/db_password \
  --type SecureString \
  --value "5up3r53cr3tPa55w0rd" \
  --description "Database password" \
  --overwrite

# Get parameters from Parameter Store
aws ssm get-parameter \
  --name /permits/db_name \
  #--query Parameter.Value

aws ssm get-parameter \
  --name /permits/db_user \
  #--query Parameter.Value

aws ssm get-parameter \
  --with-decryption \
  --name /permits/db_password \
  #--query Parameter.Value
