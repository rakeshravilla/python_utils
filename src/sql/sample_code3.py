import csv

# Read input from fields.csv and generate SQL select queries
def generate_sql_queries(input_file):
    sql_queries = {}
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table_name = row['table_name']
            field_name = row['field_name']
            if table_name not in sql_queries:
                sql_queries[table_name] = []
            sql_queries[table_name].append(field_name)
    return sql_queries

# Write SQL queries to individual .sql files
def write_sql_to_files(sql_queries):
    for table_name, fields in sql_queries.items():
        fields_str = ', '.join(fields)
        output_file = f"{table_name}.sql"
        with open(output_file, 'w') as sqlfile:
            sql_query = f"SELECT {fields_str} FROM {table_name};"
            sqlfile.write(sql_query + '\n')
        print(f"SQL select query for {table_name} has been written to {output_file}.")

# Main function
if __name__ == "__main__":
    input_file = "resources/input/fields.csv"
    sql_queries = generate_sql_queries(input_file)
    print(sql_queries)
    write_sql_to_files(sql_queries)
