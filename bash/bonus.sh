#!/bin/bash

# Input string
input_string="abc_def_ghi_Hello"

# Split the string on underscores
IFS="_" read -ra parts <<< "$input_string"

# Create subdirectories
base_dir="/path/to/your/base/directory"  # Replace with your desired base directory
for part in "${parts[@]}"; do
    base_dir="$base_dir/$part"
    mkdir -p "$base_dir"
done

# Print the final base directory
echo "Created subdirectories: $base_dir"
