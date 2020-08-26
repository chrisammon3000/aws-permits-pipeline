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

# UPSERT DATA

permits_raw_update = ("""
    CREATE TEMP TABLE tmp_permits_raw AS SELECT * FROM permits_raw LIMIT 0;
    SELECT aws_s3.table_import_from_s3(
        'tmp_permits_raw',
        '',
        '(FORMAT CSV, HEADER true)',
        aws_commons.create_s3_uri('{S3_BUCKET}', '{FILE}', 'us-east-1')
    );

    LOCK TABLE permits_raw IN EXCLUSIVE MODE;

    UPDATE permits_raw
    SET "Assessor Book" = tmp_permits_raw."Assessor Book",
        "Assessor Page" = tmp_permits_raw."Assessor Page",
        "Assessor Parcel" = tmp_permits_raw."Assessor Parcel",
        "Tract" = tmp_permits_raw."Tract",
        "Block" = tmp_permits_raw."Block",
        "Lot" = tmp_permits_raw."Lot",
        "Reference # (Old Permit #)" = tmp_permits_raw."Reference # (Old Permit #)",
        "PCIS Permit #" = tmp_permits_raw."PCIS Permit #",
        "Status" = tmp_permits_raw."Status",
        "Status Date" = tmp_permits_raw."Status Date",
        "Permit Type" = tmp_permits_raw."Permit Type",
        "Permit Sub-Type" = tmp_permits_raw."Permit Sub-Type",
        "Permit Category" = tmp_permits_raw."Permit Category",
        "Project Number" = tmp_permits_raw."Project Number",
        "Event Code" = tmp_permits_raw."Event Code",
        "Initiating Office" = tmp_permits_raw."Initiating Office",
        "Issue Date" = tmp_permits_raw."Issue Date",
        "Address Start" = tmp_permits_raw."Address Start",
        "Address Fraction Start" = tmp_permits_raw."Address Fraction Start",
        "Address End" = tmp_permits_raw."Address End",
        "Address Fraction End" = tmp_permits_raw."Address Fraction End",
        "Street Direction" = tmp_permits_raw."Street Direction",
        "Street Name" = tmp_permits_raw."Street Name",
        "Street Suffix" = tmp_permits_raw."Street Suffix",
        "Suffix Direction" = tmp_permits_raw."Suffix Direction",
        "Unit Range Start" = tmp_permits_raw."Unit Range Start",
        "Unit Range End" = tmp_permits_raw."Unit Range End",
        "Zip Code" = tmp_permits_raw."Zip Code",
        "Work Description" = tmp_permits_raw."Work Description",
        "Valuation" = tmp_permits_raw."Valuation",
        "Floor Area-L.A. Zoning Code Definition" = tmp_permits_raw."Floor Area-L.A. Zoning Code Definition",
        "# of Residential Dwelling Units" = tmp_permits_raw."# of Residential Dwelling Units",
        "# of Accessory Dwelling Units" = tmp_permits_raw."# of Accessory Dwelling Units",
        "# of Stories" = tmp_permits_raw."# of Stories",
        "Contractor's Business Name" = tmp_permits_raw."Contractor's Business Name",
        "Contractor Address" = tmp_permits_raw."Contractor Address",
        "Contractor City" = tmp_permits_raw."Contractor City",
        "Contractor State" = tmp_permits_raw."Contractor State",
        "License Type" = tmp_permits_raw."License Type",
        "License #" = tmp_permits_raw."License #",
        "Principal First Name" = tmp_permits_raw."Principal First Name",
        "Principal Middle Name" = tmp_permits_raw."Principal Middle Name",
        "Principal Last Name" = tmp_permits_raw."Principal Last Name",
        "License Expiration Date" = tmp_permits_raw."License Expiration Date",
        "Applicant First Name" = tmp_permits_raw."Applicant First Name",
        "Applicant Last Name" = tmp_permits_raw."Applicant Last Name",
        "Applicant Business Name" = tmp_permits_raw."Applicant Business Name",
        "Applicant Address 1" = tmp_permits_raw."Applicant Address 1",
        "Applicant Address 2" = tmp_permits_raw."Applicant Address 2",
        "Applicant Address 3" = tmp_permits_raw."Applicant Address 3",
        "Zone" = tmp_permits_raw."Zone",
        "Occupancy" = tmp_permits_raw."Occupancy",
        "Floor Area-L.A. Building Code Definition" = tmp_permits_raw."Floor Area-L.A. Building Code Definition",
        "Census Tract" = tmp_permits_raw."Census Tract",
        "Council District" = tmp_permits_raw."Council District",
        "Latitude/Longitude" = tmp_permits_raw."Latitude/Longitude",
        "Applicant Relationship" = tmp_permits_raw."Applicant Relationship",
        "Existing Code" = tmp_permits_raw."Existing Code",
        "Proposed Code" = tmp_permits_raw."Proposed Code"
    FROM tmp_permits_raw
    WHERE permits_raw."PCIS Permit #" = tmp_permits_raw."PCIS Permit #";

    INSERT INTO permits_raw
    SELECT tmp_permits_raw."Assessor Book",
        tmp_permits_raw."Assessor Page",
        tmp_permits_raw."Assessor Parcel",
        tmp_permits_raw."Tract",
        tmp_permits_raw."Block",
        tmp_permits_raw."Lot",
        tmp_permits_raw."Reference # (Old Permit #)",
        tmp_permits_raw."PCIS Permit #",
        tmp_permits_raw."Status",
        tmp_permits_raw."Status Date",
        tmp_permits_raw."Permit Type",
        tmp_permits_raw."Permit Sub-Type",
        tmp_permits_raw."Permit Category",
        tmp_permits_raw."Project Number",
        tmp_permits_raw."Event Code",
        tmp_permits_raw."Initiating Office",
        tmp_permits_raw."Issue Date",
        tmp_permits_raw."Address Start",
        tmp_permits_raw."Address Fraction Start",
        tmp_permits_raw."Address End",
        tmp_permits_raw."Address Fraction End",
        tmp_permits_raw."Street Direction",
        tmp_permits_raw."Street Name",
        tmp_permits_raw."Street Suffix",
        tmp_permits_raw."Suffix Direction",
        tmp_permits_raw."Unit Range Start",
        tmp_permits_raw."Unit Range End",
        tmp_permits_raw."Zip Code",
        tmp_permits_raw."Work Description",
        tmp_permits_raw."Valuation",
        tmp_permits_raw."Floor Area-L.A. Zoning Code Definition",
        tmp_permits_raw."# of Residential Dwelling Units",
        tmp_permits_raw."# of Accessory Dwelling Units",
        tmp_permits_raw."# of Stories",
        tmp_permits_raw."Contractor's Business Name",
        tmp_permits_raw."Contractor Address",
        tmp_permits_raw."Contractor City",
        tmp_permits_raw."Contractor State",
        tmp_permits_raw."License Type",
        tmp_permits_raw."License #",
        tmp_permits_raw."Principal First Name",
        tmp_permits_raw."Principal Middle Name",
        tmp_permits_raw."Principal Last Name",
        tmp_permits_raw."License Expiration Date",
        tmp_permits_raw."Applicant First Name",
        tmp_permits_raw."Applicant Last Name",
        tmp_permits_raw."Applicant Business Name",
        tmp_permits_raw."Applicant Address 1",
        tmp_permits_raw."Applicant Address 2",
        tmp_permits_raw."Applicant Address 3",
        tmp_permits_raw."Zone",
        tmp_permits_raw."Occupancy",
        tmp_permits_raw."Floor Area-L.A. Building Code Definition",
        tmp_permits_raw."Census Tract",
        tmp_permits_raw."Council District",
        tmp_permits_raw."Latitude/Longitude",
        tmp_permits_raw."Applicant Relationship",
        tmp_permits_raw."Existing Code",
        tmp_permits_raw."Proposed Code"
    FROM tmp_permits_raw
    LEFT OUTER JOIN permits_raw ON permits_raw."PCIS Permit #" = tmp_permits_raw."PCIS Permit #"
    WHERE permits_raw."PCIS Permit #" IS NULL;

    COMMIT;

    DROP TABLE tmp_permits_raw;
""")

titanic_data_update = ("""
    CREATE TEMP TABLE tmp_titanic_data AS SELECT * FROM titanic_data LIMIT 0;
    SELECT aws_s3.table_import_from_s3(
        'tmp_titanic_data',
        '',
        '(FORMAT CSV, HEADER true)',
        aws_commons.create_s3_uri('{S3_BUCKET}', '{FILE}', 'us-east-1')
    );
    
    LOCK TABLE titanic_data IN EXCLUSIVE MODE;

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
    WHERE titanic_data."name" = tmp_titanic_data."name";

    INSERT INTO titanic_data
    SELECT tmp_titanic_data."pclass", tmp_titanic_data."survived", 
        tmp_titanic_data."name", tmp_titanic_data."sex", 
        tmp_titanic_data."age", tmp_titanic_data."sibsp", 
        tmp_titanic_data."parch", tmp_titanic_data."ticket", 
        tmp_titanic_data."fare", tmp_titanic_data."cabin", 
        tmp_titanic_data."embarked", tmp_titanic_data."boat", 
        tmp_titanic_data."body", tmp_titanic_data."home.dest"
    FROM tmp_titanic_data
    LEFT OUTER JOIN titanic_data ON titanic_data."name" = tmp_titanic_data."name"
    WHERE titanic_data."name" IS NULL;

    COMMIT;

    DROP TABLE tmp_titanic_data;
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


