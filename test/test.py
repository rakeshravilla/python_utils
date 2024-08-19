import pandas as pd

def generate_create_table_query(dataframe, table_name):
    columns = ', '.join(f"{column} VARCHAR(255)" for column in dataframe.columns)
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
    return query

def upsert(table, **kwargs):
    """ update/insert rows into objects table (update if the row already exists)
        given the key-value pairs in kwargs """
    keys = ["%s" % k for k in kwargs]
    values = ["'%s'" % v for v in kwargs.values()]
    sql = list()
    sql.append("INSERT INTO %s (" % table)
    sql.append(", ".join(keys))
    sql.append(") VALUES (")
    sql.append(", ".join(values))
    sql.append(") ON DUPLICATE KEY UPDATE ")
    sql.append(", ".join("%s = '%s'" % (k, v) for k, v in kwargs.iteritems()))
    sql.append(";")
    return "".join(sql)

def generate_insert_query(dataframe, table_name):
    columns = ', '.join(dataframe.columns)
    values = ', '.join(["'" + "', '".join(map(str, row)) + "'" for row in dataframe.values])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
    return query

# Example usage:
data = pd.read_csv('test/test.csv')  # Load your CSV file into a DataFrame
table_name = 'sample'  # Name of your database table

# Generate create table query
create_table_query = generate_create_table_query(data, table_name)

# Generate insert queries
insert_queries = generate_insert_query(data, table_name)
# insert_queries = upsert(data, table_name)

# Write create table query to file
with open('create_table.sql', 'w') as create_table_file:
    create_table_file.write(create_table_query)

# Write insert queries to file
with open('insert_queries.sql', 'w') as insert_queries_file:
    for query in insert_queries:
        insert_queries_file.write(query)
