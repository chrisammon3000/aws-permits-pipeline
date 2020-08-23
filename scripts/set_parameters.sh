#!/usr/bin/env bash

aws ssm put-parameter \
  --name /permits/db_name \
  --type String \
  --value "permitsDB" \
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
  --value "postgres5ecret" \
  --description "Database password" \
  --overwrite

aws ssm put-parameter \
  --name /permits/alert_phone \
  --type String \
  --value "+15623316631" \
  --description "permits RDS alert SMS phone number" \
  --overwrite

aws ssm put-parameter \
  --name /permits/alert_email \
  --type String \
  --value "gclindsey@gmail.com" \
  --description "permits RDS alert email" \
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

aws ssm get-parameter \
  --name /permits/alert_phone \
  #--query Parameter.Name

aws ssm get-parameter \
  --name /permits/alert_email \
  #--query Parameter.Name