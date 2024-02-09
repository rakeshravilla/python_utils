#!/bin/bash

# Function to create project directories
create_project_structure() {
    local project_name="$1"
    local table_name="$2"

    # Replace underscores with hyphens to get the project name
    project_name="${table_name//_/\-}"

    # Create main directories
    mkdir -p "$project_name/src/main/$table_name/pipeline_definition"
    mkdir -p "$project_name/src/main/$table_name/schema"
    mkdir -p "$project_name/src/main/$table_name/sql"
    
    # Create test directories
    mkdir -p "$project_name/src/test/resources/testdata/$table_name"
    mkdir -p "$project_name/src/test/scala/"

    # Create sample files
    touch "$project_name/src/main/$table_name/pipeline_definition/${table_name}.yaml"
    touch "$project_name/src/main/$table_name/schema/${table_name}.avro"
    touch "$project_name/src/main/$table_name/sql/${table_name}.spark.sql"
    touch "$project_name/src/main/$table_name/etl-definition-${table_name}.conf"
    touch "$project_name/src/test/resources/testdata/$table_name/expected_${table_name}.csv"
    touch "$project_name/src/test/scala/${table_name}.scala"

    # Success message
    echo "Scala project structure created successfully in folder: $project_name"
}

# Main function
main() {
    # Check if an argument is provided
    if [ $# -eq 0 ]; then
        read -p "Enter the table name for your Scala project: " table_name
    else
        table_name="$1"
    fi

    # Check if the table name contains underscores
    if [[ "$table_name" == *"_".* ]]; then
        echo "Converting underscores (_) to hyphens (-) in table name..."
    fi

    # Create the project structure
    create_project_structure "$table_name" "$table_name"
}

# Run the main function
main "$@"
