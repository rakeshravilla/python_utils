#!/bin/bash

# Function to create directories with error handling
create_dir() {
  mkdir -p "$1" || { echo "Error creating directory: $1" >&2; exit 1; }
}

# Get the table name from the first argument
table_name=${1:-"my-table"}

# Build full project name
project_name="${table_name//_/-}"

# Create the top-level folder
create_dir "$project_name"

# Create main directories with table name interpolation
create_dir "$project_name/src/main/$table_name"
create_dir "$project_name/src/main/$table_name/pipeline_definition"
create_dir "$project_name/src/main/$table_name/schema"
create_dir "$project_name/src/main/$table_name/sql"
create_dir "$project_name/src/main/$table_name/etl-definition"
create_dir "$project_name/src/test/resources/testdata/$table_name"
create_dir "$project_name/src/test/scala/"

# Create specific files with table name interpolation
touch "$project_name/src/main/$table_name/pipeline_definition/$table_name.yaml"
touch "$project_name/src/main/$table_name/schema/$table_name.avro"
touch "$project_name/src/main/$table_name/sql/$table_name.spark.sql"
touch "$project_name/src/main/$table_name/etl-definition/$table_name.conf"
touch "$project_name/src/test/resources/testdata/$table_name/expected_$table_name.csv"

echo "Created Scala project structure for table: $table_name in directory: $project_name"
