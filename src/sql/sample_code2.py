import csv


def create_sql_select_query(table_name, field_names, data_types):
    """Creates a SQL SELECT query for the given table name, field names, and data types.

    Args:
      table_name: The name of the table to query.
      field_names: A list of the field names to select.
      data_types: A list of the data types of the field names.

    Returns:
      A SQL SELECT query string.
    """

    query = "SELECT {} FROM {}".format(", ".join(field_names), table_name)

    return query


def write_sql_select_query_to_file(query, filename):
    """Writes the given SQL SELECT query to the given file.

    Args:
      query: The SQL SELECT query string to write.
      filename: The name of the file to write the query to.
    """

    with open(filename, "w") as f:
        f.write(query)


def main():
    """Reads the input file `fields.csv` and creates a SQL SELECT query for each table.
    Then, writes each query to a separate .sql file.
    """

    with open("src/fields.csv", "r") as f:
        reader = csv.reader(f)

        for row in reader:
            table_name, field_name, data_type = row

            field_names = [field_name]
            data_types = [data_type]

            query = create_sql_select_query(
                table_name, field_names, data_types)

            filename = "{}.sql".format(table_name)
            write_sql_select_query_to_file(query, filename)


if __name__ == "__main__":
    main()
