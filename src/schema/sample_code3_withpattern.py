import os
import pandas as pd
import json

# Read Avro schema pattern from a file
def read_avro_schema_pattern(pattern_file):
    with open(pattern_file, 'r') as pattern_file:
        avro_schema = json.load(pattern_file)
    return avro_schema

# Generate Avro schema for each table and write to separate .avsc files
def generate_and_write_avro_schemas(input_file, pattern_schema):
    xls = pd.ExcelFile(input_file)
    for sheet_name in xls.sheet_names:
        table_name = sheet_name
        excel_data = pd.read_excel(input_file, sheet_name=sheet_name)
        avro_schema = pattern_schema.copy()
        avro_schema["name"] = table_name
        avro_schema["fields"] = []
        for column in excel_data.columns:
            field_name = column
            data_type = str(excel_data[column].dtype)
            avro_field = {"name": field_name, "type": data_type}
            avro_schema["fields"].append(avro_field)
        output_file = f"{table_name}_avro_schema.avsc"
        write_avro_schema_to_file(avro_schema, output_file)
        print(f"Avro schema for {table_name} has been written to {output_file}.")

# Write Avro schema JSON to a .avsc file
def write_avro_schema_to_file(avro_schema, output_file):
    with open(output_file, 'w') as avsc_file:
        avro_schema_json = json.dumps(avro_schema, indent=4)
        avsc_file.write(avro_schema_json)

# Main function
if __name__ == "__main__":
    input_file = "input.xlsx"  # Replace with the path to your Excel file
    pattern_file = "avro_schema_pattern.avsc"

    pattern_schema = read_avro_schema_pattern(pattern_file)
    generate_and_write_avro_schemas(input_file, pattern_schema)
