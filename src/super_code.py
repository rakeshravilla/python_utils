import os
import csv
import pandas as pd
import json

# Function to read data from CSV file and return a dictionary with table names as keys and field lists as values
def read_csv(input_file):
    table_fields = {}
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table_name = row['table_name']
            field_name = row['field_name']
            data_type = row['data_type']
            if table_name not in table_fields:
                table_fields[table_name] = []
            table_fields[table_name].append({"name": field_name, "type": data_type})
    return table_fields

# Function to read data from Excel file and return a dictionary with table names as keys and field lists as values
def read_excel(input_file):
    xls = pd.ExcelFile(input_file)
    table_fields = {}
    for sheet_name in xls.sheet_names:
        table_name = sheet_name
        excel_data = pd.read_excel(input_file, sheet_name=sheet_name)
        fields = [{"name": column, "type": str(excel_data[column].dtype)} for column in excel_data.columns]
        table_fields[table_name] = fields
    return table_fields

# Function to generate SQL queries and write them to a .sql file
def generate_and_write_sql_queries(table_fields, output_folder):
    sql_folder = os.path.join(output_folder, 'sql')
    os.makedirs(sql_folder, exist_ok=True)
    
    for table_name, fields in table_fields.items():
        fields_str = ', '.join([f"""CAST({field["name"]} AS {field["type"]})""" for field in fields])
        # fields_str = ', '.join([field["name"] for field in fields])
        sql_query = f"SELECT {fields_str} FROM {table_name};"
        output_file = os.path.join(sql_folder, f"{table_name}_create_table.sql")
        with open(output_file, 'w') as sqlfile:
            sqlfile.write(sql_query + '\n')

# Function to generate Avro schemas and write them to .avsc files
def generate_and_write_avro_schemas(table_fields, output_folder):
    avro_folder = os.path.join(output_folder, 'avro')
    os.makedirs(avro_folder, exist_ok=True)
    
    for table_name, fields in table_fields.items():
        avro_schema = {"type": "record", "name": table_name, "fields": fields}
        output_file = os.path.join(avro_folder, f"{table_name}_avro_schema.avsc")
        write_avro_schema_to_file(avro_schema, output_file)

# Function to write Avro schema JSON to a .avsc file
def write_avro_schema_to_file(avro_schema, output_file):
    with open(output_file, 'w') as avsc_file:
        avro_schema_json = json.dumps(avro_schema, indent=4)
        avsc_file.write(avro_schema_json)

# Main function
if __name__ == "__main__":
    input_file_csv = "resources/input/fields.csv"  # Path to CSV file
    input_file_excel = "resources/input/input.xlsx"  # Path to Excel file
    output_folder = "resources/output"  # Output folder
    
    # Read input from CSV or Excel based on file availability
    if os.path.isfile(input_file_csv):
        table_fields = read_csv(input_file_csv)
    elif os.path.isfile(input_file_excel):
        table_fields = read_excel(input_file_excel)
    else:
        print("Error: No valid input file found.")
        exit(1)
    
    # Generate and write SQL queries to .sql files
    generate_and_write_sql_queries(table_fields, output_folder)
    
    # Generate and write Avro schemas to .avsc files
    generate_and_write_avro_schemas(table_fields, output_folder)

#Super code working for both SQL and AVSC while accepting both csv and excel as inputs