import os
import csv
import json

# Read input from fields.csv and generate Avro schema
def generate_avro_schema(input_file):
    avro_schema = {"type": "record", "name": "SampleRecord", "fields": []}
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            field_name = row['field_name']
            data_type = row['data_type']
            avro_field = {"name": field_name, "type": data_type}
            avro_schema["fields"].append(avro_field)
    return avro_schema

# Write Avro schema JSON to a .avsc file
def write_avro_schema_to_file(avro_schema):
    avro_folder = "resources/output/avro"
    os.makedirs(avro_folder, exist_ok=True)
    avro_schema_json = json.dumps(avro_schema, indent=4)
    output_file = os.path.join(avro_folder, f"avro_schema.avsc")
    with open(output_file, 'w') as avsc_file:
        avsc_file.write(avro_schema_json)
    print(f"Avro schema has been written to {output_file}.")

# Main function
if __name__ == "__main__":
    input_file = "resources/input/fields.csv"
    avro_schema = generate_avro_schema(input_file)
    write_avro_schema_to_file(avro_schema)
