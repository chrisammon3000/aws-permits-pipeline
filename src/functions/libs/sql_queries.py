# INSTALL EXTENSIONS
install_ext_aws_s3 = "CREATE EXTENSION aws_s3 CASCADE;"

# Don't forget to set up IAM permissions in CLI

install_ext_postgis = ("""
    SELECT current_user;
    CREATE EXTENSION postgis;
    CREATE EXTENSION fuzzystrmatch;
    CREATE EXTENSION postgis_tiger_geocoder;
    CREATE EXTENSION postgis_topology;
    ALTER SCHEMA tiger owner TO rds_superuser;
    ALTER SCHEMA tiger_data owner TO rds_superuser;
    ALTER SCHEMA topology owner TO rds_superuser;
    CREATE FUNCTION exec(text) RETURNS text 
        LANGUAGE plpgsql volatile 
        AS $f$ 
    BEGIN 
        EXECUTE $1; 
        RETURN $1; 
    END; $f$;
    SELECT exec('ALTER TABLE ' || quote_ident(s.nspname) || '.' || quote_ident(s.relname) || ' OWNER TO rds_superuser;')
    FROM (
        SELECT nspname, relname
        FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid) 
        WHERE nspname in ('tiger','topology') AND
        relkind IN ('r','S','v') ORDER BY relkind = 'S')
    s;
    SET search_path=public,tiger;
""")

test_postgis_tiger_query = ("""
    select na.address, na.streetname, na.streettypeabbrev, na.zip
    from normalize_address('1 Devonshire Place, Boston, MA 02109') as na;
""")

test_postgis_tiger_output = "1 Devonshire Pl 02109"

# CREATE TABLES, "permitsDB", postgres
titanic_table_create = ("""
    GRANT ALL PRIVILEGES ON DATABASE "{DB_NAME}" TO {DB_USER};
    DROP TABLE IF EXISTS titanic_data;
    CREATE TABLE titanic_data (
        "pclass" TEXT,
        "survived" TEXT,
        "name" TEXT,
        "sex" TEXT,
        "age" TEXT,
        "sibsp" TEXT,
        "parch" TEXT,
        "ticket" TEXT,
        "fare" TEXT,
        "cabin" TEXT,
        "embarked" TEXT,
        "boat" TEXT,
        "body" TEXT,
        "home.dest" TEXT
    );
    SET statement_timeout = '30s';
""")

permits_raw_table_create = ("""
    GRANT ALL PRIVILEGES ON DATABASE "{DB_NAME}" TO {DB_USER};
    DROP TABLE IF EXISTS permits_raw;
    CREATE TABLE permits_raw (
        "Assessor Book" TEXT,
        "Assessor Page" TEXT,
        "Assessor Parcel" TEXT,
        "Tract" TEXT,
        "Block" TEXT,
        "Lot" TEXT,
        "Reference # (Old Permit #)" TEXT,
        "PCIS Permit #" TEXT,
        "Status" TEXT,
        "Status Date" TEXT,
        "Permit Type" TEXT,
        "Permit Sub-Type" TEXT,
        "Permit Category" TEXT,
        "Project Number" TEXT,
        "Event Code" TEXT,
        "Initiating Office" TEXT,
        "Issue Date" TEXT,
        "Address Start" TEXT,
        "Address Fraction Start" TEXT,
        "Address End" TEXT,
        "Address Fraction End" TEXT,
        "Street Direction" TEXT,
        "Street Name" TEXT,
        "Street Suffix" TEXT,
        "Suffix Direction" TEXT,
        "Unit Range Start" TEXT,
        "Unit Range End" TEXT,
        "Zip Code" TEXT,
        "Work Description" TEXT,
        "Valuation" TEXT,
        "Floor Area-L.A. Zoning Code Definition" TEXT,
        "# of Residential Dwelling Units" TEXT,
        "# of Accessory Dwelling Units" TEXT,
        "# of Stories" TEXT,
        "Contractor's Business Name" TEXT,
        "Contractor Address" TEXT,
        "Contractor City" TEXT,
        "Contractor State" TEXT,
        "License Type" TEXT,
        "License #" TEXT,
        "Principal First Name" TEXT,
        "Principal Middle Name" TEXT,
        "Principal Last Name" TEXT,
        "License Expiration Date" TEXT,
        "Applicant First Name" TEXT,
        "Applicant Last Name" TEXT,
        "Applicant Business Name" TEXT,
        "Applicant Address 1" TEXT,
        "Applicant Address 2" TEXT,
        "Applicant Address 3" TEXT,
        "Zone" TEXT,
        "Occupancy" TEXT,
        "Floor Area-L.A. Building Code Definition" TEXT,
        "Census Tract" TEXT,
        "Council District" TEXT,
        "Latitude/Longitude" TEXT,
        "Applicant Relationship" TEXT,
        "Existing Code" TEXT,
        "Proposed Code" TEXT
    );
    SET statement_timeout = '30s';
""")

# COPY DATA
permits_raw_copy = ("""
    SELECT aws_s3.table_import_from_s3(
    'permits_raw',
    '',
    '(FORMAT CSV)', 
    aws_commons.create_s3_uri('aws-permits-analysis', '{FILE}', 'us-east-1')
    );
""")

titanic_data_copy = ("""
    SELECT aws_s3.table_import_from_s3(
    'titanic_data',
    '',
    '(FORMAT CSV)', 
    aws_commons.create_s3_uri('aws-permits-analysis', '{FILE}', 'us-east-1')
    );
""")

titanic_data_update = ("""
    CREATE TEMP TABLE tmp_titanic_data AS SELECT * FROM titanic_data LIMIT 0;
    SELECT aws_s3.table_import_from_s3(
        'tmp_titanic_data',
        '',
        '(FORMAT CSV)',
        aws_commons.create_s3_uri('aws-permits-analysis', '{FILE}}', 'us-east-1')
    );
    UPDATE titanic_data
    SET "pclass" = tmp_titanic_data."pclass",
        "survived" = tmp_titanic_data."survived",
        "name" = tmp_titanic_data."name",
        "sex" = tmp_titanic_data."sex",
        "age" = tmp_titanic_data."age",
        "sibsp" = tmp_titanic_data."sibsp",
        "parch" = tmp_titanic_data."parch",
        "ticket" = tmp_titanic_data."ticket",
        "fare" = tmp_titanic_data."fare",
        "cabin" = tmp_titanic_data."cabin",
        "embarked" = tmp_titanic_data."embarked",
        "boat" = tmp_titanic_data."boat",
        "body" = tmp_titanic_data."body",
        "home.dest" = tmp_titanic_data."home.dest"
    FROM tmp_titanic_data
    WHERE titanic_data.name = tmp_titanic_data.name;
""")

# QUERIES
list_columns_types_query = ("""
    SELECT column_name, data_type
    FROM   information_schema.columns
    WHERE  table_name = 'permits_raw'
    ORDER  BY ordinal_position;
""")

# FUNCTIONS
# concatenate_address
# geocode

# Query Lists 
titanic_init_queries = [install_ext_aws_s3, titanic_table_create]
permits_init_queries = [install_ext_aws_s3, install_ext_postgis, permits_raw_table_create]


