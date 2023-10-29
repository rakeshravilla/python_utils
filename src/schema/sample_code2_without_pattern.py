import os
import csv
import json

# Generate Avro schema for each table and write to separate .avsc files
def generate_and_write_avro_schemas(input_file):
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
    
    for table_name, fields in table_fields.items():
        avro_schema = {"type": "record", "name": table_name, "fields": fields}
        output_file = f"{table_name}_avro_schema.avsc"
        write_avro_schema_to_file(avro_schema, output_file)
        print(f"Avro schema for {table_name} has been written to {output_file}.")

# Write Avro schema JSON to a .avsc file
def write_avro_schema_to_file(avro_schema, out_file):
    avro_folder = "resources/output/avro"
    os.makedirs(avro_folder, exist_ok=True)
    output_file = os.path.join(avro_folder, out_file)
    with open(output_file, 'w') as avsc_file:
        avro_schema_json = json.dumps(avro_schema, indent=4)
        avsc_file.write(avro_schema_json)

# Main function
if __name__ == "__main__":
    input_file = "resources/input/fields.csv"  # Replace with the path to your CSV file

    generate_and_write_avro_schemas(input_file)
