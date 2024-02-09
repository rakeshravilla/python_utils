#!/bin/bash

# Function to create project directories
create_project_structure() {
    local table_name="$1"
    local project_name="${table_name//_/-}"

    # Create main directories
    mkdir -p "$project_name/src/main/$table_name/pipeline-app"
    mkdir -p "$project_name/src/main/$table_name/schema"
    mkdir -p "$project_name/src/main/$table_name/sql"
    touch "$project_name/src/main/$table_name/etl-definition-${table_name}.conf"
    
    # Create test directories
    mkdir -p "$project_name/src/test/testdata/$table_name"
    mkdir -p "$project_name/src/test/scala/$table_name"

    # Create sample files
    touch "$project_name/src/main/$table_name/pipeline-app/${table_name}.yaml"
    touch "$project_name/src/main/$table_name/schema/${table_name}.avsc"
    touch "$project_name/src/main/$table_name/sql/${table_name}.spark.sql"
    touch "$project_name/src/test/testdata/$table_name/expected_${table_name}.csv"
    touch "$project_name/src/test/scala/$table_name/${table_name}.scala"

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

    # Create the project structure
    create_project_structure "$table_name"
}

# Run the main function
main "$@"
