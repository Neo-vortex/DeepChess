#!/bin/bash

# Directory containing the PGN files
pgn_directory="./"

# Loop through all PGN files in the directory
for pgn_file in "$pgn_directory"*.pgn; do
    # Get the base name of the file without extension
    base_name=$(basename -- "$pgn_file")
    file_name="${base_name%.*}"

    # Construct the output file path
    output_file="./output_${file_name}.txt"

    # Run the pgn-extract command for each file
    pgn-extract -Wepd "$pgn_file" |& tee "$output_file"

    echo "Processed $pgn_file. Output saved to $output_file"
done
